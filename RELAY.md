# The Relay — Agent Instructions

You are one leg of a relay race. Your job is to run your leg, save your output, update the baton, and hand off. A fresh instance handles the next leg — you will never see what comes after you.

## How The Relay Works (READ THIS FIRST)

**You are ONE leg of an autonomous relay.**

Architecture:
- `relay.sh` spawns a FRESH Claude instance for each leg
- Each instance: reads relay.json → finds the next incomplete leg → runs it → updates state → EXITS
- The next leg starts a NEW session with clean context
- State persists via files: `relay.json`, `baton.txt`, `artifacts/`

**Your job this session:** Complete exactly ONE leg, then EXIT.
Do NOT continue to the next leg — a fresh instance handles that.

---

## Your Workflow

### Step 1 — Read the relay state

1. Read `relay.json` — understand the legs, their status, and all config (brand, funnel path, output dir, methodology paths, etc.)
2. Read `baton.txt` — read what previous legs decided. This is your memory. Do not re-litigate decisions already made.
3. Load the methodology file referenced in relay.json under `methodology`

### Step 2 — Find your leg

Pick the **highest-priority incomplete leg** where `handed_off: false`.

Legs are sequential. Do not skip ahead. Each leg depends on artifacts saved by the previous leg.

### Step 3 — Run your leg

1. Read any artifact files from previous legs (check `[outputDir]/artifacts/`)
2. Read the funnel file specified in relay.json
3. Complete the leg fully — follow the methodology for this specific leg
4. Run ALL self-checks specified in the acceptance criteria. Write them out in full. Do not summarize or skip. Self-checks are the quality gate.
5. Save all output to the artifact file specified for this leg

### Step 4 — Verify acceptance criteria

Go through EVERY acceptance criterion line by line. Each must verifiably pass before you update state.

If a self-check fails — fix it before updating state. Do not mark a leg as handed_off until it passes.

### Step 5 — Update the baton and hand off

1. **Update relay.json** — set `handed_off: true` for the completed leg
2. **Append to baton.txt** using this format:

```
## [Date] — Leg [ID]: [Leg Title]

**Completed:**
- What was produced
- Key creative decisions made
- Artifact files saved

**Handoff notes for the next leg:**
- What the next leg needs to know
- Decisions that should not be revisited
- Any constraints discovered during this leg

---
```

3. **Update the Creative Decisions block** at the top of baton.txt if you made decisions the next leg needs (e.g. which concepts were selected, which concepts passed the gate)

### Step 6 — Check completion

After updating relay.json, check if ALL legs have `handed_off: true`.

**If ALL complete:** Output exactly this on its own line:
```
RELAY_COMPLETE
```

**If legs remain:** STOP. Do not continue to the next leg. Exit now. A fresh instance handles it.

---

## Critical Rules

1. **One leg per instance** — Complete ONE leg, then EXIT.
2. **Read baton.txt first** — All prior decisions live there. Do not redo them.
3. **Read artifact files** — Each leg builds on what the previous leg left.
4. **Self-checks are mandatory** — Write them out fully. They are not optional.
5. **Save artifacts** — Every leg saves its output to a file. If the session ends, the next instance picks up from the artifact.
6. **The ad sells the click, the funnel sells the product** — Never name the product or brand in ad copy. Never use selling language in the ad itself.
7. **Images must carry their own contradiction** — If an image concept requires reading the copy to be interesting, it fails. If it would make someone pause with no text at all, it passes.

## When You're Stuck

1. Document the blocker in baton.txt under "Blockers"
2. Try the escalation path in the methodology for this leg
3. If truly blocked after 2-3 attempts, document and move on — the next instance will have fresh context

Do not spin. If a self-check keeps failing on the same issue, document the pattern and move on.

---

**Start now.** Read relay.json and baton.txt, then begin.
