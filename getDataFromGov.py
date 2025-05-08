import os
import re
import json
import requests
import pandas as pd
from urllib.parse import urlparse, unquote

API_BASE = "https://data.gov.il/api/3/action"
OUTPUT_DIR = "datasets"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def get_all_package_ids():
    res = requests.get(f"{API_BASE}/package_list", headers=HEADERS)
    res.raise_for_status()
    return res.json()["result"]

def get_package_metadata(package_id):
    res = requests.get(f"{API_BASE}/package_show?id={package_id}", headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("result", {})
    return {}

def has_xlsx_files(folder):
    return any(f.lower().endswith('.xlsx') for f in os.listdir(folder))

def infer_dtype(series):
    if pd.api.types.is_integer_dtype(series):
        return "int"
    elif pd.api.types.is_float_dtype(series):
        return "float"
    elif pd.api.types.is_bool_dtype(series):
        return "bool"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    else:
        return "string"

def sanitize_filename(name, fallback='file'):
    name = unquote(name)
    base = os.path.basename(urlparse(name).path)
    name_only = os.path.splitext(base)[0]
    ascii_name = slugify(name_only)
    return ascii_name if ascii_name else fallback

def download_and_analyze(url, folder_path, index):
    filename_base = sanitize_filename(url, fallback=f"file-{index}")
    save_xlsx = os.path.join(folder_path, filename_base + ".xlsx")
    save_json = os.path.join(folder_path, filename_base + ".json")

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        with open(save_xlsx, "wb") as f:
            f.write(r.content)
        print(f"✅ Downloaded: {save_xlsx}")

        try:
            df = pd.read_excel(save_xlsx)
            metadata = {}
            for col in df.columns:
                clean_col = str(col).strip()
                if clean_col and df[clean_col].dropna().shape[0] > 0:
                    metadata[clean_col] = infer_dtype(df[clean_col])
            with open(save_json, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"🧾 Metadata saved to: {save_json}")
        except Exception as e:
            print(f"⚠️ Failed to read Excel: {save_xlsx} — {e}")
            with open(save_xlsx + ".error.txt", "w", encoding="utf-8") as f:
                f.write(f"Failed to open as Excel: {e}")

    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

def process_package(package_id):
    metadata = get_package_metadata(package_id)
    if not metadata:
        return

    title = metadata.get("title") or package_id
    folder_name = slugify(title)
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    print(f"\n📦 Processing: {title}")
    index = 0
    for resource in metadata.get("resources", []):
        url = resource.get("url")
        if url and '.xlsx' in url.lower():
            index += 1
            download_and_analyze(url, folder_path, index)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Optional: test network
    try:
        requests.get("https://data.gov.il", timeout=5)
    except Exception as e:
        print(f"❌ Cannot reach data.gov.il: {e}")
        return

    package_ids = get_all_package_ids()
    print(f"📚 Found {len(package_ids)} datasets. Starting...")
    for pid in package_ids:
        process_package(pid)

if __name__ == "__main__":
    main()
