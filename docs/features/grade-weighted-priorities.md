# Grade-weighted priorities: the orientation doc pattern

Every prioritization feature (Today's Focus, the due list's ordering, what-to-skip
advice) is only as good as its model of how each course actually grades. The pattern
that makes this work is a **course orientation document**: after reading each syllabus
once, carefully, your agent writes a per-course section recording how the course really
operates — and every later recommendation cites it instead of re-deriving from vibes.

What each course's section captures:

- **The grading table, verbatim**: every component and weight, with due dates.
- **The participation mechanics**, because in seminar-style courses participation is
  routinely 20–40% and it is the only component under your control every single week.
  Capture the attendance policy precisely — rules like "two unexcused absences fail the
  contribution component" change how you plan a semester.
- **What an A actually requires**, written as a short honest paragraph: which components
  have leverage, which are cheap points, what the failure modes are.
- **Course quirks**: cloned-shell stale dates, hidden tabs, which artifact is the
  authoritative session map, AI policies (these differ sharply per course and per
  assignment — record them, they're grading-relevant), submission mechanics.
- **A machine-readable twin** (`course-facts.json`: weights, participation percent,
  session count) so scripts can rank work without parsing prose.

Two standing rules from the original, adopt them verbatim:

1. **Documents win for content, Canvas wins for clocks.** The syllabus states what the
   assignment is; Canvas states when it's due. When they conflict, surface the conflict
   to the owner — never silently resolve it.
2. **Read everything once, properly.** The orientation doc is written from a full read
   of every syllabus and course page at term start (and updated the day a late syllabus
   posts). That single reading session pays for itself the first week two deadlines
   collide and something has to slip: you slip the thing the grading table says is
   cheap, calmly.

## Build sketch

One markdown doc (`docs/course-orientation.md` in your repo) plus `course-facts.json`.
Your agent drafts both from the syllabi with you correcting; scripts read the JSON;
Today's Focus quotes the prose. Update it when reality diverges — an orientation doc
nobody maintains becomes confidently wrong, which is worse than absent.
