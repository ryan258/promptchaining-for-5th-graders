"""Framework enhancements: Natural Reasoning, Adversarial Chains, Emergence Measurement."""

from .natural_reasoning import (
    scientific_method,
    socratic_dialogue,
    design_thinking,
    judicial_reasoning,
    five_whys,
    REASONING_PATTERNS
)

from .adversarial_chains import (
    red_vs_blue,
    dialectical,
    adversarial_socratic,
    ADVERSARIAL_PATTERNS
)

from .emergence_measurement import (
    measure_emergence,
    batch_measure,
    generate_report,
    quick_test
)

__all__ = [
    # Natural Reasoning
    'scientific_method',
    'socratic_dialogue',
    'design_thinking',
    'judicial_reasoning',
    'five_whys',
    'REASONING_PATTERNS',
    # Adversarial Chains
    'red_vs_blue',
    'dialectical',
    'adversarial_socratic',
    'ADVERSARIAL_PATTERNS',
    # Emergence Measurement
    'measure_emergence',
    'batch_measure',
    'generate_report',
    'quick_test'
]
