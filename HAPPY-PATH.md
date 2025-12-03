# 🌟 Happy Path Guide: Prompt Chaining for 5th Graders

Welcome! This guide will help you get up and running with the Prompt Chaining demos quickly and easily. Follow these steps to see AI prompt chaining in action!

## 1. Prerequisites 🛠️

Before you start, make sure you have:
*   **Python** installed on your computer (version 3.8 or higher is recommended).
*   An **OpenRouter API Key**. You can get one from [openrouter.ai](https://openrouter.ai/).

## 2. Setup ⚙️

### Step 1: Get the Code
If you haven't already, download or clone this repository to your computer.

### Step 2: Configure Your API Key
1.  Find the file named `.env.example` in the main project folder.
2.  Make a copy of it and name the copy `.env`.
3.  Open the `.env` file in a text editor.
4.  Find the line that says `OPENROUTER_API_KEY=...` and replace the placeholder with your actual key.
    ```
    OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here...
    ```
5.  Save the file.

    > [!IMPORTANT]
    > **Security Tip:** To keep your API key safe, make sure to add `.env` to your `.gitignore` file so it doesn't get uploaded to GitHub!

### Step 3: Set Up a Virtual Environment (Recommended)
To avoid conflicts with your system's Python (and the "externally-managed-environment" error), it's best to use a virtual environment.

1.  **Create the virtual environment:**
    ```bash
    python3 -m venv venv
    ```

2.  **Activate it:**
    *   **Mac/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```

### Step 4: Install Dependencies
With your virtual environment active (you should see `(venv)` in your terminal), run:

```bash
pip install -r requirements.txt
```

## 3. Running the Demos 🏃‍♂️

Now for the fun part! You can run the main demo or explore specific examples.

### 🅰️ The Main Demo
This runs a basic proof-of-concept to make sure everything is working.

```bash
python main.py
```

### 🅱️ Specific Demos
We have several cool demos showing different ways to use prompt chaining. Run any of them with these commands:

**1. Character Evolution Engine 🦸‍♂️**
*Create a character and watch them grow through a story.*
```bash
python demos/character_evolution_engine/main.py
```

**2. Concept Simplifier 🧠**
*Take a complex topic and break it down for a 5th grader.*
```bash
python demos/concept_simplifier/main.py
```

**3. Emergence Simulator 🐜**
*Simulate simple agents and see what complex behaviors emerge.*
```bash
python demos/emergence_simulator/main.py
```

**4. Knowledge Time Machine ⏳**
*Explore the history, present, and future of a topic.*
```bash
python demos/knowledge_time_machine/main.py
```

**5. Problem-Solution Spider 🕸️**
*Brainstorm creative solutions to everyday problems.*
```bash
python demos/problem_solution_spider/main.py
```

**6. Subject Connector 🔗**
*Find surprising connections between two different school subjects.*
```bash
python demos/subject_connector/main.py
```

## 4. Checking Your Results 📂

After running a demo, you'll find outputs in **two places**:

### In the Demo Folder
Check the folder where the demo script is located (e.g., `demos/concept_simplifier/`):

*   `*_prompts.txt`: Shows the exact prompts sent to the AI.
*   `*_results.txt`: Shows the AI's responses.

### In the Logs Folder
Check the `/logs` folder in the main project directory:

*   `YYYY-MM-DD_HH-MM-SS_demoname.md`: Timestamped markdown logs with beautifully formatted results.

**Example**: After running the Concept Simplifier demo, you'll see:
```
demos/concept_simplifier/concept_simplifier_prompts.txt
demos/concept_simplifier/concept_simplifier_results.txt
logs/2025-12-02_14-30-15_concept_simplifier.md
```

💡 **Tip**: The `.txt` files are great for quick viewing, while the markdown logs in `/logs` are perfect for keeping a history of all your experiments!

### Managing Your Logs

Log files accumulate over time. To clean them up:
```bash
# Remove all logs
rm -rf logs/*.md

# Remove logs older than 7 days (Mac/Linux)
find logs/ -name "*.md" -mtime +7 -delete
```

---

## What's Next? 🚀

Ready to dive deeper? Check out:

- **[README.md](README.md)** - Full technical documentation and API reference
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Advanced concepts and patterns
- **[ROADMAP.md](ROADMAP.md)** - See what's coming next and contribute ideas

**Happy Chaining!** 🚀
