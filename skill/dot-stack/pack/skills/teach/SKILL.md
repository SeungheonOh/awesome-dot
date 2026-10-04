---
name: teach
description: "Explain a technical concept or body of work at the reader\u2019s level, combining source-grounded mechanics with carefully qualified rationale."
---


# Teach

Help the person understand the thing they asked about. Teaching is read-only unless they requested a separate change. Match depth to their goal: reviewing, debugging, modifying, or learning a subsystem.

Start from what the conversation shows they know; ask about background only when it materially changes the explanation. Choose the few ideas needed to answer their actual question. Do not quiz them or insist on a pacing ritual unless they asked for one.

## Ground the explanation

For project-specific mechanics, follow [how](../how/SKILL.md). For historical motivation, follow [why](../why/SKILL.md) only as far as relevant. A small question may need one source read, not two delegated investigations. Independent workers can help a large subsystem when available; otherwise investigate directly.

Keep known behavior, observed execution, documented intent, and inference distinct. If history is missing, explain the present mechanism without inventing why the team chose it. Preserve confidence qualifiers through simplification.

## Explain in useful layers

Give the smallest complete answer first. Define the concept plainly, connect it to the user's concrete case, then walk through one representative action. Explain the important mechanism, not a list of function names. Use the actual names consistently when the reader needs to find the code.

Add a small example, source excerpt, or diagram when it clarifies the idea. For a complex flow, build the picture incrementally if that helps; do not force multiple diagrams for three trivial components. Use the tools and output medium actually available. Never claim a generated picture, opened debugger, or running demonstration without evidence.

For an interactive conversation, stop at a natural point and let the user steer deeper. For a requested one-shot explanation, deliver the complete requested depth rather than withholding needed details. An analogy should illuminate a mechanism and state where it stops applying.

## Preserve what matters

Use ordinary words, concise sentences, and the user's requested format. [Unslop](../unslop/SKILL.md) can improve clarity, but must not strip uncertainty or an important exception. Avoid stock framing and performative claims about how simple or difficult something is.

Example: “The list renders only nearby rows. When you scroll, it removes distant elements and loads the next visible range. That reduces the amount the browser draws; it does not by itself prove the app reads less data from storage.” The qualification matters because rendering and data loading are separate mechanisms.

Return the explanation itself with relevant source pointers. If source access is incomplete, state the specific limit without replacing the answer with a process report.
