# Siddha OS (Sydra OS) - agent instructions

1. The full plan is `docs/MASTER_PLAN.md`. Read sections 0-7 once; then only the section of the current phase.
2. Golden Rules (MASTER_PLAN section 4) are binding. Never write to disk devices except via `scripts/flash-usb.sh`. Never commit secrets.
3. Take the first task not marked DONE in `docs/PROGRESS.md`. CLAIM it, do it, run its DONE WHEN test, paste real output, commit, mark DONE.
4. Resolve every `VERIFY:` item with real commands or documentation and record it in `docs/DECISIONS.md`. Never guess package names or flags.
5. Work in small steps: one or two commands at a time, read the output, then continue.
6. Ask the human (E) only for: physical actions, decisions in MASTER_PLAN section 14, or risky commands. No routine check-ins.
7. After each task report: what changed, commands run, results, next task.

Branding vs Internal Identity:
- Public Brand: **Sydra OS** (UI titles, boot menu, ISO label `SYDRA_YYYYMM`, welcome app, docs)
- Internal Identifier: **siddha** (package prefix `siddha-*`, local repo `[siddha]`, configs `/etc/siddha/`)

Machines: Laptop A = EndeavourOS build machine (only place that builds the ISO). Laptop B = Windows (Nitro, RTX 5050) GPU/gaming test lab and Game Hub development.
