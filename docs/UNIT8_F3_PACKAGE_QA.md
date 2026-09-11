# AP Biology Unit 8 F3 Package QA

The Unit 8 F3 repository package is acceptable only if all of the following remain true at archive time.

- Uploaded Units 1–7 CI-fix baseline validated before integration.
- Units 1–7 content directories remain byte-identical to that baseline.
- Backend and frontend runtime source files remain byte-identical.
- Unit 8 F1 and F2 protected hashes pass.
- Unit 8 F3 QA passes with 8 journey briefs, 58 scene briefs, 211 uniquely assigned palace-managed records, 211 canonical term/science introductions, and 18 optional first-exposure recalls.
- Full pytest suite passes after adding Unit 8 F3 tests.
- Unit 7 F6 QA and Units 1–7 mainline QA continue to pass.
- JavaScript syntax checks and Python compilation pass.
- No source PDF is packaged.
- No `__pycache__`, `.pytest_cache`, or compiled `.pyc` files are included in the final ZIP.
- Unit 8 remains student-unreleased and the public runtime remains `v2-apbio-0.28.0-u7-f6`.
