# 🚀 Quick Start: Your Cognitive Exoskeleton

**Goal**: Get your first tool working in < 5 minutes.

## Step 1: Verify Setup (30 seconds)

```bash
# Should already work if demos work
python demos/concept_simplifier/main.py
# If this runs, you're good to go
```

## Step 2: Test Your First Tool (2 minutes)

```bash
# Generate a guide outline
python tools/content/evergreen_guide.py "Progressive overload for people with chronic fatigue"
```

**What happens**:
1. Loads your user profile from `context/user_profile.json`
2. Runs 5-step analysis chain (~2 minutes)
3. Saves markdown outline to `output/guides/`
4. Prints summary to console

**Expected output**:
```
🌲 Evergreen Guide Architect
📝 Topic: Progressive overload for people with chronic fatigue

... (chain runs) ...

✅ Guide outline saved to: output/guides/20241203-1430-progressive-overload.md
✅ Full chain log saved to: logs/...

📊 SUMMARY
==========================================================
🎯 Overall Quality Score: 8.5/10
📚 Estimated Length: 2000-2500 words
⏱️  Reading Time: 10-12 minutes
🔖 Bookmark-worthy: Yes

💪 Strengths:
   • Addresses energy management directly
   • Clear progression framework
   • Practical modifications included

✨ Ready to write! Open: output/guides/...
```

## Step 3: Review the Output (1 minute)

```bash
# Open the generated outline
open output/guides/[your-file].md
# or
cat output/guides/[your-file].md | head -50
```

You'll see:
- User intent analysis
- Differentiation strategy
- Complete section outline
- Key metaphors to use
- Research citations needed
- Evergreen audit
- Quality scores

## Step 4: Customize Your Profile (2 minutes)

Edit `context/user_profile.json`:

```json
{
  "writing_style": {
    "tone": "Your preferred tone here",
    "avoid": ["Hype", "Unsubstantiated claims"],
    "prefer": ["Personal experience", "Data"]
  }
}
```

Tools will automatically use your preferences.

## Common Workflows

### Content Creation Flow

```bash
# 1. Generate outline (2 min)
python tools/content/evergreen_guide.py "Your topic"

# 2. Review outline
open output/guides/latest.md

# 3. Write draft using outline
# (in your editor of choice)

# 4. Repurpose when done (future tool)
# python tools/content/content_repurposer.py draft.md
```

### Health Research Flow (future)

```bash
# 1. Parse new study (3 min)
python tools/health/medical_consensus.py --url "study-url"

# 2. Review risk-adjusted summary
open output/health/research/latest.md

# 3. Make decision
python tools/health/protocol_decision.py "Intervention name"

# 4. Track results
# (Update your health logs)
```

### Preparation Flow (future)

```bash
# Before important meeting/appointment
python tools/cognitive/advocacy_prep.py "Doctor appointment - requesting MRI"

# Review prep document
open output/prep/latest.md

# Walk in confident with:
# - Clear goals
# - Prepared responses
# - Must-have outcomes
```

## Energy Management Tips

### On High-Energy Days
- Generate multiple outlines
- Build up your backlog
- Batch similar tasks

### On Low-Energy Days
- Use pre-generated outlines to write
- Run research parser on articles
- Quick prep before appointments

### On "Stuck" Days
```bash
# Future tool
python tools/cognitive/blocker_breaker.py
# Get unstuck in 10 minutes
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'chain'"
```bash
# Make sure you're in project root
cd /path/to/promptchaining-for-5th-graders
python tools/content/evergreen_guide.py "Topic"
```

### "No user profile found"
Tool will still work with defaults, but customize for better results:
```bash
# Copy template if needed
cp context/user_profile.json context/user_profile-backup.json
# Edit with your preferences
```

### Tool runs but output is generic
- Customize `context/user_profile.json`
- Add `--context "More specific notes"` to command
- Try piping in your rough notes: `cat notes.md | python tools/...`

## What's Next?

1. **Try it with a real topic** you want to write about
2. **Customize your user profile** to match your voice
3. **Check the roadmap** (`RMAP-CS.md`) for upcoming tools
4. **Give feedback**: What works? What doesn't? What's missing?

---

## Quick Reference

```bash
# Content
python tools/content/evergreen_guide.py "Topic"
cat notes.md | python tools/content/evergreen_guide.py

# Health (coming soon)
python tools/health/medical_consensus.py --url "url"
python tools/health/symptom_correlator.py health/logs/2024-12.json
python tools/health/protocol_decision.py "Intervention"

# Cognitive (coming soon)
python tools/cognitive/advocacy_prep.py "Situation"
python tools/cognitive/blocker_breaker.py
```

---

**From idea to outline in 2 minutes.**
**From research to decision in 3 minutes.**
**From stuck to unstuck in 10 minutes.**

**Tools that work *especially well* on bad days.**
