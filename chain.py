# chain.py - The Heart of Prompt Chaining
# This file contains the magic that lets us chain prompts together
# Think of it like building with LEGO blocks - each prompt builds on the last one

import json  # Helps us work with data that looks like {"key": "value"}
import re    # Helps us find patterns in text (like finding JSON in markdown)
from typing import List, Dict, Callable, Any, Union  # These tell Python what types of data we expect
from pydantic import BaseModel  # Helps us create clean data structures
import concurrent.futures  # Lets us do multiple things at the same time


# This is like a report card that tells us how our fusion chain did
class FusionChainResult(BaseModel):
    """
    This is like a trophy case that holds all our results.
    When we run multiple AI models and make them compete,
    this holds who won and how everyone did.
    """
    top_response: Union[str, Dict[str, Any]]  # The best answer we got
    all_prompt_responses: List[List[Any]]     # Every answer from every model
    all_context_filled_prompts: List[List[str]]  # The actual prompts we sent
    performance_scores: List[float]           # Scores from 0 to 1 for each model
    model_names: List[str]                    # Names of all the models we used


class FusionChain:
    """
    FusionChain is like having multiple students answer the same test,
    then picking the best answer. It runs the same prompts through
    different AI models and chooses the winner.
    
    This is the "ensemble method" - when you're not sure which approach
    is best, try them all and let them compete!
    """

    @staticmethod
    def run(
        context: Dict[str, Any],           # The variables we want to use in our prompts
        models: List[Any],                 # List of AI models to compete
        callable: Callable,               # The function that talks to the AI
        prompts: List[str],               # The chain of prompts to run
        evaluator: Callable[[List[str]], List[float]],  # Function that judges who won
        get_model_name: Callable[[Any], str],           # Function to get model names
    ) -> FusionChainResult:
        """
        This is the main competition function.
        
        Imagine you have 3 friends, and you want to ask them all the same
        series of questions. Each friend builds on their own previous answers.
        At the end, you decide which friend gave the best final answer.
        
        That's exactly what this function does with AI models!
        """
        
        # Create empty lists to store results from each model
        all_outputs = []                    # Every response from every model
        all_context_filled_prompts = []     # The actual prompts sent to each model

        # Loop through each AI model and run the prompt chain
        for model in models:
            # Run the full prompt chain for this model
            # This returns two things: the outputs and the filled-in prompts
            outputs, context_filled_prompts = MinimalChainable.run(
                context, model, callable, prompts
            )
            
            # Save this model's results
            all_outputs.append(outputs)
            all_context_filled_prompts.append(context_filled_prompts)

        # Now we need to judge who did best
        # We only look at the final answer from each model
        last_outputs = [outputs[-1] for outputs in all_outputs]
        
        # Ask our evaluator function to pick the winner and give scores
        top_response, performance_scores = evaluator(last_outputs)

        # Get the names of all our models so we can remember who did what
        model_names = [get_model_name(model) for model in models]

        # Package everything up in our result object
        return FusionChainResult(
            top_response=top_response,                      # The winning answer
            all_prompt_responses=all_outputs,               # All answers from all models
            all_context_filled_prompts=all_context_filled_prompts,  # All the prompts we sent
            performance_scores=performance_scores,          # How well each model did
            model_names=model_names,                        # Names of all the models
        )

    @staticmethod
    def run_parallel(
        context: Dict[str, Any],
        models: List[Any],
        callable: Callable,
        prompts: List[str],
        evaluator: Callable[[List[str]], List[float]],
        get_model_name: Callable[[Any], str],
        num_workers: int = 4,              # How many models to run at the same time
    ) -> FusionChainResult:
        """
        This is like the regular run() function, but faster!
        
        Instead of asking each friend one at a time, we ask all our friends
        at the same time. This is called "parallel processing" - doing
        multiple things at once to save time.
        """

        def process_model(model):
            """
            This little function runs the prompt chain for one model.
            We need this because of how parallel processing works.
            """
            outputs, context_filled_prompts = MinimalChainable.run(
                context, model, callable, prompts
            )
            return outputs, context_filled_prompts

        # Create empty lists to store results
        all_outputs = []
        all_context_filled_prompts = []

        # This is the parallel magic - we create a "thread pool"
        # Think of it like having multiple workers who can all work at the same time
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Give each worker a model to process
            future_to_model = {
                executor.submit(process_model, model): model for model in models
            }
            
            # Collect the results as workers finish
            for future in concurrent.futures.as_completed(future_to_model):
                outputs, context_filled_prompts = future.result()
                all_outputs.append(outputs)
                all_context_filled_prompts.append(context_filled_prompts)

        # The rest is the same as the regular run() function
        # Judge the results and package them up
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)
        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            model_names=model_names,
        )


class MinimalChainable:
    """
    This is the heart of the whole system!
    
    MinimalChainable lets you chain prompts together like links in a chain.
    Each prompt can use:
    1. Variables from your context (like {{name}} gets replaced with a real name)
    2. Answers from previous prompts (like {{output[-1]}} gets the last answer)
    
    It's like having a conversation where each question builds on the previous answers.
    """

    @staticmethod
    def run(
        context: Dict[str, Any],    # Variables to use in prompts (like {{topic}})
        model: Any,                 # The AI model to use
        callable: Callable,        # Function that sends prompts to the AI
        prompts: List[str]          # List of prompts to run in order
    ) -> List[Any]:
        """
        This is where the magic happens!
        
        Think of this like following a recipe where each step uses ingredients
        from previous steps. We start with our context (ingredients) and
        each prompt (recipe step) can use what we made before.
        """
        
        # Create empty lists to store our results
        output = []                    # Stores AI responses
        context_filled_prompts = []    # Stores the actual prompts we sent

        # Go through each prompt one by one
        for i, prompt in enumerate(prompts):
            
            # STEP 1: Replace context variables
            # Look for things like {{topic}} and replace them with real values
            for key, value in context.items():
                # Check if this variable is in our prompt
                if "{{" + key + "}}" in prompt:
                    # Replace {{key}} with the actual value
                    prompt = prompt.replace("{{" + key + "}}", str(value))

            # STEP 2: Replace references to previous outputs
            # This is where we can use {{output[-1]}} to get the last response
            
            # We count backwards from the current prompt
            # j=1 means "1 prompt ago", j=2 means "2 prompts ago", etc.
            for j in range(i, 0, -1):
                # Get the response from j prompts ago
                previous_output = output[i - j]

                # Handle JSON (dictionary) outputs specially
                if isinstance(previous_output, dict):
                    # If they want the whole JSON object
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        # Replace with the JSON as a string
                        prompt = prompt.replace(
                            f"{{{{output[-{j}]}}}}", json.dumps(previous_output)
                        )
                    
                    # If they want a specific key from the JSON
                    for key, value in previous_output.items():
                        if f"{{{{output[-{j}].{key}}}}}" in prompt:
                            # Replace {{output[-1].title}} with the actual title
                            prompt = prompt.replace(
                                f"{{{{output[-{j}].{key}}}}}", str(value)
                            )
                            
                # Handle regular text outputs
                else:
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        # Replace with the previous text response
                        prompt = prompt.replace(
                            f"{{{{output[-{j}]}}}}", str(previous_output)
                        )

            # Save the prompt with all variables filled in
            # This helps us debug and see exactly what we sent to the AI
            context_filled_prompts.append(prompt)

            # STEP 3: Send the prompt to the AI model
            result = callable(model, prompt)

            # STEP 4: Try to parse JSON responses
            # Sometimes AIs return JSON data, and we want to handle it smartly
            try:
                # First, check if JSON is wrapped in markdown code blocks
                # Look for ```json or ``` followed by JSON
                json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", result)
                
                if json_match:
                    # Extract and parse the JSON from the markdown
                    result = json.loads(json_match.group(1))
                else:
                    # Try to parse the whole response as JSON
                    result = json.loads(result)
                    
            except json.JSONDecodeError:
                # If it's not JSON, that's fine - keep it as regular text
                pass

            # Save this result so future prompts can reference it
            output.append(result)

        # Return both the outputs and the filled-in prompts
        # This gives us the answers AND lets us see exactly what we asked
        return output, context_filled_prompts

    @staticmethod
    def to_delim_text_file(name: str, content: List[Union[str, dict]]) -> str:
        """
        This function saves our results to a text file in a pretty format.
        
        It's like creating a scrapbook of our prompt chain - each result
        gets its own section with chain emoji to show the progression.
        """
        result_string = ""  # We'll build up the final text here
        
        # Create a file with the given name
        with open(f"{name}.txt", "w") as outfile:
            # Go through each item in our content
            for i, item in enumerate(content, 1):  # Start counting from 1
                
                # Convert dictionaries and lists to JSON strings
                if isinstance(item, dict):
                    item = json.dumps(item)
                if isinstance(item, list):
                    item = json.dumps(item)
                
                # Create a pretty header with chain emoji
                # More emoji = later in the chain
                chain_text_delim = (
                    f"{'🔗' * i} -------- Prompt Chain Result #{i} -------------\n\n"
                )
                
                # Write to file and build our return string
                outfile.write(chain_text_delim)
                outfile.write(item)
                outfile.write("\n\n")

                result_string += chain_text_delim + item + "\n\n"

        return result_string