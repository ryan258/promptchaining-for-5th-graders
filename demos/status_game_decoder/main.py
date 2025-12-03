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

def status_game_demo():
    print("🚀 Running: Status Game Decoder Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Social Situation
    situation = """
    A dinner party with 6 people. 
    Person A (Host): Keeps apologizing for the food not being perfect, though it's clearly expensive.
    Person B: Loudly compliments the wine, mentioning they visited that specific vineyard in France last year.
    Person C: Quietly eats, occasionally asking deep questions that make others pause.
    Person D: Constantly checks their phone and mentions they have a 'crisis at the office' to handle.
    Person E: Agrees enthusiastically with everything Person B says.
    """
    print(f"Analyzing Situation:\n{situation}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"situation": situation},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Analyze Surface Interaction
            """Analyze this social situation:
            '{{situation}}'
            
            On the surface, what is happening? Who seems to be the most polite? Who seems the most rude? Respond in JSON: {"surface_analysis": "description", "polite_person": "Person X", "rude_person": "Person Y"}""",

            # Prompt 2: Identify Status Signals
            """Now, look deeper for status signals. 
            - Who is 'countersignaling' (showing status by downplaying it)?
            - Who is 'name-dropping' or signaling wealth/experience?
            - Who is signaling 'busy-ness' as importance?
            - Who is signaling 'intellectual dominance'?
            Respond in JSON: {"signals": [{"person": "Person X", "signal_type": "type", "description": "desc"}, ...]}""",

            # Prompt 3: Map Dominance Hierarchy
            """Based on the signals {{output[-1].signals}}, map the actual dominance hierarchy. Who is actually winning the status game? Note: It might not be the loudest person. Respond in JSON: {"hierarchy": ["1. Person X", "2. Person Y", ...], "reasoning": "why"}""",

            # Prompt 4: Reveal the Real Game
            """What is the 'Real Game' being played here? It's not just eating dinner. Is it 'Who is the most cosmopolitan?' 'Who is the most important?' 'Who is the deepest thinker?' Respond in JSON: {"real_game": "name of the game", "rules": ["rule 1", "rule 2"], "winner": "Person X"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "status_game_prompts")
    results_file_base = os.path.join(output_dir, "status_game_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("status_game_decoder", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        status_game_demo()
