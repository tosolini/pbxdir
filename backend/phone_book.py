# phone_book.py

import xmlrpc.client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# ── Config ────────────────────────────────────────────────────
ODOO_URL      = os.getenv("ODOO_URL", "https://your-odoo.example.com")
ODOO_DB       = os.getenv("ODOO_DB", "your_db")
ODOO_USER     = os.getenv("ODOO_USER", "api_user@example.com")
# Do not hardcode real secrets here; configure ODOO_PASSWORD via environment
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "")
app = FastAPI(title="Dialer Phone Book")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Odoo RPC helpers ──────────────────────────────────────────

@lru_cache()

def odoo_connect():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid    = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models

def odoo_search_read(model, domain, fields):
    uid, models = odoo_connect()
    return models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        model, "search_read",
        [domain],
        {"fields": fields, "context": {"active_test": True}}
    )

# ── Output schema ─────────────────────────────────────────────

class Contact(BaseModel):
    name:  str
    tel:   str
    short: Optional[str] = None
    role:  str
    mail:  Optional[str] = None
    notes: Optional[str] = None

# ── Helpers ───────────────────────────────────────────────────

def fmt(label: str, *parts: Optional[str]) -> str:
    """Build display name: 'Part1 – Part2 [Label]'"""
    base = " – ".join(p for p in parts if p)
    return f"{base} [{label}]"

def emit(name, tel, role, short=None, mail=None, notes=None) -> Optional[Contact]:
    if not tel:
        return None
    return Contact(name=name, tel=tel, short=short, role=role, mail=mail, notes=notes)

# ─────────────────────────────────────────────────────────────
# 1. EMPLOYEES
# ─────────────────────────────────────────────────────────────

def get_employee_contacts() -> list[Contact]:
    employees = odoo_search_read("hr.employee", [("active", "=", True)], [
        "name", "work_email", "private_email",
        "mobile_phone", "work_phone", "internal_number", "internal_number_2", "short_number",
        "phone", "mobile_personal",
        "relative_ids",
    ])

    results = []
    for e in employees:
        n    = e["name"]
        wm   = e.get("work_email")
        pm   = e.get("private_email")

        # Work numbers
        results += filter(None, [
            emit(fmt("Cellulare lavoro",  n), e.get("mobile_phone"), "Dipendenti", mail=wm),
            emit(fmt("Telefono lavoro",   n), e.get("work_phone"), "Dipendenti", mail=wm),
            emit(fmt("Interno",           n), e.get("internal_number"), "Dipendenti", short=e.get("short_number"), mail=wm),
            emit(fmt("Interno 2",         n), e.get("internal_number_2"), "Dipendenti",       mail=wm),
            # Private numbers
            emit(fmt("Tel. privato",      n), e.get("phone"),           "Dipendenti (Privato)", mail=pm),
            emit(fmt("Cell. personale",   n), e.get("mobile_personal"), "Dipendenti (Privato)", mail=pm),
        ])
    return results

# ─────────────────────────────────────────────────────────────
# 2. EMPLOYEE RELATIVES
# ─────────────────────────────────────────────────────────────

def get_relative_contacts() -> list[Contact]:
    employees = odoo_search_read("hr.employee", [("active", "=", True)], [
        "name", "relative_ids"
    ])

    # Collect all relative IDs in one batch call
    rel_ids = [rid for e in employees for rid in e.get("relative_ids", [])]
    if not rel_ids:
        return []
    relatives = odoo_search_read("hr.employee.relative", [("id", "in", rel_ids)], [
        "employee_id", "name", "relation", "phone"
    ])
    # Map employee id → name for quick lookup
    emp_map = {e["id"]: e["name"] for e in employees}
    results = []
    for r in relatives:
        emp_name = emp_map.get(r["employee_id"][0], "")
        label    = r.get("relation") or "Familiare"
        c = emit(
            f"{emp_name} – {r['name']} [{label}]",
            r.get("phone"),
            "Familiari dipendenti"
        )
        if c:
            results.append(c)
    return results

# ─────────────────────────────────────────────────────────────
# 3. CONTACTS  (res.partner – skip employee partners)
# ─────────────────────────────────────────────────────────────

def get_partner_contacts() -> list[Contact]:

    # Get partner IDs that belong to employees (work + home)
    employees = odoo_search_read("hr.employee", [], ["address_id", "address_home_id"])
    excluded  = set()
    for e in employees:
        if e.get("address_id"):      excluded.add(e["address_id"][0])
        if e.get("address_home_id"): excluded.add(e["address_home_id"][0])
    partners = odoo_search_read("res.partner",
        [("id", "not in", list(excluded)), ("active", "=", True)],
        ["name", "is_company", "parent_id", "city", "phone", "mobile", "mobile_short", "email"]
    )

    # Pre-build parent lookup
    parent_map = {p["id"]: p for p in partners if p["is_company"]}
    results = []
    for p in partners:
        name  = p["name"]
        mail  = p.get("email")
        city  = p.get("city") or ""
        if p["is_company"]:
            # ── Company ──────────────────────────────────────
            prefix = f"{name}" + (f" ({city})" if city else "")
            results += filter(None, [
                emit(f"{prefix} [Centralino]",   p.get("phone"),   "Clienti", mail=mail),
                emit(f"{prefix} [Cell. azienda]",p.get("mobile"),  "Clienti", short=p.get("mobile_short"), mail=mail),
            ])
        elif p.get("parent_id"):
            # ── Child contact (person inside a company) ───────
            parent    = parent_map.get(p["parent_id"][0], {})
            comp_name = parent.get("name", p["parent_id"][1])
            comp_city = city or parent.get("city", "")
            prefix    = f"{comp_name}" + (f" ({comp_city})" if comp_city else "") + f" – {name}"
            results += filter(None, [
                emit(f"{prefix} [Telefono]",  p.get("phone"),  "Contatti", mail=mail),
                emit(f"{prefix} [Cellulare]", p.get("mobile"), "Contatti",short=p.get("mobile_short"), mail=mail),
            ])
        else:
            # ── Standalone person ─────────────────────────────
            results += filter(None, [
                emit(f"{name} [Telefono]",  p.get("phone"),  "Contatti", mail=mail),
                emit(f"{name} [Cellulare]", p.get("mobile"), "Contatti", short=p.get("mobile_short"), mail=mail),
            ])
    return results

# ─────────────────────────────────────────────────────────────
# ENDPOINT
# ─────────────────────────────────────────────────────────────

@app.get("/phonebook", response_model=list[Contact])

def phonebook():
    return (
        get_employee_contacts()
        + get_relative_contacts()
        + get_partner_contacts()
    )
