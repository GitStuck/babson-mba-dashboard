#!/usr/bin/env python3
"""Pull upcoming work and announcements from Canvas into data/upcoming.json.

Stdlib only, on purpose (see CLAUDE.md rule 4). Reads the API token from
state/canvas-token and the course list from data/courses.json.

Usage:
  python3 scripts/canvas_pull.py             # normal pull
  python3 scripts/canvas_pull.py --discover  # list your active courses + IDs and exit
"""
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

def _ssl_context():
    """python.org installs often lack root certs; prefer certifi when present."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

CTX = _ssl_context()

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://babson.instructure.com"  # change for another school
DUE_WINDOW_DAYS = 14      # how far ahead to look for due items
ANNOUNCE_LOOKBACK_DAYS = 10


def token() -> str:
    p = ROOT / "state" / "canvas-token"
    if not p.exists():
        sys.exit("No token at state/canvas-token — see README step 1.")
    return p.read_text().strip()


def get(url: str):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token()}"})
    try:
        resp = urllib.request.urlopen(req, timeout=30, context=CTX)
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            sys.exit(
                "SSL certificates missing from this Python.\n"
                "Easiest fix: run with Apple's build:  /usr/bin/python3 scripts/canvas_pull.py\n"
                "Or, if you installed Python from python.org, run its bundled\n"
                "'Install Certificates.command' (in /Applications/Python 3.x/)."
            )
        raise
    with resp as r:
        link = r.headers.get("Link", "")
        body = json.loads(r.read().decode())
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        return body, (m.group(1) if m else None)


def get_paginated(url: str) -> list:
    """Canvas hides results past page 1 behind the Link header. Always drain it."""
    out, nxt = [], url
    while nxt:
        page, nxt = get(nxt)
        out.extend(page)
    return out


def discover():
    courses = get_paginated(f"{BASE}/api/v1/courses?enrollment_state=active&include[]=term&per_page=50")
    print("Active courses (put the ones you want in data/courses.json):")
    for c in courses:
        term = (c.get("term") or {}).get("name", "?")
        print(f"  id={c['id']}  [{term}]  {c.get('name')}")


def main():
    if "--discover" in sys.argv:
        discover()
        return

    reg_path = ROOT / "data" / "courses.json"
    if not reg_path.exists():
        sys.exit("No data/courses.json — copy the sample and fill it in (README step 2).")
    registry = json.loads(reg_path.read_text())
    now = datetime.now(timezone.utc)
    horizon = now + timedelta(days=DUE_WINDOW_DAYS)

    items, announcements = [], []
    for course in registry["courses"]:
        cid, code = course["canvasId"], course["code"]
        if not cid:
            continue  # course shell not published yet — normal early in term
        for a in get_paginated(f"{BASE}/api/v1/courses/{cid}/assignments?per_page=100"):
            due = a.get("due_at")
            if not due:
                continue
            due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
            if now - timedelta(days=1) <= due_dt <= horizon:
                items.append({
                    "id": a["id"],
                    "course": code,
                    "name": a["name"],
                    "dueAt": due,            # UTC; the page renders local time
                    "points": a.get("points_possible"),
                    "url": a.get("html_url"),
                })
        print(f"  {code}: ok")

    ctx = "&".join(f"context_codes[]=course_{c['canvasId']}" for c in registry["courses"] if c["canvasId"])
    since = (now - timedelta(days=ANNOUNCE_LOOKBACK_DAYS)).date().isoformat()
    for ann in get_paginated(f"{BASE}/api/v1/announcements?{ctx}&start_date={since}&per_page=50"):
        cid = int(str(ann.get("context_code", "0")).replace("course_", "") or 0)
        code = next((c["code"] for c in registry["courses"] if c["canvasId"] == cid), "?")
        announcements.append({
            "course": code,
            "title": ann.get("title"),
            "postedAt": ann.get("posted_at"),
            "url": ann.get("html_url"),
        })

    items.sort(key=lambda x: x["dueAt"])
    out = {
        "generatedAt": now.isoformat(),
        "dueWindowDays": DUE_WINDOW_DAYS,
        "items": items,
        "announcements": announcements,
    }
    out_path = ROOT / "data" / "upcoming.json"
    out_path.write_text(json.dumps(out, indent=1))
    nxt = items[0] if items else None
    print(f"Wrote {out_path.name}: {len(items)} due item(s), {len(announcements)} announcement(s).")
    if nxt:
        print(f"Next deadline: [{nxt['course']}] {nxt['name']} at {nxt['dueAt']} (UTC)")


if __name__ == "__main__":
    main()
