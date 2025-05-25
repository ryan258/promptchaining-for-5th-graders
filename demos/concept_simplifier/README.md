# Demo: The Concept Simplifier

This demo explains anything complex using only simple words.

**Chain:**

1.  Complex topic
2.  Break into parts
3.  Find analogies
4.  Test with examples
5.  Create teaching story

## How to Run

1.  Navigate to the `promptchaining-for-5th-graders` directory.
2.  Ensure your `.env` file is set up with your `GOOGLE_API_KEY`.
3.  Run the demo:
    ```bash
    python demos/concept_simplifier/main.py
    ```

## Expected Output

The script will output the AI's step-by-step simplification of the chosen complex topic, resulting in a short teaching story. The results will also be saved to `demos/concept_simplifier/concept_simplifier_prompts.txt` and `demos/concept_simplifier/concept_simplifier_results.txt`.
