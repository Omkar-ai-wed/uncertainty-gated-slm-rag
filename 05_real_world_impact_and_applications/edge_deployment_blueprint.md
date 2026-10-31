# Edge Deployment Blueprint: Production Engineering Architecture

This blueprint specifies how to package, deploy, and serve the **Uncertainty-Gated Selective RAG** architecture in production edge environments.

---

## 1. Supported Target Edge Platforms

| Tier | Edge Hardware Target | Compute Specs | Target SLM Model | Serving Engine |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Ultra-Light IoT / Embedded** | Raspberry Pi 5 / RK3588 | 8GB–16GB RAM (CPU only) | `Qwen2.5-0.5B-Instruct` (INT4) | `llama.cpp` / ONNX Runtime |
| **Tier 2: Embedded Edge AI** | NVIDIA Jetson Orin Nano / AGX | 8GB–64GB Unified VRAM | `Qwen2.5-1.5B` / `Llama-3.2-3B` | `TensorRT-LLM` / `vLLM` |
| **Tier 3: Secure Mobile / Laptop** | Apple MacBook (M2/M3/M4) | 16GB–36GB Unified Memory | `Llama-3.2-3B` / `Gemma-2-2B` | `MLX` / `llama.cpp` |
| **Tier 4: Enterprise On-Premises** | Single Server (1x RTX 4090) | 24GB VRAM | `Llama-3.2-3B` / `Qwen2.5-7B` | `vLLM` + `FAISS-GPU` |

---

## 2. End-to-End Production Request Lifecycle

```text
                  USER REQUEST VIA REST API / WEBSOCKET
                                    |
                                    v
                  +-----------------------------------+
                  | Fast FastAPI / vLLM Gateway Server|
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  | STEP 1: Fast Prefix Decode (M=3)  |
                  | Logits extracted via hook         |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  | STEP 2: Calculate Entropy U(q)    |
                  | Takes < 12ms on GPU               |
                  +-----------------------------------+
                                    |
                 +------------------+------------------+
                 |                                     |
          U(q) < tau                            U(q) >= tau
     (Parametric Certainty)                (Epistemic Uncertainty)
                 |                                     |
                 v                                     v
      +--------------------+                +-----------------------+
      | Direct Stream:     |                | STEP 3: Vector Query  |
      | Finish generating  |                | In-Memory FAISS Index |
      | remaining tokens   |                +-----------------------+
      +--------------------+                           |
                 |                                     v
                 |                          +-----------------------+
                 |                          | STEP 4: Cosine Filter |
                 |                          | Drop passages < 0.65  |
                 |                          +-----------------------+
                 |                                     |
                 |                                     v
                 |                          +-----------------------+
                 |                          | Grounded Generation:  |
                 |                          | Context + Query       |
                 |                          +-----------------------+
                 |                                     |
                 +------------------+------------------+
                                    |
                                    v
                  +-----------------------------------+
                  | JSON Response: {answer, gated_rag}|
                  +-----------------------------------+
```

---

## 3. Production Docker Compose Specification

Deployable on any on-premises edge workstation with an NVIDIA GPU:

```yaml
version: '3.8'

services:
  # In-Memory Vector Store for Edge Grounding
  vector-store:
    image: qdrant/qdrant:latest # or local FAISS volume
    container_name: edge_vector_store
    ports:
      - "6333:6333"
    volumes:
      - ./knowledge_base_index:/qdrant/storage
    restart: always

  # Uncertainty-Gated SLM Inference Engine
  gated-slm-service:
    build:
      context: ./01_code_prototype
      dockerfile: Dockerfile
    container_name: edge_gated_rag
    environment:
      - MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
      - ENTROPY_THRESHOLD_TAU=2.0
      - PREFIX_HORIZON_M=3
      - VECTOR_STORE_URL=http://vector-store:6333
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: always
```

---

## 4. Key Production Monitoring Metrics (Observability Dashboard)

When running in an enterprise, the telemetry tracker outputs Prometheus metrics to Grafana:

1. **Gating Bypass Ratio:** Percentage of queries served directly from memory (Target: $50\%\text{--}70\%$).
2. **Mean Time-to-First-Token (TTFT):**
   * *Bypassed queries:* $<35\text{ms}$.
   * *Retrieved queries:* $<140\text{ms}$.
3. **Retrieval Trigger Drift:** Tracks if incoming user queries are suddenly triggering higher entropy, signaling an out-of-distribution knowledge gap that requires indexing new enterprise documents.
4. **GPU Power Efficiency:** Average Watts consumed per 1,000 requests.

