# Tiffin — nutrition tracker

A self-contained, single-file HTML/CSS/JS nutrition tracker (Cronometer-style,
Indian + international food focus). No build tooling, no framework, no backend —
everything runs client-side and persists to `localStorage`.

## Structure

```
shell.html        HTML template with three placeholders (see build.py)
app.css           All styles (design tokens, components, responsive layout)
app.js            All application logic (vanilla JS, single IIFE)
food_db.json      Food database — 332 items, 45 nutrient fields each
build.py          Assembles the four files above into one dist/tiffin.html
scripts/          One-off scripts used to generate/extend food_db.json (see below)
```

The app itself is one big IIFE in `app.js` using plain event delegation
(a single `click`/`input`/`change`/`submit` listener on `document`, dispatching
on `data-action` attributes) — no build step, no bundler, no framework.
State lives in one `STATE` object, persisted to `localStorage` under the key
`tiffin_state_v1`.

## Building

```bash
python3 build.py               # -> dist/tiffin.html
python3 build.py -o tiffin.html
```

Then just open the resulting HTML file in a browser (or serve it with
`python3 -m http.server` if you want camera-based barcode scanning to work,
since some browsers restrict camera access on `file://` URLs).

## `scripts/` — food database generation history

`food_db.json` is already fully built — you don't need to re-run these unless
you're changing the underlying data generation logic:

- `build_db.py` — original hand-authored ~165 items (13 nutrient fields each)
- `extend_db.py` — added a rule-engine that derives ~30 extra nutrients
  (vitamins, minerals, fat subtypes, etc.) from each food's macros, plus a
  first batch of packaged/branded-generic Indian items (→ 221 items, 45 fields)
- `extend_db2.py` — added more raw ingredients, cooking oils, and dishes,
  plus Hindi/vernacular names in parentheses on many items (→ 332 items)

Each script reads the current `food_db.json`, adds to it, and overwrites it —
so they were applied in that order and are kept mainly for provenance/reuse if
you want to extend the database further with the same approach.

**Known limitation, worth knowing before you extend this further:** most of
the ~45 nutrient fields per food are *estimates* — derived from each food's
macro profile via heuristics, with manual overrides only for foods where a
nutrient is genuinely significant (fish → omega-3, dairy/egg/meat → B12,
leafy greens → vitamin K, etc.). They are not lab measurements. A few fields
(individual amino acids, creatine beyond meat/fish, melatonin) were left out
entirely since reliable per-food data for those doesn't really exist in
standard nutrition databases either.

## Picking this up in Claude Code

This is a normal static multi-file project, so it works fine as a Claude Code
project directory as-is:

1. Put this folder somewhere on disk and open it in Claude Code.
2. Ask Claude Code to run `build.py` after any edit to `app.js`/`app.css`/
   `shell.html`/`food_db.json`, or ask it to set up a small watch script if
   you want that automatic.
3. For quick visual iteration, open `dist/tiffin.html` directly in a browser
   and refresh after each build.

## Current feature set

- Home: calorie ring (fills consumed vs. target, tap for a BMR/TDEE/TEF energy
  breakdown), macro bars, water tracker (tap-to-fill glasses + quick-add),
  workout log with a 14-day heatmap, editable meal slots
- Add-food flow: search → pick a food → choose serving type (grams/small/
  medium/large) and a free-form amount → add → repeat → Finish
- Foods tab: browse/search the database, create custom foods and custom meals
- Nutrients tab: ~40 nutrients grouped into Macros/Fats/Vitamins/Minerals/Other
- Progress tab: weight log + chart (Chart.js, lazy-loaded), logging streak
- Profile: body metrics (sex/age/height in cm or ft-in/activity level), goal
  type + weekly rate presets → auto-calculates calorie/macro targets; unit
  (metric/imperial), theme, backup export/import
- Barcode scanning via the browser's `BarcodeDetector` API (camera + manual
  entry fallback), with a way to link barcodes to foods
