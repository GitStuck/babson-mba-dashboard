# Babson MBA Dashboard (starter)

A barebones personal academic dashboard for Babson (or any Canvas school): one page that
shows today's classes, everything due in the next seven days, and recent announcements,
fed by a small script that pulls from the Canvas API with a read-only token.

This is a **starting point, not a product**. It exists so you and your Claude Code agent
skip the plumbing (auth, pagination, API quirks) and spend your time on the part that
matters: growing a dashboard that fits *your* semester, one request at a time. The
original this grew out of is ten months of one student saying "it bugs me that..." to
Claude and having it fixed the same day. That loop is the product. Start yours.

## Quickstart (10 minutes, no dependencies beyond macOS)

1. **Get a Canvas token**: Canvas → Account → Settings → scroll to Approved Integrations →
   "+ New Access Token". Name it "this-week read-only", leave expiry blank or set end of
   term. Copy the token once (Canvas never shows it again) and save it:
   ```
   mkdir -p state && pbpaste > state/canvas-token
   ```
   `state/` is gitignored. The token never goes in code, chat, or a commit.
2. **List your courses**: copy `data/courses.sample.json` to `data/courses.json` and fill
   in your real courses. Course IDs are the number in each course's Canvas URL
   (`.../courses/1234567`). Or ask your Claude to run the `--discover` flag below and fill
   it for you.
3. **Pull**:
   ```
   python3 scripts/canvas_pull.py            # uses data/courses.json
   python3 scripts/canvas_pull.py --discover # lists your active courses + IDs, then exit
   ```
4. **Look at it**:
   ```
   python3 -m http.server 8080
   ```
   then open http://localhost:8080 — the This Week page reads the freshly pulled data.

## What's in the box

- `scripts/canvas_pull.py` — stdlib-only Python; pulls upcoming assignments and recent
  announcements for the courses you list; handles Canvas pagination; writes
  `data/upcoming.json`.
- `index.html` — the This Week page: today's classes, 7-day due list with checkboxes
  (they persist in your browser), announcements. Vanilla HTML/JS, no build step.
- `ROADMAP.md` — a phased build-out plan **written for your Claude Code agent to drive**.
  Open Claude in this folder and say "read the roadmap and start phase 0."
- `docs/LESSONS.md` — hard-won Canvas and workflow lessons from the original dashboard,
  so your agent doesn't rediscover them the slow way.
- `CLAUDE.md` — standing instructions your Claude picks up automatically in this repo.

## Privacy stance

Everything runs and stays on your machine. The token is read-only and gitignored; pulled
data (`data/upcoming.json`) is gitignored too, because your assignments and grades are
yours. If you fork this publicly, the gitignore already protects you — don't fight it.
