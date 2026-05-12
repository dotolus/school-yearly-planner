---
title: Architecture
tags:
  - project/school-timeline
  - architecture
  - technical
---

# Architecture

## File layout

```
index.html                  — HTML shell + CSS + mechanics JS (no content)
data/
  reut-2025_2026-d4.js      — Grade 4 data (self-registers into window.gradesData)
  reut-2025_2026-d5.js      — Grade 5 stub
claude/
  CLAUDE.md                 — Claude Code guidance file
  vault/                    — This Obsidian vault
```

## How data loading works

Each `data/*.js` file self-registers into a shared global:

```js
window.gradesData = window.gradesData || {};
window.gradesData['reut-2025_2026-d4'] = { config: {...}, months: [...] };
```

`index.html` loads them as `<script>` tags before the main script block — works on `file://` with no server.

## Rendering pipeline

```
page load
  → read ?grade param (default: first key in window.gradesData)
  → renderGrade(gradeKey)       sets header text + builds all month sections
  → initEventListeners()        wires click-to-expand, hover, filter buttons
  → calculateTodayMarkerPosition()  positions the floating "today" circle
```

## Month skeleton

`SCHOOL_YEAR_MONTHS` is a fixed array of Sep–Jun labels. `renderGrade` always iterates all 10 months, using grade data for items and falling back to defaults when a month has no events defined.

## CSS layout

- Two-column alternating layout: odd children go right, even go left
- Collapses to single-column at ≤768px via media query
- RTL set at `<html>` level: `dir="rtl" lang="he"`
- Filter buttons toggle `.hidden` class on `.timeline-item` elements by `data-type`

## Known coupling

> [!warning] Today marker coupling
> `calculateTodayMarkerPosition()` searches DOM text for a specific Hebrew date string (e.g. `'9 בדצמבר, 2024'`). The date is also hardcoded as `new Date('2024-12-09')`. Both must be updated together. See [[../Bugs/Today Marker - Current Day]].

## See also

- [[Overview]] — what the project does
- [[../Features/Separate Mechanics from Data]] — how data was split from markup
