# scraping/fetch_page.py

import requests

def get_page_html(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch page: {e}")
    return None
