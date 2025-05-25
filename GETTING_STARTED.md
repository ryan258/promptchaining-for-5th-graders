# 🚀 Getting Started - Your First 10 Minutes

## The Quick Launch Sequence

**For Kids:** Follow these steps and you'll be chaining prompts in 10 minutes!  
**For Teachers/Parents:** This is your step-by-step guide to help young explorers launch successfully.

---

## ✅ Pre-Flight Checklist

### Step 1: Check Your Computer

- [ ] You have Python installed (version 3.8 or newer)
  - **Test:** Open terminal and type `python --version`
  - **If missing:** Download from [python.org](https://python.org)

### Step 2: Download the Project

- [ ] Download or clone this project to your computer
- [ ] Open terminal/command prompt in the project folder

### Step 3: Create Your Workspace

```bash
# Create a virtual environment (your own private coding space)
python -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

# You should see (venv) appear in your terminal prompt
```

### Step 4: Install the Tools

```bash
# Install all the required tools
pip install -r requirements.txt

# This should download google-generativeai and other tools
```

### Step 5: Get Your AI Key

- [ ] Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Sign in with your Google account
- [ ] Click "Create API Key"
- [ ] Copy the key (starts with "AIzaSy...")

### Step 6: Configure Your Secrets

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and replace "your_google_ai_api_key_here" with your real key
```

### Step 7: Test Launch! 🎯

```bash
python main.py
```

**Expected Result:** You should see:

1. A setup verification message
2. AI creates a blog post title
3. AI creates a hook for that title
4. AI writes a first paragraph using both

---

## 🐛 Troubleshooting Guide

### "No module named 'google.generativeai'"

**Solution:** Make sure you activated your virtual environment and ran `pip install -r requirements.txt`

### "GOOGLE_API_KEY not found"

**Solution:**

1. Check that you have a `.env` file (not `.env.example`)
2. Make sure your API key is correctly copied
3. No spaces around the = sign: `GOOGLE_API_KEY=your_key_here`

### "Permission denied" or "API key invalid"

**Solution:**

1. Double-check your API key in Google AI Studio
2. Make sure you copied the entire key
3. Try creating a new API key

### "Connection error" or "Network timeout"

**Solution:**

1. Check your internet connection
2. Some school networks block AI services - try from home
3. Wait a moment and try again (sometimes services are busy)

---

## 🎓 For Teachers and Parents

### Learning Objectives (10-15 minutes)

By the end of this session, students will:

- ✅ Successfully set up a development environment
- ✅ Understand the concept of prompt chaining
- ✅ See how each AI response builds on the previous one
- ✅ Experience the power of breaking complex tasks into simple steps

### Key Concepts Introduced

- **Variable substitution**: `{{topic}}` becomes "AI Agents"
- **Reference patterns**: `{{output[-1]}}` gets the previous response
- **Sequential thinking**: Each prompt builds on what came before
- **System design**: How simple patterns create complex behaviors

### Extension Questions

- "What other topics would you like to explore with prompt chains?"
- "How is this similar to how you solve math problems step by step?"
- "What would happen if we changed the order of the prompts?"
- "Can you think of other places where you build on previous work?"

### Safety Notes

- API keys should be kept private (like passwords)
- The AI uses your credits, so monitor usage
- All generated content should be reviewed by adults
- This is a learning tool - always think critically about AI outputs

---

## 🌟 Success Indicators

### You'll Know It's Working When:

- ✅ The terminal shows no scary red error messages
- ✅ You see AI responses that reference previous responses
- ✅ Each response builds naturally on the one before
- ✅ The final paragraph connects the title and hook cleverly

### You're Ready for More When:

- ✅ You understand what each part of the code does
- ✅ You can explain prompt chaining to someone else
- ✅ You're curious about modifying the prompts
- ✅ You want to try the more advanced experiments

---

## 🎯 Your Next Adventures

Once you've got the basic system working:

1. **Experiment with Topics**: Change `{"topic": "AI Agents"}` to something you're interested in
2. **Modify the Prompts**: Add your own instructions or change the style
3. **Try the Fusion Mode**: Uncomment `fusion_chain_poc()` to see models compete
4. **Explore the Ideas**: Check out `IDEAS.md` for 50+ project inspirations

---

## 🎪 The Magic You've Just Unlocked

What seems like a simple programming exercise is actually practice for one of the most important skills of the future: **thinking in systems**. Every time you create a prompt chain, you're learning to:

- **Break complex problems into manageable pieces**
- **Design processes that build on themselves**
- **Create emergent intelligence from simple rules**
- **Think like both an engineer and an artist**

You're not just learning to code - you're learning to think like the future.

**Welcome to the journey!** 🚀✨

---

_Remember: Every expert was once a beginner who refused to give up. Every amazing discovery started with someone being curious enough to try something new. You have the tools, you have the curiosity, and now you have the first successful experience. What will you explore next?_
