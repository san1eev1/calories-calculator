#!/usr/bin/env python3
"""
Build script for Tiffin.

Assembles shell.html + app.css + app.js + food_db.json into a single
self-contained tiffin.html by substituting three placeholders in shell.html:
  /*__CSS__*/     -> contents of app.css
  /*__FOODDB__*/  -> contents of food_db.json (inlined as a JS array literal)
  /*__APPJS__*/   -> contents of app.js

Usage:
    python3 build.py                # writes ./dist/tiffin.html
    python3 build.py -o out.html    # writes to a custom path
"""
import argparse
import pathlib

ROOT = pathlib.Path(__file__).parent

def build(output_path):
    shell = (ROOT / "shell.html").read_text(encoding="utf-8")
    css = (ROOT / "app.css").read_text(encoding="utf-8")
    appjs = (ROOT / "app.js").read_text(encoding="utf-8")
    fooddb = (ROOT / "food_db.json").read_text(encoding="utf-8")

    out = (
        shell.replace("/*__CSS__*/", css)
             .replace("/*__FOODDB__*/", fooddb)
             .replace("/*__APPJS__*/", appjs)
    )

    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    print(f"Built {output_path} ({len(out.encode('utf-8')):,} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="dist/tiffin.html")
    args = parser.parse_args()
    build(args.output)
