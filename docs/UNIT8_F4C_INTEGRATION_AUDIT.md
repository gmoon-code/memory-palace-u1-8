# Unit 8 F4C Integration Audit

## Result

**PASS**

## Frozen Units 1–7 protection

The F4C repository was compared byte-for-byte with the F4B baseline package from which this gate was built.

- Units 1–7 content files in baseline **421**
- Units 1–7 content files after F4C **421**
- Missing Units 1–7 files **0**
- Extra Units 1–7 files **0**
- Changed Units 1–7 files **0**

Backend and frontend source were compared after generated Python caches were excluded.

- Baseline backend/frontend source files **15**
- Current backend/frontend source files **15**
- Missing source files **0**
- Extra source files **0**
- Changed source files **0**

The public runtime therefore remains `v2-apbio-0.28.0-u7-f6`.

## Unit 8 upstream lock protection

F4C was checked against the frozen Unit 8 F1, F2, F3, F4A, and F4B inputs.

- F3 journey briefs remain **8 / 8**
- F3 scene briefs remain **58 / 58**
- F3 palace-managed assignments remain **211 / 211**
- F4A content-lock files checked **7 / 7 identical**
- F4B content-lock files checked **7 / 7 identical**
- F4A Journey 1 scenes remain **12 / 12**
- F4B Journey 2 scenes remain **9 / 9**
- Changed F4A locked files **0**
- Changed F4B locked files **0**

The F4C narrative carries **15** Journey 3 knowledge records exactly as assigned by F3. All **11** exact-name targets retain their F2/F3 retrieval policy. The **2** first-exposure Quick Recall locations remain U8-L22 and U8-L25.

## Runtime boundary

Unit 8 now reports `F4C_JOURNEY3_POLISHED_DEVELOPER_PREVIEW` in the course registry, while `student_release` remains false. The public Unit 8 journey registry remains empty, direct public fetches of U8-J1, U8-J2, and U8-J3 return 404, and Unit 8 Application Lab remains empty. Unit 7 remains fully student-ready with all six journeys exposed.

## Repository-level changes required by the advancing preview gate

F4C adds the Journey 3 narrative source, machine-readable Journey 3 artifact, cumulative F4C preview registry, F4C lock and release manifests, F4C QA/build/test scripts, release documentation, and CI invocation for the new QA gate. Current-state F4B test and QA checks that had assumed F4B was terminal were generalized so the frozen F4B artifact continues to be validated after later F4 gates advance Unit 8 status. No F1, F2, F3, F4A, or F4B locked curriculum artifact was altered.
