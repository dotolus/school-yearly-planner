# Task: Migrate to Python + Supabase + Vercel

## Goal
Move from a static client-side SPA (GitHub Pages) to a Python/FastAPI backend with Supabase DB, deployed on Vercel. Support multiple independent grades (A1, A2, B3, B7, B1…) each with their own data, editors, and URLs.

---

## New Architecture

```
Browser
  ├── GET /grade/A1        → public/grade.html (vanilla JS fetches /api/grades/A1)
  ├── GET /admin           → public/admin.html (Supabase Auth login + grade editor forms)
  └── GET /api/grades/A1   → api/index.py (FastAPI, reads Supabase)

Supabase
  ├── PostgreSQL DB (grades, months, timeline_items, grade_editors)
  ├── Supabase Auth (email/password for editors)
  └── Row Level Security (editors only modify their own grades)

Vercel
  ├── /api/* → Python FastAPI serverless function
  └── /public/* → static files (HTML, CSS, JS)
```

---

## New File Structure

```
school-timeline/
├── api/
│   └── index.py              # FastAPI app — all API endpoints
├── public/
│   ├── index.html            # Home: grade selector list
│   ├── grade.html            # Timeline viewer (adapted from current index.html)
│   └── admin.html            # Protected admin panel (add/edit/delete items)
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
├── lib/
│   └── db.py                 # Supabase client + shared DB helpers
├── scripts/
│   └── seed.py               # One-time data migration from JS files to DB
├── requirements.txt
└── vercel.json
```

---

## Database Schema

```sql
CREATE TABLE grades (
  id           uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  grade_key    text UNIQUE NOT NULL,   -- e.g. 'A1', 'B3'
  title        text NOT NULL,
  subtitle     text,
  school_year  text NOT NULL           -- e.g. '2025-2026'
);

CREATE TABLE months (
  id           uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  grade_id     uuid REFERENCES grades(id) ON DELETE CASCADE,
  month_title  text NOT NULL,
  month_order  int  NOT NULL,          -- 0=Sep, 1=Oct, … 9=Jun
  UNIQUE(grade_id, month_order)
);

CREATE TABLE timeline_items (
  id           uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  month_id     uuid REFERENCES months(id) ON DELETE CASCADE,
  type         text NOT NULL CHECK (type IN ('lesson', 'assignment', 'test')),
  title        text NOT NULL,
  date_text    text NOT NULL,          -- Hebrew display string e.g. "3 בספטמבר, 2024"
  date_actual  date,                   -- ISO date for today-marker positioning
  description  text,
  details      text,                   -- HTML for expandable section
  icon         text,
  style        text,
  item_order   int NOT NULL DEFAULT 0
);

CREATE TABLE grade_editors (
  grade_id     uuid REFERENCES grades(id) ON DELETE CASCADE,
  user_email   text NOT NULL,          -- matches Supabase Auth user email
  PRIMARY KEY (grade_id, user_email)
);

-- RLS: public read, editors-only write
-- (see supabase/migrations/001_initial_schema.sql for full policies)
```

---

## API Endpoints

**Public (no auth):**
- `GET /api/grades` — list all grades
- `GET /api/grades/{grade_key}` — full grade data (same shape as current JS data objects)

**Protected (Supabase JWT):**
- `GET  /api/admin/my-grades` — grades the logged-in editor can manage
- `POST /api/admin/grades` — create grade
- `PUT  /api/admin/grades/{grade_key}` — update grade config
- `POST /api/admin/grades/{grade_key}/items` — add item
- `PUT  /api/admin/items/{item_id}` — update item
- `DELETE /api/admin/items/{item_id}` — delete item

---

## Implementation Checklist

- [ ] 0. This task file created ✓
- [ ] 1. Supabase project setup — create project, run `001_initial_schema.sql`
- [ ] 2. `lib/db.py` — Supabase client wrapper
- [ ] 3. `api/index.py` — FastAPI app with public read endpoints
- [ ] 4. `vercel.json` + `requirements.txt` — deploy to Vercel, verify `/api/grades` works
- [ ] 5. `public/grade.html` — adapt `index.html` to fetch from API (remove data script tags, add fetch on load)
- [ ] 6. `public/index.html` — grade selector (fetches `/api/grades`, renders cards)
- [ ] 7. Protected admin endpoints in `api/index.py`
- [ ] 8. `public/admin.html` — admin panel with Supabase Auth login + item CRUD forms
- [ ] 9. `scripts/seed.py` — migrate Grade 4 data from `data/reut-2025_2026-d4.js` into DB
- [ ] 10. Test: view grade A1, login as editor, add/edit/delete item, verify RLS blocks cross-grade edits

---

## Vercel Config

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "public/**",    "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/(.*)",   "dest": "api/index.py" },
    { "src": "/grade/(.*)", "dest": "/public/grade.html" },
    { "src": "/admin",      "dest": "/public/admin.html" },
    { "src": "/(.*)",       "dest": "/public/$1" }
  ]
}
```

---

## Notes
- Keep `data/*.js` files during migration; remove after seed script runs successfully
- Frontend rendering logic in `grade.html` stays almost unchanged — only the data loading changes from script tags to `fetch()`
- Supabase dashboard can be used to manually add grade editors (`grade_editors` table)
