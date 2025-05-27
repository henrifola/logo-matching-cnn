# 🛡️ Logo Verification MVP – Phishing Detection Tool

This is a lightweight MVP system for detecting potential phishing websites by comparing scraped logos from websites to a trained CNN classifier on known brand logos.

---

## 🧠 Project Pipeline Overview

### 1. **Logo Classifier (CNN)**

- Train a CNN (e.g., ResNet18) on a subset (50–100) of company logos from public datasets like OpenLogo, Logos in the Wild, etc.
- The model will classify an input logo image into one of the known brands.

➡️ **Output:** A PyTorch model that takes a logo image and returns a brand label.

---

### 2. **Domain Mapping**

- Use either:
  - A small hardcoded dictionary mapping brand names to their official domains (e.g., `"disney" → "disney.com"`)
  - Or dynamically fetch the official domain using the **Wikidata API**.

➡️ **Output:** Given a brand name, return its verified domain.

---

### 3. **main.py – Inference Script**

This script runs the full verification pipeline:

#### ✅ Input:
A website URL to check (e.g., `https://secure-login-disny.net`)

#### 🔍 Steps:
1. Scrape all `<img>` elements from the homepage
2. Filter likely logo candidates (e.g., using 'logo' in filename, `alt`, `class`, etc.)
3. Pass candidate images through the CNN classifier
4. Identify the brand (e.g., “Disney”)
5. Compare the current domain (`disny.net`) to the known domain (`disney.com`)

#### 🚨 Output:
Logs or prints whether the logo brand matches the URL domain – flags potential phishing.

---

## 🚀 How to Run

```bash
python main.py https://example-suspicious-site.com
```

- Ensure you have the trained model saved in a known location (default: `models/logo_classifier.pt`)
- Make sure the logo datasets and CNN training step has been completed
- Add or update domain mappings in `config/domains.json` or enable Wikidata lookup

---

## 🔧 Dependencies (To Be Finalized)

- `torch`, `torchvision`
- `requests`, `beautifulsoup4`
- `Pillow` or `opencv-python`
- `tqdm`
- (Optional) `wikidata` or `SPARQLWrapper`

---

## 📦 Project Structure (WIP)

```
.
├── main.py                  # Entry point script
├── model/                   # CNN training and model storage
├── scraping/                # Logo scraper utils
├── config/domains.json      # Optional: hardcoded brand-domain mapping
└── README.md
```

This README will be updated as the implementation progresses.
