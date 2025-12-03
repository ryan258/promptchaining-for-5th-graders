# These lines at the top are like telling Python where to find its tools.
# 'import sys' and 'import os' help us work with the computer's files and settings.
import sys
import os

# This next part figures out where our main project folder is.
# It's like finding the main entrance to our project's "house."
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first
# when we ask it to 'import' (bring in) tools.
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

# Now we're importing our special tools!
# 'MinimalChainable' is our main LEGO builder for prompts.
# 'build_models' helps set up our AI friends (the Gemini models).
# 'prompt' is the function that sends our message to the AI.
from chain import MinimalChainable # Our magic prompt chaining tool
from main import build_models, prompt # Tools from our main project file

# This is our Common Ground Finder adventure!
# A 'def' creates a function, which is like a recipe for the computer.
def common_ground_finder_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Common Ground Finder Demo")

    # First, let's get our AI models ready.
    client, model_names = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Here are two opposing views on a topic.
    # For 5th graders, let's pick something relatable like homework or screen time.
    # Try changing these to explore different disagreements!
    viewpoint_A = "Kids should have less homework so they have more time to play and relax."
    viewpoint_B = "Kids should have some homework to practice what they learn in school and develop responsibility."

    # Let's print the viewpoints we're exploring.
    print(f"Exploring common ground between:\nView A: {viewpoint_A}\nView B: {viewpoint_B}\n")

    # This is the exciting part where we run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        context={"view_A": viewpoint_A, "view_B": viewpoint_B},
        # 'model' tells it which AI friend to talk to.
        model=model_info,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        prompts=[
            # Prompt 1: Identify underlying values for each view.
            # "{{view_A}}" and "{{view_B}}" will be replaced with our chosen viewpoints.
            "For View A: '{{view_A}}', what are 1-2 important values or beliefs someone holding this view might have? " +
            "For View B: '{{view_B}}', what are 1-2 important values or beliefs someone holding this view might have? " +
            "Respond in JSON like {\"view_A_values\": [\"value1\", \"value2\"], \"view_B_values\": [\"value1\", \"value2\"]}",

            # Prompt 2: Find shared concerns.
            # "{{output[-1].view_A_values}}" and "{{output[-1].view_B_values}}" use values from the AI's last answer.
            "Even though they have different views ('{{view_A}}' vs '{{view_B}}') and values ({{output[-1].view_A_values}} vs {{output[-1].view_B_values}}), " +
            "what are 1-2 shared concerns or worries people on both sides might have about the general topic (e.g., kids' well-being, learning)? " +
            "Respond in JSON like {\"shared_concerns\": [\"concern1\", \"concern2\"]}",

            # Prompt 3: Identify common goals.
            # "{{output[-1].shared_concerns}}" uses shared concerns from the AI's last answer.
            "Given the shared concerns ({{output[-1].shared_concerns}}) for people with views '{{view_A}}' and '{{view_B}}', " +
            "what are 1-2 common goals they might both want to achieve, even if they disagree on how? " +
            "Respond in JSON like {\"common_goals\": [\"goal1\", \"goal2\"]}",

            # Prompt 4: Suggest bridge-building ideas.
            # This prompt uses information from previous steps.
            "Considering the different views ('{{view_A}}' and '{{view_B}}'), their underlying values ({{output[-3].view_A_values}} and {{output[-3].view_B_values}}), " +
            "their shared concerns ({{output[-2].shared_concerns}}), and their common goals ({{output[-1].common_goals}}), " +
            "suggest one simple bridge-building idea or a compromise that could help both sides feel understood or work together. " +
            "Respond in JSON like {\"bridge_idea\": \"description of the bridge-building idea\"}"
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "common_ground_finder_prompts")
    results_file_base = os.path.join(output_dir, "common_ground_finder_results")

    # This line uses our tool to make a nice text file of all the prompts we sent.
    chained_prompts_text = MinimalChainable.to_delim_text_file(
        prompts_file_base,      # The name for the file
        context_filled_prompts  # The actual prompts we sent
    )
    # This line makes a nice text file of all the answers the AI gave us.
    chainable_result_text = MinimalChainable.to_delim_text_file(
        results_file_base,      # The name for this file
        result                  # The AI's answers
    )

    # Let's print everything to the screen so we can see it right away!
    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    # And tell the user where the files were saved.
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    # Log the run to markdown
    log_file = MinimalChainable.log_to_markdown("common_ground_finder", context_filled_prompts, result)

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        common_ground_finder_demo()