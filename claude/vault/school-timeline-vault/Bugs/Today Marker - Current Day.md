---
title: Today Marker – Should Track Current Day
tags:
  - bug
  - project/school-timeline
status: open
priority: medium
---

# Bug: Today Marker Should Be on Current Day

## Description

The "today" marker on the timeline does not automatically track the actual current date. It is hardcoded to a fixed date and will show the wrong position on any other day.

## Current behaviour

`calculateTodayMarkerPosition()` works by:
1. Creating a `Date` object hardcoded to `new Date('2024-12-09')`
2. Searching the DOM for an `.item-date` element whose text contains `'9 בדצמבר, 2024'`
3. If found, computing that element's offset and placing the marker circle there
4. If not found, falling back to the December section header

Both the hardcoded date and the Hebrew string must be kept in sync manually — a fragile coupling.

## Expected behaviour

The marker should automatically position itself on the actual current date (`new Date()`) without any manual update.

## Root cause

- `new Date('2024-12-09')` should be `new Date()` (or `Date.now()`)
- The search string `'9 בדצמבר, 2024'` should be generated dynamically from the current date, formatted to match the `date` field format used in the data files

> [!warning] Related coupling
> The `.today-text` element in the HTML also displays a hardcoded date string. It must be updated together with the JS. See [[../Project/Architecture#Known coupling]].

## Fix approach

1. Replace `new Date('2024-12-09')` with `new Date()`
2. Format the resulting date into Hebrew locale string (or match the format used in item `date` fields) to build the search string dynamically
3. Update `.today-text` content from JS at runtime instead of hardcoding it in HTML

## See also

- [[../Project/Architecture]]
- [[../Project/Roadmap]]
