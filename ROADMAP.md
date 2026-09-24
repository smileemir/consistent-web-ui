# Roadmap

What comes next, in order. Nothing here is shipped until it appears in [CHANGELOG.md](CHANGELOG.md).

## Sectors

| Order | Sector | Status |
| --- | --- | --- |
| 01 | Ecommerce | Guidance written (routes, components, assets, responsive rules, transaction traces, motion, five direction briefs). Waiting for its real-project validation. |
| 02 | Marketplace | Next: two-sided discovery, seller identity, listings, trust, moderation, disputes |
| 03 | SaaS | Evaluation, onboarding, workspace roles, subscription, operational UI |
| Later | Blog and publishing, education, AI/chat products, finance, services and booking, and others | Chosen with demand research after the first three |

A sector counts as validated only when it passes the gate in `consistent-web-ui/references/sector-program.md`:

- private research on at least five real products;
- five original direction briefs;
- one real project done end to end with the guidance;
- an evaluation set that shows the guidance helps without wasting tokens.

## Quality work

- Keep the evaluation suite in `evals/` growing with every sector and every reported failure.
- Publish real before/after examples produced with the skill in `examples/`.
- Optimise the skill description for triggering once the evaluation set is stable.

## Long-term catalogue targets

These are **editorial targets, not current inventory**:

| Target | Amount |
| --- | --- |
| Visual approaches | 85 |
| Validated colour systems | 210 |
| Readable font pairings | 80 |
| Chart patterns | 36 |
| Framework integration guides | 20 |
| Conditional design rules | 210 |

A record counts only when it has all of the following:

- a real use case and a counterexample;
- an accessibility check;
- variants for every supported theme;
- a reviewed original example.

Specific requirements by type:

- **Palette:** text and control contrast verified in the pairs it is actually used in.
- **Font pairing:** legible in long-form reading and in UI, across locales.
- **Chart:** a meaningful scale, units, a source and an accessible table.
- **Framework guide:** a tested adaptation, not a new name on the same CSS.
- **Rule:** written as `context → choice → evidence → failure mode → test`.

One excellent, verified record is worth more than ten unverified ones.
