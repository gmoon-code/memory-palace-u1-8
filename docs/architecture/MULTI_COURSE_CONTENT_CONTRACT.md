# The Story Method multi-course content contract

This document defines the package boundary for adding a science course to The Story Method.

The platform hierarchy is **Course → Unit → Journey → Scene**. Student progress, teacher drafts, search, replacement, review, quality checks, and publication are scoped by `course_id`.

## Package files

Every runnable course has three coordinated records.

- A registry entry in `platform/courses.json`
- A package manifest in `platform/course-packages/<course_id>.json`
- Course metadata and course content under `content/<course_id>/`

The package manifest follows `platform/schemas/course-package-v1.schema.json`.

The manifest acts as an adapter. Existing validated content does not need to be renamed simply to satisfy a new global filename convention. AP Biology demonstrates this by mapping Unit 1 `journeys.json`, later-unit `journeys-f5.json` files, native Memory Object files, and the Unit 2–3 canonical-catalog compatibility adapter into one runtime contract.

## Stable identity

A course ID is stable and URL-safe, such as `ap-biology` or `ap-chemistry`. The same ID appears in the platform registry, package manifest, course metadata, student URLs, teacher drafts, and course-scoped progress.

A unit ID is only unique inside a course. `unit-1` can therefore exist independently in AP Biology, AP Chemistry, Biology, Chemistry, and later courses.

## Required unit runtime surfaces

Each unit package declares the following.

- Journey registry
- Journey JSON directory and filename template
- Canonical concept source
- Memory Object source
- Review manifest or an explicit empty adapter
- Mixed-discrimination manifest or an explicit empty adapter
- Challenge Lab

An intentionally empty feature uses `mode` set to `empty`. A missing file is never silently interpreted as empty content.

## Science component capabilities

The core runtime does not assume that all science is represented like biology. A course package can declare the scientific representations it uses.

Version 1 supports `concept`, `memory_object`, `equation`, `calculation`, `graph`, `diagram`, `data_table`, `particulate_model`, `vector`, and `lab_context`.

These are capability declarations. They do not require every scene to use every representation.

This lets AP Chemistry add equations, particulate models, calculations, graphs, data tables, and laboratory contexts while using the same Story Method hierarchy. Physics can later add vectors without changing the core course model.

## Memory Object formats

`native` reads an explicit Memory Object collection.

`canonical_catalog_as_memory_objects` is a compatibility adapter for legacy content where the validated student runtime historically treated canonical records as retrievable objects. New courses should normally use native Memory Object records.

## Readiness gates

A course becomes `available` and student-visible only after its package validates, its unit membership matches its course metadata, every registered journey file exists, every required runtime artifact stays inside that course namespace, all story Memory Object references resolve, course progress is isolated, the Content Studio catalog is ready, course-specific QA passes, and regression QA confirms existing courses remain unchanged.

A development course may be registered earlier while remaining hidden from students and disabled for teacher editing.

## AP Chemistry as the first second course

AP Chemistry should be the first real second-course package. It should preserve the shared Course → Unit → Journey → Scene model while exercising equations, quantitative calculations, particulate representations, graphs, data tables, and laboratory contexts.

The first AP Chemistry package should begin as a very small architecture fixture. Two tiny test units are enough to validate routing, progress isolation, Content Studio scoping, static deployment, and package validation before real curriculum production begins.

## Public deployment boundary

The static student-site builder copies only package-declared student artifacts for courses that are both available and student-visible.

Teacher-only source material, draft databases, private state, PDFs, office files, and administration assets remain outside the public student deployment.
