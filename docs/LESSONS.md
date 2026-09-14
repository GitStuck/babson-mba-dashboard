# Lessons learned (so your agent doesn't relearn them slowly)

Distilled from ten months of running a Canvas-fed dashboard at Babson. Course-agnostic;
your professors will rhyme.

## Canvas API mechanics

- **Auth is one header**: `Authorization: Bearer <token>`. Generate the token in Canvas →
  Account → Settings → New Access Token. Treat it as read-only by convention (Canvas
  student tokens can't be scoped, so protect it like a password: gitignored file, 0600).
- **Pagination is mandatory.** Most list endpoints cap at 100 items and hide the rest
  behind a `Link: <...>; rel="next"` response header. Always follow `rel=next` or you'll
  silently miss half a course. The starter's `get_paginated()` does this; reuse it.
- **Timezones will burn you exactly once.** All API timestamps are UTC. A deadline of
  `T03:59:00Z` or `T04:59:00Z` is 11:59 pm US Eastern *the night before* the date shown.
  Convert to local time before rendering, and never date-bucket on the UTC day.
- **Useful endpoints beyond assignments**: `/api/v1/courses?enrollment_state=active`
  (discovery, includes term with `include[]=term`); `/api/v1/planner/items` (the ONLY
  source of ungraded page to-dos like "read before class", plus submitted status);
  `/api/v1/announcements?context_codes[]=course_<id>` (batch across courses);
  `/api/v1/courses/<id>/modules?include[]=items` (the real map of session materials);
  enrollments with `include[]=total_scores` for current grade.
- **Hidden tabs 403 without warning.** Professors routinely hide the Files tab; the files
  still reach students as links on module pages. If Files 403s, walk Modules and parse
  page bodies for file links instead of concluding there's nothing.
- **Some items cannot be fetched, ever**: Harvard coursepack readings and similar
  per-seat LTI links (`/external_tools/retrieve` URLs), and items behind publisher
  paywalls. Detect them, list them as "open in Canvas by hand," and move on — don't let
  your agent spend an evening "debugging" a licensing wall.
- **Cloned-shell garbage is real.** Professors copy last term's Canvas shell, and stale
  assignments with last-spring due dates ride along. Filter to the current term window
  and treat any date not plausible for this semester as suspect.
- **Announcements post at 6 am on class days.** If you automate pulling, schedule it
  after ~7 am, or you'll fetch yesterday forever.

## Design lessons (the expensive ones)

- **One registry file.** Put courses, IDs, and meeting times in one JSON file and make
  every script read it. When next term comes, you edit data, not code.
- **Canvas wins for clocks; documents win for content.** Syllabus PDFs go stale the first
  time a professor moves a deadline in Canvas. When they disagree, show the conflict.
- **State the scope of every reading.** "Read Chapter 3, pp. 45-60" on the page beats
  "Textbook" every time; vague rows get skipped and then panic-read.
- **Checkbox state must survive.** Key persistence to stable IDs (assignment id), not
  titles — professors rename things.
- **A staleness stamp buys trust.** Show when data was last pulled; a dashboard that
  might be stale gets abandoned.
- **Grow by complaint, not by plan.** The features that survive are the ones built the
  day something annoyed the owner. Resist building ahead of need.

## Automation template (Phase 2)

macOS LaunchAgent (`~/Library/LaunchAgents/com.<you>.canvas-pull.plist`), then
`launchctl load` it:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.YOURNAME.canvas-pull</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/python3</string>
    <string>/FULL/PATH/TO/REPO/scripts/canvas_pull.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>15</integer></dict>
    <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>15</integer></dict>
  </array>
  <key>StandardErrorPath</key><string>/tmp/canvas-pull.err</string>
</dict></plist>
```

Two launchd gotchas: it runs with a minimal PATH (use absolute paths everywhere), and it
cannot read iCloud-synced folders without Full Disk Access — keep the repo in a plain
local folder.

## Python-on-Mac gotcha (found while building this starter)

python.org installs of Python ship without root SSL certificates wired up, so the very
first API call dies with CERTIFICATE_VERIFY_FAILED. Apple's `/usr/bin/python3` doesn't
have this problem. The pull script detects the failure and says exactly this; if you add
new scripts, reuse its `_ssl_context()` helper.
