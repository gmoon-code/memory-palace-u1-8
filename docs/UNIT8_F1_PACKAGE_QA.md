# Unit 8 F1 Package QA

## Scope

This package is a **Unit 8 F1 source-lock overlay** for the frozen Units 1–7 Unit 7 F6 baseline. It is not presented as a reconstructed copy of the full Units 1–7 repository because the exact frozen baseline ZIP is not present in this runtime.

## Validation completed

- Unit 8 overlay structural test: **PASS**
- teacher slide inventory: **96 / 96**
- current CED coverage: **50 / 50 atoms LOCKED**
- AP-required records: **61**
- teacher-required enrichment: **150**
- practice-only records: **13**
- scope guards: **31**
- canonical total: **255**
- review flags: **31 / 31 RESOLVED**
- assessment crosswalks: **13**
- student runtime records: **0**
- Python syntax/compilation of overlay tools: **PASS**
- overlay application mechanics on a synthetic repository baseline: **PASS**
- generated merged test archive integrity: **PASS**
- source PDFs included in overlay: **0**
- `.pyc` / `__pycache__`: **0**

## Baseline protection

The default overlay application refuses to proceed unless the supplied baseline ZIP SHA-256 equals:

```text
d344f3641dd2949fc6824bc6e7d150b681b72511572669524be22af9984a36ed
```

That is the frozen Unit 7 F6 ZIP checksum supplied for the Units 1–7 release. An explicit `--allow-unverified-baseline` override exists only for deliberate manual testing; it is not the default production path.

## No runtime release claim

F1 changes scientific/source records only. It does not add Unit 8 journeys, permanent scenes, Memory Objects, Review records, mixed-discrimination records, Challenge Lab runtime tasks, or student navigation. The frozen student runtime therefore remains `v2-apbio-0.28.0-u7-f6` until a later Unit 8 student-runtime gate intentionally changes it.
