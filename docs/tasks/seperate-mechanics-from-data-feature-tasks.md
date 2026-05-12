# Feature: Separate Mechanics from Data + Multi-Grade Support

## Goal
Move all timeline content into per-class data files and support multiple grades via URL parameter (`?grade=reut-2025_2026-d4`).

## File naming convention
`data/<school>-<startYear_endYear>-<gradeCode>.js`  
Example: `data/reut-2025_2026-d4.js`

---

## Tasks

- [x] **Task 1** — Create `data/reut-2025_2026-d4.js`  
  Register key `'reut-2025_2026-d4'` into `window.gradesData`. Populate all 10 months and every item extracted from the current hardcoded HTML in `index.html`.

- [x] **Task 1b** — Create `data/reut-2025_2026-d5.js`  
  Stub file — config only (title, subtitle), empty `months: []`. Starting point for grade 5 content.

- [x] **Task 2** — Load class files in `index.html`  
  Add before the main script block:
  ```html
  <script src="data/reut-2025_2026-d4.js"></script>
  <script src="data/reut-2025_2026-d5.js"></script>
  ```

- [x] **Task 3** — Write `renderGrade(gradeKey)` in `index.html`  
  Reads `window.gradesData[gradeKey]`, sets header title + subtitle, and builds all `.timeline-item` HTML inside `#timeline`.

- [x] **Task 4** — Wrap event listeners in `initEventListeners()`  
  Move click-to-expand and hover handlers into a function called after `renderGrade()`.

- [x] **Task 5** — Wire up the entry point  
  On page load: read `?grade` URL param (default to first key in `window.gradesData`), call `renderGrade()`, then `initEventListeners()`.

- [x] **Task 6** — Remove hardcoded HTML items from `index.html`  
  Delete all `<div class="month-section">...</div>` blocks. Remove hardcoded Hebrew text from `.header h1` and `.header p`.

---

## Per-class file template

```js
// data/<school>-<startYear_endYear>-<gradeCode>.js
window.gradesData = window.gradesData || {};
window.gradesData['reut-2025_2026-d4'] = {
  config: {
    title: '...',
    subtitle: '...'
  },
  months: [
    {
      monthTitle: '🍂 ספטמבר - ...',
      items: [
        {
          type: 'lesson',      // 'lesson' | 'assignment' | 'test'
          title: '...',
          date: '...',
          description: '...',
          details: '...',      // optional — expandable section (HTML string)
          icon: '🎉',         // optional — overrides default icon
          style: '...'        // optional — inline style on the item wrapper
        }
      ]
    }
  ]
};
```

Default icons: `lesson` → 📚, `assignment` → ✏️, `test` → 🎯

---

## How to work with classes

- **Add item:** append an object to the relevant month's `items` array in the class's `.js` file
- **Remove item:** delete its object
- **Edit item:** change field values
- **Add a new class:** create `data/<school>-<years>-<grade>.js` + add one `<script src="...">` line in `index.html`
- **Open in browser:** `index.html?grade=reut-2025_2026-d4`
