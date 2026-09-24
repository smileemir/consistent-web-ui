# Contributing

Propose changes that help a real user finish a real task, and keep everything original: code, text, assets and reasoning. Do not submit copied product interfaces, third-party icons, marketing copy, photography or source files, and do not name studied products or other projects as sources. Research notes and permission records belong in private working files, never in this repository.

## Before you open a pull request

1. Run the tests: `python3 -m unittest discover -s tests`.
2. Keep `consistent-web-ui/SKILL.md` short. Detail belongs in a reference file that SKILL.md links to directly, with a clear "read when" line, so normal use loads only what a task needs. Every line in SKILL.md costs tokens on every run.
3. New scripts use the Python standard library only, are read-only unless their purpose is to write a file the user asked for, and come with tests that exercise them for real.
4. Keep the frontend boundary. A design contribution never changes server, database, payment or authorization behaviour.
5. If you change guidance, add or update an evaluation in `evals/` that shows the change helps.

## What a rule needs

- The page, the user task and the real data it depends on.
- Control behaviour, the small-screen and keyboard equivalent, and the error or recovery case.
- A concrete failure case, and how the rule is verified.
- Unobserved behaviour marked as an inference or a proposal.

Motion guidance must leave a clear way to choose **no motion** when the animation does not help the task.

For a new sector, follow the gate in `consistent-web-ui/references/sector-program.md`: at least five private studies, five original direction briefs, one real project, and an evaluation set.

Never present a catalogue target or a design proposal as finished, production-proven work.
