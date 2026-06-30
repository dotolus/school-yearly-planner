---
title: Migrate to Python + Supabase + Vercel
tags:
  - task
  - project/school-timeline
  - backend
status: in-progress
date: 2026-06-30
---

# Task: Migrate to Python + Supabase + Vercel

## Goal

Move from a static client-side SPA (GitHub Pages) to a Python/FastAPI backend with Supabase DB, deployed on Vercel. Support multiple independent grades (A1, A2, B3, B7, B1…) each with their own data, editors, and URLs.

---

## Architecture

```
Browser
  ├── GET /grade/A1   → public/grade.html  (fetches /api/grades/A1)
  ├── GET /admin      → public/admin.html  (Supabase Auth + CRUD forms)
  └── GET /api/…      → api/index.py       (FastAPI + Mangum on Vercel)

Supabase
  ├── PostgreSQL (grades, months, timeline_items, grade_editors)
  ├── Supabase Auth (email/password for editors)
  └── Row Level Security (editors only modify their own grades)

Vercel
  └── All traffic → FastAPI serverless function
```

---

## Checklist

- [x] Create `api/index.py` — FastAPI with public read + protected admin endpoints
- [x] Create `public/grade.html` — timeline viewer fetching from API
- [x] Create `public/index.html` — grade selector home page
- [x] Create `public/admin.html` — admin panel with Supabase Auth login + item CRUD
- [x] Create `supabase/migrations/001_initial_schema.sql` — DB schema + RLS
- [x] Create `vercel.json` — routes all traffic to FastAPI
- [x] Create `requirements.txt` — fastapi, mangum, supabase, pydantic
- [x] Create `scripts/seed.py` — migrate Grade 4 JS data into Supabase
- [x] Create Supabase project (`jeliupgycfgxcgzvjdae`, eu-central-1)
- [x] Apply DB migration via `supabase db push`
- [ ] Add env vars to Vercel dashboard (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY)
- [ ] Push branch + merge to main → Vercel deploys
- [ ] Run `scripts/seed.py` to populate Grade 4 data
- [ ] Create first real grades (A1, A2, B3…) via admin panel

---

## Supabase Project

| Field | Value |
|-------|-------|
| Project ref | `jeliupgycfgxcgzvjdae` |
| Region | `eu-central-1` (Frankfurt) |
| Dashboard | https://supabase.com/dashboard/project/jeliupgycfgxcgzvjdae |

> [!important] Environment Variables
> Add these to Vercel → Project Settings → Environment Variables:
> - `SUPABASE_URL`
> - `SUPABASE_ANON_KEY`
> - `SUPABASE_SERVICE_ROLE_KEY`
> Values are in the local `.env` file (not committed).

---

## See also

- [[../Project/Architecture]]
- [[../Project/Roadmap]]
