import sys
import os

# This next part figures out where our main project folder is.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first for tools.
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

# Now we're importing our special tools!
# 'MinimalChainable' is our main LEGO builder for prompts.
# 'build_models' helps set up our AI friends.
# 'prompt' is the function that sends our message to the AI.
from chain import MinimalChainable # Our magic prompt chaining tool
from main import build_models, prompt # Tools from our main project file

# This is our Character Evolution Engine recipe! It helps us create a story.
def character_evolution_demo():
    # Let's tell everyone what this demo is about.
    print("🚀 Running: Character Evolution Engine Demo")

    # Get our AI models ready.
    client, model_names = build_models()
    # We'll use the first AI friend in our list.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # What kind of character do we want to create?
    # You can change this to "a brave knight", "a shy alien", or anything else!
    character_type = "a curious squirrel"
    # Show what kind of character we're starting with.
    print(f"Developing Character Type: {character_type}\n")

    # Let's run our prompt chain to build the character's story!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' gives the AI the starting character type.
        context={"char_type": character_type},
        # Which AI friend will help us.
        # Which AI friend will help us.
        model=model_info,
        # The function to send messages to the AI.
        callable=prompt,
        # Our list of step-by-step questions to build the story.
        prompts=[
            # Prompt 1: Describe the basic character.
            # "{{char_type}}" will be replaced with "a curious squirrel".
            # We ask for the answer in JSON format (like a dictionary).
            "Describe a basic character who is {{char_type}}. Include a name and one positive trait. Respond in JSON: {\"name\": \"name\", \"positive_trait\": \"trait\", \"description\": \"desc\"}",

            # Prompt 2: Give the character a flaw.
            # "{{output[-1].name}}" uses the 'name' from the AI's last answer.
            # "{{output[-1].description}}" uses the 'description' from the AI's last answer.
            "Give the character {{output[-1].name}} (the {{char_type}} from {{output[-1].description}}) a significant but relatable flaw for a 5th grader. Respond in JSON: {\"flaw\": \"character flaw\"}",

            # Prompt 3: Create a challenge for the character.
            # "{{output[-2].name}}" uses the 'name' from 2 answers ago.
            # "{{output[-1].flaw}}" uses the 'flaw' from the AI's last answer.
            "Create a challenge for {{output[-2].name}} (the {{char_type}} with flaw: {{output[-1].flaw}}) that forces them to confront their flaw. Describe the challenge. Respond in JSON: {\"challenge\": \"challenge_description\"}",

            # Prompt 4: Show how the character grows.
            # This uses the character's name (3 answers ago), the challenge (last answer),
            # and the flaw (2 answers ago).
            "Show how {{output[-3].name}} (the {{char_type}}) grows by facing the {{output[-1].challenge}} and overcoming their {{output[-2].flaw}}. Describe the growth. Respond in JSON: {\"growth\": \"description of growth\"}",

            # Prompt 5: Design a new adventure for the changed character.
            # This uses the character's name (4 answers ago) and their growth (last answer).
            "Design a new, brief adventure for the now changed {{output[-4].name}} that highlights their growth from {{output[-1].growth}}. Respond in JSON: {\"new_adventure\": \"description of new adventure\"}"
        ],
    )

    # Let's save the prompts we sent and the AI's story parts into files.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # Names for our output files.
    prompts_file_base = os.path.join(output_dir, "character_evolution_prompts")
    results_file_base = os.path.join(output_dir, "character_evolution_results")

    # Make a nice text file of all the prompts.
    chained_prompts_text = MinimalChainable.to_delim_text_file(
        prompts_file_base,
        context_filled_prompts
    )
    # Make a nice text file of all the AI's story parts.
    chainable_result_text = MinimalChainable.to_delim_text_file(
        results_file_base,
        result
    )

    # Show the prompts and story parts on the screen.
    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    # Tell the user where the files are saved.
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    # Also log to markdown for history
    log_file = MinimalChainable.log_to_markdown("character_evolution", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")


# This special code runs if you start this Python file directly.
if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        character_evolution_demo()