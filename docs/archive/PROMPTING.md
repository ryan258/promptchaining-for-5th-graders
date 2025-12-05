# Prompt Engineering Guide

This guide documents the "A-Grade" prompt engineering patterns used in this project. These patterns are designed to transform generic LLM outputs into high-quality, expert-level analysis.

## Core Philosophy
We treat prompts as **code**, not conversation. A good prompt "programs" the model to adopt a specific cognitive stance and adhere to strict output constraints.

## The 5 Pillars of Optimization

### 1. Role Assignment
**What:** Assign a specific, high-competence expert persona.
**Why:** Primes the model's latent knowledge, vocabulary, and tone.
**Pattern:** `You are a [Specific Expert] specializing in [Niche Domain].`

> **Example:**
> *   **Generic:** "You are a helpful assistant."
> *   **A-Grade:** "You are an Antitrust Lawyer and Institutional Economist. Detect 'Regulatory Capture' and 'Rent-Seeking'."

### 2. Perspective Framework
**What:** Force the model to apply a specific mental model, theory, or academic framework.
**Why:** Anchors analysis in established concepts, reducing hallucination and generic fluff.
**Pattern:** `Perspective Framework: - [Theory Name]: [Brief definition]`

> **Example:**
> *   **Generic:** "Analyze the incentives."
> *   **A-Grade:**
>   ```text
>   Perspective Framework:
>   - Principal-Agent Problem: The agent (employee) has different incentives than the principal (employer).
>   - Campbell's Law: "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures."
>   ```

### 3. Constraints
**What:** Strict, numerical limits on output size, format, and content.
**Why:** Forces density and precision. Without constraints, models tend to be verbose and vague.
**Pattern:** `Constraints: - [Field]: Exactly [N] items. - [Field]: Max [N] words.`

> **Example:**
> *   **Generic:** "List some reasons."
> *   **A-Grade:**
>   ```text
>   Constraints:
>   - Factions: Exactly 2-3 key players.
>   - Fault Lines: Exactly 3 structural weaknesses.
>   - Severity: Low, Medium, High.
>   ```

### 4. Examples (Few-Shot)
**What:** Provide concrete "Good" vs "Bad" examples to calibrate quality.
**Why:** Shows the model exactly what "specific" or "insightful" looks like.
**Pattern:** `✅ GOOD: [Example] | ❌ BAD: [Example]`

> **Example:**
> *   **A-Grade:**
>   ```text
>   Example for "Wildcard":
>   ✅ GOOD: "Room-temperature superconductors discovered, eliminating cooling requirements."
>   ❌ BAD: "Computers get faster." (Too vague, just a trend)
>   ```

### 5. Specificity
**What:** Replace vague adjectives with concrete, actionable requirements.
**Why:** "Interesting" is subjective; "Counter-intuitive" or "Structural" is actionable.
**Pattern:** Avoid "Analyze this". Use "Extract X", "Map Y", "Stress-test Z".

> **Example:**
> *   **Generic:** "What is the subtext?"
> *   **A-Grade:** "Identify 'Costly Signals' and 'Countersignaling'. Who is the Alpha?"

## Checklist for New Tools
When creating or upgrading a tool, ensure it meets these criteria:

- [ ] **Role**: Does it have a specific expert persona?
- [ ] **Framework**: Does it cite a specific mental model or theory?
- [ ] **Constraints**: Are there exact counts (e.g., "Exactly 3") and length limits?
- [ ] **Examples**: Is there at least one Good/Bad example pair?
- [ ] **Specificity**: Are vague terms replaced with concrete instructions?
- [ ] **Output**: Is the output strictly JSON?
