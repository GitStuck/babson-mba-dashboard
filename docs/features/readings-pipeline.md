# The readings pipeline: from Canvas postings to a checkable plan

The job: every file a professor posts lands automatically in a sensible folder, appears
on a Readings page with a checkbox, and carries enough context that you know what it is,
what order to read it in, and whether it's required — without opening Canvas.

## Filing

- **One folder per course, one subfolder per session**, named with the date:
  `FIN101/01 Readings & Cases/Session 04 (Wed Oct 7)/`. The session-dated folder is the
  unit everything else (notes, decks, debriefs) organizes around.
- **Walk the Modules API, not the Files tab.** Professors hide Files tabs routinely; the
  module structure is what students actually see, and module names usually carry the
  session number and date ("Class 4 - Oct 7"). Parse those with a per-course regex you
  can override in the course registry, because every professor names modules differently.
- **Keep an idempotency ledger** (a JSON of every file URL already fetched) so the pull
  can run three times a day forever without re-downloading or duplicating.
- **Files also hide inside pages.** Some professors attach nothing to modules and embed
  everything as links in page bodies. A page-sweep pass that parses page HTML for file
  links caught an entire course's slide decks the module walk had missed all term.
- **Report the unfetchables instead of dropping them.** Per-seat coursepack items and
  external links can't be downloaded; list them as "open by hand" with their link text.
  The original silently dropped these for weeks and its owner missed four case readings.

## The Readings page

- Checkbox per reading, **keyed to a stable id**, with per-course progress bars and an
  "open next 5 unchecked" button that queues a reading session in browser tabs.
- **Group piles into plans.** A 13-item pre-work packet displayed as 13 bare rows reads
  as noise; the fix that finally worked was a curated per-group note giving the pile a
  human title, a due line, a how-to-approach paragraph, and a recommended order, with
  rows sorted to match.
- **State the scope of every reading explicitly** — "the whole book, no chapter subset"
  or "pp. 3–29, stop at section X." An unscoped row caused a real panic ("which chapters
  was I supposed to read?!"). Never leave scope implicit.
- **Verify each course actually has rows.** A course whose Canvas API surface is locked
  down can end up with zero entries, which the page renders as "nothing to do" — exactly
  wrong. After onboarding any course, check its reading list is nonempty; hand-derive
  rows from the syllabus when the API is closed.

## Build sketch

Extend the pull script: for each course, walk modules → items; download File items into
session folders; record everything in the ledger; emit a `readings.json` manifest the
page renders. Add the page-sweep and the curated-groups file when (not before) their
problems show up.
