# AP Chemistry F0 curriculum contract

## Academic scope contract

The real AP Chemistry course will be constructed from an explicit source crosswalk. Every required framework topic must trace to the current College Board framework. Course organization and topic order follow the CED. Explanatory depth, examples, classroom emphases, and expected student reasoning trace to the supplied teacher PowerPoints. Chemistry accuracy and explanatory truth trace to Zumdahl, Zumdahl, and DeCoste, Chemistry, 11th edition, within CED scope. Laboratory contexts trace to the inventoried CED/public College Board laboratory guidance selected by user directive; specific procedures require their own source or original design.

General model knowledge is not used to silently fill source gaps during source intake.

## Course organization

The final course uses the current nine-unit College Board organization in CED order. Topic ordering inside each unit also follows the CED.

Teacher PowerPoint labels U1 through U15 are source identifiers only. They do not become Story Method units. F0B relocates each source concept into the CED topic where it belongs and may split one PowerPoint across multiple CED topics or units.

The final package may contain more than one journey per College Board unit. Journey boundaries are instructional and mnemonic design decisions. They may subdivide a CED unit while preserving CED topic order and complete auditable framework coverage.

## Story Method content contract

Each scientific record considered for production must identify the source-supported content it represents and the Story Method component it requires. Eligible components include

- concept
- memory object
- equation
- calculation
- graph
- diagram
- data table
- particulate model
- lab context

A scientific idea may use several components when the source material and AP reasoning demands require them.

## Chemistry-specific representation contract

AP Chemistry requires coordinated reasoning across observable phenomena, particle-level models, symbolic representations, mathematical relationships, and experimental evidence. F0C will therefore mark which topics require transitions among these representation levels.

Particulate models, equations, quantitative relationships, graphs, and lab evidence cannot be treated as decorative additions. Their roles must be tied to source-supported chemistry reasoning.

## Assessment contract

Later question and review construction will distinguish

- exact terminology and definition retrieval
- conceptual discrimination among confusable ideas
- symbolic and equation interpretation
- quantitative setup and calculation
- particulate-model reasoning
- graph and data interpretation
- experimental design and error reasoning
- explanation and argumentation

Released College Board questions may inform public exam-format expectations. Secure material is not required for the source contract.

## Conflict handling

When sources disagree

1. record the disagreement
2. identify the source and version on each side
3. classify the disagreement as AP scope/organization, chemistry accuracy/explanation, student-depth expectation, assessment convention, notation, or classroom convention
4. apply the authority rule explicitly: CED for AP scope and order, Zumdahl 11e for chemistry truth, teacher PowerPoints for intended student depth, and supplied scoring guides for assessment-demand evidence
5. preserve AP-specific notation or conventions when the CED requires them while keeping the underlying chemistry consistent with Zumdahl
6. do not rewrite or reconcile a disagreement silently
7. resolve the issue before the affected real content record is locked

The current fixture/official Unit 2 title difference is the first recorded architecture discrepancy.

## F0C component lock

The topic-level component plan is `docs/ap-chemistry/AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json`. Later production must preserve its required, supporting, not-primary, and excluded states unless a newly inventoried source justifies a documented revision. Lab-context planning is now grounded in the inventoried CED/public College Board laboratory source basis.

The component lock includes two explicit assessment-scope guards. Topic 8.11 does not require calculations of solubility as a function of pH. Topic 9.10 does not require Nernst-equation calculations. The CED-required particulate representation in Topic 7.8 remains required even though the teacher-PPT treatment is partial.

A teacher-specific laboratory collection is waived by user directive. F0C records the CED/public College Board lab basis and project topic-level lab-planning classes without claiming official College Board topic assignments.

## F0D gate outcome

The first F0D run is recorded in `docs/ap-chemistry/AP_CHEMISTRY_F0D_READINESS_GATE.json`.

The gate locks all nine official CED unit titles and all 91 topic boundaries. It also assigns bounded production treatments to the seven F0B source-gap topics. Topic 9.7 remains explicitly marked as lacking a direct teacher-PPT depth source and is restricted to the minimum CED requirement with Zumdahl-verified chemistry if production is later authorized.

The gate has been rerun after the user selected the CED/public College Board laboratory guidance as the lab-source basis. That basis is inventoried, the laboratory blocker is cleared, and F0D is complete. Package and content production are authorized for later commits, while student visibility and teacher editability remain locked.

## Readiness rule

F0D passes only when

- all nine official units are represented in the framework crosswalk
- each required topic has at least one authoritative framework source
- teacher-material coverage is inventoried
- textbook coverage is inventoried when a textbook is supplied
- lab coverage is inventoried when lab materials are supplied
- unresolved source conflicts are listed
- chemistry-specific component requirements are mapped
- package construction can proceed without using the architecture fixture as academic evidence

F0D has passed. The next phase may construct the real AP Chemistry package while AP Chemistry remains development-only, student-hidden, and read-only.
