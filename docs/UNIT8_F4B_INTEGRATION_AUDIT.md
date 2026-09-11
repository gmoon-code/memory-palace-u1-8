# Unit 8 F4B Integration Audit

## Result

**PASS**

## Frozen Units 1–7 protection

The F4B repository was compared byte-for-byte with the F4A baseline package from which this gate was built.

- Units 1–7 content files in baseline **421**
- Units 1–7 content files after F4B **421**
- Missing Units 1–7 files **0**
- Extra Units 1–7 files **0**
- Changed Units 1–7 files **0**

Backend and frontend source were compared after generated Python caches were removed.

- Baseline backend/frontend source files **15**
- Current backend/frontend source files **15**
- Missing source files **0**
- Extra source files **0**
- Changed source files **0**

The public runtime therefore remains `v2-apbio-0.28.0-u7-f6`.

## Unit 8 upstream lock protection

F4B was checked against the frozen Unit 8 F1, F2, F3, and F4A inputs.

- F3 journey briefs remain **8 / 8**
- F3 scene briefs remain **58 / 58**
- F3 palace-managed assignments remain **211 / 211**
- F4A content-lock files checked **7 / 7 identical**
- F4A Journey 1 scenes remain **12 / 12**
- F4A Journey 1 records remain **50 / 50**
- Changed F4A locked files **0**

The F4B narrative carries **47** Journey 2 knowledge records exactly as assigned by F3. All **24** exact-name targets retain their F2/F3 retrieval policy. The **3** first-exposure Quick Recall locations remain U8-L16, U8-L20, and U8-L21.

## Runtime boundary

Unit 8 now reports `F4B_JOURNEY2_POLISHED_DEVELOPER_PREVIEW` in the course registry, while `student_release` remains false. The public Unit 8 journey registry remains empty, direct public fetches of U8-J1 and U8-J2 return 404, and Unit 8 Application Lab remains empty. Unit 7 remains fully student-ready with all six journeys exposed.

## Repository-level changes required by the advancing preview gate

F4B adds the Journey 2 narrative source, machine-readable Journey 2 artifact, cumulative F4B preview registry, F4B lock and release manifests, F4B QA/build/test scripts, release documentation, and CI invocation for the new QA gate. Current-state tests that previously assumed F4A was terminal were generalized so the frozen F4A artifact can continue to be validated after later F4 gates advance Unit 8 status. No F1, F2, F3, or F4A locked curriculum artifact was altered.
