---
title: UI Style Rules
tags:
  - rules
  - ui
  - style
  - project/school-timeline
---

# UI Style Rules

## Layout

- Two-column alternating timeline: odd items go right, even items go left
- Collapses to single-column on screens ≤768px
- RTL direction set globally (`dir="rtl"` on `<html>`)

## Language

- All user-facing text is in Hebrew
- Dates in the data files should use the Hebrew locale format (e.g. `'9 בדצמבר, 2024'`) to match the today-marker search string

## Item types and colours

Each type has a distinct colour defined in CSS:

| Type | Class | Meaning |
|---|---|---|
| `lesson` | `.lesson` | Regular class activity |
| `assignment` | `.assignment` | Homework or project |
| `test` | `.test` | Exam or quiz |

Do not add new types without also adding the corresponding CSS class and updating the default-icon map in `renderGrade`.

## Icons

- Default icons: `lesson` → 📚, `assignment` → ✏️, `test` → 🎯
- Override per item with the `icon` field in the data file
- Special occasions (e.g. end-of-year party) use `icon: '🎉'`

## Spacing and style overrides

- Avoid inline `style` on items unless truly necessary (e.g. extra bottom margin before a section break)
- Use the `style` field in data for one-off spacing adjustments, not for colour or typography changes — those belong in CSS
