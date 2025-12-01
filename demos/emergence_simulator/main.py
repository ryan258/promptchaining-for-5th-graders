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

# This is our Emergence Simulator adventure!
# A 'def' creates a function, which is like a recipe for the computer.
def emergence_simulator_demo():
    # Let's tell everyone what we're doing!
    print("🚀 Running: Emergence Simulator Demo")

    # First, let's get our AI models ready.
    client, model_names = build_models()
    # We'll pick the first AI friend from the list to help us.
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Let's define a type of "agent" and some simple rules for it.
    # An agent can be an ant, a bird, a person, or even just a dot.
    # Try changing these!
    # Example: Agent = "Birds in a flock"
    # Rule 1: "Try to stay close to nearby birds."
    # Rule 2: "Try to fly in the same direction as nearby birds."
    # Rule 3: "Don't bump into other birds."
    agent_type = "Simple Robots on a Grid"
    rule1 = "If you sense food directly in front, move forward one step."
    rule2 = "If you bump into another robot, turn right."
    rule3 = "If you sense a wall in front, turn left."

    # Let's print the rules we're starting with.
    print(f"Simulating agents: {agent_type}")
    print(f"Rule 1: {rule1}")
    print(f"Rule 2: {rule2}")
    print(f"Rule 3: {rule3}\n")

    # This is the exciting part where we run our prompt chain!
    result, context_filled_prompts = MinimalChainable.run(
        # 'context' is like giving our AI starting information.
        context={"agent": agent_type, "rule_A": rule1, "rule_B": rule2, "rule_C": rule3},
        # 'model' tells it which AI friend to talk to.
        model=model_info,
        # 'callable' is the function that actually sends the message to the AI.
        callable=prompt,
        # 'prompts' is a list of questions we'll ask the AI, one after another.
        prompts=[
            # Prompt 1: Describe individual behavior based on the rules.
            # "{{agent}}", "{{rule_A}}", etc., will be replaced.
            """Imagine one '{{agent}}' on a large empty grid. Based *only* on these rules: 1. {{rule_A}}, 2. {{rule_B}}, 3. {{rule_C}}. What would its typical behavior be if there's food scattered randomly and occasionally other robots or walls? Describe its movement pattern. Respond in JSON like {"individual_behavior": "description of movement"}""",

            # Prompt 2: Predict group interactions.
            # "{{output[-1].individual_behavior}}" uses the behavior from the AI's last answer.
            """Now, imagine many '{{agent}}' (all following rules: 1. {{rule_A}}, 2. {{rule_B}}, 3. {{rule_C}}) are on the same grid with food. Knowing their individual behavior ({{output[-1].individual_behavior}}), how would they interact with each other? What might happen when they get close? Respond in JSON like {"group_interactions": "description of interactions"}""",

            # Prompt 3: Identify emergent patterns.
            # "{{output[-1].group_interactions}}" uses the interactions from the last answer.
            """From these group interactions ({{output[-1].group_interactions}}) of '{{agent}}' following rules: 1. {{rule_A}}, 2. {{rule_B}}, 3. {{rule_C}}, what complex group pattern or behavior might 'emerge' that you wouldn't expect from just looking at the simple rules? Think about how they might distribute themselves or find food. Respond in JSON like {"emergent_pattern": "description of the complex pattern"}""",

            # Prompt 4: Give real-world examples.
            # "{{output[-1].emergent_pattern}}" uses the pattern from the last answer.
            """The emergent pattern you described for '{{agent}}' is '{{output[-1].emergent_pattern}}'. Can you give 1-2 examples from the real world (like animals, people, or nature) where similar simple rules lead to complex group behaviors or patterns? Briefly explain the connection. Respond in JSON like {"real_world_examples": [{"example": "example name", "connection": "how it relates"}, ...]}"""
        ],
    )

    # Now we'll save our results to text files so we can look at them later.
    output_dir = os.path.dirname(__file__) # The folder where this script is.
    # We decide what to name our output files.
    prompts_file_base = os.path.join(output_dir, "emergence_simulator_prompts")
    results_file_base = os.path.join(output_dir, "emergence_simulator_results")

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
    # The API key is like a password to talk to AI models through OpenRouter.
    from dotenv import load_dotenv
    # We need to find the '.env' file, which is in our main project folder.
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path) # Load the secret key
    else:
        # If the file isn't there, print a friendly warning.
        print(f"Warning: .env file not found at {dotenv_path}. Make sure OPENROUTER_API_KEY is set in your environment.")

    # Check if we actually got the API key.
    if not os.getenv("OPENROUTER_API_KEY"):
        # If not, tell the user what to do.
        print("🚨 OPENROUTER_API_KEY not found. Please set it up in the .env file in the project root.")
    else:
        # If we have the key, then it's time to run our emergence_simulator_demo recipe!
        emergence_simulator_demo()