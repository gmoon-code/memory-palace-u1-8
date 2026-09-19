# AP Chemistry F0D readiness gate

## Result

**COMPLETE**

F0D now authorizes construction of the real AP Chemistry course package. The previous blocked F0D run correctly stopped production because the laboratory source basis had not been defined. The user has now explicitly directed the project to use the CED and public College Board laboratory guidance as that basis, and the basis has been inventoried.

The course remains development-only, hidden from students, and read-only. F0D completion authorizes later construction work. It does not publish AP Chemistry or enable editing.

## Locked academic foundation

The nine CED units and all 91 CED topic boundaries remain locked in CED order.

The authority hierarchy remains unchanged.

- The CED controls course structure, AP scope, unit/topic order, required content, science practices, and exclusions.
- Teacher PPT U1 through U15 controls intended student understanding depth after its material is relocated into CED order.
- Zumdahl, Zumdahl, and DeCoste, Chemistry 11e, controls chemistry accuracy and explanatory truth within CED scope.
- Supplied Unit 1 through Unit 9 scoring guides provide assessment-demand evidence without verbatim reuse.
- The CED and current public College Board laboratory guidance now provide the laboratory source basis.

## Laboratory blocker clearance

The prior hard blocker is cleared.

The inventoried basis is `docs/ap-chemistry/AP_CHEMISTRY_LAB_SOURCE_BASIS.json`. It records three official source layers.

1. The AP Chemistry CED supplies the course-level laboratory expectations and science-practice framework.
2. The current AP Chemistry Course Audit page supplies the 2026-27 laboratory curricular/resource requirements, student evidence requirements, and permitted laboratory modalities.
3. The College Board hands-on-lab FAQ defines hands-on and virtual laboratory experiences and clarifies that teacher demonstrations alone do not satisfy the requirement.

The later lab program must still preserve at least 25 percent laboratory instructional time, at least 16 hands-on investigations, and at least 6 guided-inquiry investigations.

The current lab basis does not claim that College Board officially assigned a specific experiment to a specific CED topic. The F0C topic mapping is a project planning classification based on experimental-reasoning priority.

The named `AP Chemistry Guided Inquiry Experiments: Applying the Science Practices` resource is referenced by the public Course Audit page, but its procedures were not ingested in this project. Later content must not reproduce or attribute procedures from that manual unless the source is actually available.

## F0B source-gap dispositions

All seven source-gap identifiers remain visible in the audit history and retain their bounded production rules.

- 1.4 Composition of Mixtures uses the CED framing with PPT-level percent-composition and purity depth.
- 2.2 Intramolecular Force and Potential Energy includes the CED-required potential-energy curve at PPT/CED depth.
- 7.8 Representations of Equilibrium includes the CED-required particulate model without claiming broader teacher-PPT coverage.
- 8.10 Buffer Capacity remains at CED depth with supplied assessment evidence.
- 8.11 pH and Solubility remains qualitative; solubility-as-a-function-of-pH calculations stay excluded.
- 9.6 Free Energy of Dissolution integrates the split solution/thermodynamics PPT material only to the CED objective.
- 9.7 Coupled Reactions remains the only direct teacher-PPT depth gap and is bounded to the CED minimum with Zumdahl-verified chemistry.

## Authorization after F0D

The following work is now authorized for later commits

- construction of the real nine-unit AP Chemistry package
- scientific-record and Memory Object production
- Story Method narrative authoring
- original question-bank and review-system production
- Challenge Lab design grounded in the inventoried laboratory basis

The following remain locked

- student visibility
- teacher editability
- publication to the student site
- any claim that an unsourced laboratory procedure came from College Board

## Runtime safety

This F0D completion commit still changes no file under `content/ap-chemistry/` and does not alter `platform/course-packages/ap-chemistry.json`. The architecture fixture remains intact until the next dedicated package-construction phase.

## Next phase

The next phase is the real AP Chemistry package foundation. That phase will replace the two-unit architecture fixture with the nine-unit CED structure and source-backed package scaffolding while keeping the course development-only, hidden from students, and read-only.
