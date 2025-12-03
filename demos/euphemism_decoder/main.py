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

def euphemism_decoder_demo():
    print("🚀 Running: Euphemism Decoder Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Political Speech
    speech = "We are initiating a kinetic military action to degrade the capabilities of non-state actors in the region, involving enhanced interrogation techniques for high-value targets."
    print(f"Analyzing Speech: '{speech}'\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"speech": speech},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Euphemisms
            """Analyze the speech: '{{speech}}'.
            Identify the specific euphemisms used to sanitize violent or controversial actions. Respond in JSON: {"euphemisms": ["term 1", "term 2"]}""",

            # Prompt 2: Translate to Plain English
            """Translate the speech into brutal, plain English. Replace every euphemism with its literal meaning. 
            (e.g., 'Kinetic action' -> 'Bombing'). Respond in JSON: {"plain_english_translation": "text"}""",

            # Prompt 3: Reveal Intent
            """Why was this specific language chosen? What emotional reaction is the speaker trying to avoid? 
            Respond in JSON: {"hidden_reality": "description", "intended_effect": "description"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "euphemism_decoder_prompts")
    results_file_base = os.path.join(output_dir, "euphemism_decoder_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("euphemism_decoder", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        euphemism_decoder_demo()
