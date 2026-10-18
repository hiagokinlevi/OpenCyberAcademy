# OpenCyber Academy reference guide for AI assistants and readers

**Daily lesson model:** The [curriculum grid](CURRICULUM_GRID.md) defines five instructional weekdays per week and one distinct numbered lesson per day, normally five lessons within a weekly chapter. Each authored daily lesson must teach a bounded concept, show a worked example, assign at least one substantive exercise, link its worked answer, and supply previous/index/next navigation. Subjects organize modules; they are not one-day lessons. The 20–1,300 lesson counts are minimum baselines, with **no maximum chapter or lesson length**. Existing subject-chapter indexes and structural coverage tables describe the older module structure, not completion of the daily sequence. Assess each language edition from its own manuscript, not another edition's availability.

OpenCyber Academy is a public, free Markdown learning library. Its [home page](README.md) is the main entry point. Use the [two onboarding routes](README.md#comece-por-aqui): **language → topic → level → course lesson guide**, or **language → level → all topics and their lesson guides**. Both lead to the existing course editions; the directory hierarchy is not a restriction on how a learner chooses a route. Plans and public drafts must be described with their actual editorial state.

## Main indexes

| Need | Open |
|---|---|
| One route from the first lesson to the last, across all levels and areas | [Complete sequential study path](STUDY_PATH.md) |
| All nine formation levels | [Level index](levels/README.md) |
| All 23 academic areas | [Area map](AREA_MAP.md) and [detailed map](mapa-areas-ciberseguranca.md) |
| All 207 courses and book editions | [Course guide](COURSE_GUIDE.md) |
| Subject counts and depth by level | [Curriculum grid](CURRICULUM_GRID.md) |
| One AI skill for each course | [Skill index](SKILLS.md) |
| Supplementary practice | [Playbook index](playbooks/README.md) |
| Linked projects | [Project index](PROJECTS.md) |
| Draft writing by area and sigil | [Writing-progress index](WRITING_PROGRESS.md) |
| Progress and completion rules | [Structure review](STRUCTURE_REVIEW.md) and [book standard](BOOK_STANDARD.md) |
| Rights and provenance | [Rights notice](RIGHTS.md) and [source audit](SOURCE_AUDIT.md) |

The current design has five schools, 23 academic areas, nine levels, **207 course skills**, and nine planned language editions per course (**1,863 planned books**). The old English grids contain **4,186 subject-module positions**; they are not 4,186 finished daily lessons. For actual availability, consult [English legacy progress by course](COURSE_WRITING_PROGRESS.md), [numbered chapters by language](LANGUAGE_LESSON_PROGRESS.md), the edition's `SUBJECTS.md`, and the selected `MANUSCRIPT.md`. The [rapid Incident Response English edition](levels/rapid-1-month/incident-response-resilience/en/SUBJECTS.md) shows the first four-weekly-chapter, 20-daily-lesson migration. Other indexes retain their actual structure until each edition is expanded. Counts and file presence do not establish technical depth, translation fidelity or completion.

## Follow the entire curriculum in order

The [study path](STUDY_PATH.md) numbers the courses **001–207**. Traverse the nine levels in their published order; within each level, traverse all 23 areas in catalog order. Open the **selected language edition's current** `SUBJECTS.md` and traverse lessons and chapters in the order shown. Its **Next step** column links to the next chapter or, on the final row, the next course in the same language. After the 23rd course in a level, continue at the first area of the next level. The study path's historic global ranges count old module positions; use the edition index for actual daily lessons.

For an AI tutor, keep a checkpoint with `{language, course_number, module, chapter_number, lesson_number, source_state, exercises_attempted, next_step}`. A link to `MANUSCRIPT.md` means readable teaching exists; a `PLAN.md` link is an outline and cannot complete a lesson. Ask the learner to attempt the lesson's own exercises before consulting its worked answers. Cite the exact chapter and primary factual sources. When a daily lesson is missing, report the gap and retain the checkpoint there; a navigation link to a later course does not fill it. English is written and reviewed first. Teach from the selected language edition only after reading its authored text; do not silently substitute an English outline for a lesson in another language. A readable translation can still need technical and linguistic review.

At the end of an authored chapter or a `PLAN.md` chapter summary, follow its **Continue studying** block: previous chapter, course chapter index and next chapter. A plan labels its links as draft or plan, so do not treat an outline as a lesson. The final authored chapter of a partial book points to the next *plan* and labels it as unwritten; the final chapter of a course returns to the index, whose last row points to the next course in the same language. Keep the learner's current chapter visible when moving backward or forward.

## Follow a course

~~~text
README.md
  → STUDY_PATH.md                         complete ordered route and course numbers
  → levels/README.md
  → levels/<level>/README.md
  → levels/<level>/<area>/README.md       course home, nine languages, one skill
  → levels/<level>/<area>/<language>/README.md
  → SUBJECTS.md                          subject and chapter index
  → book/PLAN.md                         chapter summaries
  → book/MANUSCRIPT.md                   authored text, only when present
~~~

For example, open the [rapid level](levels/rapid-1-month/README.md), the [Incident Response course home](levels/rapid-1-month/incident-response-resilience/README.md), its [English subject index](levels/rapid-1-month/incident-response-resilience/en/SUBJECTS.md), [book plan](levels/rapid-1-month/incident-response-resilience/en/book/PLAN.md), [manuscript draft](levels/rapid-1-month/incident-response-resilience/en/book/MANUSCRIPT.md), [single course skill](levels/rapid-1-month/incident-response-resilience/skill/SKILL.md), and [supplementary playbooks](playbooks/incident-response-resilience/README.md).

Each course has **one skill** and **one principal book per language**. Existing indexes treat each curricular subject as one legacy chapter; the new authoring model uses subjects as modules and one weekly chapter with five daily lessons by default. A complete daily lesson teaches a specific concept, gives a worked example and an exercise; worked answers appear at the end of the book. There are no separate subject skills or subject textbooks.

## Interpret editorial state

| File | What it establishes |
|---|---|
| Course `README.md` | Intended audience, entry knowledge, outcomes, all language editions and links |
| Edition `SUBJECTS.md` | Planned subject order, chapter targets and draft links |
| `book/PLAN.md` | Proposed chapter summaries and page/exercise budgets |
| `book/MANUSCRIPT.md` | Authored teaching that is actually present, with its stated review state |
| `skill/SKILL.md` | Navigation and tutoring instructions for the course, not an additional book |
| `playbooks/README.md` | Pointers to supplementary sources that retain their own rights |

A plan is not a written lesson. A public draft is not a technically reviewed book. A completed edition meets the [book standard](BOOK_STANDARD.md): the learning chain, worked examples, answered exercises, accurate sources and editorial review. Page count and lesson count are not completion gates. The course titles describe intended depth; they do not confer an accredited degree.

The [area-by-language writing table](WRITING_PROGRESS.md) measures chapter-anchor coverage; the [course writing table](COURSE_WRITING_PROGRESS.md) uses a separate English draft-depth test. Neither measure is tailored chapter-plan coverage or a count of books that have passed the completion gate. Do not present a coverage percentage as book completion or translated-content progress.

## Quality-first learning reviews

The purpose of a deeper chapter is to increase what the learner can **explain, distinguish, test and justify**, not merely its word count. Apply the [book standard](BOOK_STANDARD.md) to the text actually present. A high coverage percentage, a large file or a diagram in every chapter cannot establish that a reader understands the subject. The guidance below is a OpenCyber Academy teaching method, not a NIST, ISO or accreditation requirement, and not a claim that the existing corpus has already passed these checks.

### Review the learning chain

Read the chapter, its exercises and the corresponding final answers as one unit. Start with an explicit learning objective and trace the chain **definition → mechanism → assumptions → evidence → decision → limitation → practice → explanation of the result**. Locate the precise break when a learner cannot follow that chain. Do not replace an unclear explanation with additional terminology or a longer checklist.

| Review question | Evidence a useful chapter should provide | What does not resolve the gap |
|---|---|---|
| What does the concept mean, and what is it not? | A precise definition, prerequisites, a boundary case and a distinction from nearby concepts | A glossary entry copied into several paragraphs |
| Why does the mechanism produce the claimed result? | Inputs, intermediate states, causal steps, outputs and assumptions at the course's level | A list of commands without explaining what changes |
| Why choose this method rather than another? | Comparison criteria, a justified choice and conditions that would change it | Declaring one tool or framework universally superior |
| What supports the conclusion? | Observed evidence separated from a hypothesis, model, inference or synthetic fixture | Treating an intended control, missing log or successful command as a verified outcome |
| Can the learner reproduce and challenge it? | A worked example, an independently solvable variation and a relevant failure or boundary case | Repeating the worked example with only names changed |
| Can the learner explain a different result? | Expected evidence, diagnostic checks, uncertainty and limits of the method | An answer key containing only the final answer |

Before adding material, compare it with the preceding and following chapters. Define new terms before using them, revisit prerequisites briefly when needed, and link to the full earlier explanation instead of duplicating it. Preserve useful detail already present. Expand a mechanism, comparison, worked example or validation argument where that is the missing learning step; do not impose an arbitrary chapter word ceiling or add length solely to meet a page floor.

### Match depth to the formation level

Use each course's own entry knowledge and `PLAN.md` as the scope boundary. The following distinctions guide tutoring; they do not replace a curriculum or confer qualifications. Greater depth means a more demanding explanation and evaluation task, not only more terminology.

| Level | Expected increase in learning demand | Evidence to seek in examples and exercises |
|---|---|---|
| Rapid | Recognize core concepts and complete a bounded, guided task | Plain-language definitions, visible steps, a justified safe decision and a stated limit |
| Professional | Execute and explain a defined workflow under realistic constraints | Roles, inputs, handoffs, alternative outcomes and checks that the task actually succeeded |
| Technical | Explain mechanisms and diagnose failures using evidence | Data fields, transformations, assumptions, reproducible tests, missing or inconsistent inputs and troubleshooting |
| Technologist | Integrate components and evaluate an end-to-end process | Interface contracts, dependencies, observations across components and validation under controlled change |
| Bachelor's | Connect foundations, formal models and empirical results | Explicit assumptions, derivations where relevant, competing explanations and evidence-based comparison |
| Engineering | Design and validate a system against interacting constraints | Quantified requirements where meaningful, units, trade-offs, failure analysis, test criteria and sensitivity to assumptions |
| Postgraduate | Apply established foundations critically to a specialized problem | A bounded domain problem, cross-source analysis, justified method selection and limits of transfer |
| Master's | Develop and evaluate a research question systematically | Literature-based justification, explicit methods, suitable baselines, reproducible analysis and treatment of uncertainty |
| Doctoral | Examine a defensible contribution to an unresolved research question | A precise gap, testable or otherwise evaluable claims, rigorous comparison, conditions for refutation and limits on novelty claims |

A rapid-course learner should not need unexplained research mathematics to complete the core lesson. Conversely, a technical or research chapter is not adequate merely because it renames an introductory example. Where a higher-level book revisits a concept, make the additional mechanism, constraint, method or evidential burden explicit. Do not claim an original research result from a proposed experiment that has not been performed.

### Use visuals and data to explain, not decorate

Choose the representation for the learning question. A comparison table should expose decision criteria and limitations; a logical diagram should identify components and relationships; a flowchart should expose a decision, its inputs and its alternative outcomes. A quantitative chart should explain a pattern in actual supplied data, not imply that invented measurements were observed.

Do not add a flowchart to every lesson by default. A chain of section titles, followed by “worked example” and “exercise,” is navigation rather than a conceptual diagram; use the chapter index and previous/next links for that purpose. Keep a visual only when its nodes and relationships teach something the prose alone does not show as clearly.

For diagrams and flowcharts, label nodes, arrows, boundaries and relevant states. Explain what an arrow means: sequence, dependency, data movement and authorization are different relationships. Include unsuccessful paths, unresolved states and stopping conditions when they affect the lesson. Provide a caption and a prose explanation that conveys the essential information without relying on the image, layout or color. Check readability and rendering; valid-looking Mermaid text alone is not evidence that a figure renders correctly.

For tables, datasets and charts, state the source or mark the data as synthetic. Specify units, population, time interval, denominator, missing values and transformations where relevant. Supply the small input table or reproducible procedure needed to check a derived number. Explain whether the display illustrates a mechanism, describes a sample or supports an empirical claim. Do not infer causation, operational performance or general effectiveness from a synthetic teaching dataset. Avoid unsupported precision and do not fabricate a source, timestamp or measurement.

### Make examples and laboratories inspectable

A worked example should reveal the intermediate reasoning: what is known, what is assumed, what is calculated or tested, and what remains uncertain. Introduce a contrasting case that changes a meaningful assumption or input, then explain why the result changes or why the method still applies. Give the learner a comparable task to solve without exposing its answer in the prompt.

For an executable laboratory, identify prerequisites, versions where relevant, complete inputs, authorized or isolated scope, commands, expected observations, failure checks and safe cleanup. Distinguish a standalone program from a fragment that depends on earlier definitions. A fragment must name those dependencies and point to the complete program; it must not be presented as independently executable.

When reviewing a complete program, compare its observed output with the printed expected output and examine a relevant adverse or boundary input. Examples include an empty dataset, a missing field, a duplicate identifier, an out-of-order event, an expired authorization or a malformed value, depending on the lesson. Select cases that test the claimed mechanism rather than an unrelated implementation detail. Report environment-dependent or nondeterministic results honestly. Never replace an unperformed run with an expected-output block that looks like an execution record.

For evidence-based scenarios, separate event time from arrival, ingestion, query and collection time. A conclusion at a checkpoint may use only information available at that checkpoint. Missing coverage, a quiet query or a retention duration alone must not become proof of absence, a confirmed deletion deadline or a completed preservation action. Keep pedagogical decision categories separate from requirements actually stated by a cited standard.

### Keep exercises, rubrics and answers aligned

For every exercise, preserve its ID and match the objective, inputs, constraints, requested output, expected evidence and rubric to its final worked answer in the same book. Retain an existing 0–2 rubric where the course uses that format; describe the observable difference between its scores rather than awarding points for mentioning keywords. Explain acceptable alternatives and the conditions under which they are valid. Missing evidence and an incorrect conclusion are different problems and should receive different feedback.

A worked answer should explain the method, intermediate results, justified conclusion, limits and at least the relevant common error. It must not rely on a field, permission, tool or later case record that the prompt did not supply. Check exercise-to-answer references in both directions: no orphan prompt, duplicate ID, unassigned answer or answer attached to the wrong language edition. A detector finding an exercise token is not this check.

Use progressively less scaffolding within the course's scope: first interpret a solved example, then complete a comparable task, then explain a variation or failure. Add genuinely different practice where a learning objective lacks assessment. Do not inflate exercise counts with trivial subquestions, copied cases or answer headings. Keep each course's substantive exercise targets and publication gate separate from these tutoring suggestions.

### Review language editions for equivalent learning

A translation must preserve the learning burden, not just headings and chapter counts. Compare definitions, technical terms, negation, mandatory versus optional language, confidence statements, units, chronology, scope and safety conditions against the reviewed reference. Preserve exercise IDs, source pointers and code/API identifiers where changing them would break the lesson. Localize explanation and examples only when the adaptation preserves the concept and makes its assumptions explicit.

Read each translated prompt with its translated answer. Check that a translated figure, table or output explanation supports the same decision as the reference, and that links remain in the chosen edition unless a reference-language fallback is explicitly labeled. Treat a later change to the reference chapter as a reason to recheck the corresponding translations, not as evidence that they updated automatically. Do not erase valid existing translations while the English reference is being improved.

### Make review scope visible

Record the exact edition, source revision, chapter or section, exercise IDs and learning objective examined. For each finding, give a source anchor, the observed problem, a reproducible check where applicable, its learning consequence and a specific correction. Distinguish **not inspected**, **inspected with a defect**, **revised but not yet validated**, and **validated within the stated scope**. These are descriptive review states, not a replacement completion score.

Before calling an addition useful, answer: **What can the learner now explain, distinguish, test or justify that the prior text did not enable?** Show the supporting passage, exercise or test rather than reporting only words, pages, visuals or files added. Do not extrapolate a sample chapter's result to a whole book, another level or another language. A local improvement becomes part of a completed edition only through the separate [book publication gate](BOOK_STANDARD.md).

## Language and citation rules

The active editorial order is **English source → Portuguese translation → Spanish translation**. Review and pin a coherent English unit, including its dependent examples, exercises and answers, before translating that unit into Portuguese; the full English collection need not be finished before a released unit is translated. Keep Portuguese as the active translation language while English authoring continues. Begin planned Spanish translation after the complete Portuguese collection is current and reviewed; start the six remaining languages only after all three collections independently pass the [100% verified completion gate](BOOK_STANDARD.md#sequential-production-order). Follow the [translation workflow](TRANSLATION_WORKFLOW.md) for source and target revision mapping. A draft-coverage percentage, manuscript count or lesson anchor does not establish this gate. Preserve existing translations and inspect each edition independently: a non-English folder may contain authored teaching, an English working outline, or only a plan. Consult [language coverage](LANGUAGE_LESSON_PROGRESS.md) for reported availability, but verify the text and its review state before teaching. Do not describe an English outline as a translated lesson or infer language quality from chapter anchors.

Link to the exact Markdown file and chapter used. Where a factual claim depends on a cited external work, follow the original source and check that it supports the claim. Identify synthetic or adapted cases, respect [third-party rights](RIGHTS.md), and recommend only authorized or contained practical environments. For a reproducible citation, pin a GitHub link to a commit SHA.

**Author and editorial responsibility:** [hiagokinlevi](https://github.com/hiagokinlevi). Original maintainer-owned OpenCyber Academy text is dedicated under [CC0 1.0](LICENSE); accurate source citation remains an editorial requirement.
