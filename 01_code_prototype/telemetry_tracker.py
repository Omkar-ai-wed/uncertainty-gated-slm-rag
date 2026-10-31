"""
Hardware Telemetry Tracker for Edge AI Inference
Measures execution latency (TTFT, Total), peak VRAM, and GPU energy draw (Joules via NVML).
"""

import time
import threading
from typing import Dict, Any, Optional

try:
    import pynvml
    HAS_PYNVML = True
except ImportError:
    HAS_PYNVML = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class HardwareTelemetry:
    """Tracks latency, memory, and energy consumption for neural model inference."""

    def __init__(self, device_id: int = 0, sampling_interval_s: float = 0.05):
        self.device_id = device_id
        self.sampling_interval_s = sampling_interval_s
        self.nvml_initialized = False
        self.handle = None
        self._power_readings = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None

        if HAS_PYNVML and HAS_TORCH and torch.cuda.is_available():
            try:
                pynvml.nvmlInit()
                self.handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
                self.nvml_initialized = True
            except Exception as e:
                print(f"[Telemetry Warning] NVML init failed: {e}. Falling back to time-only telemetry.")

    def _sample_power(self):
        """Background thread loop sampling GPU power draw in milliwatts."""
        while self._monitoring:
            try:
                # Returns power usage in milliwatts (mW)
                power_mw = pynvml.nvmlDeviceGetPowerUsage(self.handle)
                self._power_readings.append(power_mw / 1000.0)  # Convert to Watts
            except Exception:
                pass
            time.sleep(self.sampling_interval_s)

    def start(self):
        """Starts timing and background power sampling."""
        if HAS_TORCH and torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats(self.device_id)
            torch.cuda.synchronize(self.device_id)

        self._power_readings = []
        self._monitoring = True
        self.start_time = time.perf_counter()

        if self.nvml_initialized:
            self._monitor_thread = threading.Thread(target=self._sample_power, daemon=True)
            self._monitor_thread.start()

    def stop(self) -> Dict[str, Any]:
        """Stops monitoring and returns a comprehensive metrics dictionary."""
        if HAS_TORCH and torch.cuda.is_available():
            torch.cuda.synchronize(self.device_id)
        self.end_time = time.perf_counter()
        self._monitoring = False

        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=0.2)

        duration_s = self.end_time - self.start_time
        latency_ms = duration_s * 1000.0

        # Memory usage
        peak_vram_mb = 0.0
        if HAS_TORCH and torch.cuda.is_available():
            peak_vram_mb = torch.cuda.max_memory_allocated(self.device_id) / (1024 ** 2)

        # Energy calculation: Integral of Power (Watts) * dt (seconds)
        energy_joules = 0.0
        avg_power_w = 0.0
        if self._power_readings:
            avg_power_w = sum(self._power_readings) / len(self._power_readings)
            energy_joules = avg_power_w * duration_s

        return {
            "latency_ms": round(latency_ms, 2),
            "duration_s": round(duration_s, 4),
            "peak_vram_mb": round(peak_vram_mb, 2),
            "avg_power_w": round(avg_power_w, 2),
            "energy_joules": round(energy_joules, 4),
            "samples_collected": len(self._power_readings)
        }

    def close(self):
        if self.nvml_initialized:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass

