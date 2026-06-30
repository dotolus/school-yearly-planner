#!/usr/bin/env python3
"""
One-time seed: imports data/reut-2025_2026-d4.js into Supabase.

Setup:
  pip install supabase json5 python-dotenv
  cp .env.example .env   # fill in your keys

Usage:
  python scripts/seed.py
"""
import json5
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

load_dotenv(Path(__file__).parent.parent / ".env")

sb = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

DATA_FILE = Path(__file__).parent.parent / "data" / "reut-2025_2026-d4.js"

with open(DATA_FILE, encoding="utf-8") as f:
    content = f.read()

match = re.search(
    r"window\.gradesData\['([^']+)'\]\s*=\s*(\{[\s\S]+\})\s*;?\s*$",
    content,
)
if not match:
    raise ValueError("Could not parse grade key or data object from JS file")

grade_key  = match.group(1)
grade_data = json5.loads(match.group(2))

print(f"Seeding grade: {grade_key}")

# Upsert grade row
grade_row = sb.table("grades").upsert(
    {
        "grade_key":   grade_key,
        "title":       grade_data["config"]["title"],
        "subtitle":    grade_data["config"].get("subtitle", ""),
        "school_year": "2024-2025",
    },
    on_conflict="grade_key",
).execute().data[0]

grade_id = grade_row["id"]
print(f"  Grade ID: {grade_id}")

# Clear existing months + items (cascade) before re-seeding
existing_months = sb.table("months").select("id").eq("grade_id", grade_id).execute().data
for m in existing_months:
    sb.table("timeline_items").delete().eq("month_id", m["id"]).execute()
sb.table("months").delete().eq("grade_id", grade_id).execute()
print(f"  Cleared existing months")

# Insert months and items
for order, month in enumerate(grade_data["months"]):
    month_row = sb.table("months").insert(
        {
            "grade_id":    grade_id,
            "month_title": month["monthTitle"],
            "month_order": order,
        }
    ).execute().data[0]
    month_id = month_row["id"]

    items = month.get("items", [])
    for item_order, item in enumerate(items):
        sb.table("timeline_items").insert(
            {
                "month_id":    month_id,
                "type":        item["type"],
                "title":       item["title"],
                "date_text":   item["date"],
                "description": item.get("description", ""),
                "details":     item.get("details"),
                "icon":        item.get("icon"),
                "style":       item.get("style"),
                "item_order":  item_order,
            }
        ).execute()

    print(f"  Month {order:02d}: {month['monthTitle']} — {len(items)} items")

print("Seed complete!")
