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

def diplomatic_decoder_demo():
    print("🚀 Running: Diplomatic Subtext Decoder Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Diplomatic Statement
    statement = "The Ambassador expressed 'deep concern' regarding the border incident and called on 'all parties to exercise restraint'."
    print(f"Analyzing Statement: '{statement}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"statement": statement},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Translate 'Diplomatese'
            """Translate the diplomatic statement: '{{statement}}' into Realpolitik English.
            What does 'deep concern' actually mean in terms of action? (Usually nothing).
            What does 'all parties' imply about blame? (Moral equivalence).
            Respond in JSON: {"translation": "text", "action_level": "Zero/Low/High"}""",

            # Prompt 2: Predict Response
            """Based on this weak language, what will the aggressor do next? 
            (e.g., Continue because they know there are no consequences). Respond in JSON: {"prediction": "escalation/de-escalation", "reasoning": "why"}""",

            # Prompt 3: Reveal Intent
            """Why issue a statement at all if they plan to do nothing? 
            Respond in JSON: {"political_purpose": "Domestic consumption/Saving face", "effectiveness": "Low"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "diplomatic_decoder_prompts")
    results_file_base = os.path.join(output_dir, "diplomatic_decoder_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("diplomatic_subtext_decoder", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        diplomatic_decoder_demo()
