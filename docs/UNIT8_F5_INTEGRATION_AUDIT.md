# Unit 8 F5 Integration Audit

## Runtime integration

F5 adds Unit 8 to the same generic AP Biology runtime used by the earlier released units. No separate Ecology-only learner interface was created.

The runtime now loads

- `memory-objects-f5.json`
- `journeys-f5.json`
- `application-lab.json`
- `review-manifest-f5.json`
- `mixed-discrimination-f5.json`
- `scope-guards-f5.json`
- `finalization-f5.json`

for Unit 8 through the common unit-scoped API path.

## API surfaces

```text
/api/units/unit-8
/api/units/unit-8/architecture
/api/units/unit-8/scene-briefs
/api/units/unit-8/journey-briefs
/api/units/unit-8/journeys
/api/units/unit-8/journeys/U8-J1 ... U8-J8
/api/units/unit-8/application-lab
/api/units/unit-8/review-manifest
/api/units/unit-8/mixed-discrimination
/api/units/unit-8/scope-guards
/api/units/unit-8/finalization
/api/units/unit-8/objects/{knowledge_id}
```

## Learner interface

Because Unit 8 is marked `STUDENT_READY`, Home now exposes Unit 8 as a released unit. The existing Learn view renders all eight frozen F4 journeys. Review uses the Unit 8 exact-name and mixed-discrimination manifests. Challenge Lab serves all 13 PRACTICE_ONLY application tasks.

Released-unit switching now covers Units 1–8. The unit-generic frontend source did not require a Unit 8-specific branch.

## Runtime source changes

F5 updates the backend unit registry/loaders so Unit 8 can serve its F2/F3 developer records and F5 runtime records through the same API contracts as earlier units. The runtime health version advances to

```text
v2-apbio-0.29.0-u8-f5
```

The generic frontend JavaScript remains unchanged from the F4H baseline.

## Upstream protection

Against the F4H baseline used to build F5

- all **421 Units 1–7 content files** remain byte-for-byte identical
- all **80 pre-existing Unit 8 content files** remain identical except the expected current `status.json` advancement to F5
- all frozen Unit 8 Journey JSON files remain unchanged
- the F1, F2, F3, and F4A–F4H lock artifacts remain protected
- F4 narrative QA reports remain historical artifacts and are not rewritten when those gates are revalidated under the later F5 runtime

## Historical gate compatibility

Historical F4 tests and QA continue to verify the original developer-preview artifacts. Their current-runtime assertions now recognize `UNIT8_FINALIZED_F5` as a legitimate later state while leaving every F4 narrative and content-lock assertion intact.

Historical Unit 5–7 F6 runtime-lock QA similarly accepts runtime bytes only when they are recorded in the later Unit 8 F5 content lock. The historical U1–U7 mainline manifest remains frozen at its original U7 F6 totals while the current runtime can advance to U8 F5.

## CI integration

The GitHub Actions workflow now runs the Unit 8 F5 deterministic builder, Unit 8 F5 curriculum/runtime QA, the Units 1–8 mainline gate, and Unit 8 F5 UI-logic QA. The workflow continues to run historical Unit 8 F4 gates before the F5 builder and ends with the full Python suite, JavaScript syntax checks, Python compilation, and repository-cleanliness verification.

## Remaining validation boundary

F5 confirms curriculum finalization and functional runtime integration. **F6 remains required** for the final Unit 8 classroom/browser-facing validation record. F6 may document narrowly scoped runtime or speech-preparation fixes, but it must not rewrite the frozen Unit 8 curriculum.

## Final regression closure

The remaining historical F3 compatibility issue was resolved without changing the frozen F3 artifacts. `qa_unit8_f3.py` now accepts the later `UNIT8_FINALIZED_F5` course state only when the finalized Unit 8 counts are exactly 8 journeys, 58 scenes, 211 runtime Memory Objects, and 13 Challenge Lab tasks and the F3 architecture/brief counts and `LOCKED_F3` marker remain intact.

The F5 builder was also made idempotent. Repeated execution previously could append duplicate `UNIT8_DIR` imports in `backend/content.py`, which in turn changed the F5 content-lock hash. The import normalization is now deterministic. A stabilized rebuild followed by a second rebuild checked 16 generated/runtime integration artifacts and changed 0.

The exact GitHub Actions command sequence was then run in a clean probe copy. After excluding generated caches, the probe contained the same repository files and hashes as the F5 source tree with 0 changed, 0 added, and 0 removed files.
