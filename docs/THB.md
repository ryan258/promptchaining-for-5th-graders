# Testing Handbook (THB)

**Purpose:** Simple step-by-step instructions to test the Prompt Chaining Lab
**Updated:** December 6, 2025
**For:** Phase 2 - Meta-Chain Studio, Patterns, and Parallel Lab

---

## 🎯 What You're Testing

- ✅ **Phase 1:** Tool Grid, Artifact Sidebar, Basic Tools
- ✅ **Phase 2:** Meta-Chain Studio, Reasoning Patterns, Debates & Emergence

---

## 📋 Prerequisites (One-Time Setup)

### 1. Check Python & Node Installed

```bash
python3 --version  # Should be 3.8+
node --version     # Should be 18+
npm --version      # Should be 9+
```

If missing, install them first.

### 2. Install Dependencies (if not done)

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd web
npm install
cd ..
```

### 3. Set Up OpenRouter API Key

Create `.env` file in project root:

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your key:
OPENROUTER_API_KEY=your_key_here
```

**Where to get key:** https://openrouter.ai/keys

---

## 🚀 Starting the Application

### Step 1: Start Backend Server

Open Terminal 1:

```bash
cd server
python3 main.py
```

**✅ Success looks like:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal running. Do not close it.**

---

### Step 2: Start Frontend Server

Open Terminal 2 (new terminal):

```bash
cd web
npm run dev
```

**✅ Success looks like:**
```
VITE v7.2.6  ready in 823 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Leave this terminal running. Do not close it.**

---

### Step 3: Open Browser

Go to: **http://localhost:5173**

**✅ You should see:**
- Header: "Prompt Chaining Lab"
- 4 tabs: Tools | Meta-Chain | Patterns | Debates & Emergence
- "Tools" tab is selected by default

---

## 🧪 Test Suite

### TEST 1: Basic Tools (5 minutes)

**Goal:** Verify Phase 1 still works

#### 1.1 Test Tool Grid

1. You should see tool cards in a grid
2. Click on **"Concept Simplifier"** card
3. Card should highlight in blue

**✅ Pass:** Card highlights when clicked

---

#### 1.2 Test Basic Tool Execution

1. In the topic field, type: **"Quantum Computing"**
2. Click **"Run Tool"** button
3. Button should show "Executing chain..."
4. Wait 20-60 seconds

**✅ Pass:** You see:
- Chain execution steps appear
- Each step shows a role (e.g., "Decomposer", "Analogizer")
- Final result shows formatted content
- No red error boxes

**❌ Fail:** If you see error, check:
- Is backend server running?
- Is OpenRouter API key set in .env?
- Check Terminal 1 for error messages

---

#### 1.3 Test Artifact Sidebar

1. Click **"Artifacts"** button (top right)
2. Sidebar should slide in from left
3. You should see folders or "No artifacts yet"
4. Click **X** to close sidebar

**✅ Pass:** Sidebar opens and closes smoothly

---

### TEST 2: Meta-Chain Studio (10 minutes)

**Goal:** Test chain design and execution

#### 2.1 Navigate to Meta-Chain

1. Click **"Meta-Chain"** tab at top
2. You should see Meta-Chain Studio interface
3. Brain icon on left

**✅ Pass:** Interface loads with form fields

---

#### 2.2 Design a Chain

1. **Goal field:** Type "Explain blockchain to a 10-year old"
2. **Context field:** Type "Use simple analogies"
3. **Cognitive moves:** Click these pills:
   - decompose
   - analogize
   - synthesize
4. Click **"Design chain"** button
5. Wait 30-60 seconds

**✅ Pass:** You see:
- "Designing chain..." shows while waiting
- Design appears with:
  - "Design reasoning" section
  - List of prompts (3-5 prompts shown)
  - Each prompt in editable textarea
  - "Save template" button appears

**What you're looking at:**
- The AI designed a custom chain for your goal
- Prompts are the actual steps it will run
- You can edit prompts before executing

---

#### 2.3 Execute the Designed Chain

1. Scroll down to see all prompts
2. (Optional) Edit a prompt if you want
3. Click **"Execute designed chain"** button (green)
4. Wait 30-90 seconds

**✅ Pass:** You see:
- "Executing..." message
- Chain execution trace appears below
- Shows step-by-step results
- No errors

**❌ Fail:** If error "prompts have no content":
- Make sure prompts aren't empty
- Refresh page and try again

---

#### 2.4 Save as Template

1. **Template name field:** Type "Blockchain for Kids"
2. Click **"Save template"** button (purple)
3. Look in "Saved templates" section
4. You should see your template name

**✅ Pass:** Template appears in list

**Try loading it:**
1. Refresh the page
2. Click your template name button
3. Form should fill with saved data

**✅ Pass:** Template loaded correctly

---

### TEST 3: Reasoning Patterns (10 minutes)

**Goal:** Test scientific method, socratic, etc.

#### 3.1 Navigate to Patterns

1. Click **"Patterns"** tab at top
2. You should see 5 pattern buttons:
   - Scientific Method
   - Socratic Dialogue
   - Design Thinking
   - Judicial Reasoning
   - 5 Whys

**✅ Pass:** All 5 patterns visible

---

#### 3.2 Test Scientific Method

1. Click **"Scientific Method"** (should be selected by default)
2. Fill in form:
   - **Hypothesis:** "MS fatigue is worsened by dehydration"
   - **Context:** "Exploring MS symptom management"
   - **Evidence sources:** Leave blank (optional)
3. Click **"Run pattern"** button
4. Wait 60-120 seconds (this one is slower - 5 steps)

**✅ Pass:** You see:
- "Running pattern..." message
- Multi-column viewer appears with 5 columns:
  - Observations
  - Predictions
  - Experimental Design
  - Analysis
  - Conclusion
- Each column has content
- Metadata chips below (pattern name, verdict, etc.)

**What you're seeing:**
- The full scientific method applied to your hypothesis
- Each phase of the method in a separate column

---

#### 3.3 Test Socratic Dialogue

1. Click **"Socratic Dialogue"** button at top
2. Form fields change - you should see:
   - **Belief to test:** (empty field)
   - **Questioner persona:** (default: "Philosopher")
   - **Rounds:** (default: 5)
3. Fill in:
   - **Belief:** "AI will make doctors obsolete"
   - Leave others as default
4. Click **"Run pattern"**
5. Wait 60-90 seconds

**✅ Pass:** You see:
- Chronological feed: Belief -> Rounds -> Synthesis
- Dialogue shows back-and-forth questioning
- Final synthesis card at the bottom

---

#### 3.4 Test 5 Whys

1. Click **"5 Whys"** button
2. Fill in:
   - **Problem:** "I forgot to take my medication"
   - **Context:** "This happens often"
   - **Whys:** 5 (default)
3. Click **"Run pattern"**
4. Wait 30-60 seconds

**✅ Pass:** You see:
- Chronological feed: Problem -> Why Chain -> Synthesis
- Why Chain shows 5 levels of "why"
- Root cause identified in final card

---

### TEST 4: Debates & Emergence (10 minutes)

**Goal:** Test adversarial reasoning and emergence comparison

#### 4.1 Navigate to Parallel Lab

1. Click **"Debates & Emergence"** tab
2. You should see 2 mode buttons:
   - Debate: Red vs Blue
   - Emergence Compare

**✅ Pass:** Interface loads with mode selector

---

#### 4.2 Test Red vs Blue Debate

1. **Mode:** Should be "Debate: Red vs Blue" (default)
2. Fill in form:
   - **Topic:** "Healthcare AI"
   - **Position to defend:** "AI should replace human doctors for diagnostics"
   - **Rounds:** 2 (to save time)
3. Click **"Run"** button
4. Wait 90-150 seconds (this is slow - multiple back-and-forth)

**✅ Pass:** You see:
- "Running..." message
- Chronological feed appears:
  - Blue Team (Opening)
  - Rounds (Red Attack / Blue Defense)
  - Judge's Verdict (at the bottom)
- Judge shows winner badge and detailed scoring
- Metadata below shows scores

**What you're seeing:**
- Blue Team defends the position
- Red Team attacks it
- Judge evaluates both sides
- This is adversarial reasoning in action

---

#### 4.3 Test Emergence Compare

1. Click **"Emergence Compare"** button at top
2. Form changes - you should see:
   - **Topic:** (empty)
   - **Chain to test:** (dropdown with options)
   - **Context:** (optional)
   - **Baseline prompt:** (optional)
3. Fill in:
   - **Topic:** "Machine Learning"
   - **Chain to test:** "Scientific Method" (default)
   - Leave others empty
4. Click **"Run"**
5. Wait 120-180 seconds (SLOW - runs chain twice)

**✅ Pass:** You see:
- Comparison Grid (Side-by-side):
  - Baseline Output (Left)
  - Chain Output (Right)
- Analysis & Metrics section below:
  - Executive Summary
  - Detailed Scores (Novelty, Depth, etc.)
- Winner badge shows "Chain" or "Baseline" or "Tie"

**What you're seeing:**
- Same topic processed two ways:
  1. Multi-step chain (Scientific Method)
  2. Single mega-prompt (baseline)
- AI comparing which approach produced better output
- This measures "emergence" - do chains unlock more than single prompts?

---

## 🎨 Visual Quality Check

Walk through the UI and check:

### Colors & Styling
- **Glass cards:** Translucent dark backgrounds with blur
- **Buttons:** Blue highlights when selected
- **Icons:** Lucide icons render correctly
- **Text:** Readable white/gray on dark background

**✅ Pass:** UI looks polished, no broken styling

---

### Animations
- **Sidebar:** Slides in from left smoothly
- **Loading spinners:** Rotate during execution
- **Hover effects:** Cards/buttons highlight on hover

**✅ Pass:** Animations smooth, no jank

---

### Responsive Design
1. Resize browser window to narrow (mobile width)
2. Check that:
   - Tool grid becomes single column
   - Forms stack vertically
   - Multi-column viewers stack

**✅ Pass:** Mobile layout works

---

## ⚠️ Common Issues & Fixes

### Issue: "Failed to load tools"

**Fix:**
1. Check backend server is running (Terminal 1)
2. Check URL is http://localhost:5173 (not 3000)
3. Restart backend server

---

### Issue: "Failed to design chain" / "Pattern execution failed"

**Fix:**
1. Check `.env` file has OPENROUTER_API_KEY
2. Check API key is valid (try at openrouter.ai)
3. Check Terminal 1 for Python errors
4. Try a different/simpler goal/hypothesis

---

### Issue: "Templates unavailable (storage blocked)"

**Reason:** localStorage is disabled (Safari private mode)

**Fix:**
- Use regular browser mode, OR
- Ignore - templates won't save but everything else works

---

### Issue: Execution takes forever / times out

**Reasons:**
- OpenRouter is slow
- Complex chains take time
- Network issues

**Fix:**
1. Wait up to 5 minutes max
2. Check Terminal 1 for timeout errors
3. Try simpler input
4. Check internet connection

---

### Issue: Frontend won't start / shows blank page

**Fix:**
```bash
# Terminal 2
cd web
rm -rf node_modules
npm install
npm run dev
```

---

### Issue: Backend imports fail

**Fix:**
```bash
# From project root
pip install --upgrade -r requirements.txt

# Try running from project root instead:
cd ..  # Go to project root
python3 -m server.main
```

---

## 📊 Success Criteria Checklist

After testing, you should have verified:

**Phase 1: Core Experience**
- [ ] Tool grid displays and selects tools
- [ ] Basic tool execution works (Concept Simplifier)
- [ ] Results display correctly
- [ ] Artifact sidebar opens/closes

**Phase 2: Meta-Chain Studio**
- [ ] Chain design generates prompts
- [ ] Prompts are editable
- [ ] Chain execution works
- [ ] Templates save and load

**Phase 2: Reasoning Patterns**
- [ ] All 5 patterns are listed
- [ ] Scientific Method runs and shows 5 phases
- [ ] Socratic Dialogue runs
- [ ] 5 Whys runs and shows why chain

**Phase 2: Parallel Lab**
- [ ] Red vs Blue debate runs
- [ ] Debate shows 3 columns (Blue/Red/Judge)
- [ ] Emergence compare runs
- [ ] Scores display with winner

**UI Quality**
- [ ] Glass morphism styling looks good
- [ ] No broken layouts
- [ ] Loading states show clearly
- [ ] Errors display in red boxes when they occur

---

## 🎯 Quick Smoke Test (2 minutes)

If you just want to verify everything works quickly:

1. **Start servers** (backend + frontend)
2. **Open http://localhost:5173**
3. **Test Tools tab:**
   - Run Concept Simplifier on "AI"
   - Wait for result
4. **Test Meta-Chain tab:**
   - Design chain for "Explain cars"
   - Execute it
5. **Test Patterns tab:**
   - Run 5 Whys on "I'm tired"
6. **Test Parallel Lab:**
   - Skip (slowest tests)

**If all 4 work: ✅ System is healthy**

---

## 🤯 Fast "WOW" Examples (optional)

Use these if you want to sanity-check and impress quickly:

- **Concept Simplifier:** “Why does time slow down near a black hole?” (checks analogies + step trace)
- **Meta-Chain Studio:** Goal “Optimal morning routine for peak performance” with moves decompose/analogize/synthesize/apply (checks design + execute)
- **Scientific Method:** Hypothesis “Cold showers boost immune function” (5 columns show true/false predictions and experiment design)
- **Red vs Blue Debate:** Topic “We are living in a computer simulation” | Position “Yes” | Rounds 2 (checks debate + judge verdict)
- **Emergence Compare:** Topic “Where are all the aliens (Fermi paradox)” | Chain “Design Thinking” (checks chain vs baseline scoring)

---

## 🔍 What To Report If Something Breaks

When filing an issue, include:

1. **What you did:** Exact steps
2. **What you expected:** What should have happened
3. **What happened:** Error message, behavior
4. **Terminal output:** Copy from Terminal 1 (backend logs)
5. **Browser console:** Open DevTools, copy errors

**Example Good Report:**
```
Testing: Meta-Chain Studio design
Steps:
1. Clicked Meta-Chain tab
2. Entered goal "Explain physics"
3. Clicked Design chain button

Expected: Chain design to appear
Actual: Red error box "Failed to design chain"

Backend logs:
ERROR: HTTPException 500 - Invalid response from LLM

Browser console:
POST http://localhost:8000/api/meta-chain/design 500
```

---

## 📝 Testing Notes Space

Use this space to write notes as you test:

```
Date: _______________

TEST 1 (Tools): [ ] Pass  [ ] Fail
Notes: _________________________________

TEST 2 (Meta-Chain): [ ] Pass  [ ] Fail
Notes: _________________________________

TEST 3 (Patterns): [ ] Pass  [ ] Fail
Notes: _________________________________

TEST 4 (Parallel Lab): [ ] Pass  [ ] Fail
Notes: _________________________________

Issues Found:
1. _________________________________
2. _________________________________
3. _________________________________

Overall: [ ] Ready to use  [ ] Needs fixes
```

---

## 🎉 You're Done!

If you made it through the full test suite with no failures, **the system is working perfectly**.

You now have a fully functional personal AI reasoning laboratory!

**Next Steps:**
- Use it for real work
- Save interesting templates
- Experiment with different patterns
- See how chains compare to single prompts

**Need help?** Check the logs in Terminal 1 or open browser DevTools console.

---

**Happy Testing! 🚀**
