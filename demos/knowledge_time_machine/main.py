# These lines at the top are like telling Python where to find its tools.
# 'import sys' and 'import os' help us work with the computer's files and settings.
import sys
import os

# This next part figures out where our main project folder is.
# It's like finding the main entrance to our project's "house."
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first
# when we ask it to 'import' (bring in) tools.
# It's like saying, "Hey Python, check the main project folder for tools first!"
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

# This is our Knowledge Time Machine adventure!
# A 'def' creates a function, which is like a recipe for the computer.
def knowledge_time_machine_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Knowledge Time Machine Demo")

    # First, let's get our AI models ready.
    all_models = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model = all_models[0]

    # This is the modern concept we want to explore.
    # Try changing this to "cars", "video games", "robots", or "the internet"!
    modern_concept = "Smartphones"

    # Let's print which concept we're traveling through time with.
    print(f"Exploring the timeline of: {modern_concept}\n")

    # This is the exciting part where we run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        context={"concept": modern_concept},
        # 'model' tells it which AI friend to talk to.
        model=selected_model,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        # Each question can use answers from the previous ones!
        prompts=[
            # Prompt 1: Ask for historical origins.
            # "{{concept}}" will be replaced with our chosen modern_concept.
            # We ask the AI to answer in JSON format (like a dictionary).
            "What were the earliest historical origins or very first ideas related to {{concept}}? Describe 1-2 key starting points. Respond in JSON like {'historical_origins': [{'point': 'description of point 1'}, {'point': 'description of point 2'}]}",

            # Prompt 2: Ask for key evolution points.
            # "{{output[-1].historical_origins}}" uses the 'historical_origins' from the AI's last answer.
            "Building on the origins of {{concept}} ({{output[-1].historical_origins}}), what were 2-3 key evolution points or important discoveries that led to its development? Respond in JSON like {'evolution_points': [{'event': 'description of event 1', 'impact': 'impact of event 1'}, ...]}",

            # Prompt 3: Describe the current state.
            # "{{output[-1].evolution_points}}" uses the 'evolution_points' from the AI's last answer.
            "Considering the evolution of {{concept}} ({{output[-1].evolution_points}}), what is its current state today? Briefly describe its main features and uses. Respond in JSON like {'current_state': 'description of current features and uses'}",

            # Prompt 4: Imagine future possibilities.
            # "{{output[-1].current_state}}" uses the 'current_state' from the AI's last answer.
            "Looking at the current state of {{concept}} ({{output[-1].current_state}}), what are 2-3 imaginative future possibilities for it 20 years from now? Think creatively! Respond in JSON like {'future_possibilities': [{'idea': 'description of future idea 1'}, {'idea': 'description of future idea 2'}, ...]}"
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "knowledge_time_machine_prompts")
    results_file_base = os.path.join(output_dir, "knowledge_time_machine_results")

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

# This special code block runs only when you run this file directly.
if __name__ == "__main__":
    # This part helps load our secret API key from a file named '.env'.
    # The API key is like a password to talk to Google's AI.
    from dotenv import load_dotenv
    # We need to find the '.env' file, which is in our main project folder.
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path) # Load the secret key
    else:
        # If the file isn't there, print a friendly warning.
        print(f"Warning: .env file not found at {dotenv_path}. Make sure GOOGLE_API_KEY is set in your environment.")

    # Check if we actually got the API key.
    if not os.getenv("GOOGLE_API_KEY"):
        # If not, tell the user what to do.
        print("🚨 GOOGLE_API_KEY not found. Please set it up in the .env file in the project root.")
    else:
        # If we have the key, then it's time to run our knowledge_time_machine_demo recipe!
        knowledge_time_machine_demo()