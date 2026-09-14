# Roadmap: from starter to a dashboard that fits you

Written for the Claude Code agent working in this repo, with the owner deciding pace and
priorities. Each phase ends with something the owner can see working. Don't skip ahead;
don't gold-plate. The original dashboard this pattern comes from reached each phase only
when its owner actually felt the need.

## Phase 0 — Make it yours (first session)

Goal: real data on the page. Ask the owner for their course list (or run
`python3 scripts/canvas_pull.py --discover` after the token is in place and propose
`data/courses.json` from the result). Confirm the token file exists. Run the pull, start
the local server, and have the owner open the page. Done when they see their own
assignments due this week. If any course shows nothing, check `docs/LESSONS.md` on
hidden tabs before debugging blind.

## Phase 1 — Trustworthy This Week (first week)

Goal: the page is checked every morning because it's never wrong. (Design notes: `docs/features/todays-focus.md` when you add the daily note, and `docs/features/grade-weighted-priorities.md` for how ranking should work.) Add anything the pull
misses that the owner cares about (quizzes and discussions come through the assignments
endpoint; ungraded to-dos ride the planner endpoint, see LESSONS). Make the due list
honest about timezones (Canvas returns UTC; render local; 03:59Z is 11:59 pm ET the
night before). Let checked-off items stay checked (localStorage is already wired; keep
keys stable when titles change by keying on assignment id).

## Phase 2 — It runs itself (when checking manually gets old)

Goal: fresh data without thinking. (Read `docs/features/automation.md` first — it's all scar tissue.) Add a macOS LaunchAgent that runs the pull every
morning before first class (plist template in LESSONS; professors post materials around
6 am on class days, so pull after 7). Add a "data pulled at" stamp on the page so
staleness is visible. Keep manual pull working for mid-day refreshes.

## Phase 3 — Readings and materials (when the syllabus pile bites)

Goal: the page knows what to read before each class. (Read `docs/features/readings-pipeline.md` first.) Walk each course's Modules API for
files and pages tied to upcoming sessions; list them under a "prep" section with links
into Canvas; add checkboxes. Optionally download files into a per-course folder tree.
Mind LESSONS on hidden Files tabs, page-embedded files, and per-seat items that cannot
be fetched.

## Phase 4 — The study layer (exam season)

Goal: the dashboard helps you *prepare*, not just track. (This phase has the most prior art: `docs/features/study-loop.md`, `docs/features/primers.md`, and `docs/features/exam-prep.md`.) Candidates, in the order they
tend to earn their keep: a per-course page showing the grading structure and where
points actually come from (read it from the syllabus once, store it as JSON); grades and
professor comments via the enrollments/submissions endpoints; a session-notes box (two
minutes after each class, saved locally) that becomes exam-prep raw material. Build only
what the owner's next exam needs.

## Phase 5 — Your life, not just your classes (whenever)

Goal: one honest daily picture. (Design notes: `docs/features/day-plan.md`.) Class meetings plus personal fixed blocks (gym, work,
commitments) in a simple day view; export an .ics of the semester so the phone calendar
matches; whatever the owner keeps wishing existed. By this point they'll know exactly
what to ask for — that's the sign the loop is working.

## Standing exit criteria for every phase

The owner can say what changed in one sentence; the pull runs clean; nothing personal is
committed; and the page still loads in under a second.
