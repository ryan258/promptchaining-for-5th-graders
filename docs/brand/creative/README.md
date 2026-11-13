# Creative files

## Rainy Recess teacher pack

- [Printable teacher pack and student worksheet](rainy-recess.pdf). US Letter, two pages. Print page 1 for the teacher. Print page 2 for students when leading the paper activity.
- [Editable HTML and reading version](rainy-recess.html). The teacher page uses the actual Studio workflow. The student page adapts the handoff as an exercise that works with paper and pencil.

The worksheet uses the fictional clues and prepared draft from [Rescue rainy recess](../../../lib/workbench/classroom_cases.py). The example fix on the teacher page is illustrative. Leave it for discussion after students make their own choice.

## Campaign artwork

| Use | 1200 × 630 PNG | SVG master | Alternative text |
| --- | --- | --- | --- |
| Studio overview, release page, project note | [Studio card](../assets/social-studio.png) | [Studio master](../assets/social-studio.svg) | Prompt Chaining Studio. Make the next step better. A checked answer appears in the next prompt. |
| Teacher outreach, class activity, educator newsletter | [Classroom card](../assets/social-classroom.png) | [Classroom master](../assets/social-classroom.svg) | Classroom Challenges. Find the clue. Fix the draft. |
| Workbench guide, practitioner note, project page | [Workbench card](../assets/social-workbench.png) | [Workbench master](../assets/social-workbench.svg) | Workbench. Pick up where you left off. |

Use the [editable social template](../assets/social-template.svg) to make another card. Place the same important text in the accompanying post or page. The cards are proposed campaign artwork. Use the [press and partner kit](../PRESS-AND-PARTNER-KIT.md#media-handoff) to capture current product screens for an external release. See the [visual identity guide](../VISUAL-IDENTITY.md) for wordmarks, single-color artwork, icon exports, and placement rules.

## Rebuild the teacher pack

From the repository root, use the installed WeasyPrint renderer.

```bash
weasyprint --pdf-tags docs/brand/creative/rainy-recess.html docs/brand/creative/rainy-recess.pdf
```

The PDF is tagged for document structure. After editing, confirm the PDF has two Letter pages and check the render for legible text and space to write. The HTML is the editable source.
