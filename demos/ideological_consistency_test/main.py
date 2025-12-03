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

def ideological_consistency_demo():
    print("🚀 Running: Ideological Consistency Test Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Politician History
    history = "Senator Smith opposed 'Government Healthcare' in 2010 calling it tyranny. In 2024, he supports 'Medicare for All' after his biggest donor switched from Insurance Companies to the Nurses Union."
    print(f"Analyzing History: '{history}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"history": history},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Flip-Flop
            """Analyze the history: '{{history}}'.
            What was the position in 2010? What is it in 2024? Are they compatible? 
            Respond in JSON: {"position_2010": "desc", "position_2024": "desc", "contradiction": "Yes/No"}""",

            # Prompt 2: Map to Incentives
            """What changed between 2010 and 2024? Was it a 'change of heart' or a 'change of wallet'?
            Respond in JSON: {"driver_of_change": "Donors", "evidence": "Donor switch"}""",

            # Prompt 3: Reveal the Algorithm
            """Describe the 'Power Algorithm' this politician follows. Do they have beliefs, or just inputs?
            Respond in JSON: {"algorithm": "Input -> Output", "integrity_score": "Low"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "ideological_consistency_prompts")
    results_file_base = os.path.join(output_dir, "ideological_consistency_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("ideological_consistency_test", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        ideological_consistency_demo()
