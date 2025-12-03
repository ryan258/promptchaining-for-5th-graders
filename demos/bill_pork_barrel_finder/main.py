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

def pork_barrel_demo():
    print("🚀 Running: Bill Pork Barrel Finder Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Legislation
    bill = "The 'National Defense Authorization Act' includes $50 million for a 'Shrimp Museum' in District 12 and a requirement that the Navy buy engines only from a factory in District 4."
    print(f"Analyzing Bill: '{bill}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"bill": bill},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Riders
            """Analyze the bill: '{{bill}}'.
            Identify the items that have nothing to do with 'National Defense'. 
            Respond in JSON: {"riders": ["item 1", "item 2"], "relevance_score": "0/10"}""",

            # Prompt 2: Map to Beneficiaries
            """Who represents District 12 and District 4? (Hypothetically). 
            Why are these items in the bill? Respond in JSON: {"beneficiary_politician": "Rep X", "purpose": "Buying votes"}""",

            # Prompt 3: Calculate Cost of Passage
            """If this bill needed those 2 votes to pass, what was the 'bribe' price per vote? 
            Respond in JSON: {"cost_per_vote": "$X million", "taxpayer_impact": "Waste"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "pork_barrel_prompts")
    results_file_base = os.path.join(output_dir, "pork_barrel_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("bill_pork_barrel_finder", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        pork_barrel_demo()
