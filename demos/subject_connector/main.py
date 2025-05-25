# These lines at the top are like telling Python where to find its tools.
# 'import sys' and 'import os' help us work with the computer's files and settings.
import sys
import os

# This next part figures out where our main project folder is.
# Imagine you're in your room (the 'demos/subject_connector' folder),
# and you need to tell Python where your house's front door is (the main project folder).
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# This 'if' block makes sure Python looks in our main project folder first
# when we ask it to 'import' (bring in) tools.
# It's like saying, "Hey Python, when you look for tools, check the main toybox first!"
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

# This is where our Subject Connector adventure begins!
# A 'def' creates a function, which is like a recipe for the computer.
def subject_connector_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Subject Connector Demo")

    # First, let's get our AI models ready.
    # 'build_models()' wakes up our AI friends.
    all_models = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model = all_models[0]

    # These are the two school subjects we want to connect.
    # You can change these to any subjects you like!
    subject_a = "History"
    subject_b = "Mathematics"

    # Let's print which subjects we're working with.
    print(f"Connecting Subject A: {subject_a} and Subject B: {subject_b}\n")

    # This is the exciting part where we run our prompt chain!
    # 'MinimalChainable.run' is like giving our LEGO builder the instructions.
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        # Here, we're telling it our two subjects.
        context={"subject_A": subject_a, "subject_B": subject_b},
        # 'model' tells it which AI friend to talk to.
        model=selected_model,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        # Each question can use answers from the previous ones!
        prompts=[
            # Prompt 1: Ask for connections
            # "{{subject_A}}" and "{{subject_B}}" will be replaced with "History" and "Mathematics".
            # We ask the AI to answer in a special format called JSON, which is like a dictionary.
            "List three surprising connections between {{subject_A}} and {{subject_B}}. Respond in JSON like {'connections': ['connection1', 'connection2', 'connection3']}",

            # Prompt 2: Ask why those connections matter
            # "{{output[-1].connections}}" means "use the 'connections' part from the AI's last answer".
            "For each of the connections to {{subject_A}} and {{subject_B}} from {{output[-1].connections}}, briefly explain why it matters. Respond in JSON like {'explanations': [{'connection': 'conn1', 'importance': 'importance1'}, ...]}",

            # Prompt 3: Ask for a project idea
            # "{{output[-1].explanations}}" means "use the 'explanations' from the AI's last answer".
            "Based on the connections and their importance for {{subject_A}} and {{subject_B}} found in {{output[-1].explanations}}, design a simple project idea for a 5th grader that uses both subjects. Provide a project title and a short description. Respond in JSON like {'project_title': 'title', 'project_description': 'description'}"
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    # 'os.path.dirname(__file__)' finds the folder where this script is.
    output_dir = os.path.dirname(__file__)
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "subject_connector_prompts")
    results_file_base = os.path.join(output_dir, "subject_connector_results")

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

# This special code block runs only when you run this file directly
# (not when it's imported as a tool by another file).
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
        # If we have the key, then it's time to run our subject_connector_demo recipe!
        subject_connector_demo()