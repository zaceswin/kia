# CI Troubleshooting: Fixing the `security-and-build` Failure

This document records why the **Continuous Integration** workflow was failing,
how the problems were diagnosed, and what was changed to fix them.

## Symptom

The `security-and-build` job on GitHub Actions ended with:

```
Process completed with exit code 1.
```

The log also showed this notice:

```
Node.js 20 is deprecated. The following actions target Node.js 20 but are
being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5
```

## Diagnosis

### The Node.js 20 message was not the cause

That message is a **warning**, not an error. Both actions still run correctly.
It can be silenced later by bumping `actions/checkout` and
`actions/setup-python` to their newest major versions.

The real cause was an exit code 1 from one of the job's steps. Running each
step locally (the same commands as `.github/workflows/ci.yml`) isolated two
independent failures.

### Failure 1: C compile step could not find its source file

The workflow ran:

```bash
gcc src/failed_pentest_simulation.c -o pentest_sim
```

but the file did not exist at that path. The project files were in the
repository root, some with inconsistent names (`failed_simulation.C`,
`failed simulation.sh` with a space). The Makefile, README, `docker-compose.yml`
and tests all expected them under `src/`.

A side issue: a capital `.C` extension makes `gcc` treat the file as C++, so the
file needed a lowercase `.c` extension.

### Failure 2: Ruff reported 4 lint errors

| File | Rule | Problem |
|------|------|---------|
| `dashboard.py` | C401 | `set(... for ...)` should be a set comprehension |
| `src/generate_firewall_rules.py` | FURB122 | `file.write` called inside a `for` loop |
| `tests/test_dashboard.py` | I001 | Import block unsorted |
| `tests/test_dashboard.py` | F401 | `pytest` imported but unused |

### Additional problems found while testing locally

The test suite was not run in CI, and two of its four tests were failing:

- **Starlette API change:** newer Starlette versions require `request` as the
  first argument to `TemplateResponse`. The old call style raised
  `TypeError: unhashable type: 'dict'`.
- **Template assumed every log row had `threat_score`:** rows without it
  crashed rendering with a Jinja `UndefinedError`.
- **A test asserted something the template never renders:** the empty-logs test
  looked for a metrics string (`"0</p>"`) that does not appear in
  `templates/index.html`.

## The Fix

1. **Moved sources into `src/` with consistent names**
   - `dashboard.py` -> `src/dashboard.py`
   - `failed_pentest_simulation.c` -> `src/failed_pentest_simulation.c`
   - `failed_pentest_simulation.py` -> `src/failed_pentest_simulation.py`
   - `failed_pentest_simulation.sh` -> `src/failed_pentest_simulation.sh`
   - `src/__init__.py` makes `from src.dashboard import ...` work in tests.
2. **Fixed all Ruff findings** (set comprehension, `writelines`, sorted and
   trimmed imports).
3. **Updated `TemplateResponse`** to the `(request, name, context)` signature.
4. **Made the template tolerant of missing fields** using Jinja's `default`
   filter for `threat_score` and `country`.
5. **Corrected the empty-logs test** to assert that no table rows render.
6. **Improved the workflow** (`.github/workflows/ci.yml`):
   - Installs `requirements.txt` alongside `ruff`, `bandit` and `pytest`.
   - Added a **Run Tests** step with `ADMIN_API_KEY` set, because
     `src/dashboard.py` refuses to start without it.

## Verification

All of the CI steps were reproduced locally before pushing:

```bash
ruff check .
bandit -r . -ll -ii -x ./tests,./venv -q
ADMIN_API_KEY=test python -m pytest -q      # 4 passed
gcc src/failed_pentest_simulation.c -o /tmp/ps
```

## Lessons Learned

- **Read the actual exit-code step, not the warning.** Deprecation notices are
  noisy and often unrelated to the failure.
- **Reproduce CI locally.** Running each workflow step by hand found the
  failing commands quickly.
- **Keep file paths consistent** between the Makefile, README, Dockerfile,
  `docker-compose.yml` and the CI workflow.
- **Avoid spaces and odd capitalisation in file names** (`failed simulation.sh`,
  `.C`); they break scripts and change compiler behaviour.
- **Run tests in CI**, not just linters, so breakage like the Starlette API
  change is caught early.
- **Use a virtual environment** (`python3 -m venv venv`) and keep `venv/` in
  `.gitignore` so it is never committed or scanned.

## Optional Follow-ups

- Bump `actions/checkout` and `actions/setup-python` to remove the Node.js 20
  deprecation warning.
- Pin dependency versions in `requirements.txt` for reproducible builds.
