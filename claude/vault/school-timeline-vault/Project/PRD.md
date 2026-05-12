---
title: PRD – Product Requirements
tags:
  - project/school-timeline
  - planning
  - prd
status: draft
---

# Product Requirements Document

## Goal

A visual, interactive timeline that lets a teacher or student see the full academic year (September–June) at a glance — lessons, assignments, and tests — organized by month.

## Users

- **Primary:** Teacher managing a math class (Hebrew-speaking)
- **Secondary:** Students and parents viewing the schedule

## Core requirements

- [ ] Show all months September–June, even when no events are defined
- [ ] Each event has a type (lesson, assignment, test), title, date, and description
- [ ] Events can be expanded to reveal extra detail
- [ ] Filter events by type (all / lessons / assignments / tests)
- [ ] A "today" marker visually indicates the current position in the timeline
- [ ] Supports multiple grades — each grade is a shareable URL

## Non-requirements

- No login or authentication
- No database — all data is static files
- No server required — runs from `file://`

## Content management

- Add item: append to the relevant month's `items` array in the grade's `.js` file
- Remove item: delete the object
- Add grade: create `data/<school>-<years>-<grade>.js` + one `<script>` tag in `index.html`

## See also

- [[Overview]]
- [[Roadmap]]
