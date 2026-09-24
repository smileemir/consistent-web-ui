# Evaluations

These are realistic tasks that check whether the skill changes an assistant's behaviour the way it promises.

- Each eval runs in a fresh copy of a fictional fixture.
- It runs twice: once with the skill, and once with a baseline (no skill, or the previous version).
- Graders check every expectation against the written outputs and the project diff.

Results are kept in [results/](results/).

| Eval | What it checks |
| --- | --- |
| 1 audit-existing-store | **Audit-first lane:** one report, nothing changed, evidence labels, the planted issues found, a layer map that says which element covers which |
| 2 scoped-button-fix | **Scoped-fix lane:** the named button only, behaviour preserved, no audit, verification backed by renders |
| 3 new-digital-shop-home | **New-build lane:** one theme source, light/dark, contrast, nothing invented, digital delivery and FAQ with owner placeholders, sparing help, balanced motion |
| 4 refuse-fake-urgency | **Real data only:** fake timers, stock counts and ratings are declined, with honest alternatives |
| 5 tailwind-theme-plan | **Framework mapping:** Tailwind v4's own theme as the single source, conflicts found, plan only |
| 6 premium-trust-card-motion | **Motion rules:** one-shot, keyboard without fake tab stops, reduced motion, no decorative loops on trust marks, shared parts named before they change, promises confirmed |
| 7 admin-contextual-help | **Info (i) help:** only where needed, purpose-driven and short, facts from the project's own guide, nothing invented, one accessible component |
| 8 saas-settings-page | **Outside ecommerce:** one page of a team time-tracking app brought in line with the app's own design system; dark mode, labels, switch, help, honest delete, motion and layers; no global AI instruction file touched |

## Fixtures

- `fixtures/demo-store`: a static multi-page store with planted inconsistencies and a backend stub.
- `fixtures/tailwind-shop`: Next.js + Tailwind v4 with hardcoded values and a conflicting leftover config.
- `fixtures/empty-project`: an empty project for new-build tasks.
- `fixtures/store-admin`: a clean store admin with a staff guide; one setting is deliberately left undocumented.
- `fixtures/saas-app`: a team time-tracking app whose Settings page ignores the shared design system; includes product notes and a project `AGENTS.md`.

## Planned revisions

Evals 4 and 5 still use their first wording. The graders' suggestions for them wait for the next run:

- **Eval 4:**
  - check that nothing fake is added to any page, not only the shop page;
  - check what happens to the fake claims already live: left for the owner's decision, not silently removed;
  - anchor one expectation on a checkable fact, such as the sold-out saw that still has an enabled Buy button.
- **Eval 5:**
  - require the plan to explain why dark mode "barely works" (v4's default `dark:` follows the system setting; only the header has `dark:` classes; the body colour is hardcoded);
  - require full coverage of the arbitrary and palette classes, including `bg-cyan-600`;
  - require computed contrast ratios for the key pairs in both themes;
  - check that the proposed CSS really switches at runtime.
