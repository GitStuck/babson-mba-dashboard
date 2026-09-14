# Session primers: walk into class knowing why the readings matter

A primer is a one-page brief generated before each class session from the actual posted
materials: what the readings are driving at, the frameworks the session teaches, the
questions worth holding in mind, and how the session feeds the course's big assessments.
It is the highest-leverage use of an LLM agent in this whole system — and the easiest to
ruin.

## The line that must never be crossed

A primer **primes; it never does the thinking**. It frames tensions and open questions;
it never summarizes a case's resolution, never answers the discussion questions, never
solves any part of graded work. This isn't just integrity hygiene — a primer that
pre-chews the case makes class boring and the degree worthless. Write the rule into your
agent's instructions verbatim, because a helpful LLM will drift across this line the
moment a case has an exciting ending.

## Design choices that mattered

- **Ground every primer in the professor's own framing.** If a session memo, prep page,
  or objectives doc exists, read it first and take its word on what's core versus
  optional. Honesty rule: if a reading couldn't be opened (paywalled, per-seat), the
  primer says so instead of faking familiarity.
- **Open with the reader's own last thought.** If there's a banked debrief from the
  previous session (see `study-loop.md`), the primer starts there. It makes the course
  feel continuous and proves the debrief habit pays.
- **Gloss every term at first touch.** Framework names, acronyms, Greek letters — a
  one-clause parenthetical each. The original got this as direct owner feedback and it
  became a standing rule.
- **Include a "runway" footer**: what's due in the next few days across all courses and
  where tonight's marginal hour goes. The primer is read the night before; meet the
  reader where they are.
- **Write primers to files, keyed by session** (`primers/FIN101-S04.md`), rendered in
  the dashboard. Never regenerate one that exists and is non-empty — hand-written or
  hand-corrected primers must survive automation.
- **600–900 words, full prose.** Bullet-fragment primers read like packing lists and get
  skimmed into uselessness.

## Companion: the session prep plan

Alongside each primer, a 2–4 sentence "what is this pile actually" note shown atop the
session's reading list: how many real readings versus videos versus in-class working
files, rough time cost, what's skippable. Separating the *logistics* note from the
*intellectual* primer was a real improvement — they answer different questions asked at
different moments.

## Build sketch

A nightly job: find tomorrow's sessions from the registry and session dates; gather that
session's filed materials; prompt your agent with the materials, the grading structure,
the debrief trail, and the rules above; write the file. Wrap the LLM call in a watchdog
(see `automation.md`). Start manual ("write me a primer for tomorrow") for a week before
automating — you'll learn what your version of the prompt needs.
