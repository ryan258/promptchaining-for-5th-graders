# chain_test.py - Testing Our Prompt Chain Magic
# This file contains tests that make sure our prompt chaining works correctly
# Think of tests like quality checks - we try different scenarios to make sure nothing breaks

import sys
from pathlib import Path
# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import random  # Helps us make random choices for testing
import time  # Lets us simulate different completion speeds
from src.core.chain import FusionChain, FusionChainResult, MinimalChainable  # Our magic tools


def test_chainable_solo():
    """
    TEST #1: Can we run just one simple prompt?
    
    This is like testing if a car can start before testing if it can drive.
    We make sure the basic system works with the simplest possible case.
    """
    
    # Create a fake AI model for testing
    # We don't want to spend money on real AI calls when testing!
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        """
        This pretends to be an AI but just adds "Solo response: " to whatever we ask.
        It's like having a friend who always starts their answer with the same words.
        """
        return f"Solo response: {prompt}"

    # Set up our test
    context = {"variable": "Test"}  # Our bag of ingredients
    chains = ["Single prompt: {{variable}}"]  # Just one simple prompt

    # Run our chain with the fake AI
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check that everything worked correctly
    assert len(result) == 1  # We should get exactly 1 response
    assert result[0] == "Solo response: Single prompt: Test"  # It should match what we expect


def test_chainable_run():
    """
    TEST #2: Can we run multiple prompts that use context variables?
    
    This tests if our system can replace {{variable}} with real values
    in multiple prompts. It's like testing if we can follow a recipe
    that uses the same ingredients in different steps.
    """
    
    # Create our fake AI model again
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        """
        This fake AI just adds "Response to: " before whatever we ask.
        """
        return f"Response to: {prompt}"

    # Set up a test with TWO context variables and TWO prompts
    context = {"var1": "Hello", "var2": "World"}
    chains = [
        "First prompt: {{var1}}",           # Should become "First prompt: Hello"
        "Second prompt: {{var2}} and {{var1}}"  # Should become "Second prompt: World and Hello"
    ]

    # Run our chain
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check that both prompts worked correctly
    assert len(result) == 2
    assert result[0] == "Response to: First prompt: Hello"
    assert result[1] == "Response to: Second prompt: World and Hello"


def test_chainable_with_output():
    """
    TEST #3: Can we reference previous outputs in later prompts?
    
    This is the really cool part! We test if {{output[-1]}} correctly
    gets replaced with the response from the previous prompt.
    It's like testing if we can use the result from step 1 in step 2.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return f"Response to: {prompt}"

    # This time, the second prompt uses {{output[-1]}}
    context = {"var1": "Hello", "var2": "World"}
    chains = [
        "First prompt: {{var1}}",                    # This creates output[0]
        "Second prompt: {{var2}} and {{output[-1]}}"  # This uses output[0]
    ]

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check the results
    assert len(result) == 2
    assert result[0] == "Response to: First prompt: Hello"
    # The second result should include the first result!
    assert result[1] == "Response to: Second prompt: World and Response to: First prompt: Hello"


def test_chainable_json_output():
    """
    TEST #4: Can we handle JSON responses and reference specific parts?
    
    Sometimes AIs return structured data like {"title": "My Blog Post"}.
    We test if we can use {{output[-1].title}} to get just the title part.
    This is like testing if we can open a box and take out just one thing.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        """
        This fake AI returns JSON when we ask for it, regular text otherwise.
        """
        if "Output JSON" in prompt:
            return '{"key": "value"}'  # Return JSON as a string
        return prompt  # Return the prompt unchanged

    context = {"test": "JSON"}
    chains = [
        "Output JSON: {{test}}",        # This should return {"key": "value"}
        "Reference JSON: {{output[-1].key}}"  # This should get "value" from the JSON
    ]

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check the results
    assert len(result) == 2
    assert isinstance(result[0], dict)  # First result should be a dictionary
    assert result[0] == {"key": "value"}
    assert result[1] == "Reference JSON: value"  # Should extract just the value


def test_chainable_reference_entire_json_output():
    """
    TEST #5: Can we reference the entire JSON object as a string?
    
    Sometimes we want the whole JSON object, not just one part.
    We test if {{output[-1]}} correctly converts the entire JSON
    back to a string. It's like putting the box contents back in a bag.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        if "Output JSON" in prompt:
            return '{"key": "value"}'
        return prompt

    context = {"test": "JSON"}
    chains = [
        "Output JSON: {{test}}",     # Returns {"key": "value"}
        "Reference JSON: {{output[-1]}}"  # Should get the whole JSON as a string
    ]

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert result[0] == {"key": "value"}
    assert result[1] == 'Reference JSON: {"key": "value"}'  # Whole JSON as string


def test_chainable_reference_long_output_value():
    """
    TEST #6: Can we reference outputs from multiple steps back?
    
    This tests if we can use {{output[-2]}} to go 2 steps back,
    {{output[-3]}} to go 3 steps back, etc. It's like testing if we can
    remember what happened several recipe steps ago.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return prompt  # Just return what we're given

    context = {"test": "JSON"}
    chains = [
        "Output JSON: {{test}}",              # Step 1
        "1 Reference JSON: {{output[-1]}}",   # Step 2: reference step 1
        "2 Reference JSON: {{output[-2]}}",   # Step 3: reference step 1 (2 back)
        "3 Reference JSON: {{output[-1]}}",   # Step 4: reference step 3
    ]

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check that all the references worked correctly
    assert len(result) == 4
    assert result[0] == "Output JSON: JSON"
    assert result[1] == "1 Reference JSON: Output JSON: JSON"      # References step 1
    assert result[2] == "2 Reference JSON: Output JSON: JSON"      # Also references step 1
    assert result[3] == "3 Reference JSON: 2 Reference JSON: Output JSON: JSON"  # References step 3


def test_chainable_empty_context():
    """
    TEST #7: Does everything work even with no context variables?
    
    This tests if our system works when we don't have any {{variables}}
    to replace. It's like testing if a recipe works when you don't need
    any special ingredients.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return prompt

    # Empty context - no variables to replace
    context = {}
    chains = ["Simple prompt"]  # No {{variables}} in this prompt

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    assert len(result) == 1
    assert result[0] == "Simple prompt"


def test_chainable_json_output_with_markdown():
    """
    TEST #8: Can we handle JSON that's wrapped in markdown code blocks?
    
    Real AIs often return JSON wrapped in markdown like:
    ```json
    {"key": "value"}
    ```
    
    We test if our system can extract the JSON from inside the markdown.
    It's like testing if we can unwrap a present that's in a fancy box.
    """
    
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        """
        This returns JSON wrapped in markdown, like real AIs often do.
        """
        return """
        Here's a JSON response wrapped in markdown:
        ```json
        {
            "key": "value",
            "number": 42,
            "nested": {
                "inner": "content"
            }
        }
        ```
        """

    context = {}
    chains = ["Test JSON parsing"]

    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Check that the JSON was correctly extracted from the markdown
    assert len(result) == 1
    assert isinstance(result[0], dict)  # Should be parsed as a dictionary
    assert result[0] == {
        "key": "value", 
        "number": 42, 
        "nested": {"inner": "content"}
    }


def test_fusion_chain_run():
    """
    TEST #9: Does FusionChain work with multiple competing models?
    
    This is our most complex test! We test if we can run the same prompt
    chain through multiple AI models and pick the best result.
    It's like testing if we can have a cooking contest and pick the winner.
    """
    
    # Create multiple fake AI models
    class MockModel:
        def __init__(self, name):
            self.name = name  # Each model has a name

    def mock_callable_prompt(model, prompt):
        """
        Each model returns its name in the response, so we can tell them apart.
        """
        return f"{model.name} response: {prompt}"

    def mock_evaluator(outputs):
        """
        This judges the competition by picking a random winner.
        In real life, you'd use smarter judging!
        """
        top_response = random.choice(outputs)  # Pick a random winner
        scores = [random.random() for _ in outputs]  # Random scores between 0 and 1
        return top_response, scores

    # Set up the competition
    context = {"var1": "Hello", "var2": "World"}
    chains = [
        "First prompt: {{var1}}",
        "Second prompt: {{var2}} and {{output[-1]}}"
    ]

    # Create 3 competing models
    models = [MockModel(f"Model{i}") for i in range(3)]

    def mock_get_model_name(model):
        return model.name

    # Run the fusion chain competition!
    result = FusionChain.run(
        context=context,
        models=models,
        callable=mock_callable_prompt,
        prompts=chains,
        evaluator=mock_evaluator,
        get_model_name=mock_get_model_name,
    )

    # Check that we got results from all models
    assert isinstance(result, FusionChainResult)
    assert len(result.all_prompt_responses) == 3      # 3 models
    assert len(result.all_context_filled_prompts) == 3  # 3 sets of prompts
    assert len(result.performance_scores) == 3        # 3 scores
    assert len(result.model_names) == 3               # 3 names

    # Check that each model ran both prompts
    for i, (outputs, context_filled_prompts) in enumerate(
        zip(result.all_prompt_responses, result.all_context_filled_prompts)
    ):
        assert len(outputs) == 2  # 2 prompts = 2 outputs
        assert len(context_filled_prompts) == 2  # 2 filled-in prompts

        # Check that we got a valid response from this model
        # We can't assume the order, so we check if the response starts with the model name
        response_0 = outputs[0]
        response_1 = outputs[1]
        
        # Verify the content structure matches what we expect from the mock
        assert "response: First prompt: Hello" in response_0
        assert "response: Second prompt: World and" in response_1
        
        # Verify the filled-in prompts match
        assert context_filled_prompts[0] == "First prompt: Hello"
        # The second prompt depends on the first response, so we check it contains the right parts
        assert "Second prompt: World and" in context_filled_prompts[1]

    # Check that scores are valid (between 0 and 1)
    assert all(0 <= score <= 1 for score in result.performance_scores)

    # With random scores, they should probably be different
    # (This might occasionally fail due to randomness, but very rarely)
    assert len(set(result.performance_scores)) > 1, "All performance scores are the same, which is very unlikely with random evaluator"

    # Check that we have a top response
    assert isinstance(result.top_response, (str, dict))
    print("All outputs:")
    for i, outputs in enumerate(result.all_prompt_responses):
        print(f"Model {i}:")
        for j, output in enumerate(outputs):
            print(f"  Chain {j}: {output}")

    print("\nAll context filled prompts:")
    for i, prompts in enumerate(result.all_context_filled_prompts):
        print(f"Model {i}:")
        for j, prompt in enumerate(prompts):
            print(f"  Chain {j}: {prompt}")

    print("\nPerformance scores:")
    for i, score in enumerate(result.performance_scores):
        print(f"Model {i}: {score}")

    print("\nTop response:")
    print(result.top_response)

    # Show how to convert the result to different formats
    print("result.model_dump: ", result.model_dump())      # Convert to dictionary
    print("result.model_dump_json: ", result.model_dump_json())  # Convert to JSON string


def test_fusion_chain_preserves_model_order():
    """
    Ensure FusionChain keeps outputs aligned with their originating model even
    when completion order differs (regression for as_completed ordering).
    """

    class SlowModel:
        def __init__(self, name, delay):
            self.name = name
            self.delay = delay

    def mock_callable_prompt(model, prompt):
        # Sleep proportional to delay to force completion out of input order
        time.sleep(model.delay)
        return f"{model.name}::{prompt}"

    def mock_evaluator(outputs):
        # Return a deterministic winner (first output) with dummy scores
        scores = [len(o) for o in outputs]
        return outputs[0], scores

    # Model order is fixed, but delays are reversed to flip completion order
    models = [
        SlowModel("Model-A", delay=0.3),
        SlowModel("Model-B", delay=0.1),
        SlowModel("Model-C", delay=0.2),
    ]

    result = FusionChain.run(
        context={"topic": "Ordering"},
        models=models,
        callable=mock_callable_prompt,
        prompts=["Prompt-1"],
        evaluator=mock_evaluator,
        get_model_name=lambda m: m.name,
        num_workers=3,
    )

    # Model names should match the input order
    assert result.model_names == ["Model-A", "Model-B", "Model-C"]

    # Outputs should be aligned with model_names, not completion order
    expected_prefixes = ["Model-A::Prompt-1", "Model-B::Prompt-1", "Model-C::Prompt-1"]
    for response_list, expected in zip(result.all_prompt_responses, expected_prefixes):
        assert response_list[0] == expected
