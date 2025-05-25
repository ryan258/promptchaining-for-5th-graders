# Demo: The Historical What-If Machine 📜🤔

This demo lets you pick a historical event, change one thing about it, and see what might have happened differently! It's like being a time-traveling detective.

**Chain:**

1.  **Pick historical event**: Choose an event from history.
2.  **Change one variable**: What's one small thing you could change about that event?
3.  **Predict consequences**: What might happen right away because of your change?
4.  **Trace ripple effects**: How could that one change lead to other changes, like dominoes falling?
5.  **Learn what really mattered**: What does this "what-if" story teach us about the real historical event and why things happened the way they did?

**Real magic:** History becomes a laboratory for understanding cause and effect! You get to see how small changes can sometimes have big results.

## How to Run

1.  Make sure you're in the main `promptchaining-for-5th-graders` folder in your terminal.
2.  Check that your `.env` file is ready with your `GOOGLE_API_KEY`.
3.  Run the demo with this command:
    ```bash
    python demos/historical_what_if_machine/main.py
    ```

## Expected Output

The script will guide the AI through exploring an alternate history scenario. You'll see the AI's responses to each step, from picking an event and changing a variable to predicting the ripple effects and drawing conclusions. The full exploration will also be saved into two files in the `demos/historical_what_if_machine/` folder:

- `historical_what_if_prompts.txt` (all the questions we asked the AI)
- `historical_what_if_results.txt` (all the AI's answers)
