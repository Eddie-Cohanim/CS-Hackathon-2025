import subprocess
import sys

# מתקין את הספריות הדרושות אם הן לא מותקנות
def install_requirements():
    try:
        import requests
        import bs4
    except ImportError:
        print("📦 מתקין ספריות נדרשות (requests, beautifulsoup4)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])

# קורא לפונקציה לפני הכל
install_requirements()

# ממשיך לשאר הקוד
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

BASE_URL = "https://data.gov.il"
DATASETS_URL = f"{BASE_URL}/dataset"
OUTPUT_DIR = "datasets"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def fetch_all_dataset_links():
    print("🔍 מחפש את כל הדאטהסטים הזמינים...")
    dataset_links = []
    page = 1

    while True:
        url = f"{DATASETS_URL}?page={page}"
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.dataset-content h3 a')
        if not links:
            break

        for a in links:
            href = a.get('href')
            if href:
                dataset_links.append(urljoin(BASE_URL, href))
        page += 1

    print(f"✅ נמצאו {len(dataset_links)} דפים של דאטהסטים")
    return dataset_links

def download_files_from_dataset(dataset_url):
    print(f"\n📥 עובד על: {dataset_url}")
    res = requests.get(dataset_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    title_tag = soup.select_one('h1')
    if not title_tag:
        print("❌ לא נמצא שם לדאטהסט")
        return

    dataset_name = slugify(title_tag.text)
    dataset_folder = os.path.join(OUTPUT_DIR, dataset_name)
    os.makedirs(dataset_folder, exist_ok=True)

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if ".xlsx" in href.lower():
            file_url = urljoin(BASE_URL, href)
            filename = os.path.basename(urlparse(file_url).path)
            save_path = os.path.join(dataset_folder, filename)

            if os.path.exists(save_path):
                print(f"↪ כבר הורד: {filename}")
                continue

            try:
                print(f"⬇ מוריד: {filename}")
                r = requests.get(file_url, headers=HEADERS)
                with open(save_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"⚠️ שגיאה בהורדת {filename}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dataset_links = fetch_all_dataset_links()
    for url in dataset_links:
        download_files_from_dataset(url)

if __name__ == "__main__":
    main()
