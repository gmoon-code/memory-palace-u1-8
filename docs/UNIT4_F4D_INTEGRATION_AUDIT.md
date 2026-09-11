# Unit 4 F4D Mainline Integration Audit

## Release boundary

Unit 4 remains an unreleased developer preview. F4D adds only Journey 4, **Feedback Regulation Center**, while Journeys 1–3 remain protected byte-for-byte by their earlier locks. Units 1–3 remain the only student-ready course units.

## Unit 4 F4D accounting

- Canonical scientific records protected: **180**
- F2 architecture: **7 journeys / 51 loci**
- F3 scene briefs: **51 / 51**
- Polished preview journeys: **4 / 7**
- Polished preview scenes: **25 / 51**
- Journey 4 records: **18 / 18**
- Journey 4 optional Quick Recalls: **2**
- Journey 4 narrative words: **2,727**
- Journey 4 mean scene length: **454.5 words**
- Journey 4 shortest scene: **425 words**
- Unit 4 student release: **false**
- Unit 4 preview release: **true**

## Narrative continuity

Journey 4 carries one regulated-variable gauge through Homeostasis Control Map → Sensor–Integrator–Effector Loop → Negative-Feedback Thermostat → Blood-Glucose Regulator → Positive-Feedback Amplifier → Dysregulation Alarm. The gauge preserves the direction of the disturbance, the reference range, response direction, and final regulated or dysregulated state.

The prose explicitly blocks the high-risk misconceptions identified in F1. Homeostasis remains dynamic rather than perfectly constant. Sensor, integration, and effector roles are not restricted to nervous-system anatomy. Negative feedback means opposing the initiating deviation, not “bad.” Positive feedback means reinforcing the initiating change, not “good.” Positive-feedback loops terminate when an endpoint or changed condition breaks the cycle. Dysregulated homeostasis can contribute to disease without defining all disease as homeostatic failure.

## Regression

The historical build sequence through Units 1–3 and Unit 4 F1–F4D passed. The combined Python suite passed **175 / 175** tests. Unit 3 F6 UI logic passed. Frontend JavaScript syntax and Python compilation passed. The F4C → F4D rebuild returned a clean Git tree after generation, confirming deterministic output for the current Unit 4 stage.

## API preview

The developer API exposes exactly four Unit 4 journeys in the current preview registry.

- `/api/units/unit-4/journeys/U4-J1`
- `/api/units/unit-4/journeys/U4-J2`
- `/api/units/unit-4/journeys/U4-J3`
- `/api/units/unit-4/journeys/U4-J4`

The student release flag remains false.

## Next gate

F4E may author **Journey 5, Cell-Cycle Preparation Archive** only. Journeys 1–4 must remain unchanged.
