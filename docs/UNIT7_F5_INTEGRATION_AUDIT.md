# Unit 7 F5 Integration Audit

## Runtime integration

F5 adds Unit 7 to the generic AP Biology runtime without creating a separate Unit 7 user interface.

The runtime now loads

- `memory-objects-f5.json`
- `journeys-f5.json`
- `application-lab.json`
- `review-manifest-f5.json`
- `mixed-discrimination-f5.json`
- `scope-guards-f5.json`
- `finalization-f5.json`

through the same unit-scoped API pattern used by released Units 4–6.

## API surfaces

The integration exposes

```text
/api/units/unit-7
/api/units/unit-7/architecture
/api/units/unit-7/scene-briefs
/api/units/unit-7/journey-briefs
/api/units/unit-7/journeys
/api/units/unit-7/journeys/U7-J1 ... U7-J6
/api/units/unit-7/application-lab
/api/units/unit-7/review-manifest
/api/units/unit-7/mixed-discrimination
/api/units/unit-7/scope-guards
/api/units/unit-7/finalization
/api/units/unit-7/objects/{knowledge_id}
```

## Learner interface

The existing Home, Learn, Review, and Challenge Lab interfaces are unit-generic. Because Unit 7 is now marked `STUDENT_READY`, the roadmap exposes an **Open** button for Unit 7 and the existing Learn view renders all six journeys using their frozen F4 scene structures.

No Unit 7-specific shortcut or alternate interface was added.

## Runtime version

```text
v2-apbio-0.27.0-u7-f5
```

## Protection boundaries

The Unit 7 F5 content lock protects

- all eight F5 curriculum/runtime data artifacts
- all six frozen Journey JSON files
- content locks F1 through F4F
- the runtime files required to expose the release

The historical Units 1–6 content remains protected by the existing Unit 7 upstream-protection manifest and historical unit locks.

## Remaining validation boundary

F5 confirms functional curriculum/runtime integration. It does not claim the final F6 classroom/browser-facing validation matrix. F6 remains responsible for responsive layout contracts, production render coverage, hidden recall state rendering, refresh/resume behavior, released-unit switching, review state-machine behavior, Challenge Lab interaction flow, speech normalization, and the final live package audit.
