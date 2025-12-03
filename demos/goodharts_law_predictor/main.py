import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def goodharts_law_demo():
    print("🚀 Running: Goodhart's Law Predictor Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # New Metric
    metric = "To improve software quality, we will now measure developer performance by the number of bugs they find and fix in their own code."
    print(f"Analyzing Metric: {metric}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"metric": metric},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Predict Gaming Strategy
            """Analyze the metric: '{{metric}}'.
            How will a rational (but cynical) employee game this metric to maximize their reward with minimum effort? Respond in JSON: {"gaming_strategy": "description", "effort_level": "Low/Med/High"}""",

            # Prompt 2: Identify Unintended Consequences
            """If everyone adopts the strategy '{{output[-1].gaming_strategy}}', what happens to the actual software quality? Respond in JSON: {"actual_outcome": "description", "quality_impact": "Positive/Negative"}""",

            # Prompt 3: Simulate Long-Term Distortion
            """Simulate the long-term effect. 
            - What happens to the codebase?
            - What happens to the culture?
            Respond in JSON: {"long_term_effect": "description", "culture_shift": "description"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "goodharts_law_prompts")
    results_file_base = os.path.join(output_dir, "goodharts_law_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("goodharts_law_predictor", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        goodharts_law_demo()
