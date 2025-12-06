# Quick Start Guide

Get up and running with the Prompt Chaining Framework in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- An [OpenRouter](https://openrouter.ai/) API key (provides access to Claude, GPT-4, Gemini, etc.)

## 1. Installation

Clone the repository and set up your environment:

```bash
# Clone the repo (if you haven't already)
git clone <repository-url>
cd promptchaining-for-5th-graders

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configuration

Set up your API key:

```bash
# Copy the example environment file
cp .env.example .env

# Open .env and add your key
# OPENROUTER_API_KEY=sk-or-v1-...
```

## 3. Run Your First Chain

Try the **Concept Simplifier**, which demonstrates the core "decompose → analogize → synthesize" pattern:

```bash
python tools/learning/concept_simplifier.py "Quantum Entanglement"
```

You'll see the system:
1. Break down the concept
2. Create analogies for each part
3. Generate a simple explanation
4. Save the result as an artifact

## 4. Explore Built-In Tools

### MS Blog Content Generator
Generate high-quality blog content with the Low-Energy Pipeline:

```bash
# Auto-detect format and generate content
python tools/ms_blog/ms_content_tools.py "I struggle with daily planning" --energy low
```

### Subject Connector
Find unexpected connections between two topics:

```bash
python tools/learning/subject_connector.py "Music Theory" --context "Computer Science"
```

## 5. Run the Demos

We have interactive demos that showcase advanced features:

```bash
# MS Blog Tools Demo (Content Generation)
python demos/ms_blog_demo.py --interactive

# Meta-Chain Demo (Self-Improving Chains)
python demos/meta_chain_demo.py

# Curriculum Builder (Chain Composition)
python demos/curriculum_builder_demo.py
```

## 6. Start the Web UI (Optional)

Visualize your chains in a browser interface:

1. Start the backend:
   ```bash
   python server/main.py
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd web
   npm install
   npm run dev
   ```

3. Open `http://localhost:5173`

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works.
- Check [tools/ms_blog/README.md](tools/ms_blog/README.md) for deep dives into specific tools.
- Look at [IDEAS.md](IDEAS.md) for inspiration on what to build next.
