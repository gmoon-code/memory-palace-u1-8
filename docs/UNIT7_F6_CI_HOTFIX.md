# Unit 7 F6 GitHub CI compatibility correction

## Issue

The first Unit 7 F6 archive contained a historical compatibility defect in `scripts/qa_unit6_f5.py`.

Unit 6 F5 correctly permits later locked runtime bytes, but the script only looked at the Unit 6 F6 lock and the Unit 7 F5 runtime lock. Unit 7 F6 intentionally changed `backend/main.py` and `frontend/js/audio.js`, so GitHub Actions saw current bytes that were validly recorded by `content/ap-biology/unit-7/content-lock-f6.json` but were not accepted by the historical Unit 6 F5 gate.

The resulting CI failure was:

```text
UNIT6 F5 QA FAIL
- F5 runtime file mismatch without later F6/Unit7 lock backend/main.py
- F5 runtime file mismatch without later F6/Unit7 lock frontend/js/audio.js
```

## Correction

`qa_unit6_f5.py` now discovers runtime hashes from all later unit content locks instead of hard-coding the Unit 7 F5 lock. A current shared runtime file is accepted only when its exact SHA-256 is present in a later unit's explicit `runtime_file_sha256` lock.

This keeps the historical Unit 6 F5 gate strict while making it forward-compatible with Unit 7 F6 and future locked unit integrations.

## Scope

This is a QA/CI compatibility correction only.

- No Unit 1–7 canonical science changed.
- No Unit 1–7 narrative changed.
- No Memory Object, Review target, mixed-discrimination item, Challenge Lab task, or scope guard changed.
- No student-facing runtime behavior changed.
- Unit 7 remains at runtime `v2-apbio-0.28.0-u7-f6`.

## Verification

After the correction:

- `python scripts/qa_unit6_f5.py` passes.
- The complete GitHub Actions command chain through Unit 7 F6 passes locally.
- `python -m pytest -q` passes with 372 tests.
- JavaScript syntax checks pass.
- Python compilation passes.
- A temporary Git repository test running the historical Unit 6 F5/F6 gates, Unit 7 F6 gate, and full pytest suite finishes with `git diff --exit-code` passing.
