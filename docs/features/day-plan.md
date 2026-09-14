# Day plan: one honest picture of school plus life

The academic dashboard eventually collides with the rest of life — training, work,
family, recovery — and the fix is a day-plan view: a rolling ledger (the original uses
~14 days) where each day lists its fixed blocks (classes, gym, meals, personal
commitments) and deadlines get injected automatically.

Design choices that mattered:

- **Deadlines are injected, never hand-copied.** A tagged row like `[CANVAS DUE]` is
  written into each day by the pull job and refreshed on every run. The moment a human
  has to copy due dates into a plan, the plan is three days from being wrong.
- **Tag rows by owner.** Rows written by automation carry tags (`[CANVAS DUE]`); rows
  written by the owner or a planning script carry theirs (`[GYM]`, `[WORK]`). Each
  writer updates only its own rows, so the plan can have multiple authors without
  clobbering.
- **Plan the week against energy, not just time.** The original encodes standing
  personal rules (e.g., long-run days are low-energy days: nothing heavy due those
  evenings; move Sunday-deadline work to Saturday). Encode yours — this is the feature
  where a personal dashboard beats every commercial tool, because it knows *you*.
- **Warnings, not enforcement.** The planner flags collisions ("two graded items on a
  day with zero study time scheduled") and lets the human decide. Tools that auto-
  reshuffle a person's life get turned off.
- **Every plan item must be backed by a real artifact** — an action plus the named thing
  it acts on ("draft scope v1 from the template in Session 02 folder"), never a bare
  topic label ("work on project"). Bare labels feel like planning and produce nothing.

## Build sketch

A `day-plan.json` of dated entries with tagged rows; the pull script upserts `[CANVAS
DUE]` rows; a simple page renders the next two weeks with today highlighted. Personal
fixed blocks can start as hand-edited JSON — automation for those comes only if a
pattern (a training program, a work schedule) makes generating them worthwhile.
