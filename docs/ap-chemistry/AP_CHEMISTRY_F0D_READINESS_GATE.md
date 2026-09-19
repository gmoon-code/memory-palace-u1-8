# AP Chemistry F0D readiness gate

## Result

**BLOCKED_PENDING_TEACHER_LAB_SOURCE**

The academic framework, topic order, teacher-depth crosswalk, chemistry reference, assessment evidence, and science-component plan are ready for production planning. F0D does not authorize construction of the real AP Chemistry runtime yet because the laboratory source basis remains unresolved.

The source register therefore remains at `F0C_COMPLETE`. No real package, scientific record, Memory Object, narrative, question bank, review record, Challenge Lab, or student-facing AP Chemistry content is authorized by this gate.

## What passed

F0A inventoried the supplied CED, Zumdahl 11e textbook, fifteen teacher PowerPoints, and ten Unit 1–9 scoring-guide files.

F0B mapped all 91 CED topics in exact CED order. F0C classified the required and supporting chemistry representations topic by topic.

The official nine-unit structure is now locked for future production.

| Unit | Locked title | Topic count |
| --- | --- | ---: |
| 1 | Atomic Structure and Properties | 8 |
| 2 | Compound Structure and Properties | 7 |
| 3 | Properties of Substances and Mixtures | 13 |
| 4 | Chemical Reactions | 9 |
| 5 | Kinetics | 11 |
| 6 | Thermochemistry | 9 |
| 7 | Equilibrium | 12 |
| 8 | Acids and Bases | 11 |
| 9 | Thermodynamics and Electrochemistry | 11 |

The architecture fixture is not accepted as academic evidence. Its Unit 2 title and two-unit size remain fixture-only details until a later authorized package replacement.

## F0B source-gap dispositions

The seven F0B source-gap identifiers remain in the audit trail. F0D defines bounded treatments for each so later production cannot silently inflate the curriculum.

### 1.4 Composition of Mixtures

Status  **ready_with_bounded_resolution**

CED supplies the mixture/purity framing. Teacher PPT U2 supplies percent-composition calculations, impurity reasoning, and purity checks. Zumdahl remains the chemistry reference.

Production guard  Teach the CED relationship between elemental mass composition and mixture composition using PPT-level percent-composition and purity reasoning. Do not expand into additional mixture-analysis methods without a new source.

### 2.2 Intramolecular Force and Potential Energy

Status  **ready_with_bounded_resolution**

CED requires the potential-energy-versus-internuclear-distance representation. Teacher PPT U8 directly teaches bond order, equilibrium bond length/internuclear distance, the minimum on the curve, bond strength, and bond energy. Zumdahl supplies chemistry support.

Production guard  Include the required potential-energy curve and its minimum, bond length, and bond energy. Keep depth at the CED/PPT level.

### 7.8 Representations of Equilibrium

Status  **ready_with_bounded_resolution**

CED explicitly requires a particulate model for reversible reactions at equilibrium. Teacher PPT U11 supplies dynamic-equilibrium and concentration/rate representations but does not directly supply the particulate model.

Production guard  Teach the CED-required particulate representation at minimum CED depth. Do not claim the teacher PPT provides a broader particulate-model sequence.

### 8.10 Buffer Capacity

Status  **ready_with_bounded_resolution**

CED defines the buffer-capacity relationships. Teacher PPT U12 supplies buffer composition and response to added acid/base. The Unit 8 scoring guide directly assesses how component concentration changes buffer capacity while the ratio and pH remain the same.

Production guard  Teach capacity through concentration and conjugate-pair proportions at CED depth. Keep calculations limited to what the supplied instructional and assessment sources support.

### 8.11 pH and Solubility

Status  **ready_with_bounded_resolution**

CED requires a qualitative pH-solubility relationship. Teacher PPT U13 supplies Ksp/common-ion and qualitative solubility reasoning, with supporting acid-base material from PPT U12.

Production guard  Keep reasoning qualitative. Do not require computations of solubility as a function of pH.

### 9.6 Free Energy of Dissolution

Status  **ready_with_bounded_resolution**

Teacher PPT U9 supplies the three energetic steps of solution formation. Teacher PPT U14 supplies free-energy, enthalpy, and entropy reasoning. CED supplies the integrated dissolution free-energy objective, with Zumdahl as chemistry reference.

Production guard  Integrate the PPT solution-formation and thermodynamics material only to the CED objective. Do not add textbook-only dissolution thermodynamics beyond that scope.

### 9.7 Coupled Reactions

Status  **ready_at_ced_minimum_with_teacher_depth_gap_retained**

No direct teacher-PPT treatment was located. CED requires external-energy and coupled-reaction reasoning, including shared intermediates and overall favorable free energy. Zumdahl 11e directly explains external-energy driving and coupled favorable/unfavorable reactions.

Production guard  Teach only the CED-required minimum using CED framing and Zumdahl-verified chemistry. Retain the missing teacher-depth source as a visible warning and do not add textbook-only depth.

## Remaining hard blocker

The teacher laboratory source is still unresolved.

The CED requires substantial laboratory instruction, including a minimum of 25 percent of instructional time in laboratory investigations, at least 16 hands-on investigations, and at least 6 guided-inquiry investigations. F0C therefore left every topic's teacher-lab mapping pending and explicitly marked the missing lab source as an F0D blocker.

F0D will not invent the teacher's laboratory sequence or silently substitute an external lab program. This blocks real package construction because `lab_context` and Challenge Lab are declared AP Chemistry course capabilities and because later narratives and questions may depend on experimental contexts.

The blocker can be cleared in either of two documented ways.

1. Supply the teacher's AP Chemistry lab procedures, lab manual, or intended lab sequence for inventory and mapping.
2. Explicitly direct the project to proceed without teacher-specific lab materials and to use the CED/public College Board laboratory guidance as the lab-source basis. That source basis must then be inventoried before F0D is rerun.

## Readiness decision

The following work remains authorized while blocked

- source intake and source-audit documentation
- revisions to the F0A/F0B/F0C planning artifacts when supported by new sources
- lab-source inventory and crosswalking

The following work remains locked

- replacement of the AP Chemistry architecture fixture
- construction of the real nine-unit package
- production scientific records and Memory Objects
- narrative Story Method journeys and scenes
- question-bank and review-system production
- Challenge Lab production
- AP Chemistry teacher editing or student visibility

## Runtime safety

F0D changes no file under `content/ap-chemistry/` and does not alter `platform/course-packages/ap-chemistry.json`. AP Chemistry remains development-only, student-hidden, and read-only.

## Next action

Collect or explicitly define the laboratory source basis, inventory it, update the F0C lab mappings, and rerun F0D. A passing F0D will be a separate commit and will be the first point at which real AP Chemistry package construction is authorized.
