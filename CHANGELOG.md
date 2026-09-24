# Changelog

## 0.6.0 - 2026-09-24

### Layers, dialogs, dropdowns and toasts

- **Only the top layer moves and responds.**
  - While a dialog, drawer or full-screen menu is open, the page behind does not scroll and does not react to clicks, hover or Tab.
  - Overlays and sticky bars are opaque, so text beneath never mixes with theirs.
  - Clicks never pass through an overlay.
- **Controls in a row share one height, radius and text size.** Buttons side by side differ only by variant, and a hover never adds an underline or border the others lack.
- **Dropdowns match the fields.** A closed select looks like the other fields. The open list uses the theme's surface, border, radius and type, through `appearance: base-select` with the native list as the fallback, or through the project's own component.
- **Dialogs fit their content:**
  - three sizes, and media capped at about a third of the screen;
  - only the body scrolls; the header and actions stay visible;
  - a quiet 36 px close button;
  - first focus on the title, the first field, or Cancel in destructive confirmations;
  - backdrop clicks close content dialogs only.
- **Toasts wear the brand:**
  - one position, at most three at once, above dialogs;
  - success and info leave after about 5 seconds and pause on hover or focus;
  - errors stay until closed.
- **New files:**
  - `references/overlays-and-controls.md`;
  - `assets/templates/controls.html`, `dialog.html` and `toast.html`, each checked in a real browser;
  - `scripts/ui_check.js`, which measures rows of controls and open overlays on the rendered page;
  - `--control-height` tokens, design contract items DC-37 and DC-38, and the matching audit checks.

### Instructions and help (0.5.1, not released separately)

- **Global AI instructions stay untouched.** The skill never creates or edits user-level or global instruction or memory files for any assistant, such as `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, editor rules or saved memory. Decisions live in project files:
  - the design contract;
  - at most a short pointer to it in the project's own instruction file, only if that file already exists or the owner agrees.
- **Help comes in two forms, and both are rare.** The density rule now covers visible hints as well as (i):
  - a visible hint is only for limits needed while typing and for serious, hard-to-undo consequences;
  - nice-to-know detail goes behind an (i).

  Found by the new eval, where every field got a hint.
- **New eval 8 (outside ecommerce):** the Settings page of a team time-tracking app. It also checks that existing behaviour survives and that no global AI instruction file changes.

### Checks

- 48 tests pass on Python 3.8 to 3.14.

## 0.5.0 - 2026-09-24

### Fixes from the first evaluation round

- **Shared parts.** A request that names one page no longer changes other pages silently. When the change sits in a layout, header, footer, global CSS rule or shared component, the skill does one of two things:
  - names the other pages and asks first;
  - or keeps the change on the named page and lists the rest.
- **Keyboard without fake tab stops.** Hover effects on links and buttons also run on `:focus-visible`. Non-interactive decoration never gets a tab stop.
- **Layer map in audits.** Audits list:
  - what must sit above what, and the stacking contexts;
  - every element that now covers another, checked on a real render.

### Info (i) help and UI text

- **New `references/help-and-ui-text.md`:**
  - **when an info (i) is allowed:** only where an item's purpose or effect cannot be inferred and a wrong guess costs something, and never on every card;
  - **what the text says** for each element type: page, button, toggle, field, column or metric, status, feature, chart;
  - rules for length, truth, placement and density;
  - labels, errors, empty states, confirmations, forms, numbers and dates, and page titles.
- **New `assets/templates/info-toggletip.html`:** an accessible (i) component, tested in a real browser.
  - Opens on click, tap, Enter and Space; closes on Escape or an outside click.
  - One panel open at a time, placed next to its button and kept in the viewport, with right-to-left support.
  - Fallbacks for no JavaScript and for browsers without popovers.
- **Contract and templates:** a new DC-36 (info help), a fuller DC-20 (content tone), and a help section in the page spec and the audit template.

### Motion

- **A motion floor and ceiling.**
  - Floor: every change the user causes gets brief feedback.
  - Ceiling: nothing moves on its own except real progress and at most one attention moment per view.
- A ten-second idle test.
- Anything that moves on its own has a visible pause control and pauses while the pointer or keyboard focus is inside it.

### Pages and visual system

- **Home page (C01):** a simple first version with plain text on how buying works, a short FAQ with owner placeholders, and at most one optional information card.
- **Design contract reference:** notes on dark theme depth, font loading and link underlines.

### Package

- `agents/openai.yaml` keeps only documented fields.
- The MIT license holder is set.
- **Claude Code plugin marketplace file:** install with `/plugin marketplace add smileemir/consistent-web-ui`.
- **GitHub Actions workflow:** runs the tests on Python 3.10, 3.12 and 3.14. The suite also passes on 3.8.

### Evaluations

- Evals 1, 2, 3 and 6 are reworded from the graders' feedback.
- New eval 7 (admin info help), with a store-admin fixture.
- 44 tests, including the toggletip markup, unique contract IDs, link checks and the marketplace entry.

## 0.4.0 - 2026-09-24

### Tools

- **`scripts/frontend_index.py` rewritten.**
  - Route detection now covers Next.js app and pages routers, Nuxt, Astro, SvelteKit, Remix / React Router / TanStack file routes, React Router, Vue Router and Angular configs, Shopify templates, WordPress and WooCommerce templates, Rails, Laravel Blade, ASP.NET Razor and plain HTML.
  - The scan skips generated, vendored, hidden and backend folders without entering them.
  - It now reports:
    - theme sources and token gaps (used but undefined, defined but unused, defined in several files);
    - raw colours and near-duplicates, and utility arbitrary values;
    - the spread of values and the share already on tokens, for spacing, font size, radius, z-index and durations;
    - looping animations, `will-change`, reduced-motion guards, locales and the detected stack.
  - The output is a compact text summary by default, `--json` on request.
- **New `scripts/contrast_check.py`.** A dependency-free WCAG 2.x contrast checker for design tokens in every theme.
  - Reads `:root`, `@theme`, `[data-theme]`, `.dark`, `.theme-*`, `[data-bs-theme]` and `prefers-color-scheme` blocks, and resolves `var()` chains.
  - Understands hex, rgb, hsl, hwb, lab, lch, oklab, oklch, named colours, `light-dark()`, `color-mix()` and bare channel values.
  - Composites translucent colours.
  - Pairs come from a file or are guessed from token names with `--pairs auto`.
- **Tests.** 40 tests (`python3 -m unittest discover -s tests`). The tools were also checked against real open-source storefront and component-library code.

### Templates (`assets/templates/`)

- Audit report, design contract, page spec, motion record and asset register.
- A starter theme file with semantic roles, light and dark themes, an ordered layer (z-index) scale, motion roles, reduced motion and visible focus. It passes its own 24 contrast pairs in all three theme variants.

### Skill

- **Lanes.** SKILL.md now matches effort to the request: scoped fix, audit first, new build or blueprint. A one-component fix no longer triggers a full-site audit.
- **Token thrift** is an explicit rule.
- **Real-render verification.** A step-by-step procedure: viewports, zoom, themes, longest locale, keyboard, reduced motion, before/after screenshots, honest "unverified".
- **Framework mapping.** New `references/framework-mapping.md`: where the single theme source lives in plain CSS/Sass, Tailwind v3/v4, shadcn/ui, Bootstrap 5.3, MUI, Chakra, CSS-in-JS, Angular Material, Vue/Svelte/Astro, Shopify and WordPress.
- **Motion split.** The 30 KB motion file is split into `motion-core.md` (rules for every sector) and three ecommerce files: browse M01–M19, buy M20–M36, after purchase M37–M49. A motion task now reads about half as much. All 49 records are unchanged.
- **New motion rules:**
  - at most one looping animation visible at a time;
  - trust and payment logos stay static;
  - `will-change` only while animating;
  - no novelty presets;
  - WCAG 2.2.2 pause control for auto-moving content.
- **New layout rules:** an ordered layer scale, empty shelves are hidden, the missing card-to-motion links are added (K15 → M10, K22 → M07), and outcome measurement guidance.
- **Directions.** The index is slimmed. Each brief's customer job, brand language and failure test now live in its detailed blueprint. A contrast note was added: the directions' dividers are decorative only.
- **Sector gate.** Five private studies + five direction briefs + one real project + an evaluation set. Five full prototypes are no longer required. Sector order is ecommerce → marketplace → SaaS. The catalogue targets moved to [ROADMAP.md](ROADMAP.md).
- **Removed.** `references/sample-audit.md` was folded into the audit template.
- **Frontmatter.** Added `license: MIT` and a version to SKILL.md, and a trigger-focused description.
- **License file inside the skill folder** (`LICENSE.txt`), so a copied or uploaded folder keeps its license.

## 0.3.0 - 2026-09-23

- Five detailed ecommerce direction blueprints (D1–D5) mapping every customer and operator route.
- An ecommerce asset register, a phone and tablet interaction specification, and transaction traces T01–T12.
- A skill icon.

## 0.2.0 - 2026-09-23

- Renamed to `consistent-web-ui`.
- Owner decisions added:
  - list toolbar with visible-column choice;
  - optional information cards (X, Minimize to an in-place `!` box, Remind me in a week, Never show again);
  - same-page actions without a full reload;
  - a project-level design contract saved as project memory.
- An illustrative audit report and example tasks.

## 0.1.0 - 2026-09-23

- First skill: audit-first workflow, frontend-only boundary, design contract, and ecommerce pages, components, motion and direction briefs.
