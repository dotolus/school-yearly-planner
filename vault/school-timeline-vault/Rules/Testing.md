---
title: Testing Rules
tags:
  - rules
  - testing
  - project/school-timeline
---

# Testing Rules

> [!note]
> There is no automated test suite — the project is a static HTML file. Testing is manual.

## Manual testing checklist

When changing `index.html` or any `data/*.js` file, verify:

- [ ] Default load (`index.html` with no param) renders grade 4 with correct title and all 10 months
- [ ] `?grade=reut-2025_2026-d4` renders grade 4 correctly
- [ ] `?grade=reut-2025_2026-d5` renders grade 5 stub (months present, no items)
- [ ] Filter buttons (all / lessons / assignments / tests) show and hide items correctly
- [ ] Clicking an item with `details` expands it; clicking again collapses it
- [ ] Items without `details` do not break on click
- [ ] Today marker appears in the correct month
- [ ] Layout is correct at desktop width and at ≤768px (mobile)
- [ ] RTL text renders correctly in Hebrew

## Adding a new grade

After creating a new `data/*.js` file and adding its `<script>` tag, open `index.html?grade=<new-key>` and confirm the title, subtitle, and all months render.
