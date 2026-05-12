# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A static, single-file interactive timeline for a 4th-grade math class school year (Hebrew/RTL). Deployed via GitHub Pages at `https://dotolus.github.io/school-yearly-planner/`.

## Running locally

No build step. Open `index.html` directly in a browser. There are no dependencies, no package manager, and no server required.

## Architecture

Everything lives in a single `index.html`:

- **HTML** — timeline items are static markup, each a `.timeline-item` div with a `data-type` attribute (`lesson`, `assignment`, or `test`). Content is hardcoded in Hebrew.
- **CSS** — fully inline in `<style>`. Two-column alternating layout (odd children go right, even go left) collapses to single-column at ≤768px via media query. RTL is set at the `<html>` level (`dir="rtl" lang="he"`).
- **JS** — inline `<script>` at the bottom. Three main behaviors:
  1. `filterItems(type)` — toggles `.hidden` class on `.timeline-item` elements by `data-type`
  2. `calculateTodayMarkerPosition()` — positions the floating "today" circle by finding a matching date string in the DOM, then computing its offset relative to `.timeline`
  3. Click-to-expand — toggles `.expanded` on `.item-details` elements (max-height transition)

## Key implementation details

- The "today" date is hardcoded as `new Date('2024-12-09')` in the script and also appears as literal text in `.today-text`. Both must be updated together when changing the current date.
- The today marker is positioned by searching for a DOM element whose `.item-date` text contains `'9 בדצמבר, 2024'`. If no match is found it falls back to the December section header. This coupling between the JS and the HTML content means date changes require updating both the search string and the hardcoded date.
- Timeline items inside `.item-details` are expandable only when they contain that child element — items without `.item-details` silently ignore clicks.

## Other branches

- `Basic` — an earlier, simpler version
- `simple1` — another variant
