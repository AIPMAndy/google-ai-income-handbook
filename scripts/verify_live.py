#!/usr/bin/env python3
"""Verify actual GitHub Pages bytes; a successful commit alone is not deployment."""
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/google-ai-income-handbook/"
FILES = (
    "index.html", "print.html", "assets/app.js", "assets/data.js",
    "robots.txt", "sitemap.xml", "llms.txt",
    "pdf/google-ai-income-handbook.pdf",
)

def run():
    expected = {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in FILES}
    for attempt in range(1, 19):
        errors = []
        for path in FILES:
            try:
                request = Request(BASE + path, headers={"User-Agent": "AIPMAndy-GitHub-Pages-QA/1.0", "Cache-Control": "no-cache"})
                with urlopen(request, timeout=20) as response:
                    body = response.read()
                    if response.status != 200:
                        raise ValueError(f"HTTP {response.status}")
                digest = sha256(body).hexdigest()
                if digest != expected[path]:
                    errors.append(f"{path}: SHA mismatch: {digest[:12]} != {expected[path][:12]}")
            except (HTTPError, URLError, ValueError, TimeoutError) as error:
                errors.append(f"{path}: {error}")
        if not errors:
            print(f"PASS: {len(FILES)}/{len(FILES)} live HTTP 200 and byte-identical SHA-256 at {BASE}")
            for path in FILES: print(f"  {path}: {expected[path]}")
            return
        print(f"Attempt {attempt}/18: " + "; ".join(errors), flush=True)
        if attempt < 18: time.sleep(8)
    raise SystemExit("FAIL: Pages is not byte-identical to the checked-out source; do not mark deployed")

if __name__ == "__main__":
    run()
