#!/usr/bin/env python3
"""
Build script for Tiffin.

Assembles shell.html + app.css + app.js + food_db.json into a single
self-contained tiffin.html by substituting four placeholders in shell.html:
  __CSP__         -> a Content-Security-Policy, with sha256 hashes for the
                     two inline <script> blocks below computed at build time
  /*__CSS__*/     -> contents of app.css
  /*__FOODDB__*/  -> contents of food_db.json (inlined as a JS array literal)
  /*__APPJS__*/   -> contents of app.js

The CSP hashes must match the exact text browsers see between each pair of
<script> tags, so they're computed from the same wrapping shell.html uses
around /*__FOODDB__*/ and /*__APPJS__*/ (see fooddb_script_body /
appjs_script_body below) rather than the placeholder-free file contents.

Usage:
    python3 build.py                # writes ./dist/tiffin.html
    python3 build.py -o out.html    # writes to a custom path
"""
import argparse
import base64
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).parent

def sha256_b64(text):
    return base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode("ascii")

def build(output_path):
    shell = (ROOT / "shell.html").read_text(encoding="utf-8")
    css = (ROOT / "app.css").read_text(encoding="utf-8")
    appjs = (ROOT / "app.js").read_text(encoding="utf-8")
    fooddb = (ROOT / "food_db.json").read_text(encoding="utf-8")

    fooddb_script_body = "\nconst FOOD_DB = " + fooddb + ";\n"
    appjs_script_body = "\n" + appjs + "\n"
    script_hashes = " ".join(
        f"'sha256-{sha256_b64(body)}'" for body in (fooddb_script_body, appjs_script_body)
    )

    # Only these two inline scripts (by hash) and the Chart.js CDN (loaded
    # dynamically by app.js, trusted via 'strict-dynamic') may run. No
    # unsafe-inline/unsafe-eval for scripts, so an injected <script> or an
    # onerror=/onclick=-style attribute -- the exact shape of the two XSS
    # bugs already found and fixed in app.js -- can't execute even if a
    # future change reintroduces an unescaped string in the HTML. style-src
    # still needs unsafe-inline: dynamic inline style="" attributes (bar
    # widths, ring rotation, etc.) are pervasive throughout app.js's
    # generated markup and aren't hashable.
    csp = "; ".join([
        "default-src 'none'",
        f"script-src {script_hashes} https://cdnjs.cloudflare.com 'strict-dynamic'",
        "style-src 'unsafe-inline' https://fonts.googleapis.com",
        "font-src https://fonts.gstatic.com",
        "img-src 'self'",
        "media-src 'self'",
        "connect-src 'none'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
    ])

    out = (
        shell.replace("__CSP__", csp)
             .replace("/*__CSS__*/", css)
             .replace("/*__FOODDB__*/", fooddb)
             .replace("/*__APPJS__*/", appjs)
    )

    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    print(f"Built {output_path} ({len(out.encode('utf-8')):,} bytes)")

    # Also copy to index.html for Capacitor/web server compatibility
    index_path = output_path.parent / "index.html"
    if output_path.name != "index.html":
        index_path.write_text(out, encoding="utf-8")

    # Home-screen icon (iOS "Add to Home Screen" / Android PWA install), referenced
    # by shell.html's apple-touch-icon link -- ships alongside the built HTML.
    icon_src = ROOT / "icon-180.png"
    if icon_src.exists():
        (output_path.parent / "icon-180.png").write_bytes(icon_src.read_bytes())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="dist/tiffin.html")
    args = parser.parse_args()
    build(args.output)
