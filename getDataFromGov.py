import subprocess
import sys
import os
import re
import requests
from urllib.parse import urlparse

# התקנת ספריות אם צריך
def install_requirements():
    try:
        import requests  # noqa
    except ImportError:
        print("📦 Installing required libraries...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

install_requirements()

# --- הגדרות בסיס ---
API_BASE = "https://data.gov.il/api/3/action"
OUTPUT_DIR = "datasets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

# הפיכת שם תיקייה לחוקי
def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

# שליפת כל המאגרים שמכילים קובצי XLSX
def fetch_packages_with_xlsx(limit=2000):
    print("📡 Fetching list of datasets with XLSX files...")
    url = f"{API_BASE}/package_search?q=format:XLSX&rows={limit}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json().get("result", {}).get("results", [])

# הורדת קובץ בודד
def download_file(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Downloaded: {save_path}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

# עיבוד מאגר יחיד
def process_package(pkg):
    title = pkg.get("title") or "unnamed_dataset"
    pkg_id = pkg.get("id")
    folder_name = slugify(title)
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    print(f"\n📁 Processing dataset: {title}")

    # קבלת כל המשאבים של המאגר
    res = requests.get(f"{API_BASE}/package_show?id={pkg_id}", headers=HEADERS)
    res.raise_for_status()
    resources = res.json().get("result", {}).get("resources", [])

    for resource in resources:
        if resource.get("format", "").lower() == "xlsx":
            file_url = resource.get("url")
            if file_url:
                filename = os.path.basename(urlparse(file_url).path)
                save_path = os.path.join(folder_path, filename)
                if os.path.exists(save_path):
                    print(f"↪ Already exists: {filename}")
                else:
                    print(f"⬇ Downloading file: {filename}")
                    download_file(file_url, save_path)

# הרצת הכל
def main():
    packages = fetch_packages_with_xlsx()
    print(f"🔍 Total datasets found: {len(packages)}")
    for pkg in packages:
        process_package(pkg)

if __name__ == "__main__":
    main()
