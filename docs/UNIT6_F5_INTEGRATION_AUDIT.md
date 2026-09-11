# Unit 6 F5 Integration Audit

## Result

**PASS**

Unit 6 is integrated into the existing student application without changing the locked Units 1–5 curriculum files or any Unit 6 F4 narrative.

## Student runtime

The course registry now marks Unit 6 as `STUDENT_READY`. The generic Home, Learn, Review, and Challenge Lab flows therefore include Unit 6 through the same unit-scoped runtime used by the earlier releases.

The backend now serves

- `/api/units/unit-6`
- `/api/units/unit-6/journeys`
- `/api/units/unit-6/journeys/{palace_id}`
- `/api/units/unit-6/objects/{object_id}`
- `/api/units/unit-6/application-lab`
- `/api/units/unit-6/review-manifest`
- `/api/units/unit-6/mixed-discrimination`
- `/api/units/unit-6/scope-guards`
- `/api/units/unit-6/finalization`

## Frozen narrative hashes

- **U6-J1** `fe01ed27cd6a8830022f131c22bcce74f9ad094aef189c991effb66f09741b83`
- **U6-J2** `62745c2fdcf98af10667a7cefa9907b420036952050d59aea7231dbd66de1ec6`
- **U6-J3** `91995e5f1e8f30072d511701556214fa16ba28b8533b460719bfe5b136722715`
- **U6-J4** `e074f28b35de6fe96de2015b1d8732055bc238235fa87367cf1976cb1df30b89`
- **U6-J5** `23b21efa45badeaef8db794af47f6fed87a623758e3c87487de2dcd68326aac1`
- **U6-J6** `cbb16bdd2ca5e9f386150860c5b802c93fadae25ff918db7bc366190f1f6c95c`

## Upstream protection

The original Unit 6 F1 upstream-protection manifest covers **291 Units 1–5 content files**. Those protected files remain unchanged. Historical Units 1–5 QA gates continue to pass in the Unit 6 F5 repository.

The older Unit 5 F6 runtime hash is preserved as a historical validation artifact. Because Unit 6 necessarily extends shared backend/runtime files, the Unit 6 F5 content lock now records the current runtime hashes. Historical Unit 5 F6 QA accepts a runtime-file change only when the current file is protected by the later Unit 6 runtime lock.

## Mainline totals

- Canonical records Units 1–6 **1,091**
- Guided journeys **44**
- Permanent scenes/loci **335**
- Challenge Lab tasks **83**

## Runtime version

`v2-apbio-0.25.0-u6-f5`

## Next gate

Unit 6 F6 should validate the classroom/browser-facing experience without changing curriculum artifacts or narrative bytes.
