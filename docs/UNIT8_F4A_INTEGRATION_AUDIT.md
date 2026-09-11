# Unit 8 F4A Integration Audit

## Result

**PASS**

## Frozen Units 1–7 protection

The F4A repository was compared with the validated Unit 8 F3 integrated baseline that was built from the user-supplied Units 1–7 CI-fix package.

- Units 1–7 content files in baseline **421**
- Units 1–7 content files after F4A **421**
- Missing Units 1–7 files **0**
- Extra Units 1–7 files **0**
- Changed Units 1–7 files **0**

Backend and frontend source were also compared after generated Python caches were removed.

- Baseline backend/frontend source files **15**
- Current backend/frontend source files **15**
- Missing source files **0**
- Extra source files **0**
- Changed source files **0**

The public runtime therefore remains `v2-apbio-0.28.0-u7-f6`.

## Unit 8 upstream lock protection

F4A was checked against the frozen Unit 8 F1, F2, and F3 inputs before narrative generation.

- Checked F1/F2/F3 lock and core artifacts **12**
- Changed protected artifacts **0**
- F3 journey briefs remain **8 / 8**
- F3 scene briefs remain **58 / 58**
- F3 palace-managed assignments remain **211 / 211**

The F4A narrative carries **50** Journey 1 knowledge records exactly as assigned by F3. All **35** exact-name targets retain their F2/F3 retrieval policy, and the **2** first-exposure Quick Recall locations remain U8-L02 and U8-L06.

## Runtime boundary

Unit 8 now reports `F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW` in the course registry, but `student_release` remains false. The public Unit 8 journey registry remains empty, direct public fetch of U8-J1 returns 404, and Unit 8 Application Lab remains empty. Unit 7 remains fully student-ready with all six journeys exposed.
