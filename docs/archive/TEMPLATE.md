# Tool Prompt Template

Use this template to ensure all new tools meet the "A-Grade" standard.

## Python String Format

```python
"""You are a [Specific Expert Role]. [Action Verb] this [Input].

[Brief Context/Goal].
Tone: {{tone}}

[Input Variable]:
{{input_variable}}

Perspective Framework:
- [Concept 1]: [Definition]
- [Concept 2]: [Definition]

Constraints:
- [Output Field 1]: Exactly [N] items.
- [Output Field 2]: Max [N] words.
- [Quality Control]: [Specific instruction, e.g., "No fluff"].

Example for [Specific Scenario]:
✅ GOOD: "[Concrete example of high-quality output]"
❌ BAD: "[Vague example of low-quality output]" ([Why it is bad])

Respond in JSON:
{
  "field_1": "Description (max N words)",
  "field_2": [
    "Item 1",
    "Item 2"
  ]
}"""
```

## Checklist
- [ ] **Role**: Is it specific? (e.g., "Antitrust Lawyer" vs "Lawyer")
- [ ] **Framework**: Does it cite a mental model? (e.g., "Principal-Agent Problem")
- [ ] **Constraints**: Are limits numeric and strict? (e.g., "Exactly 3")
- [ ] **Examples**: Is there a Good/Bad pair?
- [ ] **JSON**: Is the output valid JSON?
