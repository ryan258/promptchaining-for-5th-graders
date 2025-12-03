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

def campaign_promise_demo():
    print("🚀 Running: Campaign Promise Tracker Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Promise vs Reality
    promise = "I will never raise taxes on the middle class!"
    action = "Voted for the 'Fiscal Responsibility Act' which removed 3 major tax deductions used primarily by middle-income families, effectively raising their tax burden by 4%."
    
    print(f"Analyzing Promise: '{promise}'\nAction: '{action}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"promise": promise, "action": action},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify the Gap
            """Compare the campaign promise: '{{promise}}' with the actual legislative action: '{{action}}'.
            Is this a kept promise, a broken promise, or a 'technical' truth but spiritual lie? Respond in JSON: {"verdict": "Broken/Kept/Deceptive", "explanation": "reasoning"}""",

            # Prompt 2: Map to Donor Interests
            """Who benefits from the specific action taken (removing deductions)? 
            Who would have been hurt if taxes were raised directly on the wealthy instead?
            Respond in JSON: {"beneficiaries": ["Group A"], "protected_interests": ["Group B"]}""",

            # Prompt 3: Reveal the Real Constituency
            """Based on this, who is the politician's 'Real Constituency'? (The people they actually work for).
            Respond in JSON: {"real_constituency": "description", "voter_role": "The Product/The Customer/The Distraction"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "campaign_promise_prompts")
    results_file_base = os.path.join(output_dir, "campaign_promise_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("campaign_promise_tracker", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        campaign_promise_demo()
