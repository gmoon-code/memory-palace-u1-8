# Multi-course classroom and browser acceptance

## Purpose

This acceptance gate validates the completed multi-course architecture through the teacher-facing Content Studio workflow before any merge into production or any real AP Chemistry curriculum expansion.

The gate exercises the two intentional course states currently present in the repository. AP Biology is the editable classroom course. AP Chemistry is a hidden architecture fixture that can be inspected throughout Content Studio while all authoring and publication mutations remain locked.

## Acceptance path

The automated acceptance covers the same transitions a teacher performs in the browser.

1. Sign in to Content Studio and load the course selector.
2. Confirm AP Biology is catalog-ready and editable.
3. Confirm AP Chemistry is catalog-ready and read-only.
4. Switch between the two course maps and verify their course-local Unit 1 records resolve independently.
5. Open an AP Biology scene in the generic editor and Student Preview, then create a protected Biology working copy.
6. Switch to AP Chemistry and inspect a Chemistry scene in the generic editor, Student Preview, Complete Story Replacement plan, Question Bank, Review System, Challenge Lab, Content Health, and Publication status.
7. Attempt protected AP Chemistry mutations and confirm the server rejects each one because editing is disabled.
8. Create an AP Biology working copy, switch course context, and confirm the Biology draft cannot be fetched through the Chemistry course identity.
9. Verify every browser workspace listens for the shared course-change event and that persistent Current Record context clears when its course no longer matches.
10. Verify student GitHub Pages still selects only courses that are both available and student-visible.

## Automated evidence

The API-level classroom acceptance lives in

```text
tests/test_multi_course_classroom_browser_acceptance.py
```

The browser-contract QA lives in

```text
scripts/qa_multi_course_classroom_browser_acceptance.py
```

Both are part of the normal repository QA. They complement the package, subsystem, integration, and full Python regression gates already present.

## Safety conditions

The acceptance pass must leave these conditions unchanged.

- AP Biology curriculum source files are not modified.
- AP Chemistry remains `status=development`, `student_visible=false`, and `editable=false`.
- No AP Chemistry working copy, proposal, replacement draft, or publication candidate can be created.
- Course-local IDs cannot cross course boundaries.
- Content Studio browser state is refreshed on course changes.
- Student Pages does not publish AP Chemistry fixture content or administrator assets.
- Production `main` remains untouched.

## Completion condition

The classroom/browser acceptance passes when the dedicated acceptance tests and browser-contract QA succeed together with the entire GitHub Actions workflow on the exact architecture branch head. Passing this gate means the multi-course foundation is ready for a separate release decision or, while remaining on the architecture branch, the later start of real AP Chemistry curriculum production.
