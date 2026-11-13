# Advanced tools

Use Advanced when a specialised reasoning pattern, an existing learning tool or the Python API gives you something beyond the saved recipe workflow. Ordinary reusable work belongs in the main workbench so it keeps its checkpoint and resume behavior.

[Documentation index](README.md) · [Custom workbench chains](CHAIN-BUILDING.md) · [Architecture](ARCHITECTURE.md)

## Know which execution path you are using

Advanced tools have their own forms, provider calls, logs and artifact flows. Each logical step sends once; automatic transport and JSON-format retries have been removed. They do not become resumable workbench runs merely because you opened them from the same app.

| Workbench | Advanced framework flows |
| --- | --- |
| Prepare saves a ready run without calling a model. | A Run or Design action can make provider requests immediately. |
| One explicitly dispatched call per step, no automatic retries. | A function can make several explicit steps; each is attempted once. |
| SQLite checkpoint after every completed answer. | Outputs/logs/artifacts depend on the particular function. |
| Pause, review and edit the latest answer of an unfinished run. | The workbench's review and pause controls do not govern these executions. |
| ZIP workspace backups and single-run JSON exports. | Advanced designs and artifact JSON have their own formats. |

The workbench's one-active-run claim covers its own executor. It is not a global spending or concurrency limit across Advanced tools and separate CLI scripts. Keep those requests deliberate.

## Find the right tool

Open **Advanced** in the app.

| Tool area | Path | A useful job |
| --- | --- | --- |
| Learning tools | `/studio/tools` | Use the existing concept simplifier or subject connector. |
| Reasoning patterns | `/studio/reasoning` | Examine a question through a named reasoning method. |
| Adversarial patterns | `/studio/adversarial` | Generate opposing arguments and inspect weaknesses. |
| Meta-chain designer | `/studio/meta` | Ask a model to propose a prompt sequence. |
| Artifacts library | `/studio/artifacts` | Read framework outputs and final answers explicitly copied there. |

The forms use plain text. **Autofill Demo** loads example inputs; the separate Run/Design action executes them. Inspect what was filled before starting a live operation.

## Reasoning patterns

| Pattern | Use it to structure… | Your judgment still needs to establish… |
| --- | --- | --- |
| Scientific method | A hypothesis, proposed evidence and possible tests | Whether evidence exists, is accurately represented, and supports the claim |
| Socratic dialogue | Questions about a belief and its assumptions | Which answers actually match your situation |
| Design thinking | A problem, user needs, possibilities and proposed prototypes | Whether those needs and constraints come from real observations |
| Judicial reasoning | Facts, principles, precedent-like comparisons and a proposed judgment | The accuracy and applicability of any cited facts or authorities |
| Five whys | Possible root cause hypotheses for a recurring problem | Which causes are supported by observation and could be tested |

An evidence-source field is input text, not a browser or a document-fetch service. Providing a URL or source title does not mean the app retrieved its contents. Supply relevant material deliberately and check important claims outside the generated analysis.

These methods produce model-generated reasoning. The Scientific method pattern does not conduct an actual experiment; Judicial reasoning does not establish a legal conclusion. Choose the method for its structure, and verify the evidence needed for the real task.

## Adversarial patterns

**Red vs Blue** generates attacks, defences and a model judgment. Use it to surface objections to a plan you can describe concretely.

**Dialectical** develops a thesis, opposition and synthesis. Use it to explore a third approach when the original options are too narrow.

**Adversarial Socratic** applies critical questioning to a claim. Use it when you want assumptions and weak spots to become visible.

Depth and round settings change how much work these functions do. A model judge is another model output, not an independent verdict or factual benchmark. Depth and rounds accept 1–5; the form updates the request count before execution. Avoid treating debate length or confidence as evidence that a claim is true.

## Let a model propose a chain

In **Meta-Chain Designer**, enter a goal, plain context notes and one constraint per line. **Design Chain** calls the provider to generate a proposal. **Execute This Chain** is another explicit action that runs the proposed prompts.

Before executing, read **Generated Prompts**. Check that the sequence serves the goal, inputs are present, references point to existing earlier outputs, and the result has a useful form. Design generation itself can make provider calls even if you choose not to execute the proposal.

To keep a proposed method in the main workbench:

1. Open **Recipes → Build my own**.
2. Adapt the generated prompts into 1–8 named steps.
3. Replace any extra variables with the workbench's supported inputs or ordinary prompt text.
4. Check positional references using [Build your own chains](CHAIN-BUILDING.md).
5. Save the recipe and prepare a new workbench run when ready.

There is no automatic meta-design-to-workbench import button. **Copy design** and **Execution-ready JSON** provide the designer's own format; they are not Studio workspace backups.

## Reuse artifacts explicitly

The artifacts library is separate from saved recipes and runs. A completed workbench run can use **Save final to artifacts** to copy its final answer with a run-specific key. This does not move the run or make the artifact part of every future request.

For ordinary work, copy only the relevant artifact material into the next run's context. For Python workflows, `ArtifactStore` and `MinimalChainable` can resolve explicit references such as `{{artifact:topic:step}}` when an artifact store is supplied.

Artifacts persist as JSON files. Chroma holds a local mirror using deterministic hash vectors; these are not semantic embeddings, and the main workbench does not offer automatic semantic recall from that mirror.

## Use the Python framework when you need code

Run `./verify_demos.sh` for an offline demonstration of `MinimalChainable` with a fixed callable. This uses the same handoff syntax as a live script. [Demo guide](DEMOS.md)

The Python example below sends two live provider requests when run with a configured model. The portable API returns the answers, rendered prompts, and usage. Keep checkpointed work in the main workbench.

```python
from lib.core.chain import MinimalChainable
from lib.core.llm_client import get_model, request_completion

outputs, sent_prompts, usage = MinimalChainable.run(
    context={"topic": "Python dictionaries"},
    model=get_model(),
    llm_callable=request_completion,
    prompts=[
        "Identify three essential ideas in {{topic}} for someone who knows lists.",
        "Using {{output[-1]}}, give a short worked example and a practice question.",
    ],
    return_usage=True,
)
print(outputs[-1])
```

Core modules live in `lib/core/`: `chain.py`, `artifact_store.py`, `chain_composer.py`, `meta_chain_generator.py` and `llm_client.py`. Reasoning functions live in `lib/enhancements/`. Tool scripts live under `tools/`; they are not all exposed by the web tool picker.

`FusionChain` supports comparing configured models with a supplied evaluator. The emergence-measurement module can ask a model to compare outputs. Such scores reflect their evaluator; they do not establish truth or prove that every chain outperforms a single prompt.

Inspect the script and arguments before choosing a live demo. [Demo guide](DEMOS.md) · [Verification](TESTING.md)

## Execution limits and comparison records

Each learning tool runs four model steps. Scientific method, design thinking and judicial reasoning use five; Dialectical uses four. Five Whys uses `depth + 2`; Socratic, adversarial Socratic and Red vs Blue use `2 × depth/rounds + 2`. Depth and rounds are limited to 1–5. Meta design makes two calls; its separate execution action accepts 1–8 prompts. Failed calls and malformed JSON are never retried automatically.

Advanced operations run in worker threads so the workbench remains responsive. They still have no workbench checkpoint, pause or resume contract. After an ambiguous failure, check provider usage before another action.

The comparison module evaluates the first 2,000 characters of each output. It reports truncation, validates the score shape and range, and excludes failed comparisons from wins and ties. A failed chain does not trigger baseline or judge requests. Batch comparisons accept 1–20 topics. The retained significance field explicitly says that no statistical test was performed.

Legacy log costs are estimates only. Configure both `LOG_INPUT_TOKEN_PRICE_PER_MILLION` and `LOG_OUTPUT_TOKEN_PRICE_PER_MILLION` if you deliberately want an estimate. Otherwise cost is unknown. The local cost-report tool excludes workbench records and unreported attempts and cannot establish an account spending total.
