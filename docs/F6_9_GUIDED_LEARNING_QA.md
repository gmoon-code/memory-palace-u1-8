# F6.9 QA Report — Simplified Guided Learning Experience

## Purpose

F6.9 responds to a learner-usability problem identified after Unit 1 content completion: the internal memory engine had become more complex than the student experience should be. The scientific and mastery machinery remains available, but initial learning is now designed to feel like a guided story rather than a sequence of nine named instructional phases.

## Student-visible learning loop

The top-level student navigation is reduced to:

- **Learn**
- **Review**
- **More**

Teacher Mode remains role-gated.

The default Learn experience presents only three recurring actions:

1. Follow the story.
2. Try an occasional Quick Recall.
3. Keep going.

The former Study, Eyes Closed, Hook Lab, and Unit 1 Check tools are no longer four equal top-level choices. They remain available under **More** for students who want or need additional practice.

## Guided-story rollout

- Guided palace stories: **9 / 9**
- Permanent loci represented as story scenes: **78 / 78**
- Permanent-locus Memory Objects carried inside those stories: **199 / 199**
- Transfer Bench objects intentionally kept out of first-exposure stories: **8**
- Quick Recall pauses across all nine palaces: **21**
- Maximum Quick Recall pauses in any one palace: **3**
- Short palaces use only **1** recall pause; medium routes use **2**; long routes use at most **3**.

Each palace now has a named narrative, premise, mission, recurring guide, causal route, and payoff. Examples include **The Flooded Sky Hotel**, **The Protein Tailor's Emergency**, **The Lost Genetic Manuscript**, and **The Membrane Rescue Wing**.

## Narrative-quality criteria

Every guided palace passes the following structural checks:

- **Premise present.** Something concrete has happened before instruction begins.
- **Goal present.** The learner has a reason to move through the route.
- **Recurring guide present.** The story does not introduce a new cast at every locus.
- **Spatial clarity.** Every story scene uses one of the 78 already fixed palace loci.
- **Causal continuity.** Every non-final scene contains a story-specific transition that moves the existing problem into the next locus.
- **Science-bearing imagery.** The object-level action remains the existing F6.8 mnemonic/scientific interaction.
- **Canonical translation.** Every story beat displays the exact unchanged canonical definition after the memorable action.
- **Payoff present.** The final locus resolves the problem established by the premise.
- **Decorative-science boundary.** New narrative wrappers cannot introduce a new canonical scientific claim.

## Cognitive-load protections implemented

1. **No route-primer requirement before guided learning.** The narration teaches the route while the student moves through it.
2. **No visible nine-phase progression in Learn.** Discover, Connect, Produce, Reverse, Spell, cue fading, discrimination, and application remain internal/advanced mechanisms.
3. **No visible dependency meter in Learn.** The 5→0 cue model remains diagnostic infrastructure.
4. **No mastery-gate dashboard in Learn.** Seven-gate mastery remains in the engine and Advanced Recall.
5. **No quiz after every Memory Object.** F6.9 uses 21 recall pauses across 78 scenes.
6. **One retrieval item per pause.** A Quick Recall does not branch into spelling, reverse recall, discrimination, and application on the same screen.
7. **Weak recall produces one consequence.** “I need a hint” shows the approved cue/answer and schedules a later review.
8. **Strong recall produces one consequence.** “I remembered it” schedules a later low-priority recheck.
9. **First-exposure story completion does not silently award full mastery.** Guided exposure never writes to mastery gates or marks nine-phase checks as passed.

## Retrieval leakage protection

A checkpoint initially appears only as **Try quick recall**. When the student begins the check, the story scene is hidden before the retrieval prompt appears. This prevents the target term or definition from remaining visible directly above the question.

After the learner chooses **I remembered it** or **I need a hint**, the answer appears and the story continues. There is no required multi-question remediation chain.

## Reading/listening load

The 78 guided scenes have a median of **193 spoken/read words**. The densest scene contains **451 words** and remains one continuous scene rather than six separate required interactions. Students may pause or replay browser text-to-speech at any time.

## Scientific preservation

F6.8 and F6.9 were compared across all 207 runtime Memory Objects.

**Memory Objects changed: 0 / 207.**

The 229 canonical records were compared for canonical statement, canonical label, AP scope class, scientific lock, source reference, retrieval demand, exact-name requirement, spelling requirement, confusable set, and release status.

**Scientific/source changes: 0 / 229.**

Every one of the 199 first-exposure story beats points back to an unchanged Memory Object, and the displayed `science` field is an exact copy of that object's locked canonical definition.

## Backend and migration QA

- `/health` reports **F6.9** and 229 canonical records.
- Runtime contains 207 Memory Objects and 9 guided journeys.
- Student content summary remains 207 runtime / 22 intentional non-runtime / 0 stageable.
- `guidedState` survives authenticated server round-trip synchronization.
- Guided completion/recall events are accepted by the append-only attempt log.
- Student access to teacher content remains blocked.
- A real **F6.8 → F6.9 SQLite migration** preserved a learner-state probe at revision 41 and synchronized all 207 released content records.

## Static QA

- JavaScript syntax: PASS
- Python compilation: PASS
- HTML parsing: PASS
- `runtime-data.js` equals `runtime-data.json`: PASS
- Guided object coverage: PASS
- Story route order: PASS
- Checkpoint density: PASS
- Mastery non-inflation audit: PASS

## Deliberate limitation

F6.9 solves the first-exposure usability problem at the architecture level and supplies a complete guided story route for Unit 1. It does not yet claim that real students will prefer every story, remember every image equally well, or find every scene optimally paced. Those questions require classroom usability data. The next validation should therefore measure completion rate, replay frequency, “need a hint” frequency, delayed retrieval, and student-reported cognitive load before the same interface is scaled to Unit 2.
