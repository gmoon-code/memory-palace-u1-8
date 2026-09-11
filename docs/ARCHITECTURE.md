# Memory Palace V2 Architecture

V2 separates four concerns.

1. **Canonical scientific authority** — source-locked scientific records and provenance.
2. **Learning content** — Memory Objects, palace routes, narrative scenes, transfer tasks, and scope guards.
3. **Learner presentation** — Home, Learn, Review, and the compact Challenge Lab.
4. **Application code** — a modular frontend and FastAPI content service.

## Student experience

The main navigation remains deliberately small:

**Home → Learn → Review**

The Challenge Lab is launched from Home only when the learner wants application practice. Internal metadata such as cue dependency, exact-name flags, source traces, scope classes, and content-release states are not exposed as work the learner must manage.

## Unit 1 content partition

Unit 1 has 207 student-runtime Memory Objects.

- **199 permanent-palace objects** are taught through 9 stories across 78 locations.
- **8 practice-only runtime objects** remain outside permanent loci and are represented through the Unit 1 Challenge Lab.

The Challenge Lab contains 16 transfer/application tasks because several permanent-palace concepts also require calculation or novel-context practice.

## Review scheduling

Completing a scene schedules each exact-name target from that scene for later retrieval. Targets are staggered over multiple days. Review displays a maximum of five due memories in a session view even when the internal queue is larger.

## Content service

The API is unit-aware:

```text
/api/course
/api/units
/api/units/{unit_id}
/api/units/{unit_id}/journeys
/api/units/{unit_id}/journeys/{palace_id}
/api/units/{unit_id}/objects/{object_id}
/api/units/{unit_id}/application-lab
```

The same routes will serve Units 2–8 after their content is scientifically locked and released.

## Scientific boundary

Narrative generation never becomes the source of scientific truth. Unit source material is audited first. Canonical science is locked. Narrative fields may make that science concrete and memorable but may not change formulas, definitions, causal direction, AP scope, or answer basis.

## Current persistence boundary

V2 currently stores learner progress in browser `localStorage`. Authentication, managed learner databases, teacher dashboards, and production persistence should be reintroduced only after the learning architecture is stable.
