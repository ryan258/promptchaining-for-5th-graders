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

def corporate_theater_demo():
    print("🚀 Running: Corporate Theater Director Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Corporate Scenario
    stated_value = "We value innovation and risk-taking above all else."
    observed_behavior = "The last three people promoted were those who managed safe, incremental updates to legacy systems. The one person who launched a risky new product that failed was fired."

    print(f"Analyzing Corporate Dynamic:\nStated Value: {stated_value}\nObserved Behavior: {observed_behavior}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"stated": stated_value, "observed": observed_behavior},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify the Gap
            """Compare the stated value '{{stated}}' with the observed behavior '{{observed}}'. 
            What is the specific contradiction here? Respond in JSON: {"contradiction": "description", "gap_size": "Huge/Medium/Small"}""",

            # Prompt 2: Decode Incentive Structure
            """Based on the observed behavior, what is the ACTUAL incentive structure? What behavior is actually being rewarded? Respond in JSON: {"real_incentive": "description", "punished_behavior": "description"}""",

            # Prompt 3: Predict Future Behavior
            """If a new employee joins and wants to get promoted, what should they do? (Ignore the handbook, follow the incentives). Respond in JSON: {"winning_strategy": "description", "losing_strategy": "description"}""",

            # Prompt 4: Reveal the 'Theater'
            """Why does the company maintain the 'Innovation' theater if they reward safety? What function does the lie serve? Respond in JSON: {"theater_purpose": "reason", "who_benefits": "role"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "corporate_theater_prompts")
    results_file_base = os.path.join(output_dir, "corporate_theater_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("corporate_theater_director", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        corporate_theater_demo()
