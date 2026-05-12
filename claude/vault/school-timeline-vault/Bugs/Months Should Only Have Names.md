---
title: Months Should Only Have Names
tags:
  - bug
  - project/school-timeline
status: open
priority: low
---

# Bug: Months Should Only Have Names

## Description

Month section headers may display more than just the month name — for example, a subtitle or extra label — when they should show only the month title.

## Expected behaviour

Each month header in the timeline shows only the month name (e.g. `🍂 ספטמבר`), with no additional subtitle or secondary text.

## Current behaviour

*(To be investigated — reproduce by opening `index.html` and inspecting the `.month-header` elements.)*

## Fix approach

- Review the `renderGrade` function's month header template in `index.html`
- Ensure only `monthData.monthTitle || defaultTitle` is rendered inside `.month-title`, with no other child elements

## See also

- [[../Project/Architecture]]
- [[../Project/Roadmap]]
