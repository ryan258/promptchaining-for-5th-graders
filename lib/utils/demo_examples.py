from copy import deepcopy
from typing import Any, Dict, Iterable, List


_TOOL_FORM_EXAMPLES = (
    {
        "label": "Photosynthesis primer",
        "fields": {
            "tool_key": "learning:concept_simplifier",
            "topic": "Photosynthesis",
            "context": "Audience: 5th graders\nTone: practical and vivid\nUse a plant-in-the-window example",
        },
    },
    {
        "label": "Fractions and basketball",
        "fields": {
            "tool_key": "learning:subject_connector",
            "topic": "Fractions and basketball",
            "context": "Audience: 5th graders\nShow how math shows up during a game\nKeep it concrete",
        },
    },
    {
        "label": "Volcanoes in plain language",
        "fields": {
            "tool_key": "learning:concept_simplifier",
            "topic": "Volcanoes",
            "context": "Audience: 5th graders\nUse cooking and pressure examples\nAvoid technical jargon",
        },
    },
    {
        "label": "Reading meets ecosystems",
        "fields": {
            "tool_key": "learning:subject_connector",
            "topic": "Ecosystems and reading comprehension",
            "context": "Audience: 5th graders\nConnect science ideas to nonfiction reading strategies",
        },
    },
    {
        "label": "Electricity quick demo",
        "fields": {
            "tool_key": "learning:concept_simplifier",
            "topic": "Electric circuits",
            "context": "Audience: 5th graders\nUse a flashlight as the anchor example\nKeep it under 5 short ideas",
        },
    },
)

_REASONING_FORM_EXAMPLES = (
    {
        "label": "Scientific method",
        "fields": {
            "pattern_name": "scientific_method",
            "hypothesis": "Bean plants grow faster when they get morning sunlight instead of afternoon sunlight",
            "context": "Audience: 5th graders\nFocus on fair testing and simple observations",
            "evidence_sources": "Plant journal\nWindow-light chart\nClassroom observations",
        },
    },
    {
        "label": "Socratic dialogue",
        "fields": {
            "pattern_name": "socratic_dialogue",
            "belief": "Homework should be optional for every student",
            "teacher_persona": "Curious principal",
            "depth": 4,
        },
    },
    {
        "label": "Design thinking",
        "fields": {
            "pattern_name": "design_thinking",
            "problem": "Students lose track of library books during busy weeks",
            "target_user": "5th grade student helper",
            "constraints": "Cheap materials\nEasy to use during class\nNo phone required",
        },
    },
    {
        "label": "Judicial reasoning",
        "fields": {
            "pattern_name": "judicial_reasoning",
            "case": "Should students be allowed one redo on a major quiz after extra practice?",
            "relevant_principles": "Fairness\nLearning growth\nClear expectations",
            "precedents": "Some teachers allow one retake\nAthletes improve with practice before a rematch",
        },
    },
    {
        "label": "Five whys",
        "fields": {
            "pattern_name": "five_whys",
            "problem": "Students forget to bring their water bottles to science lab",
            "depth": 5,
            "context": "Look for systems issues instead of blaming one student",
        },
    },
)

_ADVERSARIAL_FORM_EXAMPLES = (
    {
        "label": "Lunch debate",
        "fields": {
            "pattern_name": "red_vs_blue",
            "topic": "School lunch",
            "position_to_defend": "School lunch should include a daily salad bar",
            "rounds": 3,
            "judge_criteria": "Nutrition\nCost\nStudent buy-in",
        },
    },
    {
        "label": "Group work dialectic",
        "fields": {
            "pattern_name": "dialectical",
            "thesis": "Students should always work in groups during class projects",
            "context": "Think about both collaboration and independent focus time",
            "domain": "Elementary classroom design",
        },
    },
    {
        "label": "AI tutor stress test",
        "fields": {
            "pattern_name": "adversarial_socratic",
            "claim": "AI tutors can help 5th graders revise their writing",
            "depth": 4,
            "aggressive": True,
        },
    },
    {
        "label": "Homework debate",
        "fields": {
            "pattern_name": "red_vs_blue",
            "topic": "Homework",
            "position_to_defend": "Homework should be limited to 20 minutes a night in elementary school",
            "rounds": 2,
            "judge_criteria": "Learning value\nFamily stress\nConsistency",
        },
    },
    {
        "label": "Recess schedule dialectic",
        "fields": {
            "pattern_name": "dialectical",
            "thesis": "Recess should always come after lunch",
            "context": "Consider energy, behavior, and transition time across the school day",
            "domain": "School schedule planning",
        },
    },
)

_META_FORM_EXAMPLES = (
    {
        "label": "Fractions through sports",
        "fields": {
            "goal": "Teach fractions using basketball and soccer examples",
            "context_text": "audience: 5th graders\ntone: energetic\nUse sports kids already know",
            "constraints": "Keep it under 3 prompts\nUse everyday vocabulary",
        },
    },
    {
        "label": "Volcanoes with cooking",
        "fields": {
            "goal": "Explain volcanoes using cooking and pressure-cooker metaphors",
            "context_text": "audience: 5th graders\ntone: playful\nMake the science feel safe and concrete",
            "constraints": "Avoid scary disaster details\nEnd with one classroom demo idea",
        },
    },
    {
        "label": "Ecosystem food web",
        "fields": {
            "goal": "Design a chain that teaches food webs through a pond ecosystem story",
            "context_text": "audience: 5th graders\ntone: visual\nInclude predator and prey vocabulary support",
            "constraints": "Use no more than 4 prompts\nInclude one check for misconceptions",
        },
    },
    {
        "label": "Revision coach",
        "fields": {
            "goal": "Create a chain that helps 5th graders revise opinion paragraphs",
            "context_text": "audience: 5th graders\ntone: encouraging\nFocus on claim, evidence, and closing sentence",
            "constraints": "Keep each prompt short\nUse rubric-friendly language",
        },
    },
    {
        "label": "Weather patterns",
        "fields": {
            "goal": "Build a chain to explain weather patterns using local forecast examples",
            "context_text": "audience: 5th graders\ntone: curious\nUse clouds, wind, and temperature changes",
            "constraints": "Connect to a weekly forecast\nKeep examples classroom-friendly",
        },
    },
)


def _clone_examples(examples: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return deepcopy(list(examples))


def get_tool_demo_examples(available_tool_keys: Iterable[str]) -> List[Dict[str, Any]]:
    examples = _clone_examples(_TOOL_FORM_EXAMPLES)
    normalized_keys = sorted({str(key) for key in available_tool_keys if key})
    if not normalized_keys:
        return examples

    fallback_key = normalized_keys[0]
    for example in examples:
        tool_key = str(example["fields"].get("tool_key") or "")
        if tool_key not in normalized_keys:
            example["fields"]["tool_key"] = fallback_key
    return examples


def get_reasoning_demo_examples() -> List[Dict[str, Any]]:
    return _clone_examples(_REASONING_FORM_EXAMPLES)


def get_adversarial_demo_examples() -> List[Dict[str, Any]]:
    return _clone_examples(_ADVERSARIAL_FORM_EXAMPLES)


def get_meta_demo_examples() -> List[Dict[str, Any]]:
    return _clone_examples(_META_FORM_EXAMPLES)
