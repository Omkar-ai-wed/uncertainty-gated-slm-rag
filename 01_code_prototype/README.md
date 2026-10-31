# Option 1: Experimental Prototype & Pilot Code

This module implements the core experimental framework for the research paper:
> **"Uncertainty-Gated Selective Retrieval in Quantized Small Language Models (SLMs): Mitigating Noise-Induced Hallucination and Latency in Edge Deployment"**

---

## 1. Directory Structure

```text
01_code_prototype/
Γö£ΓöÇΓöÇ requirements.txt           # Verified Python dependencies (PyTorch, Transformers, FAISS, NVML)
Γö£ΓöÇΓöÇ telemetry_tracker.py         # Hardware telemetry tracking TTFT, latency, peak VRAM, and Joules
Γö£ΓöÇΓöÇ pilot_entropy_gate.py        # Core algorithm: calculates prefix entropy U(q) and benchmarks gating
Γö£ΓöÇΓöÇ noise_injection_test.py      # Noise stress-test: proves static RAG causes SLM distraction
ΓööΓöÇΓöÇ README.md                    # Setup and execution guide
```

---

## 2. Theoretical Formulation

The system replaces unconditional (static) retrieval with an internal epistemic confidence gate.
For an input query $q$, the model performs an initial greedy prefix decode of $M=3$ tokens:

$$\mathcal{U}(q) = -\frac{1}{M} \sum_{m=1}^M \sum_{v \in \mathcal{V}} P_\theta(y_m = v \mid q, y_{<m}) \log P_\theta(y_m = v \mid q, y_{<m})$$

* **If $\mathcal{U}(q) < \tau$ (High Parametric Confidence):**  
  The query is answered directly from the SLM's internal weights. This eliminates retriever latency, cuts token costs, and prevents distraction from noisy documents.
* **If $\mathcal{U}(q) \ge \tau$ (Epistemic Uncertainty):**  
  The system queries the external vector store (FAISS), filters passages with low semantic similarity, and feeds the grounded context to the generator.

---

## 3. How to Run It Yourself (Step-by-Step)

The environment and model weights are already configured and cached locally in `.venv`.

### Method A: Direct Execution in Windows PowerShell (Fastest & Recommended)
Open PowerShell (or press `Ctrl + \`` in VS Code/Antigravity) and run directly:

```powershell
# 1. Run the Noise Injection & Context Distraction Test
& "d:\play\RAG\01_code_prototype\.venv\Scripts\python.exe" "d:\play\RAG\01_code_prototype\noise_injection_test.py" --model "Qwen/Qwen2.5-0.5B-Instruct"

# 2. Run the Full 20-Query Factual Entropy Benchmark
& "d:\play\RAG\01_code_prototype\.venv\Scripts\python.exe" "d:\play\RAG\01_code_prototype\pilot_entropy_gate.py" --model "Qwen/Qwen2.5-0.5B-Instruct" --tau 2.0 --m 3
```

*(Because weights are cached locally, it will start immediately with 0 download wait time).*

---

### Method B: Virtual Environment Activation Workflow
If you prefer activating the `.venv` first:

```powershell
# Navigate into the prototype directory
cd "d:\play\RAG\01_code_prototype"

# Activate the pre-configured virtual environment
.\.venv\Scripts\Activate.ps1

# Execute scripts
python noise_injection_test.py --model Qwen/Qwen2.5-0.5B-Instruct
python pilot_entropy_gate.py --model Qwen/Qwen2.5-0.5B-Instruct --tau 2.0 --m 3
```

---

### Method C: Testing Your Own Custom Questions
You can add your own test questions to the benchmark:
1. Open [`pilot_entropy_gate.py`](pilot_entropy_gate.py).
2. Locate `SAMPLE_BENCHMARK` (lines 20–40).
3. Add custom questions into the list:
   ```python
   {"id": "custom_01", "type": "popular", "query": "What is the capital of India?", "gold": "New Delhi"},
   ```
4. Re-run `python pilot_entropy_gate.py` to see whether the model's internal entropy triggers retrieval or generates directly from parametric memory.

---

## 4. Google Colab 1-Click Execution (Cloud GPU)

To run larger models (e.g., `Llama-3.2-3B`, `Gemma-2-2B`) on a free Google Colab T4 GPU:

1. Create a notebook on [colab.research.google.com](https://colab.research.google.com/).
2. Change runtime: **Runtime $\to$ Change runtime type $\to$ T4 GPU**.
3. Upload `01_code_prototype` files, and run:

```bash
pip install torch transformers accelerate numpy tabulate
python pilot_entropy_gate.py --model Qwen/Qwen2.5-1.5B-Instruct --tau 2.0
python noise_injection_test.py --model Qwen/Qwen2.5-1.5B-Instruct
```

---

## 5. Output Deliverables for Your AAIR Paper

Running these scripts directly produces the empirical data required for:
1. **Table 2 in Manuscript:** Factual Accuracy and Latency Comparison (Direct SLM vs. Static RAG vs. Gated RAG).
2. **Figure 3 in Manuscript:** Empirical Distribution of Token Entropy for Known vs. Long-Tail Entities (showing the separation margin).
3. **Table 4 in Manuscript:** Hallucination Vulnerability under Contradictory Distractor Context.

