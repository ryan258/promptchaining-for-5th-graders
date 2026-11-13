# chain.py - The Heart of Prompt Chaining
# This file contains the magic that lets us chain prompts together
# Think of it like building with LEGO blocks - each prompt builds on the last one

import json  # Helps us work with data that looks like {"key": "value"}
import re    # Helps us find patterns in text (like finding JSON in markdown)
from typing import List, Dict, Callable, Any, Union, Tuple, Optional, Literal, overload  # These tell Python what types of data we expect
from pydantic import BaseModel  # Helps us create clean data structures
import concurrent.futures  # Lets us do multiple things at the same time
import os
import math
import datetime
from uuid import uuid4

from .errors import InputError
from .limits import validate_prompts
from .llm_client import Completion, normalize_usage
from .templates import render_template, validate_template_inputs

# Import artifact store for persistent knowledge accumulation
from .artifact_store import ArtifactStore, _atomic_replace

def _parse_response_json(response: Any, *, allow_embedded: bool = False) -> Any:
    """Recognize JSON without repairing an incomplete answer into a valid handoff."""
    if not isinstance(response, str):
        return response
    fence = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
    fenced = fence.search(response) if allow_embedded else fence.fullmatch(response.strip())
    candidate = fenced[1] if fenced else response.strip()
    if allow_embedded and not fenced:
        start = re.search(r"[{\[]", candidate)
        end = max(candidate.rfind("}"), candidate.rfind("]"))
        if start and end >= start.start():
            candidate = candidate[start.start():end + 1]
    if not candidate.startswith(("{", "[")):
        return response
    try:
        return json.loads(candidate)
    except (ValueError, RecursionError):
        return response


# This is like a report card that tells us how our fusion chain did
class FusionChainResult(BaseModel):
    """
    This is like a trophy case that holds all our results.
    When we run multiple AI models and make them compete,
    this holds who won and how everyone did.
    """
    top_response: str
    all_prompt_responses: List[List[Any]]
    all_context_filled_prompts: List[List[str]]
    performance_scores: List[float]
    model_names: List[str]
    all_usage_stats: List[List[Any]]

class FusionChain:
    """
    FusionChain runs multiple AI models in parallel and makes them compete!
    """
    @staticmethod
    def run(
        context: Dict[str, Any],
        models: List[Any],
        llm_callable: Optional[Callable] = None,
        prompts: Optional[List[str]] = None,
        evaluator: Optional[Callable[[List[str]], Tuple[str, List[float]]]] = None,
        get_model_name: Optional[Callable[[Any], str]] = None,
        num_workers: int = 4,              # How many models to run at the same time
        artifact_store: Optional['ArtifactStore'] = None,  # Optional artifact store
        topic: Optional[str] = None,  # Optional topic for artifacts
        callable: Optional[Callable] = None,  # Legacy alias for llm_callable
    ) -> FusionChainResult:
        """
        This is like the regular run() function, but faster!
        
        Instead of asking each friend one at a time, we ask all our friends
        at the same time. This is called "parallel processing" - doing
        multiple things at once to save time.
        """
        # Backward compatibility:
        # Historically this argument was named `callable`. Keep supporting it.
        if llm_callable is None:
            llm_callable = callable
        if llm_callable is None:
            raise ValueError("FusionChain.run requires `llm_callable` (or legacy `callable`).")
        if prompts is None:
            raise ValueError("FusionChain.run requires `prompts`.")
        if evaluator is None:
            raise ValueError("FusionChain.run requires `evaluator`.")
        if get_model_name is None:
            raise ValueError("FusionChain.run requires `get_model_name`.")

        fusion_id = uuid4().hex[:12]

        def process_model(index, model):
            """
            This little function runs the prompt chain for one model.
            We need this because of how parallel processing works.
            """
            outputs, context_filled_prompts, usage_stats, trace = MinimalChainable.run(
                context, model, llm_callable, prompts,
                return_trace=True,
                artifact_store=artifact_store,
                topic=f"{topic or 'fusion'}_{fusion_id}_model_{index + 1}" if artifact_store is not None else topic
            )
            if not trace["completion_complete"]:
                raise InputError("A comparison answer did not finish. Review saved artifacts before evaluating it.")
            return outputs, context_filled_prompts, usage_stats

        # Create empty lists to store results
        # Pre-size the result lists so we can populate them by model index
        all_outputs = [None] * len(models)
        all_context_filled_prompts = [None] * len(models)
        all_usage_stats = [None] * len(models)

        # This is the parallel magic - we create a "thread pool"
        # Think of it like having multiple workers who can all work at the same time
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit tasks and remember which future belongs to which model index
            future_to_index = {
                executor.submit(process_model, idx, model): idx
                for idx, model in enumerate(models)
            }
            
            # Collect the results as workers finish, storing them by index to preserve ordering
            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                outputs, context_filled_prompts, usage_stats = future.result()
                all_outputs[idx] = outputs
                all_context_filled_prompts[idx] = context_filled_prompts
                all_usage_stats[idx] = usage_stats

        # The rest is the same as the regular run() function
        # Judge the results and package them up
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)
        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            model_names=model_names,
            all_usage_stats=all_usage_stats,
        )

class MinimalChainable:
    """
    This is the heart of the whole system!

    MinimalChainable lets you chain prompts together like links in a chain.
    Each prompt can use:
    1. Variables from your context (like {{name}} gets replaced with a real name)
    2. Answers from previous prompts (like {{output[-1]}} gets the last answer)

    It's like having a conversation where each question builds on the previous answers.
    """

    @staticmethod
    def _extract_role_from_prompt(prompt: str) -> Optional[str]:
        """
        Extract the persona/role from a prompt.
        Looks for patterns like "You are a [role]" or "You are an [role]"
        """
        patterns = [
            r"You are an? ([^.,\n]+(?:specializing in [^.,\n]+)?)",
            r"As an? ([^.,\n]+),",
        ]

        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                role = match.group(1).strip()
                # Clean up and title case
                role = role.replace("  ", " ")
                return role

        return None

    @staticmethod
    @overload
    def run(
        context: Dict[str, Any],
        model: Any,
        llm_callable: Optional[Callable] = None,
        prompts: Optional[List[str]] = None,
        return_usage: Literal[False] = False,
        return_trace: Literal[False] = False,
        artifact_store: Optional['ArtifactStore'] = None,
        topic: Optional[str] = None,
        callable: Optional[Callable] = None,
    ) -> Tuple[List[Any], List[str]]:
        ...

    @staticmethod
    @overload
    def run(
        context: Dict[str, Any],
        model: Any,
        llm_callable: Optional[Callable] = None,
        prompts: Optional[List[str]] = None,
        return_usage: Literal[True] = True,
        return_trace: Literal[False] = False,
        artifact_store: Optional['ArtifactStore'] = None,
        topic: Optional[str] = None,
        callable: Optional[Callable] = None,
    ) -> Tuple[List[Any], List[str], List[Any]]:
        ...

    @staticmethod
    @overload
    def run(
        context: Dict[str, Any],
        model: Any,
        llm_callable: Optional[Callable] = None,
        prompts: Optional[List[str]] = None,
        return_usage: bool = False,
        return_trace: Literal[True] = True,
        artifact_store: Optional['ArtifactStore'] = None,
        topic: Optional[str] = None,
        callable: Optional[Callable] = None,
    ) -> Tuple[List[Any], List[str], List[Any], Dict[str, Any]]:
        ...

    @staticmethod
    def run(
        context: Dict[str, Any],    # Variables to use in prompts (like {{topic}})
        model: Any,                 # The AI model to use
        llm_callable: Optional[Callable] = None,  # Function that sends prompts to the AI
        prompts: Optional[List[str]] = None,      # List of prompts to run in order
        return_usage: bool = False,  # Whether to return usage stats
        return_trace: bool = False,   # Whether to return execution trace
        artifact_store: Optional['ArtifactStore'] = None,  # Store for saving/loading artifacts
        topic: Optional[str] = None,  # Topic name for artifact storage (auto-detected if not provided)
        callable: Optional[Callable] = None,  # Legacy alias for llm_callable
    ) -> Union[Tuple[List[Any], List[str]], Tuple[List[Any], List[str], List[Any]], Tuple[List[Any], List[str], List[Any], Dict]]:
        """
        This is where the magic happens!

        Think of this like following a recipe where each step uses ingredients
        from previous steps. We start with our context (ingredients) and
        each prompt (recipe step) can use what we made before.

        Returns:
            - If return_usage=False and return_trace=False: (outputs, context_filled_prompts)
            - If return_usage=True and return_trace=False: (outputs, context_filled_prompts, usage_stats)
            - If return_trace=True: (outputs, context_filled_prompts, usage_stats, execution_trace)
        """
        # Backward compatibility:
        # Historically this argument was named `callable`. Keep supporting it.
        if llm_callable is None:
            llm_callable = callable
        if llm_callable is None:
            raise ValueError("MinimalChainable.run requires `llm_callable` (or legacy `callable`).")
        if prompts is None:
            raise ValueError("MinimalChainable.run requires `prompts`.")
        
        validate_prompts(prompts)

        # Create empty lists to store our results
        output = []                    # Stores AI responses
        context_filled_prompts = []    # Stores the actual prompts we sent
        usage_stats_list = []          # Stores usage stats

        # Auto-detect topic from context if not provided
        if topic is None and artifact_store is not None:
            topic = context.get("topic") or context.get("subject_A") or context.get("subject_a")

        validate_template_inputs(prompts, context, allow_artifacts=artifact_store is not None)

        steps = []
        artifact_names = set()
        completion_complete = True
        # Go through each prompt one by one
        for i, prompt in enumerate(prompts):

            prompt, artifact_keys_used = render_template(prompt, context, output, artifact_store)

            # Save the prompt with all variables filled in
            # This helps us debug and see exactly what we sent to the AI
            context_filled_prompts.append(prompt)

            # One logical step invokes its callable once. Formatting mistakes
            # and provider errors never trigger hidden billable requests.
            result_raw = llm_callable(model, prompt)
            completion = result_raw if isinstance(result_raw, Completion) else None
            usage = None
            if completion is not None:
                result, usage = completion.text, completion.usage
                if completion.finish_reason not in (None, "stop"):
                    completion_complete = False
                else:
                    result = _parse_response_json(result)
            else:
                if isinstance(result_raw, tuple) and len(result_raw) == 2:
                    result_raw, usage = result_raw
                result = _parse_response_json(result_raw, allow_embedded=True)
            output.append(result)

            role = MinimalChainable._extract_role_from_prompt(prompts[i])
            counts = normalize_usage(usage)
            if usage is None:
                stored_usage = {}
            elif hasattr(usage, "model_dump"):
                stored_usage = usage.model_dump()
            elif hasattr(usage, "dict"):
                stored_usage = usage.dict()
            elif hasattr(usage, "__dict__"):
                stored_usage = vars(usage)
            else:
                stored_usage = usage
            usage_stats_list.append(stored_usage)
            artifact_key = None
            if artifact_store is not None and topic:
                step_name = re.sub(r"[^a-z0-9]+", "_", (role or "").lower()).strip("_")[:100]
                step_name = step_name or f"step_{i + 1}"
                if step_name in artifact_names:
                    step_name = f"{step_name}_{i + 1}"
                    while step_name in artifact_names:
                        step_name = f"{step_name}_"
                artifact_names.add(step_name)
                artifact_store.save(
                    topic=topic,
                    step_name=step_name,
                    data=result,
                    metadata={
                        "prompt_index": i,
                        "original_prompt": prompts[i][:100] + "..." if len(prompts[i]) > 100 else prompts[i],
                        "artifacts_used": artifact_keys_used,
                        **({"finish_reason": completion.finish_reason, "response_id": completion.response_id,
                            "response_model": completion.response_model} if completion is not None else {}),
                    },
                )
                artifact_key = f"{artifact_store._normalize_key(topic)}:{step_name}"

            if return_trace:
                step = {"step_number": i + 1, "role": role or f"Step {i + 1}",
                        "prompt": prompt, "response": result, "tokens": counts.get("total_tokens")}
                if artifact_key is not None:
                    step["artifact_key"] = artifact_key
                if completion is not None:
                    step.update(raw_response=completion.text, finish_reason=completion.finish_reason,
                                response_id=completion.response_id, response_model=completion.response_model)
                steps.append(step)

            if not completion_complete:
                if not return_trace and i + 1 < len(prompts):
                    raise InputError(f"Step {i + 1} did not finish. Review the partial answer before continuing.")
                break

        if return_trace:
            execution_trace = {
                "steps": steps,
                "final_result": output[-1] if output else None,
                "total_tokens": sum(step["tokens"] or 0 for step in steps),
                "usage_complete": all(step["tokens"] is not None for step in steps),
                "completion_complete": completion_complete,
            }
            return output, context_filled_prompts, usage_stats_list, execution_trace

        # Return outputs, filled-in prompts, and usage stats (if requested)
        if return_usage:
            return output, context_filled_prompts, usage_stats_list

        return output, context_filled_prompts

    @staticmethod
    def to_delim_text_file(name: str, content: List[Union[str, dict]]) -> str:
        """
        This function saves our results to a text file in a pretty format.
        
        It's like creating a scrapbook of our prompt chain - each result
        gets its own section with chain emoji to show the progression.
        """
        result_string = ""  # We'll build up the final text here
        
        # Create a file with the given name
        with open(f"{name}.txt", "w", encoding="utf-8") as outfile:
            # Go through each item in our content
            for i, item in enumerate(content, 1):  # Start counting from 1
                
                # Convert dictionaries and lists to JSON strings
                if isinstance(item, dict):
                    item = json.dumps(item)
                if isinstance(item, list):
                    item = json.dumps(item)
                
                # Create a pretty header with chain emoji
                # More emoji = later in the chain
                chain_text_delim = (
                    f"{'🔗' * i} -------- Prompt Chain Result #{i} -------------\n\n"
                )
                
                # Write to file and build our return string
                outfile.write(chain_text_delim)
                outfile.write(item)
                outfile.write("\n\n")

                result_string += chain_text_delim + item + "\n\n"

        return result_string

    @staticmethod
    def log_to_markdown(
        demo_name: str,
        prompts: List[str],
        responses: List[Any],
        usage_stats: List[Any] = None
    ) -> str:
        """
        Logs the run results to a markdown file in the /logs directory.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logs_dir = os.path.join(project_root, "logs")

        # Create logs directory if it doesn't exist
        os.makedirs(logs_dir, exist_ok=True)

        # Generate timestamped filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", demo_name)[:100] or "chain"
        filename = f"{timestamp}_{safe_name}.md"
        filepath = os.path.join(logs_dir, filename)

        markdown_content = f"# 🪵 Log: {demo_name}\n\n"
        markdown_content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Only estimate when both prices are explicitly configured. Unknown
        # usage or prices must never look like a zero-dollar provider invoice.
        counts = [normalize_usage(usage) for usage in (usage_stats or [])]
        total_input_tokens = sum(usage.get("prompt_tokens", 0) for usage in counts)
        total_output_tokens = sum(usage.get("completion_tokens", 0) for usage in counts)
        complete = len(counts) == len(prompts) and bool(counts) and all(
            {"prompt_tokens", "completion_tokens"} <= usage.keys() for usage in counts
        )
        label = "Tokens reported" if complete else "Known token subtotal (some usage unavailable)"
        markdown_content += f"**{label}**: {total_input_tokens} in / {total_output_tokens} out\n\n"
        try:
            input_price = float(os.environ["LOG_INPUT_TOKEN_PRICE_PER_MILLION"])
            output_price = float(os.environ["LOG_OUTPUT_TOKEN_PRICE_PER_MILLION"])
            if not complete or not all(math.isfinite(v) and v >= 0 for v in (input_price, output_price)):
                raise ValueError()
            estimate = (total_input_tokens * input_price + total_output_tokens * output_price) / 1_000_000
            markdown_content += f"**Estimated Cost**: ${estimate:.6f}\n"
            markdown_content += f"**Price assumptions**: ${input_price:g} input / ${output_price:g} output per million tokens; configured rates, not verified billing.\n\n"
        except (KeyError, ValueError):
            markdown_content += "**Estimated Cost**: Unknown — complete usage and explicit token prices are required.\n\n"

        markdown_content += "## 🗣️ Prompts Sent\n\n"
        for i, prompt in enumerate(prompts, 1):
            markdown_content += f"### Prompt #{i}\n"
            markdown_content += f"```text\n{prompt}\n```\n\n"

        markdown_content += "## 🤖 AI Responses\n\n"
        for i, response in enumerate(responses, 1):
            markdown_content += f"### Response #{i}\n"

            # Format response nicely
            if isinstance(response, (dict, list)):
                formatted_response = json.dumps(response, indent=2)
                markdown_content += f"```json\n{formatted_response}\n```\n\n"
            else:
                markdown_content += f"{response}\n\n"

        try:
            _atomic_replace(filepath, markdown_content)
            return filepath
        except OSError:
            print("Could not save the local chain log.")
            return ""
