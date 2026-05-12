---
title: Project Overview
tags:
  - project/school-timeline
  - overview
date: 2025-09-01
---

# School Yearly Planner

A year-long interactive timeline for a school pupil, covering multiple subjects across the academic year (September–June).

## What it is

- Static single-page app (`index.html`) — no build step, no server
- Hebrew/RTL UI (`dir="rtl"`, `lang="he"`)
- Deployed on GitHub Pages at `https://dotolus.github.io/school-yearly-planner/`
- Supports multiple grades, each with its own data file and configuration

## How it works

Each grade's timeline data lives in a separate JS file under `data/`:

| File | Grade |
|---|---|
| `data/reut-2025_2026-d4.js` | Grade 4, Reut school, 2025–2026 |
| `data/reut-2025_2026-d5.js` | Grade 5 stub |

The active grade is selected via URL parameter:  
`index.html?grade=reut-2025_2026-d4`

## Item types

| Type | Default icon | Usage |
|---|---|---|
| `lesson` | 📚 | Regular class activity |
| `assignment` | ✏️ | Homework or project |
| `test` | 🎯 | Exam or quiz |

## See also

- [[Architecture]] — how the code is structured
- [[PRD]] — product requirements
- [[Roadmap]] — planned work
