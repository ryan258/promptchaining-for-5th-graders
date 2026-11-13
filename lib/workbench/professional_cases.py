"""Authored practice packets and answers. The examples make no provider requests."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProfessionalCase:
    title: str
    topic: str
    audience: str
    context: str
    description: str
    rubric: tuple[str, ...]
    steps: tuple[tuple[str, str, str], ...]
    outputs: tuple[str, ...]


CASES = {
    "decision-memo": ProfessionalCase(
        title="Decision memo",
        topic="Should we standardize how internal service requests are submitted?",
        audience="Operations lead who can approve a limited trial",
        description="Use a small operating sample to choose a reversible next step.",
        context="""[D1] Intake log. Over two weeks, 14 of 40 requests by email needed follow-up for missing details. In the same period, 5 of 20 requests submitted through the form needed follow-up. Teams chose their own channel. The log does not break down request type or urgency.

[D2] Service constraints. The operations lead can approve a two-week pilot for one team with no software purchase. Urgent requests must retain the existing phone route. The help desk lead can count follow-ups and check daily for missed urgent requests.

[D3] Options raised. Keep the current channels, offer the form as the default to one team, or make the form mandatory for every team.""",
        rubric=(
            "Quote the sample as 14/40 and 5/20 and explain the limits of self-selection.",
            "Compare keeping the current process, piloting the form, and requiring it across teams.",
            "Name who can approve the next step, what to measure, and when to pause or reconsider.",
        ),
        steps=(
            ("Frame the choice", "Identify the options, constraints, and quality of the evidence.",
             "For {{audience}}, frame this decision: {{topic}}\n\nPacket:\n{{context}}\n\nList the options and constraints. Cite packet IDs and distinguish observations from conclusions."),
            ("Test the recommendation", "Check whether the evidence justifies the proposed choice.",
             "Use this framing:\n{{output[-1]}}\n\nCheck against the original packet:\n{{context}}\n\nCompare the options, explain what the sample can support, and suggest a reversible decision with a way to test it."),
            ("Write the memo", "Use the reviewed recommendation to produce a decision someone can act on.",
             "Write a short decision memo for {{audience}}. Question: {{topic}}\n\nOriginal packet:\n{{context}}\n\nReviewed recommendation:\n{{output[-1]}}\n\nInclude the decision, evidence limits, pilot owner, success and stop criteria, and when to reconsider."),
        ),
        outputs=(
            "D1 reports 14/40 email requests (35%) and 5/20 form requests (25%) needing follow-up. Teams self-selected their channel, and case mix is unknown. D2 permits a one-team pilot and requires that the urgent phone route stay open. D3 gives three options: current process, a one-team default, or an all-team mandate.",
            "The form reduced follow-up by 10 percentage points, so make it mandatory across teams. The two-week pilot could confirm the gain after rollout.",
            "Recommendation: approve a two-week form-default pilot for one team. Keep email available and preserve the urgent phone route.\n\nEvidence: follow-up was needed for 14/40 email requests (35%) and 5/20 form requests (25%) [D1]. The observed gap is 10 percentage points. Channel choice and unknown case mix prevent attributing that gap to the form. The current process avoids transition costs but leaves the follow-up burden untested. A mandate exceeds the current approval and would make reversal harder [D2, D3].\n\nThe operations lead approves the pilot. The help desk lead tracks follow-up counts by channel and request type and checks daily for missed urgent requests. Pause if the urgent route fails or an urgent request is missed. At two weeks, review matched request types and record whether the follow-up pattern warrants a wider trial. If the counts are too small to compare, keep the pilot conclusion open.",
        ),
    ),
    "evidence-brief": ProfessionalCase(
        title="Evidence brief",
        topic="What does the accessible-template pilot establish about publication checks?",
        audience="A documentation manager preparing a pilot update",
        description="Trace claims to a supplied source packet and identify what remains unknown.",
        context="""[E1] Baseline checklist export. In April, 76 of 100 reviewed pages passed all automated publishing checks. The sample came from the help and reference sections.

[E2] Pilot checklist export. In May, 91 of 100 reviewed pages passed the same automated checks. The sample came from the help section only. The team switched to the updated template and ran a staff refresher in the same week.

[E3] Accessibility acceptance notes. The checklist checks heading order, missing form labels and missing alternative-text attributes. No screen-reader or keyboard testing was recorded. The checklist cannot determine whether alternative text is meaningful.""",
        rubric=(
            "Report 76/100 and 91/100 with source IDs and describe the 15-percentage-point observed change.",
            "Separate automated checks, accessibility acceptance, and attribution to the template.",
            "Name what to sample next and what direct human check would support a stronger conclusion.",
        ),
        steps=(
            ("Build the evidence table", "Record what each source can support before writing the conclusion.",
             "Task: {{topic}}\n\nSource packet:\n{{context}}\n\nSummarize each source with ID, observation, sample and limitation."),
            ("Review draft claims", "Check whether causal and accessibility claims go beyond the sources.",
             "Evidence table:\n{{output[-1]}}\n\nSource packet:\n{{context}}\n\nPropose an update for {{audience}}. Label each claim supported, inference, or unsupported. Flag missing direct checks."),
            ("Write the evidence brief", "Leave the reader with supportable claims and the next verification step.",
             "Use the reviewed claims below and write a short evidence brief for {{audience}}.\n\nClaims:\n{{output[-1]}}\n\nSource packet:\n{{context}}\n\nState what the data show, what remains unknown, and a practical verification step. Cite source IDs near claims."),
        ),
        outputs=(
            "E1: 76/100 April pages passed the automated checklist. The sample covers help and reference. E2: 91/100 May pages passed the same checks. The sample covers help only. The template and refresher started together. E3: the checklist checks three machine-detectable conditions. It contains no record of keyboard or screen-reader testing and cannot judge alternative-text quality.",
            "Supported: The new template improved accessibility by 15 percentage points [E1, E2]. The automated checks prove keyboard and screen-reader acceptance [E3].",
            "Finding: 91 of 100 May pages passed the automated checklist, compared with 76 of 100 April pages. The observed difference is 15 percentage points [E1, E2].\n\nLimits: April included help and reference pages, while May included help only. The template and staff refresher changed together. The records cannot isolate either change’s effect [E1, E2]. Automated checks cover headings, label presence, and alternative-text presence. Keyboard navigation, screen-reader use, and the meaning of the alternative text still need review [E3].\n\nNext check: compare help pages of the same type across both periods or run a paired sample. On a small representative set, record keyboard navigation, screen-reader findings, and the quality of alternative text separately from the automated pass rate.",
        ),
    ),
    "document-review": ProfessionalCase(
        title="Document review",
        topic="Review an incident handoff procedure before the next support rotation.",
        audience="Support lead revising an internal procedure",
        description="Turn source-anchored findings into edits and a quick rehearsal.",
        context="""[R1] Draft procedure, Handoff §2: “The outgoing engineer posts the open incident in the team channel and leaves when their shift ends.”

[R2] Draft procedure, Escalation §4: “If there is no reply, contact the incident lead.” No reply window or backup contact is stated.

[R3] Support policy excerpt: “For active severity-one incidents, ownership changes only after the incoming engineer acknowledges the handoff. After five minutes without acknowledgement, page the duty manager. The outgoing engineer remains responsible until acknowledgement.”

[R4] Available tools. The team channel and paging tool are already in use. No new service is needed.""",
        rubric=(
            "Anchor each finding to a draft passage and the controlling policy wording.",
            "Preserve outgoing ownership until acknowledgement and page the duty manager after five minutes.",
            "Leave a concrete patch and a rehearsal for both timely and missing acknowledgement.",
        ),
        steps=(
            ("Read draft against policy", "Find gaps a reviewer can verify directly in the supplied text.",
             "For {{audience}}, {{topic}}\n\nPacket:\n{{context}}\n\nIdentify draft statements that conflict with or omit policy. Cite source IDs and quote the relevant text."),
            ("Propose and check edits", "Correct the handoff language before it becomes a revision plan.",
             "Findings:\n{{output[-1]}}\n\nPacket:\n{{context}}\n\nPropose a short replacement for each affected draft section. Keep it faithful to the controlling policy."),
            ("Hand over the review", "Deliver prioritized edits and a rehearsal for the two paths.",
             "Write a handoff-ready review for {{audience}}.\n\nPacket:\n{{context}}\n\nReviewed edits:\n{{output[-1]}}\n\nPrioritize the findings, provide replacement text, and give two rehearsal scenarios. Preserve policy details exactly."),
        ),
        outputs=(
            "High impact: R1 says the outgoing engineer ‘leaves when their shift ends.’ R3 says they remain responsible until acknowledgement for an active severity-one incident. R2 says to ‘contact the incident lead’ but omits a reply window. R3 names the duty manager and a five-minute interval. R4 confirms both team channel and paging are available.",
            "Change §2 to transfer ownership when the outgoing engineer posts to the team channel. Change §4 to page the incident lead after 15 minutes with no reply.",
            "Fix before the next rotation. Handoff §2 currently says the outgoing engineer ‘leaves when their shift ends’ [R1]. For active severity-one incidents, the policy requires acknowledgement first [R3]. Replace §2 with: ‘Post the active severity-one incident handoff in the team channel and request acknowledgement from the incoming engineer. The outgoing engineer remains responsible until the incoming engineer acknowledges. Transfer ownership on acknowledgement.’\n\nFix §4 in the same revision. ‘Contact the incident lead’ [R2] omits both the five-minute deadline and the correct role [R3]. Replace it with: ‘If the incoming engineer has not acknowledged after five minutes, page the duty manager. The outgoing engineer remains responsible until acknowledgement.’\n\nRehearse two paths using the existing tools [R4]. With acknowledgement at minute two, confirm the new owner is recorded then. With no acknowledgement at minute five, confirm the duty manager is paged and the outgoing engineer remains responsible.",
        ),
    ),
}
