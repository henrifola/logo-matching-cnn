# scraping/extract_logos.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import hashlib
from scraping.utils import get_image_hash, is_duplicate

SCRAPE_DIR = Path("scraping/scraped-logos")


def get_page_html(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch page: {e}")
    return None


def sanitize_filename(text):
    return "_" + hashlib.md5(text.encode()).hexdigest()[:8]


def extract_logo_images(html, base_url, max_results=5):
    soup = BeautifulSoup(html, "html.parser")
    logo_candidates = []


    img_tags = soup.find_all("img")
    for i, img in enumerate(img_tags):
        score = 0
        src = img.get("src", "")
        alt = img.get("alt", "")
        class_name = " ".join(img.get("class", [])) if img.get("class") else ""
        img_id = img.get("id", "")

        if "logo" in src.lower():
            score += 2
        if "logo" in alt.lower():
            score += 2
        if "logo" in class_name.lower():
            score += 1
        if "logo" in img_id.lower():
            score += 1

        if score > 0 and src:
            full_img_url = urljoin(base_url, src)

            print(f"[DEBUG] IMG tag matched:")
            print(f"  URL      : {full_img_url}")
            print(f"  SRC      : {src}")
            print(f"  ALT      : {alt}")
            print(f"  CLASS    : {class_name}")
            print(f"  ID       : {img_id}")
            print(f"  SCORE    : {score}")
            print("-" * 50)

            logo_candidates.append(("img", full_img_url, score))


    svg_tags = soup.find_all("svg")
    for i, svg in enumerate(svg_tags):
        score = 0
        class_name = " ".join(svg.get("class", [])) if svg.get("class") else ""
        svg_id = svg.get("id", "")

        if "logo" in class_name.lower():
            score += 2
        if "logo" in svg_id.lower():
            score += 1

        if score > 0:
            raw_svg = str(svg)

            print(f"[DEBUG] SVG tag matched:")
            print(f"  CLASS    : {class_name}")
            print(f"  ID       : {svg_id}")
            print(f"  SCORE    : {score}")
            print(f"  PREVIEW  : {raw_svg[:100]}...")
            print("-" * 50)

            logo_candidates.append(("svg", raw_svg, score))

    logo_candidates = sorted(logo_candidates, key=lambda x: x[2], reverse=True)
    return logo_candidates[:max_results]


def save_logos(logos, base_url):
    domain = urlparse(base_url).netloc.replace(".", "_")
    folder = SCRAPE_DIR / domain
    folder.mkdir(parents=True, exist_ok=True)

    seen_hashes = set()

    for i, (tag_type, content, _) in enumerate(logos):
        if tag_type == "img":
            try:
                img_data = requests.get(content).content
                img_hash = get_image_hash(img_data)
                if is_duplicate(img_hash, seen_hashes):
                    print(f"[SKIP] Duplicate IMG (hash: {img_hash})")
                    continue
                seen_hashes.add(img_hash)

                ext = Path(urlparse(content).path).suffix or ".img"
                name = f"logo_{i}{ext}"
                with open(folder / name, "wb") as f:
                    f.write(img_data)
                    print(f"[SAVE] Saved IMG: {folder / name}")
            except Exception as e:
                print(f"[ERROR] Could not save image from {content}: {e}")

        elif tag_type == "svg":
            try:
                svg_hash = get_image_hash(content.encode("utf-8"))
                if is_duplicate(svg_hash, seen_hashes):
                    print(f"[SKIP] Duplicate SVG (hash: {svg_hash})")
                    continue
                seen_hashes.add(svg_hash)

                name = f"logo_{i}.svg"
                with open(folder / name, "w", encoding="utf-8") as f:
                    f.write(content)
                    print(f"[SAVE] Saved SVG: {folder / name}")
            except Exception as e:
                print(f"[ERROR] Could not save SVG: {e}")


def process(url):
    print(f"[SCRAPE] Getting HTML from: {url}")
    html = get_page_html(url)

    if not html:
        print("[SCRAPE] Failed to fetch page content.")
        return []

    logos = extract_logo_images(html, url)
    if logos:
        print(f"[SCRAPE] Found {len(logos)} logo candidate(s):")
        for tag_type, content, _ in logos:
            print(f" - ({tag_type}) {content[:100]}..." if tag_type == "svg" else f" - ({tag_type}) {content}")
        save_logos(logos, url)
    else:
        print("[SCRAPE] No logos found.")

    return logos
