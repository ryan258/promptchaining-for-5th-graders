# Demo: The Problem-Solution Spider 🕸️💡

This demo helps you take any problem, break it down, and spin out creative solutions, just like a spider spinning a web!

**Chain:**

1.  **Define problem clearly**: What exactly is the problem?
2.  **List constraints**: What are the limits or rules we have to work with (like time, materials, or budget)?
3.  **Brainstorm wild ideas**: Think of any solution, no matter how silly or impossible it sounds at first!
4.  **Combine best parts**: Look at the wild ideas and see if you can mix and match the best bits to create more realistic solutions.
5.  **Test with scenarios**: Imagine trying out your combined solution. What might happen? How could it work?

**Real magic:** You become an idea generator for everything in life! This helps you think creatively and find solutions to all sorts of challenges.

## How to Run

1.  Make sure you're in the main `promptchaining-for-5th-graders` folder in your terminal.
2.  Check that your `.env` file is ready with your `GOOGLE_API_KEY`.
3.  Run the demo with this command:
    ```bash
    python demos/problem_solution_spider/main.py
    ```

## Expected Output

The script will guide the AI through the problem-solving steps for a sample problem. You'll see the AI define the problem, list constraints, brainstorm, combine ideas, and then test the solution with a scenario. The full process will also be saved into two files in the `demos/problem_solution_spider/` folder:

- `problem_solution_spider_prompts.txt` (all the questions we asked the AI)
- `problem_solution_spider_results.txt` (all the AI's answers)
