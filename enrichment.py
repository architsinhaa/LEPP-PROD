import pandas as pd
import re

FREE_DOMAINS = {"gmail.com", "yahoo.com", "outlook.com"}

def is_valid_email(email: str) -> bool:
    if pd.isna(email):
        return False

    email = str(email).strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):
        return False

    domain = email.split("@")[-1]
    if domain in FREE_DOMAINS:
        return False

    return True


def normalize_title(title):
    if pd.isna(title):
        return ""

    title = str(title).lower()
    title = title.replace("senior", "sr").replace("manager", "mgr")
    return title.title().strip()


def normalize_company(company):
    if pd.isna(company):
        return ""
    return str(company).title().strip()


def clean_and_enrich_leads(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize core fields
    df["Email"] = df["Email"].astype(str).str.strip().str.lower()
    df["Title"] = df.get("Title", "").apply(normalize_title)
    df["Company"] = df.get("Company", "").apply(normalize_company)

    # Filter invalid emails
    df = df[df["Email"].apply(is_valid_email)]

    # Deduplicate
    df = df.drop_duplicates(subset=["Email"])

    # Enrichment placeholders (same logic as notebook)
    if "Industry" not in df.columns:
        df["Industry"] = "Unknown"

    if "Company_Size" not in df.columns:
        df["Company_Size"] = "Unknown"

    if "Location" not in df.columns:
        df["Location"] = "Unknown"

    return df