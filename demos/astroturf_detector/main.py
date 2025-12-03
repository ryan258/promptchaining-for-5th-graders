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

def astroturf_demo():
    print("🚀 Running: Astroturf Detector Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Movement Analysis
    movement = "A new group called 'Moms for Sugar' is protesting soda taxes, claiming it hurts family budgets. Their website was registered 2 weeks ago and their 'protest signs' are all professionally printed with the same font."
    print(f"Analyzing Movement: '{movement}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"movement": movement},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Analyze Coordination
            """Analyze the movement: '{{movement}}'.
            Look for signs of artificial coordination vs organic growth. 
            (e.g., Timing, funding, messaging consistency). Respond in JSON: {"signs_of_artificiality": ["sign 1", "sign 2"], "organic_probability": "High/Low"}""",

            # Prompt 2: Identify Beneficiaries
            """Who benefits financially if this 'movement' succeeds? 
            (e.g., Soda companies). Respond in JSON: {"beneficiary": "Industry/Group", "financial_stake": "High/Med/Low"}""",

            # Prompt 3: Reveal the Sponsors
            """Based on the beneficiary and the professional organization, who is likely funding 'Moms for Sugar'?
            Respond in JSON: {"likely_sponsor": "entity", "confidence": "High/Med/Low"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "astroturf_prompts")
    results_file_base = os.path.join(output_dir, "astroturf_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("astroturf_detector", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        astroturf_demo()
