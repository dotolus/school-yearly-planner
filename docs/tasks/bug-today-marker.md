# Bug: Today Marker Should Track Current Date

## Problem

The today marker is hardcoded to `2024-12-09` in two places in `index.html`:

1. **Line 323** — static Hebrew text in the header badge:
   ```html
   <span class="today-text">היום: 9 בדצמבר, 2024</span>
   ```

2. **Line 348** — hardcoded `Date` object used nowhere functionally (leftover):
   ```js
   const currentDate = new Date('2024-12-09');
   ```

3. **Line 358** — `calculateTodayMarkerPosition()` searches the DOM for a literal date string:
   ```js
   return dateText.includes('9 בדצמבר, 2024');
   ```
   If no item has that exact string, it falls back to the December section header.

---

## Tasks

- [ ] **Task 1 — Replace hardcoded date with `new Date()`**  
  Change `const currentDate = new Date('2024-12-09')` to `const currentDate = new Date()`.  
  This variable is currently unused by `calculateTodayMarkerPosition` — the next tasks will wire it up.

- [ ] **Task 2 — Generate the Hebrew search string dynamically**  
  `calculateTodayMarkerPosition` currently searches for the literal string `'9 בדצמבר, 2024'`.  
  Replace it with a string built from `currentDate` using `toLocaleDateString`:
  ```js
  const todayString = currentDate.toLocaleDateString('he-IL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
  });
  ```
  Then use `dateText.includes(todayString)` in the find. Verify the output format matches
  the `date` field format used in `data/reut-2025_2026-d4.js` (e.g. `'9 בדצמבר, 2024'`).

- [ ] **Task 3 — Update the fallback to use the current month**  
  The fallback currently always looks for `'דצמבר'` (December).  
  Replace it with the current month name derived from `currentDate`:
  ```js
  const currentMonthName = currentDate.toLocaleDateString('he-IL', { month: 'long' });
  // then search: title.textContent.includes(currentMonthName)
  ```

- [ ] **Task 4 — Update the header badge text dynamically**  
  Line 323 has a hardcoded Hebrew date string in the HTML.  
  Remove the static text and set it from JS after `currentDate` is defined:
  ```js
  document.querySelector('.today-text').textContent =
      'היום: ' + currentDate.toLocaleDateString('he-IL', {
          day: 'numeric', month: 'long', year: 'numeric'
      });
  ```

- [ ] **Task 5 — Verify date format matches data files**  
  Open `data/reut-2025_2026-d4.js` and confirm the `date` field format (e.g. `'9 בדצמבר, 2024'`)
  matches what `toLocaleDateString('he-IL', {...})` produces in the browser.  
  If they differ, adjust the `toLocaleDateString` options or normalize both sides.

- [ ] **Task 6 — Test in browser**  
  Open `index.html` and confirm:
  - The header badge shows today's actual date
  - The marker circle sits at or near today's date on the timeline
  - If today has no matching item, the marker falls back to the current month section
  - Resize the window — marker repositions correctly
  - Filter buttons — marker stays in place after filtering
