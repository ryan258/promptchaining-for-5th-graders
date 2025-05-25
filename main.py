# main.py - Using the Prompt Chain Magic
# This file shows how to use our prompt chaining system
# Think of this as the cookbook that shows you how to cook with our tools

import os  # Helps us read secret keys from the computer
from typing import List, Dict, Union  # Tells Python what types of data we expect
from dotenv import load_dotenv  # Helps us load secret keys from a file
from chain import MinimalChainable, FusionChain  # Our magic prompt chaining tools
import llm  # Library that talks to AI models
import json  # Helps us work with data that looks like {"key": "value"}


def build_models():
    """
    This function sets up our AI models so we can talk to them.
    
    Think of this like getting phone numbers for three different friends
    who are really good at writing. Each friend has different strengths:
    - Claude 3.5 Sonnet: The smartest friend
    - Claude 3 Sonnet: Pretty smart friend  
    - Claude 3 Haiku: Fast friend who gives quick answers
    """
    
    # Load our secret API key from a file called .env
    # This is like getting the password to call our AI friends
    load_dotenv()
    
    # Get the secret key from our computer's environment
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # Set up our three AI model friends
    # Each one needs the same secret key to work
    
    # Claude 3.5 Sonnet - the newest and smartest
    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    # Claude 3 Sonnet - still very smart, just not the newest
    sonnet_3_model: llm.Model = llm.get_model("claude-3-sonnet")
    sonnet_3_model.key = ANTHROPIC_API_KEY

    # Claude 3 Haiku - faster but simpler responses
    haiku_3_model: llm.Model = llm.get_model("claude-3-haiku")
    haiku_3_model.key = ANTHROPIC_API_KEY

    # Return all three models so we can use them later
    return [sonnet_3_5_model, sonnet_3_model, haiku_3_model]


def prompt(model: llm.Model, prompt: str):
    """
    This function sends a message to an AI model and gets back an answer.
    
    It's like sending a text message to your smart friend and waiting
    for them to text you back with an answer.
    """
    
    # Send the prompt to the model with some settings
    # Temperature 0.5 means "be creative, but not too crazy"
    res = model.prompt(
        prompt,
        temperature=0.5,  # How creative should the AI be? (0 = boring, 1 = very creative)
    )
    
    # Get just the text part of the response
    return res.text()


def prompt_chainable_poc():
    """
    This function shows how to use MinimalChainable to chain prompts together.
    
    POC means "Proof of Concept" - we're proving that our idea works!
    
    We're going to:
    1. Ask AI to create a blog post title about AI Agents
    2. Ask AI to create a hook for that title  
    3. Ask AI to write the first paragraph using the title and hook
    
    Each step builds on the previous one, like building with blocks!
    """
    
    # Get our smartest AI model to work with
    sonnet_3_5_model, _, _ = build_models()

    # Run our prompt chain!
    # This returns two things:
    # - result: the answers from each prompt
    # - context_filled_prompts: the actual prompts we sent (with variables filled in)
    result, context_filled_prompts = MinimalChainable.run(
        
        # Our starting context - this is like our bag of ingredients
        context={"topic": "AI Agents"},
        
        # Which AI model to use
        model=sonnet_3_5_model,
        
        # The function that sends prompts to the AI
        callable=prompt,
        
        # Our chain of prompts - each one builds on the previous ones!
        prompts=[
            # PROMPT #1: Create a blog title
            # {{topic}} gets replaced with "AI Agents"
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {'title': '<title>'}",
            
            # PROMPT #2: Create a hook for that title
            # {{output[-1].title}} gets the title from the previous response
            "Generate one hook for the blog post title: {{output[-1].title}}",
            
            # PROMPT #3: Write the first paragraph
            # {{output[-2].title}} gets the title from 2 prompts ago
            # {{output[-1]}} gets the hook from the last prompt
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
    )

    # Save our results to text files so we can see what happened
    # This creates two files:
    # 1. A file showing the prompts we actually sent
    # 2. A file showing the responses we got back
    
    chained_prompts = MinimalChainable.to_delim_text_file(
        "poc_context_filled_prompts",  # Name of the file
        context_filled_prompts         # The prompts with variables filled in
    )
    
    chainable_result = MinimalChainable.to_delim_text_file(
        "poc_prompt_results",  # Name of the file  
        result                 # The AI responses
    )

    # Print everything to the screen so we can see what happened
    print(f"\n\n📖 Prompts~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chained_prompts}")
    print(f"\n\n📊 Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chainable_result}")


def fusion_chain_poc():
    """
    This function shows how to use FusionChain to make AI models compete!
    
    Instead of using just one AI model, we use three different ones
    and make them all answer the same questions. Then we pick the best answer!
    
    It's like asking three different friends the same question and
    choosing who gave the best response.
    """
    
    # Get all three of our AI models
    sonnet_3_5_model, sonnet_3_model, haiku_3_model = build_models()

    def evaluator(outputs: List[str]) -> tuple[str, List[float]]:
        """
        This function decides which AI model did the best job.
        
        Our simple strategy: the longest answer wins!
        (In real life, you might use more complex judging)
        """
        
        # Count how many characters each output has
        scores = [len(output) for output in outputs]
        
        # Find the highest score
        max_score = max(scores)
        
        # Turn scores into percentages (0 to 1)
        normalized_scores = [score / max_score for score in scores]
        
        # The output with the highest score wins
        top_response = outputs[scores.index(max_score)]
        
        return top_response, normalized_scores

    # Run the fusion chain - this is where the magic happens!
    result = FusionChain.run(
        
        # Same context as before
        context={"topic": "AI Agents"},
        
        # Use all three AI models - they'll compete!
        models=[sonnet_3_5_model, sonnet_3_model, haiku_3_model],
        
        # Function to send prompts
        callable=prompt,
        
        # Same prompt chain as before
        prompts=[
            # PROMPT #1: Create a blog title
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {'title': '<title>'}",
            
            # PROMPT #2: Create a hook
            "Generate one hook for the blog post title: {{output[-1].title}}",
            
            # PROMPT #3: Write first paragraph
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
        
        # Our judging function
        evaluator=evaluator,
        
        # Function to get model names for the report
        get_model_name=lambda model: model.model_id,
    )

    # Convert our result to a dictionary so we can save it as JSON
    result_dump = result.dict()

    # Print the results to the screen
    print("\n\n📊 FusionChain Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(json.dumps(result_dump, indent=4))  # Pretty print the JSON

    # Save the complete results to a JSON file
    with open("poc_fusion_chain_result.json", "w") as json_file:
        json.dump(result_dump, json_file, indent=4)


def main():
    """
    This is the main function that runs when we start the program.
    
    It's like the conductor of an orchestra - it decides which
    pieces of music (functions) to play and in what order.
    """
    
    # First, show how basic prompt chaining works
    prompt_chainable_poc()

    # Uncomment the next line if you want to see fusion chaining too!
    # (We comment it out because it uses more AI calls and costs more money)
    # fusion_chain_poc()


# This special code means "only run main() if this file is being run directly"
# It's like saying "if someone double-clicks this file, run the main function"
if __name__ == "__main__":
    main()