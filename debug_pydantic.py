from chain import FusionChainResult
from typing import List, Any
import json

import concurrent.futures

def create_result():
    return FusionChainResult(
        top_response="test",
        all_prompt_responses=[["response"]],
        all_context_filled_prompts=[["prompt"]],
        performance_scores=[1.0],
        model_names=["model"],
        all_usage_stats=[[{"usage": 1}]]
    )

try:
    print("Running with ThreadPoolExecutor...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(create_result)
        result = future.result()
    
    print("Instantiation successful.")
    
    print("Dumping model...")
    dump = result.model_dump()
    print("Dump successful.")
    print(json.dumps(dump))

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
