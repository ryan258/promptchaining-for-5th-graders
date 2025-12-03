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

def meeting_forensics_demo():
    print("🚀 Running: Meeting Dynamics Forensics Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Meeting Transcript Snippet
    transcript = """
    Manager (Bob): "Okay, let's decide on the budget."
    Engineer (Sarah): "I think we need to allocate more for--"
    VP (David): [Interrupting] "Actually, Bob, did you see the email I sent?"
    Manager (Bob): "Yes David, right away. Sarah, hold that thought."
    VP (David): "We're cutting the tool budget. Any objections?"
    [Silence]
    Engineer (Sarah): "Um, well, technically if we--"
    VP (David): "Great, settled then. Moving on."
    """
    print(f"Analyzing Transcript:\n{transcript}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"transcript": transcript},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Map Interruption Patterns
            """Analyze the transcript: '{{transcript}}'.
            Who interrupts whom? Who allows themselves to be interrupted? Respond in JSON: {"interruptions": [{"interrupter": "Name", "victim": "Name"}], "dominance_score": {"Name": 10, "Name": 5}}""",

            # Prompt 2: Identify Deference Markers
            """Look for language of deference or submission. Who asks for permission? Who gives orders disguised as questions? Respond in JSON: {"deference_markers": [{"speaker": "Name", "phrase": "phrase", "analysis": "desc"}]}""",

            # Prompt 3: Reveal Actual Power Structure
            """Based on the behavioral data, draw the 'Real Org Chart' for this room. 
            Does it match the titles (Manager, Engineer, VP)? Who holds the veto power? Respond in JSON: {"real_hierarchy": ["1. Name", "2. Name"], "power_dynamic": "description"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "meeting_forensics_prompts")
    results_file_base = os.path.join(output_dir, "meeting_forensics_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("meeting_dynamics_forensics", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        meeting_forensics_demo()
