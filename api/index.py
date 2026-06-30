import os
import pathlib
from typing import Optional

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from mangum import Mangum
from supabase import create_client, Client

PUBLIC_DIR = pathlib.Path(__file__).parent.parent / "public"

app = FastAPI(title="School Timeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _sb() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])


def _sb_admin() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])


def _require_auth(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    try:
        user = _sb().auth.get_user(token)
        return user.user.email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def _assert_editor(email: str, grade_key: str) -> str:
    """Verifies user is an editor for the grade. Returns grade_id."""
    sb = _sb_admin()
    grade = sb.table("grades").select("id").eq("grade_key", grade_key).maybe_single().execute()
    if not grade.data:
        raise HTTPException(status_code=404, detail="Grade not found")
    grade_id = grade.data["id"]
    editor = (
        sb.table("grade_editors")
        .select("user_email")
        .eq("grade_id", grade_id)
        .eq("user_email", email)
        .maybe_single()
        .execute()
    )
    if not editor.data:
        raise HTTPException(status_code=403, detail="Not an editor for this grade")
    return grade_id


# ── Config ────────────────────────────────────────────────────────────────────

@app.get("/api/config")
def get_config():
    return {
        "supabase_url": os.environ["SUPABASE_URL"],
        "supabase_anon_key": os.environ["SUPABASE_ANON_KEY"],
    }


# ── Public read ───────────────────────────────────────────────────────────────

@app.get("/api/grades")
def list_grades():
    result = _sb().table("grades").select("grade_key, title, subtitle, school_year").order("grade_key").execute()
    return result.data


@app.get("/api/grades/{grade_key}")
def get_grade(grade_key: str):
    sb = _sb()
    g = sb.table("grades").select("*").eq("grade_key", grade_key).maybe_single().execute()
    if not g.data:
        raise HTTPException(status_code=404, detail="Grade not found")
    grade = g.data

    months = (
        sb.table("months")
        .select("id, month_title, month_order")
        .eq("grade_id", grade["id"])
        .order("month_order")
        .execute()
    ).data

    items_raw = []
    if months:
        items_raw = (
            sb.table("timeline_items")
            .select("*")
            .in_("month_id", [m["id"] for m in months])
            .order("item_order")
            .execute()
        ).data

    items_by_month: dict = {}
    for item in items_raw:
        items_by_month.setdefault(item["month_id"], []).append({
            "type": item["type"],
            "title": item["title"],
            "date": item["date_text"],
            "description": item.get("description") or "",
            "details": item.get("details"),
            "icon": item.get("icon"),
            "style": item.get("style"),
        })

    return {
        "config": {"title": grade["title"], "subtitle": grade.get("subtitle") or ""},
        "months": [
            {"monthTitle": m["month_title"], "items": items_by_month.get(m["id"], [])}
            for m in months
        ],
    }


# ── Admin: my grades ──────────────────────────────────────────────────────────

@app.get("/api/admin/my-grades")
def my_grades(authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    rows = (
        _sb_admin()
        .table("grade_editors")
        .select("grades(grade_key, title, subtitle, school_year)")
        .eq("user_email", email)
        .execute()
    ).data
    return [r["grades"] for r in rows if r.get("grades")]


@app.get("/api/admin/grades/{grade_key}")
def get_grade_admin(grade_key: str, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    _assert_editor(email, grade_key)
    sb = _sb_admin()

    grade = sb.table("grades").select("*").eq("grade_key", grade_key).single().execute().data
    months = (
        sb.table("months")
        .select("*")
        .eq("grade_id", grade["id"])
        .order("month_order")
        .execute()
    ).data

    items_raw = []
    if months:
        items_raw = (
            sb.table("timeline_items")
            .select("*")
            .in_("month_id", [m["id"] for m in months])
            .order("item_order")
            .execute()
        ).data

    items_by_month: dict = {}
    for item in items_raw:
        items_by_month.setdefault(item["month_id"], []).append(item)

    return {**grade, "months": [{**m, "items": items_by_month.get(m["id"], [])} for m in months]}


# ── Admin: grade CRUD ─────────────────────────────────────────────────────────

@app.post("/api/admin/grades")
def create_grade(body: dict, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    sb = _sb_admin()
    grade = sb.table("grades").insert({
        "grade_key": body["grade_key"],
        "title": body["title"],
        "subtitle": body.get("subtitle"),
        "school_year": body["school_year"],
    }).execute().data[0]
    sb.table("grade_editors").insert({"grade_id": grade["id"], "user_email": email}).execute()
    return grade


@app.put("/api/admin/grades/{grade_key}")
def update_grade(grade_key: str, body: dict, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    _assert_editor(email, grade_key)
    return (
        _sb_admin()
        .table("grades")
        .update({"title": body["title"], "subtitle": body.get("subtitle")})
        .eq("grade_key", grade_key)
        .execute()
        .data[0]
    )


# ── Admin: month CRUD ─────────────────────────────────────────────────────────

@app.post("/api/admin/grades/{grade_key}/months")
def add_month(grade_key: str, body: dict, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    grade_id = _assert_editor(email, grade_key)
    return (
        _sb_admin()
        .table("months")
        .insert({"grade_id": grade_id, "month_title": body["month_title"], "month_order": body["month_order"]})
        .execute()
        .data[0]
    )


# ── Admin: item CRUD ──────────────────────────────────────────────────────────

@app.post("/api/admin/grades/{grade_key}/items")
def add_item(grade_key: str, body: dict, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    _assert_editor(email, grade_key)
    return (
        _sb_admin()
        .table("timeline_items")
        .insert({
            "month_id":    body["month_id"],
            "type":        body["type"],
            "title":       body["title"],
            "date_text":   body["date_text"],
            "date_actual": body.get("date_actual"),
            "description": body.get("description"),
            "details":     body.get("details"),
            "icon":        body.get("icon"),
            "style":       body.get("style"),
            "item_order":  body.get("item_order", 0),
        })
        .execute()
        .data[0]
    )


def _get_grade_key_for_item(sb, item_id: str) -> str:
    item = sb.table("timeline_items").select("month_id").eq("id", item_id).single().execute().data
    month = sb.table("months").select("grade_id").eq("id", item["month_id"]).single().execute().data
    grade = sb.table("grades").select("grade_key").eq("id", month["grade_id"]).single().execute().data
    return grade["grade_key"]


@app.put("/api/admin/items/{item_id}")
def update_item(item_id: str, body: dict, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    sb = _sb_admin()
    _assert_editor(email, _get_grade_key_for_item(sb, item_id))
    fields = {k: v for k, v in {
        "type":        body.get("type"),
        "title":       body.get("title"),
        "date_text":   body.get("date_text"),
        "date_actual": body.get("date_actual"),
        "description": body.get("description"),
        "details":     body.get("details"),
        "icon":        body.get("icon"),
        "style":       body.get("style"),
        "item_order":  body.get("item_order"),
    }.items() if v is not None}
    return sb.table("timeline_items").update(fields).eq("id", item_id).execute().data[0]


@app.delete("/api/admin/items/{item_id}")
def delete_item(item_id: str, authorization: Optional[str] = Header(None)):
    email = _require_auth(authorization)
    sb = _sb_admin()
    _assert_editor(email, _get_grade_key_for_item(sb, item_id))
    sb.table("timeline_items").delete().eq("id", item_id).execute()
    return {"deleted": item_id}


# ── Static pages ──────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return FileResponse(PUBLIC_DIR / "index.html")


@app.get("/grade/{grade_key}")
def grade_page(grade_key: str):
    return FileResponse(PUBLIC_DIR / "grade.html")


@app.get("/admin")
def admin_page():
    return FileResponse(PUBLIC_DIR / "admin.html")


handler = Mangum(app)
