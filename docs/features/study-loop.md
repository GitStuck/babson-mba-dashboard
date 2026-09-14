# The study loop: reflections, your notes, and the professor's record

The single highest-value feature in the original dashboard, and the least obvious one.
It rests on a three-source model: every class session produces three different records —
**your notes in the moment** (often a Word file), **your reflection afterward** (what
actually clicked, what the professor signaled matters), and **the professor's official
record** (the slides or recap deck posted after class). Each is unreliable alone. Exam
prep is where you diff them against each other, and that only works if all three were
captured while they were cheap.

## The debrief habit (the keystone)

After every class, a two-minute free-text "debrief" gets banked: what clicked, what the
professor signaled matters, and one takeaway for your own projects. Design choices that
took iteration to get right:

- **The capture box lives on the home page and appears on class day itself** — not after
  the day ends. Its owner's actual request was to jot a thought *before* class from the
  readings and finish the note after. Show the box all day; label it by session.
- **Nag gently, once.** An unbanked session from yesterday lingers one extra day with a
  "still unbanked" tag, then stops guilting. Guilt-trip UIs get abandoned.
- **Key debriefs by course and session number** (`FIN101:S3`), never by date — sessions
  move, dates lie.
- **Make the payoff visible or the habit dies.** Debriefs must feed something the owner
  sees again: the next session's primer opens by quoting the last debrief ("after S3 you
  noted X; today tests it"), and exam prep assembles from the trail. A notes box that
  never resurfaces its contents trains people to stop filling it.

## Word-file class notes as a first-class source

If the owner takes notes in Word/OneNote during class, don't fight it — integrate it.
The original's pattern: one .docx per session, named `YYYYMMDD-COURSE-Sn Notes.docx`,
saved in the course's session folder. The agent reads them (a .docx is just a zip of
XML; stdlib can extract the text) when building study material, and treats anything in
them addressed to the agent ("Claude: make a drill on this") as a request. Two rules
learned the hard way: never *edit* the owner's notes files, and never copy private
reflections into anything that could reach teammates.

## The professor's post-class record

Many professors post a recap deck, annotated slides, or highlights after each session.
Those are the closest thing to the exam's source of truth. File them per session the
moment they post (the readings pipeline handles this), and treat them as the **spine**
of exam prep: your notes and debriefs get read *against* them, and gaps between what the
professor emphasized and what you captured are precisely the list of what to study.

## Build sketch

Storage: one JSON of debriefs keyed `COURSE:Sn` plus a timestamp map (last-writer-wins
if you ever sync two devices). UI: a textarea per today's session on the home page,
saving on keystroke. Integration: primer and exam-prep generators read the debrief file
and the session folder (notes .docx + professor deck) together. Start with the textarea
and the JSON — the habit matters before any of the downstream consumers exist.
