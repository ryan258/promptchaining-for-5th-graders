#!/usr/bin/env python3
"""
🎯 Dream Job Reverse Engineer (adult mode)

Decode a job posting for hidden priorities, pain points, application strategy, resume bullets, and STAR stories.

Usage:
    python tools/career/dream_job_reverse_engineer.py "path/to/job.txt"
    python tools/career/dream_job_reverse_engineer.py "Job text here" --context "Your profile, target angle"
"""

import os
import json
from datetime import datetime

try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args

project_root = setup_project_root(__file__)

from chain import MinimalChainable
from main import build_models, prompt


def _load_text(input_str: str) -> str:
    if os.path.isfile(input_str):
        with open(input_str, "r", encoding="utf-8") as f:
            return f.read()
    return input_str


def dream_job_reverse_engineer(job_posting: str, additional_context: str = ""):
    print("🎯 Dream Job Reverse Engineer")

    posting = _load_text(job_posting)
    print(f"Posting length: {len(posting)} chars")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Confident and direct")
    career = user_profile.get("career_profile", {})

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "job_posting": posting,
        "tone": tone,
        "additional_context": additional_context,
        "target_role": career.get("target_role", ""),
        "notable_wins": ", ".join(career.get("wins", [])),
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Decode hidden priorities
            """You are a veteran tech recruiter and hiring manager with 15+ years experience decoding job postings to identify what companies ACTUALLY want (not what they say they want), specializing in reading between the lines for organizational pain points and culture fit signals.

Decode this job posting to reveal hidden priorities by analyzing:

**Job posting decoder framework:**

1. **Repeated themes** - Words/phrases appearing 3+ times reveal true priorities (e.g., "fast-paced" 5x = chaos/burnout culture)
2. **Order matters** - First 3 requirements = must-haves, rest = nice-to-haves
3. **Urgency signals** - "Immediate start", "backlog", "scaling" = fire drill, someone quit/was fired
4. **Buzzword density** - High buzzword count + vague outcomes = inexperienced manager or troubled team
5. **What's NOT said** - Missing elements reveal gaps (no mention of team size = you'll be solo, no growth path = dead-end)

**Culture tells in language:**
- "Wear many hats" = understaffed, no specialists
- "Fast-paced, dynamic" = long hours, shifting priorities
- "Startup mentality" at large corp = dysfunctional politics
- "Self-starter" = little mentorship/support
- "Passionate" = expect off-hours work

**Example for job posting saying "Looking for passionate, self-starting full-stack engineer in fast-paced startup. Must excel at wearing many hats. Bonus: experience scaling systems from 0-1M users":**
✅ GOOD:
Hidden priorities: [
  "Solo firefighter - 'many hats' + 'self-starter' + no team size mentioned = you'll be only engineer or in tiny team with urgent backlog",
  "Scaling crisis - 'fast-paced' + 'scaling 0-1M users' in required section = actively breaking under load, need immediate fix",
  "Understaffed/underfunded - every buzzword signals resource constraint: 'startup' + 'many hats' + 'passionate' (code for 'accept below-market pay')",
  "Culture of overwork - 'passionate' (2x) + 'fast-paced' = expect 50-60hr weeks, limited work-life boundary"
]
Culture vibe: "Firefighting mode with minimal support. High urgency, likely came from someone leaving abruptly (vacancy). Expect autonomy by necessity, not by design. Startup language at what might be later stage = organizational dysfunction or overpromised growth."
Red flags: ["No mention of team size/structure (solo role risk)", "'Passionate' and 'fast-paced' = burnout culture", "Scaling problem in requirements (not optional) = critical production issues", "Many hats = no specialization, everything is your problem"]

❌ BAD:
Hidden priorities: ["They want a good engineer", "Startup culture", "Need to scale"]
Culture vibe: "Fast-paced"
Red flags: ["Might be busy"]
(Too generic, doesn't decode specific language, misses urgency signals, no analysis of what's omitted)

Tone: {{tone}}
Additional context: {{additional_context}}
Target role (if provided): {{target_role}}

Job posting:
{{job_posting}}

Respond in JSON:
{
  "hidden_priorities": [
    "Specific decoded priority with evidence from posting language (max 35 words each)"
  ],
  "culture_vibe": "Synthesized culture reading from language patterns, buzzwords, what's emphasized vs omitted (max 50 words)",
  "red_flags": [
    "Specific concern with evidence from posting (max 25 words each)"
  ],
  "green_flags": [
    "Positive signals if any (specific examples, max 25 words each)"
  ]
}

Provide exactly 3-5 hidden priorities, exactly 2-4 red flags, exactly 1-3 green flags (or state 'None detected' if truly none). Quote specific posting language when decoding.""",
            # Manager pain points
            """You are an organizational psychologist and recruitment consultant expert in diagnosing team/manager pain points from job postings and role requirements.

Identify the specific problems this manager is trying to solve by hiring for this role.

**Pain point framework - Ask:**

1. **What broke?** - Is this role replacing someone who left/failed? (Urgency, detailed requirements = post-mortem)
2. **What's blocking them?** - What can't they ship/do without this role? (Requirements reveal bottlenecks)
3. **What's their risk?** - What are they afraid of? (Requirements that seem excessive = past failures)
4. **Who burned them?** - Oddly specific requirements = previous hire disaster (e.g., "must meet deadlines" = last person missed deadlines)

**Pain point quality - Make them specific:**
✅ GOOD: "Shipping velocity stalled (backlog mentions '6mo of work queued'). Last PM couldn't scope/say no → 3 half-finished projects, eng team demoralized. Need someone to enforce scope discipline and ship small iterations fast."

❌ BAD: "Wants good communication" (too generic, not a pain point, just a preference)

**Example for posting emphasizing "Must work cross-functionally with sales, support, and engineering":**
✅ GOOD:
Manager pain points: [
  "Siloed teams creating misalignment - sales promising features that don't exist, support escalating bugs that aren't prioritized, eng building features nobody asked for. Need someone to coordinate roadmap across functions and prevent overpromises.",
  "Lack of technical credibility with stakeholders - repeated emphasis on 'translating technical concepts to non-technical audiences' suggests eng team can't/won't communicate, causing trust issues. Need diplomat who can bridge gap.",
  "Backlog chaos - no mention of existing roadmap or strategy, all language is about 'prioritization' and 'tradeoffs'. Likely have 100+ requests, no framework to decide. Need someone to establish ruthless prioritization system."
]

❌ BAD:
Manager pain points: ["Need cross-functional collaboration", "Want better communication", "Have to prioritize work"]
(Not actual problems, just responsibilities; no specificity about what's broken or why)

Hidden priorities: {{output[-1].hidden_priorities}}
Culture vibe: {{output[-1].culture_vibe}}
Red flags: {{output[-1].red_flags}}

Respond in JSON:
{
  "manager_pain_points": [
    "Specific problem with evidence/context of why it's painful and what failure looks like (max 45 words each)"
  ]
}

Provide exactly 3-5 pain points in priority order. Each must describe a PROBLEM (what's broken/blocked/failing), not a wish (what they want).""",
            # Application strategy
            """You are a career strategist expert in candidate positioning, personal branding, and creating narrative differentiation in competitive job markets.

Design an application strategy that positions you as THE solution to their top pain points.

**Positioning framework:**

1. **Pick ONE theme** - Don't be everything, be the one thing they need most
   - If pain = chaos → theme = "Brings order to complexity"
   - If pain = slow execution → theme = "Rapid shipper who delivers"
   - If pain = failed hires → theme = "Proven track record in [exact context]"

2. **Proof > promises** - Theme means nothing without concrete evidence
   - Weak: "I'm a great communicator" (claim)
   - Strong: "Aligned eng/sales/support on 12mo roadmap, reduced feature request escalations 60%" (proof)

3. **Mirror their language** - Use their exact pain point keywords in your positioning
   - They say "scaling bottleneck" → you say "scaled from X to Y users"
   - They say "cross-functional alignment" → you say "unified 4 teams under single roadmap"

**Example for pain points: shipping velocity stalled, scope creep, team demoralization:**
✅ GOOD:
Application theme: "Ruthless scope enforcer who ships fast"
Strategy angle: "You need someone who can say no to stakeholders, cut features aggressively, and ship weekly iterations instead of quarterly releases. I've done this before: at X company, inherited 6-month backlog, killed 60% of features, shipped MVP in 3 weeks that captured 80% of value."
Proof targets: [
  "Shipped X product MVP in 3 weeks by cutting scope 60%, captured $2M revenue in Q1 (pain: slow shipping)",
  "Reduced scope creep by implementing RFC process, decreased feature requests by 40% (pain: scope creep)",
  "Turned around demoralized eng team (5.1→7.8 engagement score) by shipping visible wins weekly (pain: team morale)"
]

❌ BAD:
Application theme: "Experienced product manager"
Strategy angle: "I have PM experience and work well with teams"
Proof targets: ["Led projects", "Worked with engineers", "Made decisions"]
(Generic theme, no specific solution to pain points, vague proof with no measurements)

Pain points identified: {{output[-1].manager_pain_points}}
Notable wins (if provided): {{notable_wins}}
Additional context: {{additional_context}}

Respond in JSON:
{
  "application_theme": "4-8 word memorable phrase that positions you as solution to #1 pain (max 10 words)",
  "strategy_angle": "Your 'pitch' explaining why you're THE solution to their pain, tying theme to specific past successes (max 50 words)",
  "proof_targets": [
    "Specific achievement/project that proves you've solved similar pain, with measurements (max 30 words each)"
  ],
  "language_mirror": "List 5-7 exact keywords/phrases from job posting to echo in application (max 10 words total)"
}

Provide exactly 3-4 proof targets. Each must directly address one of their top pain points with quantified outcomes.""",
            # Resume bullets
            """You are a professional resume writer expert in achievement-oriented bullet points, specializing in tech/product roles and ATS optimization.

Write resume bullets that prove your positioning theme using the pain-proof-result pattern.

**Resume bullet framework:**

**Formula: [Action verb] + [specific project/situation] + [quantified outcome] + [(tie to pain point)]**

**Action verbs by type:**
- Leadership: Led, Directed, Spearheaded, Orchestrated, Championed
- Speed/execution: Shipped, Delivered, Launched, Accelerated, Streamlined
- Problem-solving: Resolved, Eliminated, Reduced, Diagnosed, Restructured
- Growth: Scaled, Grew, Expanded, Increased, Improved

**Quantification rules:**
- Use %: "Increased X by 45%" (not "significantly improved")
- Use $: "Generated $2.4M in revenue" (not "drove revenue")
- Use time: "Reduced from 6 weeks to 3 days" (not "made faster")
- Use scale: "0 to 50K users in 3 months" (not "grew user base")

**Example bullets for theme "Ruthless scope enforcer who ships fast":**
✅ GOOD:
- "Shipped MVP in 3 weeks (vs. 6mo plan) by cutting 60% of requirements, generating $2M Q1 revenue and validating product-market fit before competitors entered market"
- "Eliminated scope creep by implementing RFC process with kill criteria, reducing feature requests by 40% and increasing engineering focus time from 55% to 82%"
- "Accelerated delivery cadence from quarterly to weekly releases by ruthlessly prioritizing top 3 features, improving team velocity 3.2x and NPS by 23 points"

❌ BAD:
- "Managed product development and delivered features" (no specifics, no outcome, passive voice)
- "Worked with engineering team to improve processes" (vague action, no measurement, no result)
- "Successfully launched product that users liked" (no timeline, no metrics, "successfully" is filler)

Pain points: {{output[-2].manager_pain_points}}
Theme: {{output[-1].application_theme}}
Strategy angle: {{output[-1].strategy_angle}}
Proof targets: {{output[-1].proof_targets}}

Respond in JSON:
{
  "resume_bullets": [
    "Bullet following formula: action verb + specific project + quantified outcome tied to pain point (max 25 words each)"
  ]
}

Provide exactly 3 bullets. Each must include at least 2 numbers (%, $, time, scale). Start with powerful action verb. No weak qualifiers like 'helped', 'assisted', 'tried', 'successfully'.""",
            # STAR stories
            """You are an interview coach expert in STAR method storytelling and behavioral interview preparation.

Create STAR story outlines for each bullet that you can expand in interviews - these prove your bullets are real, not embellished.

**STAR story framework:**

**Situation (15-20% of story)**: Context - what was broken? Set up the problem
- Include: Team size, timeline, what was at stake
- Example: "Inherited product with 6mo backlog, team burned out from 3 failed launches, revenue target at risk"

**Task (10-15% of story)**: Your specific responsibility - what were YOU asked to do?
- Include: Your role, what success looked like, constraints
- Example: "Asked to ship revenue-generating MVP in Q1 (10 weeks) with same team, no new resources"

**Action (50-60% of story)**: What YOU did - specific steps, decisions, how you handled obstacles
- Include: Your decisions, specific tactics, how you handled resistance/obstacles
- Example: "Killed 60% of features using cost-benefit matrix, implemented weekly ship cycles, dealt with stakeholder pushback by showing revenue projections for MVP-first approach"

**Result (15-20% of story)**: Quantified outcome - numbers, impact, what changed
- Include: Metrics that improved, dollars earned/saved, time saved, team impact
- Example: "Shipped in 3 weeks (7 weeks early), $2M Q1 revenue (exceeded target), team velocity 3x, model used for next 4 products"

**Example STAR for bullet "Shipped MVP in 3 weeks by cutting 60% of requirements, generating $2M Q1 revenue":**
✅ GOOD:
Situation: "Joined product team with 6-month backlog for new B2B feature. Previous PM had scoped massive release (15 features). Team was burned out from 3 prior projects that launched late with bugs. $5M annual revenue target depended on Q1 launch. I inherited this 2 weeks before Q1."
Task: "Asked to ship something revenue-generating in 10 weeks with 4-person eng team, no additional resources. Success = at least $2M Q1 revenue, working software (not buggy mess), team doesn't quit."
Action: "Week 1: interviewed sales (identified 3 features generating 80% of revenue interest), created kill matrix (effort vs. revenue impact), presented to CEO. Killed 60% of features, focused on top 3. Week 2-3: daily standups to catch blockers, said 'no' to 7 stakeholder requests, protected eng focus time. Pushed back on QA wanting 2-week test cycle (negotiated to 3 days with automated tests). Shipped MVP week 3."
Result: "Generated $2.1M in Q1 (beat target), MVP had 2 minor bugs (vs. typical 20+), shipped 7 weeks early saving $120K in eng cost, team velocity increased from 8 → 25 story points/sprint. Approach became template for next 4 product launches. Two stakeholders initially angry, but both later admitted focus was right."

❌ BAD:
Situation: "Product launch was behind"
Task: "Needed to ship it"
Action: "Made a plan and executed it"
Result: "Launched successfully"
(No specifics, no numbers, no obstacles mentioned, no proof this actually happened, sounds fabricated)

Resume bullets: {{output[-1].resume_bullets}}

Respond in JSON:
{
  "interview_stories": [
    {
      "bullet": "Quote the bullet this story proves (max 25 words)",
      "star": {
        "situation": "Context and problem setup with specifics: team size, timeline, what was at stake (max 50 words)",
        "task": "Your specific responsibility and success criteria (max 35 words)",
        "action": "3-5 specific actions YOU took, including how you handled obstacles/resistance (max 80 words)",
        "result": "Quantified outcomes with at least 3 metrics: revenue, time, efficiency, team impact (max 50 words)"
      },
      "proof_points": [
        "Specific detail that makes story verifiable/believable (names, numbers, tools, processes used)"
      ]
    }
  ]
}

Provide exactly 3 STAR stories, one per bullet. Include enough detail that the story sounds real, not generic. Add 3-4 proof points per story (specific tools, people, processes, numbers that make it credible)."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "career", "dream_job_reverse_engineer")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-dream_job.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("dream_job_reverse_engineer", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    posting, context = get_input_from_args(
        description="Reverse engineer a job posting into strategy, bullets, and STAR stories",
        default_context_help="Your profile, constraints, or angle"
    )
    dream_job_reverse_engineer(posting, context)


if __name__ == "__main__":
    main()
