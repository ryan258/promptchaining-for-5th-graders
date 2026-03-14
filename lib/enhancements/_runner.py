"""Shared helpers for enhancement pattern execution."""

from typing import Any, Callable, Dict, List, Optional, Tuple

from ..core.chain import MinimalChainable
from ..core.llm_client import get_model, prompt


def execute_pattern(
    pattern_name: str,
    prompts: List[str],
    *,
    model_info: Optional[Tuple[Any, str]] = None,
    llm_callable: Callable = prompt,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Any], List[Any]]:
    """Run a pattern with shared logging and injectable model/callable dependencies."""
    active_model = model_info or get_model()
    result, filled_prompts, usage, _trace = MinimalChainable.run(
        context=context or {},
        model=active_model,
        llm_callable=llm_callable,
        return_trace=True,
        prompts=prompts,
    )
    MinimalChainable.log_to_markdown(pattern_name, filled_prompts, result, usage)
    return result, usage
