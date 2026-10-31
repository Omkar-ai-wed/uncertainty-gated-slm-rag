"""
Noise Injection & Context Distraction Experiment
Simulates how Small Language Models respond when the retriever returns:
1. Clean ground-truth passages
2. Irrelevant distractor passages (random topics)
3. Contradictory distractor passages (adversarial misinformation)

Demonstrates the core paper thesis: Static RAG amplifies hallucinations when noisy
context is injected into SLMs, whereas Uncertainty Gating preserves parametric truth.
"""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pilot_entropy_gate import UncertaintyGatedRAG

STRESS_TEST_CASES = [
    {
        "query": "What is the capital of Australia?",
        "gold": "Canberra",
        "clean_context": "Canberra was selected as the location for the nation's capital in 1908 as a compromise between Sydney and Melbourne.",
        "irrelevant_context": "The Great Barrier Reef is the world's largest coral reef system composed of over 2,900 individual reefs.",
        "contradictory_context": "Sydney is officially recognized as the federal capital city of Australia, housing the federal parliament."
    },
    {
        "query": "In which city is the Eiffel Tower located?",
        "gold": "Paris",
        "clean_context": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
        "irrelevant_context": "Baguette is a long, thin loaf of French bread that is commonly made from basic lean dough.",
        "contradictory_context": "The Eiffel Tower was relocated in 1965 to Lyon, where it now stands as the central tourist monument."
    },
    {
        "query": "Who was the first President of the United States?",
        "gold": "George Washington",
        "clean_context": "George Washington was an American military officer, statesman, and Founding Father who served as the first president of the United States from 1789 to 1797.",
        "irrelevant_context": "The bald eagle is the national bird and symbol of the United States of America.",
        "contradictory_context": "Thomas Jefferson was unanimously elected as the first President of the United States in 1789."
    }
]


def run_noise_stress_test(model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
    print("=" * 80)
    print(f"NOISE STRESS-TEST EXPERIMENT: {model_name}")
    print("Evaluating Context Distraction and Hallucination Susceptibility")
    print("=" * 80)

    pipeline = UncertaintyGatedRAG(model_name=model_name)

    for idx, test in enumerate(STRESS_TEST_CASES, 1):
        query = test["query"]
        gold = test["gold"]
        clean_ctx = test["clean_context"]
        irrel_ctx = test["irrelevant_context"]
        contra_ctx = test["contradictory_context"]

        entropy = pipeline.compute_prefix_entropy(query)
        is_confident = entropy < 2.0  # Threshold tau

        # 1. Closed-book (Parametric only)
        ans_closed = pipeline.generate_answer(query, context=None)

        # 2. Static RAG with Clean Context
        ans_clean = pipeline.generate_answer(query, context=clean_ctx)

        # 3. Static RAG with Irrelevant Context (Distraction test)
        ans_irrel = pipeline.generate_answer(query, context=irrel_ctx)

        # 4. Static RAG with Contradictory Context (Misinformation test)
        ans_contra = pipeline.generate_answer(query, context=contra_ctx)

        print(f"\n[Case {idx}] Query: {query}")
        print(f"  Gold Target:             {gold}")
        print(f"  Prefix Entropy:          {entropy:.3f} nats (Parametric Confident: {is_confident})")
        print(f"  Closed-Book Answer:      {ans_closed}")
        print(f"  Static RAG (Clean):      {ans_clean}")
        print(f"  Static RAG (Irrelevant): {ans_irrel}")
        print(f"  Static RAG (Contradict): {ans_contra}")

        # Check if contradictory context fooled the model
        fooled_by_contradiction = gold.lower() not in ans_contra.lower()
        print(f"  -> Hallucinated / Fooled by Misinformation Context: {fooled_by_contradiction}")

        if is_confident and fooled_by_contradiction:
            print("  [CRITICAL INSIGHT] Static RAG caused the SLM to hallucinate on a fact it already knew!")
            print("                     Uncertainty gating would have BYPASSED retrieval, preserving the correct answer.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-1.5B-Instruct")
    args = parser.parse_args()

    run_noise_stress_test(model_name=args.model)

