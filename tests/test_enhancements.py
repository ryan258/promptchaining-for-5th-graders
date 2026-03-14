from unittest.mock import patch

from lib.enhancements.adversarial_chains import adversarial_socratic
from lib.enhancements.emergence_measurement import _invoke_chain_function, measure_emergence
from lib.enhancements.natural_reasoning import five_whys


def test_five_whys_supports_injected_model_and_callable(mock_model_info, sequence_llm):
    responses = [
        {
            "problem_statement": "Missed homework",
            "observable_symptoms": ["late submission"],
            "impact": "Grades drop",
        },
        {
            "why_number": 1,
            "question": "Why did it happen?",
            "cause": "Forgot the deadline",
            "evidence": "Calendar was empty",
            "is_root_cause": False,
        },
        {
            "why_number": 2,
            "question": "Why was the deadline forgotten?",
            "cause": "No weekly planning habit",
            "evidence": "Tasks tracked ad hoc",
            "is_root_cause": True,
        },
        {
            "causal_chain": ["Missed homework -> Forgot deadline -> No weekly planning habit"],
            "root_cause": "No weekly planning habit",
            "why_this_is_root": "It affects every assignment",
            "systemic_solutions": ["Create a planner routine"],
            "quick_fixes": ["Ask for reminders"],
            "prevention": "Review assignments every Sunday",
            "effort_vs_impact": "Low effort, high impact",
        },
    ]

    with patch("lib.core.chain.MinimalChainable.log_to_markdown", return_value="mock_log.md"):
        result, metadata = five_whys(
            "Missed homework",
            depth=2,
            model_info=mock_model_info,
            llm_callable=sequence_llm(responses),
        )

    assert result["synthesis"]["root_cause"] == "No weekly planning habit"
    assert metadata["depth"] == 2
    assert metadata["root_cause"] == "No weekly planning habit"


def test_adversarial_socratic_supports_injected_model_and_callable(mock_model_info, sequence_llm):
    responses = [
        {
            "claim": "School should start later",
            "initial_defense": "Students sleep more",
            "key_premises": ["Teens need sleep"],
            "confidence": "High",
        },
        {
            "round": 1,
            "target_weakness": "Bus schedules",
            "question": "What breaks if buses run later?",
            "why_this_matters": "Families rely on timing",
            "trap": "Admit logistics are harder",
        },
        {
            "round": 1,
            "response_type": "Refine",
            "response": "Phase changes by district",
            "revised_claim": "Later starts where transit allows",
            "confidence_now": "Medium",
            "what_you_learned": "Logistics matter",
        },
        {
            "survived": "Partially",
            "strongest_objections": ["Transit complexity"],
            "strongest_defenses": ["Student sleep improves"],
            "credibility": "Same",
            "clear_limits": "Transit-constrained districts",
            "refined_claim": "Later starts where transit allows",
            "confidence_verdict": "Case-by-case",
            "remaining_vulnerabilities": ["Staffing"],
        },
    ]

    with patch("lib.core.chain.MinimalChainable.log_to_markdown", return_value="mock_log.md"):
        result, metadata = adversarial_socratic(
            "School should start later",
            depth=1,
            model_info=mock_model_info,
            llm_callable=sequence_llm(responses),
        )

    assert result["verdict"]["survived"] == "Partially"
    assert metadata["rounds"] == 1
    assert metadata["survived"] == "Partially"


def test_measure_emergence_uses_explicit_chain_name_and_injected_dependencies(mock_model_info, sequence_llm):
    captured = {}

    def fake_chain(topic, model_info=None, llm_callable=None):
        captured["topic"] = topic
        captured["model_info"] = model_info
        captured["llm_callable"] = llm_callable
        return {"answer": "chain"}, {"total_tokens": 18}

    measurement_responses = [
        {"baseline": "one shot"},
        {
            "scores": {
                "approach_a": {"novelty": 9, "depth": 8, "coherence": 8, "pedagogical": 7, "actionability": 8},
                "approach_b": {"novelty": 6, "depth": 6, "coherence": 6, "pedagogical": 6, "actionability": 6},
            },
            "qualitative": {"summary": "Chain wins on depth and novelty."},
            "summary": "Chain wins on depth and novelty.",
        },
    ]

    comparison, metadata = measure_emergence(
        topic="Neural Networks",
        chain_function=fake_chain,
        chain_name="scientific_method",
        model_info=mock_model_info,
        llm_callable=sequence_llm(measurement_responses),
    )

    assert captured["topic"] == "Neural Networks"
    assert captured["model_info"] == mock_model_info
    assert comparison["chain_approach"] == "scientific_method"
    assert metadata["chain_function"] == "scientific_method"


def test_invoke_chain_function_uses_named_primary_argument_without_duplication(mock_model_info):
    captured = {}

    def scientific_method_like(hypothesis, model_info=None, llm_callable=None):
        captured["hypothesis"] = hypothesis
        captured["model_info"] = model_info
        captured["llm_callable"] = llm_callable
        return {"ok": True}, {"total_tokens": 0}

    result, metadata = _invoke_chain_function(
        scientific_method_like,
        "Gravity",
        mock_model_info,
        lambda *_: ("{}", {}),
        {"hypothesis": "Gravity"},
    )

    assert result == {"ok": True}
    assert metadata == {"total_tokens": 0}
    assert captured["hypothesis"] == "Gravity"
