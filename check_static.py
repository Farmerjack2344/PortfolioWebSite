import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Locations of static folders
STATIC_DIRS = [
    BASE_DIR / 'Overview' / 'static',
    BASE_DIR / 'Blog' / 'static',
    BASE_DIR / 'PowerFromUndergroundApp' / 'static'
]

# Folder where templates are
TEMPLATES_DIR = BASE_DIR / 'templates'

# Regex to match {% static 'path' %}
STATIC_RE = re.compile(r"""{%\s*static\s+['"]([^'"]+)['"]\s*%}""")

def check_static():
    print("Checking static file references...\n")
    for root, _, files in os.walk(TEMPLATES_DIR):
        for f in files:
            if f.endswith(".html"):
                file_path = Path(root) / f
                with open(file_path, 'r', encoding='utf-8') as html_file:
                    content = html_file.read()
                    for match in STATIC_RE.findall(content):
                        # Look for the file in any static folder
                        found = any((static_dir / match).exists() for static_dir in STATIC_DIRS)
                        status = "OK" if found else "MISSING"
                        print(f"{file_path.relative_to(BASE_DIR)} -> {match} : {status}")

if __name__ == "__main__":
    check_static()
