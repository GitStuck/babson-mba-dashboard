# Today's Focus: the prioritized daily note

A short written briefing at the top of the home page, regenerated once or twice a day
(the original settled on ~1:15 pm and 8 pm), that ranks the next ~48 hours of work by
grade impact and says plainly what to do first, what to skip, and how to get ahead. This
is the feature that turns a dashboard from a list into an advisor, and it's the natural
first job for your Claude agent once the data pull works: feed it the due list, the
course grading weights, and the calendar, and have it write the note.

Design choices that mattered:

- **Clock honesty is non-negotiable.** The note is read hours after it's written, so it
  must never say "today," "tonight," or "tomorrow" — only absolute days and times
  ("Friday 9:00 am"). The first line is a machine-readable timestamp comment, and the
  page shows the note's age and flags it loudly when stale. An advisor that might be
  reading yesterday's clock gets ignored forever after one bad miss.
- **Rank by grade impact and reversibility, not proximity.** A 5-point quiz due tonight
  can outrank a reading due tomorrow, but a group deliverable outranks both because
  other people block on it. The weights come from each course's grading structure (see
  `grade-weighted-priorities.md`).
- **"What to skip" earns the reader's trust.** Explicitly naming the optional work not
  worth doing this week is the section owners quote back most. An advisor that only ever
  adds work is a stress generator.
- **Cover through the end of the next class day**, in the order the work must happen,
  and resurface anything already overdue that can still be salvaged.
- **Length cap.** 250–450 words. Past that it stops being read.

Pitfall from the original: the generating job must be watchdogged (see `automation.md`);
when the LLM call silently hung, the note went stale for three days before anyone
noticed, and staleness flags were added only after that incident. Build the staleness
flag on day one.
