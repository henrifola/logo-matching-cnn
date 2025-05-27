from scraping import extract_logos
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"[INFO] Processing URL: {url}")

    extract_logos.process(url)

if __name__ == "__main__":
    main()
# This script is the entry point for the logo matching CNN application.
# It takes a URL as a command line argument and processes it to extract logos.
# The `extract_logos` function is called to handle the logo extraction logic.