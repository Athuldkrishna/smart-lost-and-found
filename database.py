import os
import uuid
import hashlib
import secrets

import streamlit as st
from supabase import create_client, Client
from postgrest.exceptions import APIError

IMAGE_BUCKET = "item-images"


# ============================================================
# CONNECTION
# ============================================================
def _get_setting(name):
    """Read a setting from .streamlit/secrets.toml, falling back to env vars."""
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name)


@st.cache_resource
def get_client() -> Client:
    url = _get_setting("SUPABASE_URL")
    key = _get_setting("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY "
            "to .streamlit/secrets.toml (see secrets.toml.example)."
        )

    return create_client(url, key)


def initialize_database():
    """
    Tables are created once via supabase_schema.sql in the Supabase SQL Editor.
    This just checks the connection so the app fails early with a clear message.
    """
    try:
        get_client().table("reports").select("id").limit(1).execute()
    except RuntimeError as error:
        st.error(str(error))
        st.stop()
    except Exception as error:
        st.error(
            "Could not reach Supabase. Check your SUPABASE_URL / SUPABASE_KEY "
            "and that supabase_schema.sql has been run.\n\n"
            f"Details: {error}"
        )
        st.stop()


# ============================================================
# USERS
# ============================================================
def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()


def create_user(username, password):
    salt = secrets.token_hex(16)
    password_hash = _hash_password(password, salt)

    try:
        get_client().table("users").insert({
            "username": username,
            "password": f"{salt}:{password_hash}",
        }).execute()
        return True

    except APIError as error:
        # 23505 = unique_violation (username already taken)
        if error.code == "23505":
            return False
        raise


def verify_user(username, password):
    result = (
        get_client()
        .table("users")
        .select("password")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    if not result.data:
        return False

    salt, stored_hash = result.data[0]["password"].split(":")
    password_hash = _hash_password(password, salt)

    return secrets.compare_digest(password_hash, stored_hash)


# ============================================================
# IMAGES
# ============================================================
def upload_image(file_bytes, extension, content_type):
    """Upload an image to Supabase Storage and return its public URL."""
    extension = extension if extension.startswith(".") else f".{extension}"
    object_path = f"reports/{uuid.uuid4().hex}{extension}"

    storage = get_client().storage.from_(IMAGE_BUCKET)
    storage.upload(
        object_path,
        file_bytes,
        {"content-type": content_type or "image/jpeg"}
    )

    return storage.get_public_url(object_path)


# ============================================================
# REPORTS
# ============================================================
def add_report(
    report_type,
    item_name,
    category,
    description,
    location,
    date_reported,
    image_path,
    contact,
    reported_by=None
):
    get_client().table("reports").insert({
        "report_type": report_type,
        "item_name": item_name,
        "category": category,
        "description": description,
        "location": location,
        "date_reported": date_reported,
        "image_path": image_path or None,
        "contact": contact,
        "reported_by": reported_by,
    }).execute()


def get_reports():
    """Return all reports (newest first) as a list of dicts."""
    result = (
        get_client()
        .table("reports")
        .select("*")
        .order("id", desc=True)
        .execute()
    )
    return result.data or []
