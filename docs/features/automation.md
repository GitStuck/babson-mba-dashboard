# Automation: scheduled jobs that fail loudly instead of lying quietly

The dashboard earns its keep when it runs without you. The original's architecture:
macOS LaunchAgents fire a **morning pull** (files only, fast, no LLM — professors post
around 6 am on class days, so run at ~7:15) and **two heavier runs** (~1:15 pm and 8 pm)
that pull, refresh due dates, rebuild the Today's Focus note, and write tomorrow's
primers via a headless LLM call. The plist template is in `../LESSONS.md`. The lessons
below are the ones that cost real debugging days.

- **Watchdog every LLM call.** A headless agent call can hang for hours; wrap it in a
  kill-after-N-seconds watchdog with one shorter retry, and log the kill. The original's
  briefing went silently stale for three days because a hung call blocked the job
  nightly. Related: time-sensitive output first — the job writes the daily note *before*
  the slow primer work, so a hang can't starve the urgent artifact.
- **Expired auth looks like a hang, not an error.** When the headless agent's login
  expired, the scheduled runs hung until the watchdog killed them, with no useful error
  anywhere. Symptom signature: repeated watchdog kills in the log plus a stale timestamp
  on the newest artifact. Test by running one tiny headless call by hand; the fix is an
  interactive re-login. Check this *first* when generation stops.
- **Order jobs so consumers run after producers** in the same run: pull files → sweep
  pages → rebuild manifests → generate notes. Same-run consistency saves a whole
  cycle of "why isn't it showing up."
- **launchd's environment is not your shell's.** Minimal PATH (absolute paths for every
  binary — `node`/`python3` resolving in your terminal proves nothing), no access to
  iCloud-synced folders without Full Disk Access, and a different Python than you tested
  with if you're not explicit. Pin interpreters by full path.
- **Idempotency everywhere.** Every job must be safe to run twice: ledgers for
  downloads, upserts for injected rows, never-overwrite rules for generated files a
  human may have edited (a non-empty primer is sacred).
- **Log one line per run to one file**, with a `==== timestamp ====` header. When
  something breaks weeks later, that log is the only witness. Grep-ability beats
  structure.
- **Every artifact self-reports its age**, and pages flag staleness loudly. The trust
  chain is: jobs might fail → artifacts admit their age → the human notices within
  hours, not weeks.

## Build sketch (Phase 2 of the roadmap)

Start with ONE LaunchAgent running the pull twice a day, a run log, and the staleness
stamp on the page. Add the LLM-generating jobs only after your manual "write me a
primer" habit has stabilized the prompt — automating a prompt you haven't settled just
schedules disappointment.
