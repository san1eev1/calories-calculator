#!/usr/bin/env python3
"""
Generate a complete, beginner-to-interview-ready PDF guide for the Tiffin app.
Part 1 teaches every language/technology used, from zero.
Part 2 walks through the entire codebase, section by section.
Part 3 covers architecture & design decisions.
Part 4 is an interview Q&A guide.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime

PAGE_W, PAGE_H = letter
CONTENT_W = PAGE_W - 1.5*inch

styles = getSampleStyleSheet()

title_style = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontSize=32,
    textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold', spaceAfter=6)
cover_sub = ParagraphStyle('CoverSub', parent=styles['Heading2'], fontSize=16,
    textColor=colors.HexColor('#555555'), fontName='Helvetica', spaceAfter=4)

part_style = ParagraphStyle('Part', parent=styles['Heading1'], fontSize=24,
    textColor=colors.HexColor('#E8552F'), fontName='Helvetica-Bold',
    spaceBefore=0, spaceAfter=18, borderPadding=0)

chapter_style = ParagraphStyle('Chapter', parent=styles['Heading1'], fontSize=19,
    textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold',
    spaceBefore=4, spaceAfter=12)

h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14.5,
    textColor=colors.HexColor('#2c3e50'), fontName='Helvetica-Bold',
    spaceBefore=14, spaceAfter=8)

h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=12.5,
    textColor=colors.HexColor('#34495e'), fontName='Helvetica-Bold',
    spaceBefore=10, spaceAfter=6)

body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10.3,
    leading=15, spaceAfter=8, alignment=TA_LEFT)

bullet_style = ParagraphStyle('Bullet', parent=body, leftIndent=14, spaceAfter=4)

qa_q = ParagraphStyle('QAQuestion', parent=body, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#E8552F'), fontSize=10.8, spaceBefore=10, spaceAfter=4)
qa_a = ParagraphStyle('QAAnswer', parent=body, leftIndent=10, spaceAfter=10)

code_font_style = ParagraphStyle('CodeInner', parent=styles['Normal'], fontName='Courier',
    fontSize=8.3, leading=10.6, textColor=colors.HexColor('#1a1a1a'))

note_style = ParagraphStyle('Note', parent=body, backColor=colors.HexColor('#FFF4E5'),
    borderColor=colors.HexColor('#E8B84A'), borderWidth=0.6, borderPadding=8,
    spaceBefore=6, spaceAfter=10)

toc_style = ParagraphStyle('TOC', parent=body, spaceAfter=3)
toc_part_style = ParagraphStyle('TOCPart', parent=body, fontName='Helvetica-Bold',
    fontSize=11.5, textColor=colors.HexColor('#E8552F'), spaceBefore=10, spaceAfter=4)

story = []

def part(title):
    story.append(PageBreak())
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(title, part_style))
    story.append(Spacer(1, 0.3*inch))

def chapter(title):
    story.append(PageBreak())
    story.append(Paragraph(title, chapter_style))

def sec(title):
    story.append(Paragraph(title, h2))

def sub(title):
    story.append(Paragraph(title, h3))

def p(text):
    story.append(Paragraph(text, body))

def bullets(items):
    for it in items:
        story.append(Paragraph("&#8226;&nbsp; " + it, bullet_style))

def note(text):
    story.append(Paragraph("<b>Note:</b> " + text, note_style))

def qa(question, answer):
    story.append(Paragraph("Q: " + question, qa_q))
    story.append(Paragraph("A: " + answer, qa_a))

def code(text, width=CONTENT_W):
    pre = Preformatted(text, code_font_style)
    t = Table([[pre]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F5F5')),
        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#D8D8D8')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

def spacer(h=10):
    story.append(Spacer(1, h))

# ================================================================
# COVER PAGE
# ================================================================
story.append(Spacer(1, 1.3*inch))
story.append(Paragraph("🍱 Tiffin", title_style))
story.append(Paragraph("The Complete Beginner-to-Interview Guide", cover_sub))
story.append(Spacer(1, 0.25*inch))
story.append(Paragraph(
    "Every language used in this app, taught from zero — then the entire codebase, "
    "explained line by line — then an interview-ready Q&amp;A guide.",
    body))
story.append(Spacer(1, 0.35*inch))
story.append(Paragraph(f"<b>Prepared:</b> {datetime.now().strftime('%B %Y')}", body))
story.append(Paragraph("<b>Audience:</b> Complete beginners with zero programming background", body))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph(
    "<b>How to use this document:</b> Read Part 1 top to bottom even if some of it feels slow — "
    "it builds the vocabulary Part 2 assumes you already have. Part 2 quotes real code from this "
    "project and explains every line. Part 4 is for interview prep once you understand the rest.",
    body))

# ================================================================
# TABLE OF CONTENTS
# ================================================================
story.append(PageBreak())
story.append(Paragraph("Table of Contents", chapter_style))

toc = [
    ("PART 1 — LEARN THE LANGUAGES (FROM ZERO)", True),
    ("1. How the Web Works", False),
    ("2. HTML — The Skeleton", False),
    ("3. CSS — The Styling", False),
    ("4. JavaScript Part A — Values, Variables, Operators", False),
    ("5. JavaScript Part B — Control Flow (if/else, loops)", False),
    ("6. JavaScript Part C — Functions", False),
    ("7. JavaScript Part D — Arrays & Objects", False),
    ("8. JavaScript Part E — Modern Syntax (arrow fns, destructuring, spread)", False),
    ("9. JavaScript Part F — The DOM & Events", False),
    ("10. JavaScript Part G — Event Delegation, Closures, IIFEs", False),
    ("11. JavaScript Part H — Async Code & Promises", False),
    ("12. JSON — The Data Format", False),
    ("13. Browser Storage — localStorage", False),
    ("14. Browser APIs — Camera, Files, Clipboard", False),
    ("15. Python — Just Enough to Read build.py", False),
    ("16. Git & GitHub Actions — Version Control and CI/CD", False),
    ("17. Capacitor — Turning a Website into a Phone App", False),
    ("PART 2 — THE APP, EXPLAINED END TO END", True),
    ("18. Project Tour — Every File and What It's For", False),
    ("19. The Build Pipeline — build.py Deep Dive", False),
    ("20. shell.html Deep Dive", False),
    ("21. app.css Deep Dive", False),
    ("22. food_db.json Deep Dive", False),
    ("23. app.js Part 1 — Setup & The Shape of the Data", False),
    ("24. app.js Part 2 — Storage & Security", False),
    ("25. app.js Part 3 — Utility & Math Functions", False),
    ("26. app.js Part 4 — The Diary & Meal System", False),
    ("27. app.js Part 5 — Energy Calculations (BMR/TDEE)", False),
    ("28. app.js Part 6 — The Rendering System", False),
    ("29. app.js Part 7 — The Today (Home) View", False),
    ("30. app.js Part 8 — The Food Picker Flow", False),
    ("31. app.js Part 9 — Custom Foods & Custom Meals", False),
    ("32. app.js Part 10 — Progress View & Charts", False),
    ("33. app.js Part 11 — Profile View", False),
    ("34. app.js Part 12 — Barcode Scanning", False),
    ("35. app.js Part 13 — Export / Import / Theme", False),
    ("36. app.js Part 14 — THE EVENT SYSTEM (the app's heart)", False),
    ("37. app.js Part 15 — Startup", False),
    ("PART 3 — ARCHITECTURE & DESIGN DECISIONS", True),
    ("38. Why No Framework, No Backend?", False),
    ("39. Security: XSS, CSP, Prototype Pollution", False),
    ("40. The Full Data Flow, End to End", False),
    ("PART 4 — INTERVIEW GUIDE", True),
    ("41. The 30-Second Pitch", False),
    ("42. Core Technical Q&A", False),
    ("43. Deep-Dive Design Questions", False),
    ("44. Glossary — Every Term Used in This Guide", False),
]
for title, is_part in toc:
    story.append(Paragraph(title, toc_part_style if is_part else toc_style))

# ================================================================
# PART 1 — LEARN THE LANGUAGES
# ================================================================
part("PART 1<br/>Learn the Languages, From Zero")
p("Before we look at a single line of the Tiffin app, we need a shared vocabulary. "
  "This part explains every technology the app uses, assuming you've never programmed before. "
  "Don't skim it — Part 2 will constantly refer back to words defined here.")

# ---------------- Chapter 1: How the web works ----------------
chapter("1. How the Web Works")
p("A website is just <b>files</b> — text files, really — that a browser (Chrome, Safari, Firefox) "
  "downloads and turns into the page you see. There are three core file types, and each one does "
  "a different job:")
bullets([
    "<b>HTML</b> files describe the <i>structure</i> — \"there's a heading here, a button there, a list of items below it.\"",
    "<b>CSS</b> files describe the <i>appearance</i> — colors, spacing, fonts, layout.",
    "<b>JavaScript</b> files describe the <i>behavior</i> — what happens when you click a button, type in a box, or scroll.",
])
p("Think of building a house: HTML is the frame and rooms, CSS is the paint and furniture arrangement, "
  "and JavaScript is the electricity and plumbing — the stuff that actually <i>does</i> things.")
p("Normally, a website talks to a <b>server</b> — a remote computer — to fetch data (like your bank balance "
  "or a friend's photos). Tiffin is unusual: it has <b>no server at all</b>. Every file it needs is loaded once, "
  "and after that the app runs entirely inside your browser, saving your data on your own device. "
  "We'll see exactly how later — this is one of the most interesting design decisions in the whole project.")

# ---------------- Chapter 2: HTML ----------------
chapter("2. HTML — The Skeleton")
p("HTML stands for <b>HyperText Markup Language</b>. It isn't a programming language — it has no logic, "
  "no math, no decisions. It's a <i>markup</i> language: you wrap text in <b>tags</b> to say what that text is.")
sec("2.1 Tags and elements")
p("A tag looks like <font face='Courier'>&lt;tagname&gt;</font>. Most tags come in pairs: an opening tag and a "
  "closing tag (which has a forward slash). Everything between them is that element's content.")
code('''<p>This is a paragraph of text.</p>
<h1>This is a big heading</h1>
<button>Click me</button>''')
p("Some tags never wrap content and don't need a closing tag, like the line-break tag "
  "<font face='Courier'>&lt;br&gt;</font> or the meta-information tag <font face='Courier'>&lt;meta&gt;</font>.")
sec("2.2 Attributes")
p("Tags can carry extra information called <b>attributes</b>, written inside the opening tag as "
  "<font face='Courier'>name=\"value\"</font> pairs:")
code('''<button id="saveBtn" class="btn btn-primary" type="submit">Save</button>''')
bullets([
    "<font face='Courier'>id</font> — a unique name for one specific element, used to find it later.",
    "<font face='Courier'>class</font> — a label (that can be reused on many elements) mainly used by CSS to style groups of elements the same way.",
    "<font face='Courier'>type</font> — tag-specific meaning, e.g. a button's type or an input's kind (text, number, date...).",
])
p("Tiffin's code uses one attribute constantly that isn't a standard HTML attribute: "
  "<font face='Courier'>data-action=\"...\"</font>. Any attribute starting with <font face='Courier'>data-</font> "
  "is a \"custom data attribute\" — HTML explicitly allows you to invent your own, and JavaScript can read them. "
  "Tiffin uses these to label every clickable element with what it should <i>do</i> when clicked, e.g. "
  "<font face='Courier'>data-action=\"delete-entry\"</font>. We'll see exactly how in Chapter 36.")
sec("2.3 The document skeleton")
p("Every HTML page has the same basic shape:")
code('''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Page title shown in the browser tab</title>
  <style>/* CSS can go here */</style>
</head>
<body>
  <!-- everything visible on the page goes here -->
  <script>/* JavaScript can go here */</script>
</body>
</html>''')
bullets([
    "<font face='Courier'>&lt;!doctype html&gt;</font> tells the browser \"this is a modern HTML document.\"",
    "<font face='Courier'>&lt;head&gt;</font> holds information <i>about</i> the page (title, styles, metadata) — nothing in here is directly visible.",
    "<font face='Courier'>&lt;body&gt;</font> holds everything the user actually sees.",
    "A <font face='Courier'>&lt;script&gt;</font> tag either contains JavaScript code directly, or points to a "
    "<font face='Courier'>.js</font> file via <font face='Courier'>src=\"...\"</font>.",
])
sec("2.4 Common tags you'll see in this project")
tags_table_data = [
    ["Tag", "Meaning"],
    ["<div>", "A generic box/container with no special meaning — used purely for grouping and styling"],
    ["<span>", "Like <div>, but for inline (within a line of text) grouping"],
    ["<button>", "A clickable button"],
    ["<input>", "A field the user types into (or a checkbox, date picker, number field, etc.)"],
    ["<select>", "A dropdown menu"],
    ["<form>", "Groups related inputs together so they can be submitted as one unit"],
    ["<svg>", "Draws vector graphics (used here for all icons — no image files needed)"],
    ["<canvas>", "A blank drawing surface (used here by the charting library)"],
    ["<video>", "Plays a video stream (used here to show the live camera feed for barcode scanning)"],
    ["<nav>", "Marks a navigation menu"],
    ["<label>", "Text describing an input field"],
]
tt = Table(tags_table_data, colWidths=[100, CONTENT_W-100])
tt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(0,-1),'Courier'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(tt)
spacer(10)
note("Tiffin builds ALL of its HTML at runtime using JavaScript — there's barely any HTML written by hand. "
     "The one hand-written file, shell.html, is just an empty shell with a few placeholder containers "
     "(like &lt;div id=\"viewRoot\"&gt;&lt;/div&gt;) that JavaScript fills in. This pattern is explained fully in Chapter 20.")

# ---------------- Chapter 3: CSS ----------------
chapter("3. CSS — The Styling")
p("CSS stands for <b>Cascading Style Sheets</b>. It answers questions like: what color is this text? "
  "How much space is around this box? Should this be hidden on small screens?")
sec("3.1 The basic rule shape")
code('''selector {
  property: value;
  property: value;
}

/* Real example: */
.btn-primary {
  background: #FF6B4A;
  color: white;
  padding: 10px 18px;
  border-radius: 999px;
}''')
p("A <b>selector</b> picks which HTML elements the rule applies to. <font face='Courier'>.btn-primary</font> "
  "(dot prefix) selects every element with <font face='Courier'>class=\"btn-primary\"</font>. "
  "<font face='Courier'>#saveBtn</font> (hash prefix) selects the one element with "
  "<font face='Courier'>id=\"saveBtn\"</font>. A bare word like <font face='Courier'>button</font> selects every "
  "<font face='Courier'>&lt;button&gt;</font> tag on the page.")
sec("3.2 The box model")
p("Every HTML element is treated as a rectangular box with four layers, from inside out: "
  "<b>content</b> (the text/image itself), <b>padding</b> (space inside the border), "
  "<b>border</b> (a line around the padding), and <b>margin</b> (space outside the border, "
  "separating it from other elements).")
sec("3.3 Flexbox and Grid — modern layout")
p("Tiffin lays out almost everything with <b>Flexbox</b> (one-dimensional layout — a row or a column) "
  "and occasionally <b>Grid</b> (two-dimensional layout — rows AND columns at once).")
code('''.row {
  display: flex;          /* children line up in a row */
  align-items: center;    /* vertically centered */
  justify-content: space-between; /* push children to opposite ends */
  gap: 12px;               /* space between children */
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* two equal-width columns */
  gap: 14px;
}''')
sec("3.4 CSS variables (custom properties)")
p("CSS lets you define your own named values, and reuse them everywhere, similar to a variable in "
  "programming. Tiffin defines its entire color palette this way at the top of app.css:")
code(''':root {
  --accent: #FF6B4A;
  --text: #241C12;
  --radius-m: 20px;
}

/* used elsewhere as: */
.btn-primary { background: var(--accent); }''')
p("The huge benefit: to support <b>dark mode</b>, Tiffin doesn't need to rewrite every single rule — "
  "it just redefines these same variable names inside a dark-mode block, and every rule that used "
  "<font face='Courier'>var(--accent)</font> automatically updates. We'll see this exact trick in Chapter 21.")
sec("3.5 Media queries — responsive design")
p("A media query is a conditional rule that only applies when the browser window matches some condition, "
  "most commonly a maximum or minimum width — this is how a page adapts between desktop and mobile.")
code('''@media (max-width: 860px) {
  .sidenav { display: none; }   /* hide the sidebar on small screens */
  .bottomnav { display: flex; } /* show a bottom tab bar instead */
}''')
sec("3.6 Pseudo-classes")
p("A pseudo-class targets an element in a particular <i>state</i>, written with a colon:")
bullets([
    "<font face='Courier'>:hover</font> — while the mouse is over the element",
    "<font face='Courier'>:active</font> — while it's being clicked/pressed",
    "<font face='Courier'>:focus</font> — while a text input is selected/typing",
    "<font face='Courier'>:first-child</font> — if it's the first element inside its parent",
])

# ---------------- Chapter 4: JS Part A ----------------
chapter("4. JavaScript Part A — Values, Variables, Operators")
p("JavaScript (\"JS\") is the one true <b>programming language</b> in this stack — it has logic, math, "
  "decisions, and memory. It's the only language capable of making the app actually <i>do</i> things "
  "rather than just look a certain way.")
sec("4.1 Variables — named storage")
p("A variable is a labeled box that holds a value. JavaScript has three ways to create one:")
code('''const name = "Alice";   // cannot be reassigned later
let score = 100;        // CAN be reassigned later
score = 150;             // OK, because it was declared with let

var old = "avoid this";  // an older, quirky way — not used in this app''')
p("Tiffin uses <font face='Courier'>const</font> for almost everything, and <font face='Courier'>let</font> "
  "only for values that genuinely change over time (like which screen is currently showing). "
  "This is considered good modern style: it signals intent to future readers.")
sec("4.2 Data types")
data_types = [
    ["Type", "Example", "What it's for"],
    ["Number", "42, 3.14, -7", "Any numeric value — JS has only one number type"],
    ["String", "'hello', \"world\"", "Text, wrapped in quotes"],
    ["Boolean", "true / false", "A yes/no, on/off value"],
    ["Array", "[1, 2, 3]", "An ordered list of values"],
    ["Object", "{name: 'Alice'}", "A collection of named values (key-value pairs)"],
    ["null", "null", "\"Intentionally nothing\" — explicitly set to empty"],
    ["undefined", "undefined", "\"Nothing was ever set here\" — JS's own default"],
]
tt2 = Table(data_types, colWidths=[70, 110, CONTENT_W-180])
tt2.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(1,-1),'Courier'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(tt2)
spacer(10)
p("Tiffin's food data is a perfect real example of an object nested inside an array of objects:")
code('''const food = {
  id: "rice-cooked-white",
  name: "Rice, cooked (Chawal, white)",
  kcal: 200,
  protein: 4.2,
  carbs: 44
};

const foodList = [food, anotherFood, yetAnotherFood]; // an array of objects''')
sec("4.3 Operators")
bullets([
    "<b>Arithmetic:</b> <font face='Courier'>+  -  *  /  %</font> (% is \"remainder\", e.g. 7 % 2 = 1)",
    "<b>Comparison:</b> <font face='Courier'>===</font> (equal), <font face='Courier'>!==</font> (not equal), "
    "<font face='Courier'>&gt;  &lt;  &gt;=  &lt;=</font>",
    "<b>Logical:</b> <font face='Courier'>&amp;&amp;</font> (AND — both sides must be true), "
    "<font face='Courier'>||</font> (OR — at least one side true), <font face='Courier'>!</font> (NOT — flips true/false)",
    "<b>Assignment:</b> <font face='Courier'>=</font> (set), <font face='Courier'>+=</font> (add and reassign), etc.",
])
note("Always use <font face='Courier'>===</font> instead of <font face='Courier'>==</font> in JavaScript. "
     "<font face='Courier'>==</font> silently converts types before comparing (so <font face='Courier'>0 == '0'</font> "
     "is true, which causes bugs), while <font face='Courier'>===</font> requires an exact match. "
     "This codebase uses <font face='Courier'>===</font> throughout.")
sec("4.4 Template literals — building strings with data inside them")
p("Backtick-quoted strings let you embed JavaScript expressions directly inside text using "
  "<font face='Courier'>${...}</font>. This is used <i>constantly</i> in Tiffin to build HTML:")
code('''const name = "chicken curry";
const kcal = 350;

// Old way:
const msg1 = "Added " + name + " (" + kcal + " kcal)";

// Template literal way (used everywhere in this app):
const msg2 = `Added ${name} (${kcal} kcal)`;

// Can even span multiple lines, which is how HTML gets built:
const html = `<div class="food-row">
  <span>${name}</span>
  <span>${kcal} kcal</span>
</div>`;''')

# ---------------- Chapter 5: JS Part B — control flow ----------------
chapter("5. JavaScript Part B — Control Flow")
sec("5.1 if / else — making decisions")
code('''if (age >= 18) {
  console.log("adult");
} else if (age >= 13) {
  console.log("teen");
} else {
  console.log("child");
}''')
sec("5.2 The ternary operator — a compact if/else")
p("Tiffin uses this shorthand everywhere inside template literals, because a full if/else statement "
  "can't be embedded inside a string expression:")
code('''const label = age >= 18 ? "adult" : "minor";

// Real example from the app (choosing an emoji fallback):
`Hi, ${name ? escapeHtml(name) + ' 👋' : 'Welcome back 👋'}`''')
sec("5.3 Loops — repeating an action")
code('''// for loop: repeat a known number of times
for (let i = 0; i < 5; i++) {
  console.log(i); // prints 0,1,2,3,4
}

// while loop: repeat until a condition becomes false
let count = 0;
while (hasMoreItems) {
  count++;
}''')
p("In practice, this codebase almost never writes a raw <font face='Courier'>for</font> loop over arrays — "
  "it uses array methods like <font face='Courier'>.map()</font> and <font face='Courier'>.forEach()</font> "
  "instead (Chapter 7), which is the modern, preferred style.")
sec("5.4 Truthy and falsy values")
p("In an <font face='Courier'>if</font> condition, JavaScript treats some non-boolean values as \"falsy\" "
  "(counted as false) and everything else as \"truthy\". The falsy values are: "
  "<font face='Courier'>false, 0, '', null, undefined, NaN</font>. Everything else — including any "
  "non-empty string, any object, any array (even an empty one!) — is truthy.")
code('''if (name) { /* runs only if name is a non-empty string */ }
if (list.length) { /* runs only if the array has at least 1 item */ }''')

# ---------------- Chapter 6: Functions ----------------
chapter("6. JavaScript Part C — Functions")
p("A function is a named, reusable block of code. You define it once, then <b>call</b> (run) it as many "
  "times as you like, optionally feeding it different inputs (\"arguments\" / \"parameters\") each time.")
code('''function add(a, b) {
  return a + b;
}

const result = add(2, 3); // result is 5''')
sec("6.1 Why functions matter here")
p("Tiffin has roughly 100 functions. Breaking a huge program into small, named functions is the single "
  "most important organizing idea in this codebase — instead of one giant block of code, there's a function "
  "for each distinct job: <font face='Courier'>saveState()</font> saves data, <font face='Courier'>renderToday()</font> "
  "builds the home screen's HTML, <font face='Courier'>calcBMR()</font> does one specific calculation, and so on. "
  "Each one is small enough to read and understand on its own.")
sec("6.2 Return values")
p("A function can hand back a result using <font face='Courier'>return</font>. Whatever follows "
  "<font face='Courier'>return</font> becomes the value of calling that function.")
code('''function round1(n) {
  return Math.round((n + Number.EPSILON) * 10) / 10;
}

round1(3.14159); // returns 3.1''')
p("This exact function, <font face='Courier'>round1</font>, exists in app.js and is used everywhere numbers "
  "are displayed, to avoid showing ugly values like 3.14159265 to the user.")
sec("6.3 Functions as values")
p("In JavaScript, a function is just another kind of value — it can be stored in a variable, put in an array, "
  "or passed into another function as an argument. This is used constantly for event handling: "
  "\"when this button is clicked, run this function.\"")
code('''button.addEventListener('click', function() {
  console.log('clicked!');
});

// same thing, using a shorter arrow-function syntax (see Chapter 8):
button.addEventListener('click', () => console.log('clicked!'));''')

# ---------------- Chapter 7: Arrays & Objects ----------------
chapter("7. JavaScript Part D — Arrays & Objects")
sec("7.1 Arrays — ordered lists")
code('''const fruits = ['apple', 'banana', 'cherry'];

fruits[0];          // 'apple'  (indexes start at 0!)
fruits.length;       // 3
fruits.push('date'); // adds to the end''')
sec("7.2 Array methods used throughout this app")
p("These four methods appear on almost every page of app.js. Learn them well:")
sub(".map() — transform every item into something new")
code('''const kcals = foods.map(food => food.kcal);
// foods = [{kcal:100}, {kcal:200}] -> kcals = [100, 200]

// Real use: turning a list of foods into a list of HTML strings
const html = foods.map(f => `<div>${f.name}</div>`).join('');''')
sub(".filter() — keep only items that pass a test")
code('''const cheap = foods.filter(f => f.kcal < 150);
// keeps only foods with fewer than 150 calories''')
sub(".forEach() — do something with every item (no new array returned)")
code('''NUTRIENT_KEYS.forEach(key => {
  total[key] = (a[key] || 0) + (b[key] || 0);
});''')
sub(".find() — get the first item that matches, or undefined")
code('''function dbFoodById(id) {
  return FOOD_DB.find(f => f.id === id) || null;
}''')
note("This exact pattern — <font face='Courier'>.find(...) || null</font> — appears constantly in this "
     "codebase. <font face='Courier'>.find()</font> returns <font face='Courier'>undefined</font> if nothing "
     "matches; the <font face='Courier'>|| null</font> converts that into an explicit, intentional "
     "<font face='Courier'>null</font>, which is easier to check for deliberately later.")
sub(".join() — turn an array back into one string")
code('''['a','b','c'].join('');    // "abc"  — used to combine many HTML snippets into one block
['a','b','c'].join(', ');  // "a, b, c"''')
sub(".reduce() and .sort()")
code('''// .sort compares two items at a time; return negative to put `a` first
const sorted = [...list].sort((a,b) => a.date < b.date ? -1 : 1);''')
sec("7.3 Objects — labeled bundles of data")
code('''const food = {
  name: "Rice",
  kcal: 200,
  protein: 4.2
};

food.name;        // "Rice"      — dot notation
food['kcal'];      // 200         — bracket notation (needed for dynamic keys)

const key = 'protein';
food[key];          // 4.2  — you can't do food.key, that would look for a literal "key" property''')
p("Bracket notation with a variable key is essential in this app because nutrient names are stored as "
  "strings in a list (<font face='Courier'>NUTRIENT_KEYS</font>) and looked up dynamically — see Chapter 25.")
sec("7.4 Object.keys, Object.assign, and friends")
code('''Object.keys({a:1, b:2});          // ['a', 'b']
Object.assign({}, obj1, obj2);      // merges obj2's keys into a NEW copy of obj1
Object.entries({a:1, b:2});         // [['a',1], ['b',2]]''')
p("<font face='Courier'>Object.assign({}, ...)</font> — starting from an empty object — is a common way "
  "to make a <i>copy</i> rather than mutating the original, which avoids accidental side effects.")

# ---------------- Chapter 8: Modern syntax ----------------
chapter("8. JavaScript Part E — Modern Syntax")
sec("8.1 Arrow functions")
p("A shorter way to write a function, especially a short one used as an argument to another function:")
code('''// Old style
function double(x) { return x * 2; }

// Arrow function, same thing
const double = (x) => { return x * 2; };

// Arrow function, shortest form (implicit return, no braces/return needed)
const double = x => x * 2;

// Used constantly in .map/.filter/.forEach:
foods.map(f => f.kcal);
foods.filter(f => f.category === 'Indian');''')
sec("8.2 Destructuring — unpacking values in one step")
code('''// Array destructuring
const [first, second] = ['a', 'b'];  // first='a', second='b'

// Real example from this app (a nutrient row definition):
const [key, label, unit, goalKey] = ['protein', 'Protein', 'g', 'proteinGoal'];

// Object destructuring
const { name, age } = person;  // pulls out person.name and person.age directly''')
sec("8.3 Spread syntax (...) — expanding a collection")
code('''const a = [1, 2, 3];
const b = [...a, 4, 5];   // [1, 2, 3, 4, 5] — copies `a`'s items, then adds more

const original = {x: 1, y: 2};
const copy = {...original, y: 99};  // {x: 1, y: 99} — copy with one field overridden

// Real example: copying the weight log before sorting, so the original array
// used elsewhere in STATE isn't accidentally reordered:
const sorted = [...STATE.weightLog].sort((a, b) => a.date < b.date ? -1 : 1);''')
sec("8.4 Optional/default parameters and short-circuiting")
code('''function greet(name) {
  name = name || 'friend';   // if name is falsy (missing), fall back to 'friend'
  return `Hello, ${name}`;
}

opts = opts || {};   // a very common Tiffin pattern: "if no options object was
                       // passed in, use an empty one instead of crashing later"''')

# ---------------- Chapter 9: DOM & Events ----------------
chapter("9. JavaScript Part F — The DOM & Events")
sec("9.1 What is the DOM?")
p("When a browser loads HTML, it builds a live, in-memory tree of objects representing every element on "
  "the page — this tree is called the <b>DOM</b> (Document Object Model). JavaScript can read this tree, "
  "and — critically — <i>change</i> it. Any change to the DOM is instantly reflected on screen; you never "
  "have to manually \"redraw\" anything.")
sec("9.2 Finding elements")
code('''document.getElementById('viewRoot');        // the one element with id="viewRoot"
document.querySelector('.food-row');           // the FIRST element matching this CSS selector
document.querySelectorAll('.food-row');         // ALL elements matching it, as a list''')
sec("9.3 Changing elements")
code('''el.textContent = 'Hello';         // sets plain text (safe — no HTML parsing)
el.innerHTML = '<b>Hello</b>';     // sets HTML (parses tags — can be dangerous, see Ch.39)
el.classList.add('active');         // adds a CSS class
el.classList.remove('active');      // removes a CSS class
el.style.width = '50%';             // sets one inline CSS property directly
el.setAttribute('data-id', '123');  // sets any HTML attribute''')
p("Tiffin's entire UI is built by constantly setting <font face='Courier'>.innerHTML</font> on a handful of "
  "container elements to giant strings of freshly-generated HTML. This is explained fully in Chapter 28.")
sec("9.4 Events")
p("An <b>event</b> is something that happens — a click, a keystroke, a form submission, the page finishing "
  "loading. You <b>listen</b> for an event on an element, providing a function to run when it happens:")
code('''button.addEventListener('click', function(event) {
  console.log('Button was clicked!');
  console.log(event.target); // the exact element that triggered this
});''')
p("Common events used in this app: <font face='Courier'>click</font>, <font face='Courier'>input</font> "
  "(fires on every keystroke in a text field), <font face='Courier'>change</font> (fires when a value is "
  "committed, e.g. picking a file), <font face='Courier'>submit</font> (fires when a form is submitted), and "
  "<font face='Courier'>DOMContentLoaded</font> (fires once, when the page has finished loading).")

# ---------------- Chapter 10: delegation, closures, IIFEs ----------------
chapter("10. JavaScript Part G — Event Delegation, Closures, IIFEs")
sec("10.1 Event delegation — the single most important pattern in this app")
p("Imagine a page with 50 \"delete\" buttons — one per food logged today. You could attach 50 separate "
  "click listeners, one to each button. But there's a smarter way, based on a real DOM behavior called "
  "<b>event bubbling</b>: when you click a button, the click event doesn't just fire on that button — it "
  "then \"bubbles up\" and also fires on its parent, its grandparent, all the way up to "
  "<font face='Courier'>document</font> itself.")
p("<b>Event delegation</b> exploits this: instead of 50 listeners, you attach ONE listener to "
  "<font face='Courier'>document</font> itself, and when it fires, you check "
  "<i>which element was actually clicked</i> (via <font face='Courier'>event.target</font>) to decide what to do.")
code('''document.addEventListener('click', function(e) {
  const el = e.target.closest('[data-action]');
  if (!el) return;                 // click wasn't on anything actionable
  const action = el.dataset.action; // reads the data-action="..." attribute

  if (action === 'delete-entry') { /* ... */ }
  if (action === 'add-water') { /* ... */ }
  // ...dozens more branches
});''')
p("<font face='Courier'>closest()</font> walks up from the clicked element through its ancestors until it "
  "finds one with a <font face='Courier'>data-action</font> attribute (or gives up and returns null). This "
  "means the click could land on an icon INSIDE a button, and it still correctly finds the button.")
p("This is exactly Tiffin's entire strategy: one listener, one big if-chain, ~150 possible actions. "
  "New buttons never need new JavaScript to be \"wired up\" — they just need a "
  "<font face='Courier'>data-action</font> attribute matching an existing branch. Full detail in Chapter 36.")
sec("10.2 Closures")
p("A closure is a function that \"remembers\" the variables that were in scope where it was defined, "
  "even after that outer code has finished running.")
code('''function makeCounter() {
  let count = 0;              // this variable is private to makeCounter
  return function() {
    count = count + 1;
    return count;
  };
}
const counter = makeCounter();
counter(); // 1
counter(); // 2  -- it remembered `count` between calls!''')
sec("10.3 IIFEs — Immediately Invoked Function Expressions")
p("app.js is wrapped, top to bottom, in this pattern:")
code('''(function(){
  "use strict";
  // ...the ENTIRE app's code lives in here...
})();''')
p("This defines an anonymous function and calls it immediately (note the <font face='Courier'>()</font> at "
  "the very end). Why bother? Because every <font face='Courier'>const</font>/<font face='Courier'>let</font> "
  "declared inside is scoped to that function — completely invisible to the outside world. This keeps the "
  "app's ~100 internal function and variable names from ever clashing with anything else on the page (like "
  "the Chart.js library it loads separately). It's a lightweight, no-tooling substitute for what other "
  "projects achieve with a module bundler.")
p("<font face='Courier'>\"use strict\"</font> turns on JavaScript's stricter rule set — for example, it "
  "makes accidentally creating a global variable (by forgetting <font face='Courier'>const</font>/"
  "<font face='Courier'>let</font>) throw an error instead of silently succeeding.")

# ---------------- Chapter 11: Async ----------------
chapter("11. JavaScript Part H — Async Code & Promises")
p("Some operations take time and shouldn't freeze the whole page while waiting: asking for camera access, "
  "reading a file the user picked, fetching something from the network. JavaScript handles this with "
  "<b>Promises</b> and the <font face='Courier'>async</font>/<font face='Courier'>await</font> keywords.")
code('''async function startCamera() {
  // `await` pauses THIS function (not the whole page) until the promise resolves
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
}''')
p("A function marked <font face='Courier'>async</font> can use <font face='Courier'>await</font> inside it. "
  "<font face='Courier'>await somePromise</font> means \"pause here, let other things on the page keep "
  "working, and resume this function once the promise finishes.\" Tiffin uses this for camera access "
  "(barcode scanning, Chapter 34) and for its optional \"save file\" integration (Chapter 35).")
code('''try {
  const stream = await navigator.mediaDevices.getUserMedia({video:true});
} catch (err) {
  // runs if the user denies camera permission, or no camera exists
  showMessage("Camera access isn't available here.");
}''')
p("<font face='Courier'>try { ... } catch (err) { ... }</font> is how JavaScript handles errors: code that "
  "might fail goes in the <font face='Courier'>try</font> block; if it throws an error, execution jumps "
  "straight to <font face='Courier'>catch</font> instead of crashing the whole app.")

# ---------------- Chapter 12: JSON ----------------
chapter("12. JSON — The Data Format")
p("JSON (JavaScript Object Notation) is a text format for representing data — arrays, objects, strings, "
  "numbers, booleans, null. It looks almost exactly like JavaScript object/array syntax, with a few stricter "
  "rules (keys must be in double quotes; no comments allowed; no trailing commas).")
code('''{
  "id": "rice-cooked-white",
  "name": "Rice, cooked (Chawal, white)",
  "category": "Indian",
  "kcal": 200,
  "protein": 4.2,
  "tags": ["staple", "gluten-free"]
}''')
p("JSON is the universal language for storing and transmitting structured data. In this project it's used "
  "for three separate things:")
bullets([
    "<b>food_db.json</b> — the entire 332-food nutrition database (Chapter 22).",
    "<b>localStorage</b> — the user's own data (profile, diary, custom foods) is converted to a JSON string "
    "to be saved in the browser, then parsed back when the app reopens (Chapter 24).",
    "<b>package.json / capacitor.config.json</b> — configuration files that describe the project to various "
    "tools (Node.js, Capacitor).",
])
sec("Converting between JavaScript objects and JSON text")
code('''const data = { name: "Alice", age: 30 };

const text = JSON.stringify(data);   // '{"name":"Alice","age":30}'  (a STRING)
const back = JSON.parse(text);        // { name: "Alice", age: 30 }  (an OBJECT again)''')
p("<font face='Courier'>JSON.stringify</font> turns a JS value into JSON text (used when saving); "
  "<font face='Courier'>JSON.parse</font> turns JSON text back into a live JS value (used when loading). "
  "If the text isn't valid JSON, <font face='Courier'>JSON.parse</font> throws an error — which is exactly "
  "why it's always wrapped in a <font face='Courier'>try/catch</font> in this app.")

# ---------------- Chapter 13: localStorage ----------------
chapter("13. Browser Storage — localStorage")
p("Normally, anything a JavaScript variable holds disappears the instant the tab is closed. "
  "<font face='Courier'>localStorage</font> is a small key-value database built into every browser that "
  "<i>persists</i> — it survives page refreshes, tab closes, even computer restarts. It's tied to one "
  "website's origin (domain), and typically allows a few megabytes of storage — plenty for this app's data.")
code('''localStorage.setItem('myKey', 'some text value'); // save (must be a string!)
const value = localStorage.getItem('myKey');            // load (or null if never set)
localStorage.removeItem('myKey');                        // delete one key
localStorage.clear();                                      // delete everything''')
p("Because localStorage only stores <i>strings</i>, saving a whole object means combining it with JSON "
  "(Chapter 12) — stringify before saving, parse after loading. This exact pattern is the entire "
  "persistence layer of Tiffin, covered in full in Chapter 24:")
code('''localStorage.setItem('tiffin_state_v1', JSON.stringify(STATE));

const raw = localStorage.getItem('tiffin_state_v1');
const STATE = JSON.parse(raw);''')
note("This is why Tiffin needs no backend server, no account, no login. Your data lives only on your own "
     "device, inside your browser. The tradeoff: it doesn't sync between devices, and clearing your browser "
     "data would erase it — which is exactly why the app has an Export/Import backup feature (Chapter 35).")

# ---------------- Chapter 14: Browser APIs ----------------
chapter("14. Browser APIs — Camera, Files, Clipboard")
p("Beyond the DOM, browsers expose many built-in \"Web APIs\" that JavaScript can call to do more advanced "
  "things. Tiffin uses a few:")
sub("BarcodeDetector")
p("A relatively new browser API that can scan a video feed for barcodes and report what it finds, with no "
  "external library needed. Not every browser supports it, so Tiffin always checks first: "
  "<font face='Courier'>if ('BarcodeDetector' in window)</font> before trying to use it, and falls back to a "
  "manual numeric-entry field if it's unavailable.")
sub("MediaDevices / getUserMedia")
p("Requests access to the device's camera (or microphone). Returns a live video \"stream\" that can be shown "
  "inside a <font face='Courier'>&lt;video&gt;</font> tag. Always requires the user's explicit permission.")
sub("FileReader")
p("Reads the contents of a file the user has selected (e.g. via a file-picker input), asynchronously, so "
  "large files don't freeze the page. Used for the \"Import backup\" feature.")
code('''const reader = new FileReader();
reader.onload = () => {
  const text = reader.result; // the file's full text content
  const data = JSON.parse(text);
};
reader.readAsText(file);''')
sub("Clipboard API")
p("<font face='Courier'>navigator.clipboard.writeText(...)</font> copies text to the system clipboard "
  "programmatically — used by the \"Copy to clipboard\" button on the export screen.")
sub("Chart.js (a third-party library, not a browser API)")
p("Tiffin doesn't reinvent chart-drawing. It loads the popular open-source Chart.js library dynamically "
  "from a CDN (Content Delivery Network — a server that just hosts popular public files) only when the user "
  "opens the Progress tab, to avoid slowing down initial page load for people who never look at it. "
  "Details in Chapter 32.")

# ---------------- Chapter 15: Python ----------------
chapter("15. Python — Just Enough to Read build.py")
p("Python is a different programming language from JavaScript, used here for exactly one job: a small "
  "build script that glues the app's files together before shipping (Chapter 19). You don't need deep "
  "Python knowledge — just enough to follow ~85 lines of fairly readable code.")
sec("15.1 What's different from JavaScript (at a glance)")
compare = [
    ["Concept", "JavaScript", "Python"],
    ["Variable", "const x = 5;", "x = 5"],
    ["Blocks", "{ curly braces }", "indentation (whitespace) defines blocks"],
    ["String", '"text" or `${x}`', "'text' or f\"{x}\""],
    ["Function", "function f(x) { return x; }", "def f(x):\n    return x"],
    ["Import code", "<script src=...>", "import module_name"],
]
tt3 = Table(compare, colWidths=[85, 165, 165])
tt3.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(1,1),(-1,-1),'Courier'),
    ('FONTSIZE',(0,0),(-1,-1),8.3),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(tt3)
spacer(10)
sec("15.2 Reading and writing files")
code('''import pathlib

path = pathlib.Path("app.js")
text = path.read_text(encoding="utf-8")   # read the whole file as a string
path.write_text("new content", encoding="utf-8")  # overwrite a file''')
sec("15.3 f-strings — Python's template literals")
code('''name = "world"
print(f"Hello, {name}!")   # "Hello, world!"  -- just like JS's `Hello, ${name}!`''')
sec("15.4 String methods used in build.py")
code('''text.replace("__CSP__", actual_csp_value)   # find-and-replace, like JS's .replace()''')
p("build.py uses this repeatedly to substitute placeholders like "
  "<font face='Courier'>/*__CSS__*/</font> inside shell.html with real file contents — see Chapter 19.")

# ---------------- Chapter 16: Git & CI/CD ----------------
chapter("16. Git & GitHub Actions — Version Control and CI/CD")
sec("16.1 Git — tracking changes over time")
p("Git is a <b>version control system</b>: it records a history of every change made to a project's files, "
  "letting you see what changed, when, and by whom — and revert if something breaks.")
bullets([
    "A <b>commit</b> is a saved snapshot of the project at one point in time, with a message describing what changed.",
    "A <b>branch</b> is an independent line of development — you can experiment on a branch without touching the main, working version.",
    "<b>Pushing</b> uploads your local commits to a remote copy (usually on GitHub); <b>pulling</b> downloads new commits from there.",
])
sec("16.2 GitHub Actions — automation that runs on every push")
p("GitHub Actions runs scripts automatically in response to events in a repository — most commonly, "
  "\"whenever someone pushes new code.\" These automated scripts are called <b>workflows</b>, and this "
  "practice — automatically building and testing code the moment it changes — is called "
  "<b>CI/CD</b> (Continuous Integration / Continuous Deployment).")
p("This project has two workflow files, each a small YAML (a simple, indentation-based configuration "
  "format) recipe of steps:")
code('''# .github/workflows/build-android.yml (simplified)
on:
  push:
    branches: [ main, claude/friendly-davinci-kz02xp ]

jobs:
  build:
    runs-on: ubuntu-latest      # a fresh Linux machine, just for this job
    steps:
      - uses: actions/checkout@v4      # download the repo's code
      - run: npm install                 # install dependencies
      - run: npm run build               # run the Python build script
      - run: npx cap sync android         # copy the built web app into the Android project
      - run: cd android && ./gradlew assembleRelease   # compile the Android app
      - uses: actions/upload-artifact@v4  # make the finished .apk downloadable''')
p("Every time code is pushed to this project's branch, GitHub spins up two temporary virtual machines "
  "(one for Android, one for iOS/macOS), each runs its recipe end to end, and the finished app files "
  "(.apk for Android, .ipa for iOS) become downloadable \"artifacts\" — with zero manual work.")

# ---------------- Chapter 17: Capacitor ----------------
chapter("17. Capacitor — Turning a Website into a Phone App")
p("Capacitor is a tool that takes a normal web app (HTML/CSS/JS) and wraps it inside a real native mobile "
  "app shell, for both iOS and Android. Concretely, it creates a native app whose entire screen is just a "
  "full-screen embedded browser (called a \"WebView\") pointed at your built HTML file. Your JavaScript "
  "keeps running exactly as it does in a normal browser tab — Capacitor's main value is packaging it as "
  "something installable from an app store, with access to native device features if needed.")
code('''// capacitor.config.json
{
  "appId": "com.example.tiffin",
  "appName": "Tiffin",
  "webDir": "dist"    // <-- tells Capacitor which folder holds the built web app
}''')
p("The workflow is: 1) build.py assembles the single dist/index.html file, "
  "2) <font face='Courier'>npx cap sync android</font> (or ios) copies that file into a native Android "
  "Studio / Xcode project template that Capacitor generated once, "
  "3) the platform's own native build tool (Gradle for Android, Xcode for iOS) compiles that into an "
  "actual installable app. This is exactly what the two GitHub Actions workflows from Chapter 16 automate.")
note("Because Tiffin already stores everything in localStorage and needs no server, wrapping it with "
     "Capacitor required almost no extra code — the same JavaScript that runs in a desktop browser tab "
     "runs unmodified inside the native app's embedded WebView.")

# ================================================================
# PART 2 — THE APP EXPLAINED
# ================================================================
part("PART 2<br/>The App, Explained End to End")
p("With that vocabulary in hand, we can now read every file in this project and understand exactly what "
  "it does and why. We'll go file by file, then work through app.js — the largest and most important file "
  "— section by section, in the order it's actually written.")

chapter("18. Project Tour — Every File and What It's For")
files_table = [
    ["File", "Language", "Job"],
    ["shell.html", "HTML", "The empty page skeleton — a few containers JS fills in"],
    ["app.css", "CSS", "All visual styling, including dark mode and responsive layout"],
    ["app.js", "JavaScript", "The entire application logic — ~1,700 lines, one big IIFE"],
    ["food_db.json", "JSON", "332 pre-loaded foods with full nutrition data"],
    ["build.py", "Python", "Glues the four files above into one dist/index.html"],
    ["package.json", "JSON", "Project metadata + npm scripts + dependency list"],
    ["capacitor.config.json", "JSON", "Tells Capacitor which folder is the built web app"],
    [".github/workflows/*.yml", "YAML", "CI/CD recipes that auto-build Android/iOS apps"],
]
tt4 = Table(files_table, colWidths=[145, 65, CONTENT_W-210])
tt4.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(1,-1),'Courier'),
    ('FONTSIZE',(0,0),(-1,-1),8.6),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(tt4)
spacer(10)
p("Notice what's <i>not</i> here: no backend server code, no database server, no API. Everything the app "
  "needs — the food database included — ships as static files, and all logic runs inside the user's own "
  "browser. This single decision shapes nearly everything else about the project (Chapter 38).")

chapter("19. The Build Pipeline — build.py Deep Dive")
p("shell.html contains four placeholder markers that aren't real HTML — they're just text build.py knows "
  "to search and replace:")
code('''<style>
/*__CSS__*/
</style>
...
<script>
const FOOD_DB = /*__FOODDB__*/;
</script>
<script>
/*__APPJS__*/
</script>''')
p("build.py reads all four source files, then does a simple find-and-replace for each placeholder, "
  "producing one giant, fully self-contained HTML file at dist/index.html — CSS, food data, and app "
  "logic all inlined directly into the page, no separate file requests needed:")
code('''shell = (ROOT / "shell.html").read_text(encoding="utf-8")
css = (ROOT / "app.css").read_text(encoding="utf-8")
appjs = (ROOT / "app.js").read_text(encoding="utf-8")
fooddb = (ROOT / "food_db.json").read_text(encoding="utf-8")

out = (
    shell.replace("__CSP__", csp)
         .replace("/*__CSS__*/", css)
         .replace("/*__FOODDB__*/", fooddb)
         .replace("/*__APPJS__*/", appjs)
)
output_path.write_text(out, encoding="utf-8")''')
p("Why bother splitting the source into 4 files just to glue them back together? <b>Developer ergonomics.</b> "
  "Editing app.js in a dedicated .js file gets you syntax highlighting, linting, and autocomplete in a code "
  "editor — none of which work well for JS embedded inside an HTML string. Splitting the source and "
  "reassembling it at build time gets the best of both: a nice editing experience, and a single "
  "zero-dependency HTML file to actually ship.")
sec("19.1 The Content-Security-Policy (CSP) — a security feature")
p("The trickiest part of build.py computes a cryptographic <b>SHA-256 hash</b> (a unique fingerprint) of "
  "the exact text inside each of the two inline <font face='Courier'>&lt;script&gt;</font> tags:")
code('''def sha256_b64(text):
    return base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode("ascii")

script_hashes = " ".join(
    f"'sha256-{sha256_b64(body)}'" for body in (fooddb_script_body, appjs_script_body)
)''')
p("This hash gets embedded into a <font face='Courier'>Content-Security-Policy</font> HTTP header/meta tag "
  "that tells the browser: \"only run inline scripts whose exact content matches one of these fingerprints — "
  "refuse to run anything else.\" If an attacker somehow injected a rogue "
  "<font face='Courier'>&lt;script&gt;</font> tag into the page (Chapter 39 explains how that could even "
  "happen), its hash wouldn't match, and the browser would simply refuse to execute it. This is a strong, "
  "defense-in-depth security measure explained fully in Chapter 39.")

chapter("20. shell.html Deep Dive")
p("Once you strip out the placeholders, shell.html is almost nothing — deliberately so:")
code('''<div class="topbar">...</div>                <!-- mobile-only top bar -->
<div class="app">
  <nav class="sidenav" id="sideNav"></nav>       <!-- EMPTY — JS fills this -->
  <main class="main">
    <div id="viewRoot"></div>                     <!-- EMPTY — JS fills this -->
  </main>
</div>
<nav class="bottomnav" id="bottomNav"></nav>       <!-- EMPTY — JS fills this -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal" id="modalContent"></div>       <!-- EMPTY — JS fills this -->
</div>
<div class="toast-wrap" id="toastWrap"></div>        <!-- EMPTY — JS fills this -->''')
p("Five containers, each with an <font face='Courier'>id</font>, and every single one starts completely "
  "empty. This is the hallmark of a JavaScript-driven single page app: HTML provides only the <i>slots</i>; "
  "JavaScript generates 100% of what actually appears inside them, and keeps regenerating it as the app's "
  "data changes. We'll see exactly how in Chapter 28.")

chapter("21. app.css Deep Dive")
sec("21.1 Design tokens and dark mode, revisited")
p("Recall from Chapter 3 that CSS variables let you name a value once and reuse it everywhere. app.css "
  "defines its full palette under <font face='Courier'>:root</font>, then <i>redefines the exact same "
  "variable names</i> inside a dark-mode block:")
code(''':root {
  --paper: #FBF3E7;   /* warm cream background */
  --text: #241C12;    /* near-black text */
  --accent: #FF6B4A;  /* the brand orange */
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #161210;  /* near-black background */
    --text: #F5ECDF;   /* warm off-white text */
    --accent: #FF7D5E; /* a slightly brighter orange, for contrast on dark */
  }
}

:root[data-theme="dark"] {
  /* the SAME dark values, but applied whenever the app's own theme setting
     is explicitly "dark" — regardless of the OS setting */
  --paper: #161210; --text: #F5ECDF; --accent: #FF7D5E;
}''')
p("Three theme states are supported: <b>system</b> (follow the OS's light/dark preference automatically, "
  "via the <font face='Courier'>@media (prefers-color-scheme: dark)</font> query), or an explicit "
  "<b>light</b> / <b>dark</b> override, applied by JavaScript setting a "
  "<font face='Courier'>data-theme</font> attribute on the <font face='Courier'>&lt;html&gt;</font> element "
  "(Chapter 35 shows the JS side of this). Not one other CSS rule in the whole file needs to know or care "
  "which theme is active — they all just say <font face='Courier'>color: var(--text)</font>, and the "
  "variable's current value does the rest.")
sec("21.2 Mobile vs desktop layout")
p("Recall the media query pattern from Chapter 3.6. app.css uses exactly one breakpoint, 860px, to switch "
  "between a desktop sidebar and a mobile bottom tab bar:")
code('''.sidenav { width: 216px; /* ...desktop sidebar styles... */ }
.bottomnav { display: none; /* hidden by default (desktop) */ }

@media (max-width: 860px) {
  .sidenav { display: none; }     /* hide sidebar on narrow screens */
  .bottomnav { display: flex; }    /* show the tab bar instead */
  .topbar { display: flex; }       /* show the mobile top bar */
}''')
p("Both navigation elements exist in the HTML at all times — CSS alone decides which one is visible, "
  "based purely on the browser window's width, no JavaScript involved.")
sec("21.3 Reduced motion accessibility")
code('''@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .001ms !important;
    transition-duration: .001ms !important;
  }
}''')
p("Some users configure their OS to minimize animations (often for motion-sensitivity/vestibular reasons). "
  "This query respects that system preference by effectively disabling all CSS animations and transitions "
  "for them, app-wide, in one rule.")

chapter("22. food_db.json Deep Dive")
p("This file is a single JSON array containing 332 food objects. Every object has the exact same set of "
  "keys — the same 44 nutrient fields, always present (even if zero), plus a few descriptive fields:")
code('''{
  "id": "rice-cooked-white",
  "name": "Rice, cooked (Chawal, white)",
  "category": "Indian",
  "servingLabel": "1 cup",
  "servingGrams": 150,
  "kcal": 200,
  "protein": 4.2,
  "carbs": 44,
  "fat": 0.4,
  "satFat": 0.1,
  "fiber": 0.6,
  ... (continues through all 44 nutrients — vitamins, minerals, fats, etc.)
}''')
bullets([
    "<font face='Courier'>id</font> — a unique, human-readable identifier (used to reference this food from the diary, never the display name, since names could change).",
    "<font face='Courier'>category</font> — 'Indian' or 'International', used for the filter chips in the Foods tab.",
    "<font face='Courier'>servingLabel</font> / <font face='Courier'>servingGrams</font> — a human-friendly serving description (\"1 cup\") paired with its weight in grams, so any other serving size can be computed proportionally.",
    "Every other key matches one entry in the app's own <font face='Courier'>NUTRIENT_KEYS</font> list (Chapter 23) — this consistency is what lets the same generic nutrient-math functions work identically on every food.",
])
note("This file is loaded once, embedded directly as a JS array literal via build.py's "
     "<font face='Courier'>__FOODDB__</font> placeholder (Chapter 19) — there's no network request to fetch "
     "it at runtime, which is why the app works completely offline.")

chapter("23. app.js Part 1 — Setup & The Shape of the Data")
p("Everything from here through Chapter 37 walks through app.js top to bottom. Line numbers refer to the "
  "actual file in this repository.")
sec("23.1 The wrapper (lines 1-8)")
code('''(function(){
"use strict";''')
p("As explained in Chapter 10.3, this is an IIFE: it isolates every name the app defines from the rest of "
  "the page, and turns on JavaScript's strict mode.")
sec("23.2 Icons (lines 9-27)")
p("An object literal, <font face='Courier'>ICON</font>, mapping short names like "
  "<font face='Courier'>home</font>, <font face='Courier'>flame</font>, <font face='Courier'>x</font> to "
  "raw SVG markup strings. Recall from Chapter 2 that <font face='Courier'>&lt;svg&gt;</font> draws vector "
  "graphics directly in markup — no image files are downloaded for any icon in this app; they're all just "
  "text, embedded directly into whatever HTML string needs them, e.g. <font face='Courier'>${ICON.flame}</font>.")
sec("23.3 Constants (lines 29-114)")
code('''const STORAGE_KEY = 'tiffin_state_v1';   // the localStorage key everything is saved under

const NUTRIENT_KEYS = [
  'kcal','protein','carbs','fat','satFat','fiber','sugar','sodium', ...  // all 44, by name
];''')
p("<font face='Courier'>NUTRIENT_KEYS</font> is the single source of truth for \"what nutrients does this "
  "app track?\" — every nutrient-math function (Chapter 25) loops over this list rather than hardcoding "
  "44 separate lines, so adding a 45th nutrient in the future would mean editing this one list, not every "
  "function in the file.")
code('''const NUTRIENT_GROUPS = [
  {title:'Macros', rows:[
    ['protein','Protein','g','proteinGoal'],
    ['carbs','Carbohydrates','g','carbGoal'],
    ['fat','Fat','g','fatGoal'],
    ...
  ]},
  {title:'Vitamins', rows:[ ... ]},
  {title:'Minerals', rows:[ ... ]},
  ...
];''')
p("<font face='Courier'>NUTRIENT_GROUPS</font> is a richer structure used purely for display: it groups "
  "related nutrients under headings (Macros, Vitamins, Minerals...) and, per nutrient, bundles its internal "
  "key, its human-readable label, its unit, and which goal setting (if any) it's measured against. This one "
  "list drives both the Nutrients tab (Chapter 27) and the custom-food-entry form (Chapter 29) — define a "
  "nutrient's metadata once, get two different screens generated from it automatically.")
code('''const FIXED_TARGETS = {
  addedSugarLimit: 50, omega3AlaGoal: 1.4,
  vitB1Goal: 1.2, vitB2Goal: 1.3, ... // general adult nutrition reference values
};

const ACTIVITY_MULT = {sedentary:1.2, light:1.375, moderate:1.55, active:1.725, very_active:1.9};

const DEFAULT_GOALS = {
  calorieGoal: 2000, proteinGoal: 100, carbGoal: 250, fatGoal: 65, ...
};''')
p("<font face='Courier'>FIXED_TARGETS</font> holds general recommended daily amounts (for nutrients too "
  "obscure to let users customize) — merged in at display time, never stored per-user. "
  "<font face='Courier'>ACTIVITY_MULT</font> holds the standard multipliers used in the Mifflin-St Jeor "
  "energy formula (Chapter 26). <font face='Courier'>DEFAULT_GOALS</font> is what a brand-new user starts "
  "with before they customize anything in Profile.")
sec("23.4 Default-state factory functions (lines 116-133)")
code('''function defaultMealSlots(){
  return [
    {id:'meal-1', name:'Meal 1', emoji:'🍳'},
    {id:'meal-2', name:'Meal 2', emoji:'🍚'},
    ... // 5 meals by default
  ];
}
function defaultProfile(){
  return { name:'', sex:null, age:null, heightCm:null, ... };
}
function defaultState(){
  return {
    goals: {...DEFAULT_GOALS}, profile: defaultProfile(), diary: {}, weightLog: [],
    customFoods: [], customMeals: [], barcodeMap: {}, mealSlots: defaultMealSlots(),
  };
}''')
p("Notice each of these is a <i>function that returns a fresh object</i>, not a shared constant object. "
  "This matters: if <font face='Courier'>defaultState()</font> were instead one constant object reused "
  "everywhere, every new user (and the \"Reset all data\" feature, Chapter 35) would end up sharing and "
  "accidentally mutating the exact same object in memory. Calling a function guarantees a brand new, "
  "independent copy every time.")
p("This block also defines the complete shape of the app's data: goals (calorie/macro targets), profile "
  "(the user's body stats), diary (a dictionary of date &#8594; meals eaten), weightLog (an array of "
  "weigh-ins), customFoods / customMeals (anything the user created themselves), barcodeMap (barcode "
  "numbers linked to specific foods), and mealSlots (the user's customizable list of meal names, replacing "
  "a fixed \"Breakfast/Lunch/Dinner\" scheme).")

chapter("24. app.js Part 2 — Storage & Security")
sec("24.1 Loading and saving (lines 150-190)")
code('''let STATE = loadState();   // <-- the app's ENTIRE data lives in this one variable

function saveState(){
  try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(STATE)); }
  catch(e){ storageOk = false; }
}''')
p("This is the pattern from Chapter 13, applied to the whole app's data at once. Every single place in "
  "app.js that changes something — adding a food, logging weight, changing a setting — calls "
  "<font face='Courier'>saveState()</font> immediately afterward. There is no \"Save\" button for the app "
  "as a whole; changes are persisted the instant they happen.")
p("The <font face='Courier'>try/catch</font> matters because <font face='Courier'>localStorage</font> can "
  "fail — private/incognito browsing sometimes disables it entirely, or storage could be full. Rather than "
  "crash, the app sets a flag (<font face='Courier'>storageOk = false</font>) and later warns the user "
  "their data won't be saved, so they know to back it up manually (Chapter 35).")
sec("24.2 mergeKnownFields — a security-conscious loader")
p("This is the single most important function to understand for interview purposes, because it fixes a "
  "real, named security vulnerability class. Read the code and its own comment carefully:")
code('''// Copies only keys already present on `defaults` from `source`, so a
// stored/imported JSON blob can never introduce arbitrary keys (including
// "__proto__", which Object.assign(target, source) would otherwise use to
// repoint target's prototype -- CWE-1321 prototype pollution).
function mergeKnownFields(defaults, source){
  const out = Object.assign({}, defaults);
  if(source && typeof source === 'object'){
    Object.keys(defaults).forEach(k=>{
      if(Object.prototype.hasOwnProperty.call(source, k)) out[k] = source[k];
    });
  }
  return out;
}''')
p("This deserves the full explanation, because it's exactly the kind of thing an interviewer will probe. "
  "The naive way to merge \"saved settings\" over \"default settings\" would be:")
code('''const merged = Object.assign({}, defaults, source);  // DANGEROUS with untrusted `source`''')
p("The problem: every JavaScript object secretly has a hidden <font face='Courier'>__proto__</font> "
  "property pointing to its prototype (the object it inherits shared behavior from). If "
  "<font face='Courier'>source</font> came from untrusted JSON — like an imported backup file someone could "
  "hand-edit, or in principle data planted by an attacker — and that JSON contained a key literally named "
  "<font face='Courier'>\"__proto__\"</font>, a naive <font face='Courier'>Object.assign</font> would "
  "follow it and let the attacker inject properties onto Object.prototype itself, corrupting the behavior "
  "of <i>every</i> object in the entire running app. This class of bug has an official name and ID: "
  "<b>CWE-1321, Prototype Pollution</b>.")
p("<font face='Courier'>mergeKnownFields</font> defends against this in two ways at once: (1) it only ever "
  "copies keys that already exist on <font face='Courier'>defaults</font> — since "
  "<font face='Courier'>defaults</font> is always a hardcoded object this app itself wrote, "
  "<font face='Courier'>\"__proto__\"</font> is never one of its keys, so the loop simply never looks at "
  "it; and (2) it uses <font face='Courier'>Object.prototype.hasOwnProperty.call(source, k)</font> rather "
  "than the simpler <font face='Courier'>source.hasOwnProperty(k)</font> or <font face='Courier'>k in "
  "source</font> — the former can itself be spoofed if <font face='Courier'>source</font> has been tampered "
  "with to no longer inherit the normal Object prototype; calling the trusted, original method explicitly "
  "sidesteps that.")
p("This function is used in two places: loading state from localStorage on startup (which, strictly, is "
  "data the app itself wrote, so lower risk) and importing a backup file the user selects (Chapter 35) — "
  "the more realistic risk, since backup files could be shared, edited, or come from an untrusted source.")
sec("24.3 Legacy data migration")
p("loadState() also contains a one-time migration for users who had the app before \"meal slots\" became "
  "customizable, converting their old fixed <font face='Courier'>breakfast/lunch/dinner/snacks</font> keys "
  "into the new generic <font face='Courier'>meal-1/meal-2/...</font> scheme automatically, so nobody's "
  "existing diary history is lost when the app is updated.")

chapter("25. app.js Part 3 — Utility & Math Functions")
sec("25.1 General-purpose helpers (lines 193-210)")
code('''function uid(){ return Math.random().toString(36).slice(2,9); }
function round1(n){ return Math.round((n + Number.EPSILON) * 10) / 10; }
function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({...}[c])); }''')
bullets([
    "<font face='Courier'>uid()</font> generates a short random ID — used for every custom food, custom "
    "meal, and meal slot the user creates, so each can be referenced uniquely.",
    "<font face='Courier'>round1()</font> rounds to 1 decimal place, used for nearly every displayed number.",
    "<font face='Courier'>clamp(v, a, b)</font> forces a value to stay between a and b (used to keep progress "
    "bars from visually overflowing past 100%).",
    "<font face='Courier'>escapeHtml()</font> is Tiffin's central XSS defense — full explanation in Chapter 39.",
])
sec("25.2 Date helpers")
code('''function toKey(d){ return d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate()); }
function todayKey(){ return toKey(new Date()); }
function addDaysKey(key, delta){ const d = keyToDate(key); d.setDate(d.getDate()+delta); return toKey(d); }''')
p("The whole app represents a date not as a JavaScript Date object, but as a plain string key like "
  "<font face='Courier'>'2024-09-17'</font>. This makes it trivially usable as an object key (for the diary, "
  "see Chapter 26) and easy to compare/sort as plain strings, while still allowing arithmetic (\"give me "
  "yesterday\") by briefly converting back to a real Date object, changing it, and converting back to a key.")
sec("25.3 Nutrient math — the core arithmetic of the whole app")
code('''function zeroNutrients(){
  const o = {}; NUTRIENT_KEYS.forEach(k=>o[k]=0); return o;
}
function scaleNutrients(base, qty){
  const o = {}; NUTRIENT_KEYS.forEach(k=> o[k] = (base[k]||0) * qty); return o;
}
function addNutrients(a,b){
  const o = {}; NUTRIENT_KEYS.forEach(k=> o[k] = (a[k]||0) + (b[k]||0)); return o;
}''')
p("These three tiny functions are the mathematical foundation everything else builds on, and they're a "
  "perfect example of the <font face='Courier'>NUTRIENT_KEYS</font> list paying off (Chapter 23.3): instead "
  "of 44 lines of <font face='Courier'>o.protein = a.protein + b.protein; o.carbs = a.carbs + b.carbs; ...</font>, "
  "one loop handles every current and future nutrient identically.")
bullets([
    "<font face='Courier'>zeroNutrients()</font> — an empty starting point (everything 0), used as the "
    "running total before summing a day's meals.",
    "<font face='Courier'>scaleNutrients(base, qty)</font> — multiplies every nutrient by a quantity, e.g. "
    "\"1.5 servings of rice\" scales rice's per-serving nutrients by 1.5.",
    "<font face='Courier'>addNutrients(a, b)</font> — adds two nutrient sets together, key by key, e.g. "
    "combining breakfast's total with lunch's total.",
])
sec("25.4 Resolving a \"reference\" into actual nutrition data")
p("A logged diary entry doesn't store a copy of a food's nutrients — it stores a lightweight "
  "<i>reference</i>: <font face='Courier'>{type: 'db', id: 'rice-cooked-white'}</font> plus how many "
  "servings. This keeps the diary small and means editing a custom food's nutrition later automatically "
  "updates every past log entry that referenced it.")
code('''function resolveRefBase(ref){
  if(!ref) return null;
  if(ref.type === 'db'){
    const f = dbFoodById(ref.id); if(!f) return null;
    return {name:f.name, servingLabel:f.servingLabel, servingGrams:f.servingGrams, nutrients:f, ...};
  }
  if(ref.type === 'custom'){ ... }
  if(ref.type === 'meal'){
    // a custom "meal" (recipe) is a LIST of other refs -- resolve each ingredient
    // recursively and sum them together
    let n = zeroNutrients(); let grams = 0;
    m.items.forEach(it=>{
      const b = resolveRefBase(it.ref);
      if(!b) return;
      n = addNutrients(n, scaleNutrients(b.nutrients, it.qty));
      grams += (b.servingGrams||0) * it.qty;
    });
    return {name:m.name, servingLabel:'1 recipe', servingGrams:grams, nutrients:n, ...};
  }
  return null;
}''')
p("There are exactly three kinds of reference: <font face='Courier'>'db'</font> (one of the 332 built-in "
  "foods), <font face='Courier'>'custom'</font> (a food the user created), and "
  "<font face='Courier'>'meal'</font> (a custom recipe made of several other foods). The "
  "<font face='Courier'>'meal'</font> case is recursive — it calls "
  "<font face='Courier'>resolveRefBase</font> again on each of its own ingredients — which correctly "
  "handles a recipe containing several ingredients, each individually looked up and summed, in one small "
  "function.")

chapter("26. app.js Part 4 — The Diary & Meal System")
p("Recall from Chapter 23 that <font face='Courier'>STATE.diary</font> is an object mapping date-key "
  "strings to that day's data:")
code('''STATE.diary = {
  '2024-09-17': {
    'meal-1': [ {ref:{type:'db', id:'rice-cooked-white'}, qty: 1.5}, ... ],
    'meal-2': [ ... ],
    water: 2000,       // ml logged
    workouts: [ {name:'Run', duration:30} ]
  },
  '2024-09-16': { ... }
};''')
code('''function getDay(key){
  if(!STATE.diary[key]) STATE.diary[key] = {};
  const d = STATE.diary[key];
  STATE.mealSlots.forEach(s=>{ if(!d[s.id]) d[s.id] = []; });
  if(typeof d.water !== 'number') d.water = 0;
  if(!Array.isArray(d.workouts)) d.workouts = [];
  return d;
}''')
p("<font face='Courier'>getDay()</font> is a \"get-or-create\" function — a very common pattern. Rather "
  "than every caller checking \"does today's entry exist yet?\", this one function guarantees a fully-formed "
  "day object always comes back, creating and filling in any missing pieces (each meal slot's empty array, "
  "a zero water total, an empty workout list) on the fly. This also means adding a brand new meal slot "
  "later still works for old diary days that were created before that slot existed — <font face='Courier'>"
  "getDay()</font> patches it in automatically.")
code('''function dayTotals(key){
  const d = getDay(key);
  let total = zeroNutrients();
  STATE.mealSlots.forEach(s=>{
    (d[s.id]||[]).forEach(entry=>{ total = addNutrients(total, entryNutrients(entry)); });
  });
  return total;
}''')
p("<font face='Courier'>dayTotals()</font> combines everything from Chapter 25: for every meal slot, for "
  "every entry logged in it, resolve its nutrients (scaled by quantity) and fold it into a running total "
  "with <font face='Courier'>addNutrients</font>. This one function powers the calorie ring, the macro "
  "bars, and the entire Nutrients tab.")
code('''function computeStreak(){
  let d = todayKey();
  if(!dayHasEntries(d)) d = addDaysKey(d,-1);   // don't break the streak just because
                                                    // today hasn't been logged YET
  let count = 0;
  while(dayHasEntries(d)){ count++; d = addDaysKey(d,-1); }
  return count;
}''')
p("The \"logging streak\" (shown as a flame icon + number) counts consecutive days backward from today "
  "that have at least one food logged. The small but thoughtful detail: if <i>today</i> has nothing logged "
  "yet, it starts counting from yesterday instead — so your streak doesn't visually reset to zero first "
  "thing in the morning before you've had a chance to log breakfast.")

chapter("27. app.js Part 5 — Energy Calculations (BMR/TDEE)")
p("This section implements real nutrition science: the <b>Mifflin-St Jeor equation</b>, a widely-used "
  "formula for estimating how many calories someone burns per day at rest.")
code('''function calcBMR(){
  const p = STATE.profile;
  if(!p.sex || !p.age || !p.heightCm) return null;  // can't calculate without these
  const weight = latestWeightKg();
  if(weight == null) return null;
  const s = p.sex === 'male' ? 5 : -161;
  return 10*weight + 6.25*p.heightCm - 5*p.age + s;
}''')
p("BMR (Basal Metabolic Rate) is roughly \"calories burned just to stay alive, lying still all day.\" The "
  "formula needs weight (kg), height (cm), age (years), and biological sex (the sole reason this formula "
  "needs it: average differences in body composition), each multiplied by its own scientifically-derived "
  "coefficient. Note the guard clauses at the top: if any required profile field is missing, the function "
  "returns <font face='Courier'>null</font> rather than calculating with garbage/missing data — and every "
  "caller of this function is expected to check for that <font face='Courier'>null</font> before using the "
  "result (Chapter 31 shows the UI's fallback message when it's missing).")
code('''function calcTDEE(){
  const bmr = calcBMR(); if(bmr == null) return null;
  const mult = ACTIVITY_MULT[STATE.profile.activityLevel || 'moderate'];
  return bmr * mult;
}''')
p("TDEE (Total Daily Energy Expenditure) scales BMR up by an activity multiplier (from Chapter 23.3's "
  "<font face='Courier'>ACTIVITY_MULT</font>) to account for exercise and daily movement — someone who's "
  "very active burns meaningfully more than their BMR alone.")
code('''function calculateTargetsFromProfile(){
  const bmr = calcBMR();
  if(bmr == null){ toast('Add your sex, age, and height in Profile first.'); return; }
  const weight = latestWeightKg();
  const tdee = calcTDEE();
  const p = STATE.profile;
  const dailyAdj = ((p.weeklyRateKg||0) * 7700) / 7;   // 7700 kcal ~= 1 kg of body fat
  let calorieGoal = tdee;
  if(p.goalType === 'cut') calorieGoal = tdee - dailyAdj;
  else if(p.goalType === 'bulk') calorieGoal = tdee + dailyAdj;
  calorieGoal = Math.max(1200, Math.round(calorieGoal));  // never recommend below 1200 kcal
  const proteinPerKg = p.goalType === 'cut' ? 2.0 : 1.8;
  const proteinGoal = Math.round(weight * proteinPerKg);
  const fatGoal = Math.round(calorieGoal*0.25/9);          // ~25% of calories from fat (9 kcal/g)
  const carbGoal = Math.max(0, Math.round((calorieGoal - proteinGoal*4 - fatGoal*9)/4));  // remainder as carbs
  ...
}''')
p("This function turns the science into an actionable set of daily goals with one button click "
  "(\"Calculate my targets\", Chapter 31). It uses the well-known approximation that roughly 7,700 kcal of "
  "sustained surplus or deficit corresponds to about 1 kg of body weight change, to translate a user's "
  "desired weekly rate of loss/gain into a daily calorie adjustment. It sets protein higher (per kg of "
  "bodyweight) during a \"cut\" (calorie deficit) than during maintenance or a \"bulk,\" reflecting real "
  "nutrition guidance to preserve muscle while losing fat. Fat and carbs are then derived from what's left "
  "of the calorie budget, using the standard calorie-per-gram figures (9 kcal/g fat, 4 kcal/g carbs/protein). "
  "Note the safety floor: <font face='Courier'>Math.max(1200, ...)</font> refuses to ever suggest a "
  "dangerously low calorie target, regardless of what the math alone would produce.")

chapter("28. app.js Part 6 — The Rendering System")
p("This is the architectural core of the whole UI, and it's worth understanding deeply, because it's the "
  "pattern that replaces what a framework like React would normally provide.")
code('''function renderApp(){ renderShell(); renderView(); }

function renderShell(){
  document.getElementById('sideNav').innerHTML = `...`;   // nav, streak, theme buttons
  document.getElementById('bottomNav').innerHTML = renderNav();
  document.getElementById('topbarTitle').textContent = ({...})[currentView];
}

function renderView(){
  const root = document.getElementById('viewRoot');
  let html = '';
  if(currentView === 'today') html = renderToday();
  else if(currentView === 'foods') html = renderFoodsView();
  else if(currentView === 'progress') html = renderProgressView();
  else if(currentView === 'nutrients') html = renderNutrientsView();
  else if(currentView === 'profile') html = renderProfileView();
  root.innerHTML = `<div class="fade-in">${html}</div>`;
}''')
p("The pattern, in one sentence: <b>every render function is a pure function that takes the current "
  "STATE and returns an HTML string</b> — it reads data, builds a template-literal string full of "
  "<font face='Courier'>${...}</font> interpolations, and hands it back. Nothing inside "
  "<font face='Courier'>renderToday()</font>, for instance, ever touches the DOM directly; it just returns "
  "text. The <i>caller</i> — <font face='Courier'>renderView()</font> — is the only place that actually "
  "assigns to <font face='Courier'>.innerHTML</font>, replacing everything inside "
  "<font face='Courier'>#viewRoot</font> in one shot.")
sec("28.1 The render cycle — how a click becomes a screen update")
p("This five-step loop happens every single time the user does anything at all in this app:")
bullets([
    "<b>1.</b> User clicks/types/submits something.",
    "<b>2.</b> The event delegation system (Chapter 36) figures out what action that corresponds to.",
    "<b>3.</b> The handler code directly mutates <font face='Courier'>STATE</font> (e.g. pushes a new entry "
    "into today's meal array).",
    "<b>4.</b> The handler calls <font face='Courier'>saveState()</font> (persists to localStorage) and then "
    "<font face='Courier'>renderView()</font> or <font face='Courier'>renderApp()</font>.",
    "<b>5.</b> The relevant render function reads the now-updated <font face='Courier'>STATE</font> and "
    "regenerates the HTML from scratch; the browser updates the screen.",
])
note("This is a much simpler, hand-rolled version of the same idea frameworks like React are built around: "
     "\"the UI is a function of state.\" The tradeoff for not using a real framework is efficiency — Tiffin "
     "regenerates and replaces entire chunks of HTML on every change (no fine-grained diffing), which is "
     "wasteful in theory, but for an app this size, running on a modern device, it's fast enough to be "
     "invisible to the user, and it comes with zero framework dependency and near-zero build tooling. "
     "This is a real, defensible trade-off — see Chapter 38.")
sec("28.2 Lazy-loading Chart.js")
code('''function ensureChartLoaded(cb){
  if(typeof Chart !== 'undefined'){ cb(); return; }           // already loaded, run callback now
  if(chartLoadState === 'loading'){ /* wait and retry */ return; }
  chartLoadState = 'loading';
  const s = document.createElement('script');
  s.src = CHART_CDN_URL;
  s.onload = ()=>{ chartLoadState='loaded'; cb(); };
  s.onerror = ()=>{ chartLoadState='error'; cb(); };
  document.head.appendChild(s);
}''')
p("Rather than always loading the (fairly large) Chart.js library up front, the app only fetches it the "
  "first time the user opens the Progress tab, by dynamically creating a "
  "<font face='Courier'>&lt;script&gt;</font> element pointed at a CDN URL and inserting it into the page. "
  "It tracks loading state so simultaneous or repeated requests don't trigger duplicate downloads, and "
  "handles the failure case (no internet) gracefully by still calling the callback, which then shows a "
  "\"chart unavailable\" fallback instead of crashing.")

chapter("29. app.js Part 7 — The Today (Home) View")
p("<font face='Courier'>renderToday()</font> is the single most complex render function, and a good "
  "example of composing several smaller render functions together:")
code('''function renderToday(){
  const totals = dayTotals(currentDate);
  ...
  const macroRows = [
    barRow('Protein', totals.protein, g.proteinGoal, 'g'),
    barRow('Carbs', totals.carbs, g.carbGoal, 'g'),
    barRow('Fat', totals.fat, g.fatGoal, 'g'),
  ].join('');

  const mealSections = STATE.mealSlots.map(slot=>{
    const items = day[slot.id] || [];
    const rows = items.length ? items.map((entry, idx) => `...`).join('') : `<div class="meal-empty">...</div>`;
    return `<div class="meal-card">...${rows}...</div>`;
  }).join('');

  return `
    ${dateNavHtml()}
    <div class="card">
      ${ringSvg(kcalPct, fillColor)}
      <div class="macro-rows">${macroRows}</div>
    </div>
    ${waterCardHtml()}
    ${workoutCardHtml()}
    ${mealSections}
  `;
}''')
p("Every piece — the date navigator, the calorie ring, the macro bars, the water card, the workout card, "
  "each meal card — is its own small function returning its own HTML fragment. "
  "<font face='Courier'>renderToday()</font>'s only job is to call each one and stitch the results together "
  "with template literals. This mirrors \"component composition\" from frameworks, just without any "
  "framework machinery behind it — a function returning a string <i>is</i> the component.")
sec("29.1 The SVG progress ring")
code('''function ringSvg(pct, fillColor){
  const size=200, cx=size/2, cy=size/2, r=84;
  const circumference = 2*Math.PI*r;
  const p = clamp(pct,0,1);
  const dash = circumference*p;
  return `<svg viewBox="0 0 ${size} ${size}" style="transform:rotate(-90deg);">
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="var(--surface-2)" stroke-width="16"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${fillColor}" stroke-width="16"
            stroke-dasharray="${dash} ${circumference}"/>
  </svg>`;
}''')
p("This is a classic SVG trick for drawing a progress ring without any image or canvas drawing: draw a "
  "full circle twice — once as a plain gray \"track\", then again on top with a dashed stroke pattern where "
  "the first \"dash\" length equals <i>percentage complete &#215; the circle's full circumference</i> and "
  "the second number is the remainder, which SVG then renders as one continuous colored arc covering "
  "exactly that percentage of the circle. Rotating the whole SVG -90 degrees makes the arc start from the "
  "top (12 o'clock) instead of SVG's default 3 o'clock starting point.")

chapter("30. app.js Part 8 — The Food Picker Flow")
p("Adding a food is a small multi-step \"wizard\" flow, entirely modeled as one JavaScript object, "
  "<font face='Courier'>picker</font>, that gets read and mutated as the user moves through it:")
code('''function openPicker(opts){
  picker = Object.assign({
    step:'list', query:'', cat:'All', meal:null, dateKey:currentDate,
    cart: [], activeRef:null, activeUnit:'medium', activeAmount:1, ...
  }, opts||{});
  renderPickerModal();
}
function renderPickerModal(){
  if(!picker) return;
  const html = picker.step === 'list' ? renderListStep() : renderServingStep();
  openModalHtml(html, 'generic');
}''')
p("<font face='Courier'>picker.step</font> is a simple state machine with two states: "
  "<font face='Courier'>'list'</font> (search and browse foods) and "
  "<font face='Courier'>'serving'</font> (pick a quantity for one selected food). "
  "<font face='Courier'>renderPickerModal()</font> just checks which step it's in and calls the matching "
  "render function — the exact same \"render function reads state, returns HTML\" pattern from Chapter 28, "
  "scoped down to a modal instead of a whole page.")
p("The picker also supports a shopping-cart-like flow: tapping a food doesn't immediately log it — it "
  "walks you to the serving-size step, then back to the list (with that food now shown in a running "
  "\"Added so far\" cart), so you can add several foods to one meal in a row before finally hitting "
  "\"Finish\" to commit them all to the diary at once:")
code('''if(action === 'picker-finish'){
  const meal = picker.meal || STATE.mealSlots[0].id;
  const day = getDay(picker.dateKey);
  picker.cart.forEach(item=>{
    const base = resolveRefBase(item.ref);
    const qty = base && base.servingGrams>0 ? item.grams/base.servingGrams : 1;
    day[meal].push({ref:item.ref, qty});
  });
  saveState(); closeModal();
  renderView();
}''')
p("The same underlying <font face='Courier'>picker</font> object is reused for several related flows by "
  "just changing its starting options: <font face='Courier'>singleMode</font> (skip the cart, add "
  "immediately — used by the Foods tab's \"quick add\"), editing an existing entry (pre-fill "
  "<font face='Courier'>editMeal</font>/<font face='Courier'>editIndex</font> so \"Add\" becomes \"Save\" "
  "and replaces the old entry instead of creating a new one), and <font face='Courier'>linkOnly</font> "
  "(used when linking a scanned barcode to an existing food, Chapter 34, where picking a food should link "
  "it rather than log it).")

chapter("31. app.js Part 9 — Custom Foods & Custom Meals")
p("A custom food form dynamically generates one input field per nutrient, reusing "
  "<font face='Courier'>NUTRIENT_GROUPS</font> from Chapter 23 so the form's organization exactly matches "
  "the Nutrients tab's organization:")
code('''function customFoodNutrientFieldsHtml(){
  return NUTRIENT_GROUPS.map(grp=>{
    const rows = grp.rows.filter(([key])=> !CUSTOM_FOOD_PRIMARY_KEYS.includes(key));
    ...
    return `<details class="settings-group"><summary>${grp.title}</summary>${pairsHtml}</details>`;
  }).join('');
}''')
p("(<font face='Courier'>&lt;details&gt;</font>/<font face='Courier'>&lt;summary&gt;</font> is a native "
  "HTML element pair that creates a collapsible section with zero JavaScript needed — clicking the summary "
  "text toggles it open/closed automatically, which is why this appears nowhere in the event-handling "
  "chapter.) Calories, protein, carbs, and fat are excluded from this generated list because they're always "
  "shown as separate, prominent fields at the top of the form — everything else (all ~40 vitamins/minerals/"
  "fat-subtypes) is generated.")
code('''function handleCustomFoodSubmit(form){
  const fd = new FormData(form);
  const name = (fd.get('name')||'').toString().trim();
  if(!name){ toast('Please name this food.'); return; }
  const num = (k, d)=>{ const v = parseFloat(fd.get(k)); return isNaN(v) ? d : v; };
  const food = { id: 'custom-'+uid(), name, category:'Custom', ... };
  NUTRIENT_KEYS.forEach(k=> food[k] = num(k, 0));
  STATE.customFoods.push(food);
  saveState(); closeModal(); renderView();
}''')
p("<font face='Courier'>FormData</font> is a built-in browser API that reads every named input inside a "
  "<font face='Courier'>&lt;form&gt;</font> at once, keyed by each input's <font face='Courier'>name</font> "
  "attribute — much simpler than manually querying and reading dozens of individual input elements. The "
  "small inline helper <font face='Courier'>num(k, d)</font> parses a field as a number and falls back to a "
  "default <font face='Courier'>d</font> if it's empty or invalid, so a nutrient field left blank quietly "
  "becomes 0 rather than <font face='Courier'>NaN</font> corrupting later math.")
sec("31.1 Custom meals (recipes)")
p("A custom meal is built interactively: search for an ingredient, tap it to add it to the recipe, repeat, "
  "then save. Recall from Chapter 25.4 that a meal reference resolves recursively — so once saved, a custom "
  "meal behaves exactly like any other loggable food everywhere else in the app, including being usable as "
  "an ingredient in searches, but not nestable inside another custom meal (the picker explicitly filters "
  "meal-type items out of the ingredient search to prevent that).")

chapter("32. app.js Part 10 — Progress View & Charts")
p("The weight-trend chart is a thin wrapper around the Chart.js library introduced in Chapter 14 and "
  "lazy-loaded in Chapter 28.2:")
code('''function renderWeightChartNow(){
  const canvas = document.getElementById('weightChart');
  if(typeof Chart === 'undefined'){ /* show fallback text instead */ return; }
  const log = [...STATE.weightLog].sort((a,b)=> a.date < b.date ? -1 : 1);
  const labels = log.map(w=>w.date.slice(5));
  const data = log.map(w=> round1(toDisplayWeight(w.kg)));
  if(weightChart){ weightChart.destroy(); weightChart = null; }  // clean up the old chart first!
  weightChart = new Chart(canvas.getContext('2d'), {
    type:'line',
    data:{ labels, datasets:[ {label:'Weight', data, ...}, ...(goal!=null ? [{label:'Goal', ...}] : []) ] },
    options:{ responsive:true, ... }
  });
}''')
p("Two details worth knowing for an interview: (1) <font face='Courier'>weightChart.destroy()</font> is "
  "called before creating a new chart instance — Chart.js attaches its own internal event listeners and "
  "canvas state to each chart object, and failing to destroy the old one before replacing it (which happens "
  "every time this view re-renders) would leak memory and cause visual glitches over time; and (2) the "
  "optional goal-line dataset is added conditionally using the spread-into-array trick from Chapter 8.3 — "
  "<font face='Courier'>...(goal!=null ? [{...}] : [])</font> spreads in either one extra dataset object or "
  "nothing at all, cleanly avoiding an <font face='Courier'>if</font> statement in the middle of an object "
  "literal (which isn't syntactically possible in JavaScript).")
p("The chart's colors are read directly from the current CSS variables (via the "
  "<font face='Courier'>css()</font> helper from Chapter 23) so the chart automatically matches whichever "
  "theme — light or dark — is currently active, without any separate \"chart theme\" configuration.")

chapter("33. app.js Part 11 — Profile View")
p("The Profile view is the largest single render function in the app, but structurally it's just several "
  "independent <font face='Courier'>&lt;form&gt;</font> elements stacked together — each with its own "
  "<font face='Courier'>id</font>, handled separately in <font face='Courier'>onSubmit</font> (Chapter 36). "
  "A few UI details worth noting:")
bullets([
    "Height can be entered in cm or ft/in — internally, the app <i>always</i> stores height as centimeters "
    "(<font face='Courier'>heightCm</font>); the ft/in inputs are converted on the way in and out, so all "
    "downstream math (like <font face='Courier'>calcBMR</font>) only ever has to deal with one unit.",
    "Similarly, weight is always stored internally in kilograms, with <font face='Courier'>toDisplayWeight()</font> "
    "/ <font face='Courier'>fromDisplayWeight()</font> converting to/from pounds only at the point of "
    "display or input, based on the user's chosen unit preference.",
    "The micronutrient goal-editing section is wrapped in a collapsible &lt;details&gt; element (see "
    "Chapter 31) since most users won't want to micromanage 40 individual targets.",
])

chapter("34. app.js Part 12 — Barcode Scanning")
p("This feature combines three ideas already covered: the <font face='Courier'>BarcodeDetector</font> and "
  "<font face='Courier'>MediaDevices</font> browser APIs (Chapter 14), <font face='Courier'>async</font>/"
  "<font face='Courier'>await</font> (Chapter 11), and a recursive polling loop using "
  "<font face='Courier'>requestAnimationFrame</font>:")
code('''async function startScan(){
  if(!('BarcodeDetector' in window)){ showScanMessage("not supported"); return; }
  try{
    scanDetector = new window.BarcodeDetector({formats});
    scanStream = await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'}});
    video.srcObject = scanStream;
    await video.play();
    scanning = true;
    scanLoop();
  }catch(err){ showScanMessage("Camera access isn't available here."); }
}

function scanLoop(){
  if(!scanning) return;
  scanDetector.detect(video).then(codes=>{
    if(codes && codes.length){ handleBarcode(codes[0].rawValue); }
    else if(scanning){ requestAnimationFrame(scanLoop); }   // check again next frame
  }).catch(()=>{ if(scanning) requestAnimationFrame(scanLoop); });
}''')
p("<font face='Courier'>facingMode:'environment'</font> requests the phone's rear (outward-facing) camera "
  "specifically, since that's the one normally used for scanning things. "
  "<font face='Courier'>requestAnimationFrame</font> is a browser API that schedules a function to run "
  "right before the next screen repaint (typically ~60 times per second) — using it for the scan loop "
  "means the app keeps checking each new video frame for a barcode, but automatically pauses this work if "
  "the browser tab isn't visible, which is more efficient than a fixed timer.")
p("When a code is found, <font face='Courier'>handleBarcode()</font> looks it up in "
  "<font face='Courier'>STATE.barcodeMap</font> (Chapter 23.4); if it's already linked to a food, it offers "
  "to log that food directly; if it's a never-before-seen barcode, it offers to either link it to an "
  "existing food or create a brand new custom food for it — after which future scans of that same barcode "
  "resolve instantly.")

chapter("35. app.js Part 13 — Export / Import / Theme")
sec("35.1 Backup export")
code('''async function exportData(){
  const json = JSON.stringify(STATE, null, 2);
  const filename = 'tiffin-backup-'+todayKey()+'.json';
  try{
    if(window.claude && window.claude.use){
      const downloads = await window.claude.use('downloads');
      if(downloads){ await downloads.save({filename, data: json}); return; }
    }
  }catch(e){}
  // fallback: show the JSON in a text box with a "copy" button
  openModalHtml(`<textarea readonly>${escapeHtml(json)}</textarea> ...`, 'generic');
}''')
p("<font face='Courier'>JSON.stringify(STATE, null, 2)</font> — the third argument, "
  "<font face='Courier'>2</font>, tells it to pretty-print with 2-space indentation, making the exported "
  "file human-readable if someone opens it directly. The function first tries an optional platform-specific "
  "save-file API (available when running inside certain host environments), and falls back to simply "
  "displaying the raw JSON text in a read-only textbox with a \"copy to clipboard\" button when that's not "
  "available — always giving the user <i>some</i> way to get their data out, regardless of environment.")
sec("35.2 Backup import")
code('''function importFromFile(file){
  const reader = new FileReader();
  reader.onload = ()=>{
    try{
      const parsed = JSON.parse(reader.result);
      const s = defaultState();
      s.goals = mergeKnownFields(DEFAULT_GOALS, parsed.goals);       // <-- security, Ch.24.2
      s.profile = mergeKnownFields(defaultProfile(), parsed.profile); // <-- security, Ch.24.2
      ...
      STATE = s;
      saveState(); applyTheme(); renderApp();
    }catch(e){ toast("That file couldn't be read as a Tiffin backup."); }
  };
  reader.readAsText(file);
}''')
p("This is exactly the loader logic from <font face='Courier'>loadState()</font> (Chapter 24), reused for "
  "an imported file — and it's the more important of the two places <font face='Courier'>"
  "mergeKnownFields</font> gets used, since an imported file is more plausibly something a user downloaded, "
  "shared, or hand-edited, rather than something the app wrote itself.")
sec("35.3 Theme switching")
code('''function applyTheme(){
  const t = STATE.goals.theme || 'system';
  if(t === 'system') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
}''')
p("This is the JavaScript half of the dark-mode system introduced in Chapter 21.1: setting or removing the "
  "<font face='Courier'>data-theme</font> attribute on the root <font face='Courier'>&lt;html&gt;</font> "
  "element is the ONLY thing this function does — every visual consequence is handled entirely by the CSS "
  "variable rules already defined in app.css reacting to that attribute changing.")

chapter("36. app.js Part 14 — The Event System (the app's heart)")
p("Everything explained so far describes functions that <i>could</i> run — this section is what actually "
  "decides <i>when</i> they run. Recall the event delegation pattern from Chapter 10.1; this is its full, "
  "real implementation.")
code('''function onClick(e){
  const t = e.target.closest('[data-action]');
  if(!t) return;
  const action = t.dataset.action;

  if(action === 'nav'){ currentView = t.dataset.view; renderApp(); return; }
  if(action === 'date-prev'){ currentDate = addDaysKey(currentDate,-1); renderView(); return; }
  if(action === 'open-picker'){ openPicker({meal:t.dataset.meal}); return; }
  if(action === 'delete-entry'){
    e.stopPropagation();
    const meal = t.dataset.meal, idx = parseInt(t.dataset.index,10);
    getDay(currentDate)[meal].splice(idx,1);
    saveState(); renderView();
    return;
  }
  // ... roughly 60 more branches, covering every button in the app
}''')
p("This single function is around 260 lines long and handles essentially every click in the entire "
  "application — nav switching, date navigation, opening every modal, every delete button, every settings "
  "toggle, the whole food picker flow, barcode scanning controls, meal slot management, and more. Each "
  "branch follows an almost identical shape: read some data out of the clicked element's "
  "<font face='Courier'>dataset</font> (the collection of its <font face='Courier'>data-*</font> "
  "attributes, per Chapter 2.2), mutate <font face='Courier'>STATE</font> or another module-level variable "
  "accordingly, then <font face='Courier'>return</font> immediately — the early <font face='Courier'>"
  "return</font> after every branch is what makes an otherwise 60-branch if-chain readable: once one "
  "matches, nothing below it is even checked.")
p("<font face='Courier'>e.stopPropagation()</font>, seen in the delete-entry branch, prevents this click "
  "from also bubbling up and triggering a <i>different</i> data-action on a parent element (in this "
  "specific case, the delete (×) icon sits inside a row that itself has its own "
  "<font face='Courier'>data-action=\"edit-entry\"</font> for opening the edit screen — without "
  "<font face='Courier'>stopPropagation()</font>, clicking delete would also immediately trigger edit).")
sec("36.1 Three sibling listeners for three other event types")
code('''function onInput(e){    // fires on every keystroke (live search-as-you-type, live nutrient preview)
  const el = e.target;
  if(el.id === 'foodsSearch'){ foodsFilter.query = el.value; /* re-render just the list */ return; }
  if(el.id === 'servingAmount'){ /* recompute and redraw just the nutrition preview numbers */ return; }
  ...
}
function onChange(e){   // fires when a <input type="file"> selection is confirmed
  if(el.id === 'importFileInput' && el.files[0]){ importFromFile(el.files[0]); return; }
}
function onSubmit(e){   // fires when any <form> is submitted
  if(form.id === 'customFoodForm'){ e.preventDefault(); handleCustomFoodSubmit(form); return; }
  if(form.id === 'profileForm'){ e.preventDefault(); /* save name */ return; }
  if(form.id === 'weightForm'){ e.preventDefault(); /* validate + save a weigh-in */ return; }
  ...
}''')
p("<font face='Courier'>e.preventDefault()</font> inside every form handler stops the browser's default "
  "behavior for a form submission — which is to reload the entire page and send the data to a server via a "
  "URL, exactly what a no-backend app must never let happen. Note also that "
  "<font face='Courier'>onInput</font>'s live-search handler deliberately updates <i>only</i> the small "
  "results-list element (<font face='Courier'>document.getElementById('foodsList').innerHTML = ...</font>) "
  "rather than calling the full <font face='Courier'>renderView()</font> — re-rendering the entire page on "
  "every single keystroke of a search box would be needlessly wasteful and could even steal focus away "
  "from the input the user is actively typing in.")

chapter("37. app.js Part 15 — Startup")
code('''let inited = false;
function init(){
  if(inited) return; inited = true;
  applyTheme();
  document.addEventListener('click', onClick);
  document.addEventListener('input', onInput);
  document.addEventListener('change', onChange);
  document.addEventListener('submit', onSubmit);
  document.getElementById('modalOverlay').addEventListener('click', function(e){
    if(e.target.id === 'modalOverlay') closeModal();   // click OUTSIDE the modal box closes it
  });
  renderApp();   // the very first paint of the whole app
}
document.addEventListener('DOMContentLoaded', init);
if(document.readyState !== 'loading') init();''')
p("This is the last thing in the file, and it's where everything described in this entire part actually "
  "kicks off: apply the saved theme, attach the four delegated event listeners from Chapter 36 exactly "
  "once, wire up \"click the dark overlay behind a modal to close it,\" and finally call "
  "<font face='Courier'>renderApp()</font> for the very first time, painting the initial screen from "
  "whatever <font face='Courier'>STATE</font> was loaded at the very top of the file (Chapter 24).")
p("The <font face='Courier'>inited</font> guard flag exists because of the two lines at the very bottom: "
  "<font face='Courier'>DOMContentLoaded</font> fires once, when the browser finishes parsing the HTML — "
  "but if the script happens to load and execute <i>after</i> that event already fired (a real possibility "
  "depending on exactly how/when the script tag runs), the listener would simply never fire at all, and "
  "the app would never start. The second line, checking <font face='Courier'>document.readyState</font>, "
  "catches that case by calling <font face='Courier'>init()</font> immediately if the document has already "
  "finished loading. The guard flag ensures that if <i>both</i> paths somehow end up running, "
  "<font face='Courier'>init()</font> still only ever truly executes once.")

# ================================================================
# PART 3 — ARCHITECTURE
# ================================================================
part("PART 3<br/>Architecture &amp; Design Decisions")

chapter("38. Why No Framework, No Backend?")
sec("38.1 No framework (no React / Vue / Angular)")
p("This app achieves everything a framework normally provides — a render-on-state-change loop, reusable "
  "\"components,\" event handling — using nothing but the patterns from Chapters 28 and 36: template "
  "literals for components, one delegated listener for events, and full-innerHTML-replacement for updates.")
bullets([
    "<b>Pro:</b> Zero dependencies, zero build step needed to develop (only to bundle for shipping), and a "
    "single ~1,700-line file that a reader can genuinely hold in their head — nothing hides behind an "
    "abstraction layer or framework \"magic.\"",
    "<b>Con:</b> No fine-grained DOM diffing (a framework only updates the exact DOM nodes that actually "
    "changed; this app replaces whole chunks of HTML every time), no built-in component reuse/composition "
    "tooling, and the burden of avoiding bugs like memory leaks (Chapter 32's chart cleanup) falls entirely "
    "on the developer instead of the framework.",
    "<b>Why it's a reasonable choice here:</b> the app's total data size is small (one user's diary, not "
    "millions of rows), so the performance cost of \"just re-render everything\" never becomes noticeable, "
    "and the simplicity payoff — no build tooling required to even run the app locally, trivial to audit "
    "for security since every line of logic is visible in one file — is worth it for a project this size.",
])
sec("38.2 No backend, no server, no database")
p("Every user's data lives only in their own browser's localStorage (Chapter 13). There is no login, no "
  "account, no API calls that send personal data anywhere.")
bullets([
    "<b>Pro:</b> Perfect privacy by construction (nothing to breach — there's no server holding anyone's "
    "data), zero server hosting cost, and the app works fully offline once loaded, since even the food "
    "database is baked directly into the page (Chapter 22).",
    "<b>Con:</b> No cross-device sync (your diary on your phone and your laptop are two separate, "
    "unconnected datasets), and clearing browser data destroys everything unless a backup was manually "
    "exported (Chapter 35).",
    "<b>Why it's a reasonable choice here:</b> a personal nutrition tracker's core value doesn't strictly "
    "require sync or accounts, and trading that away buys meaningful simplicity and privacy.",
])

chapter("39. Security: XSS, CSP, Prototype Pollution")
sec("39.1 XSS (Cross-Site Scripting) and escapeHtml")
p("Because so much of this app's HTML is built by directly interpolating data into template literals "
  "(<font face='Courier'>`&lt;div&gt;${food.name}&lt;/div&gt;`</font>), there's a real risk: if "
  "<font face='Courier'>food.name</font> ever contained something like "
  "<font face='Courier'>&lt;img src=x onerror=\"steal_data()\"&gt;</font> — for instance, typed in by the "
  "user themselves when naming a custom food — and it were inserted unescaped, the browser would parse it "
  "as real HTML and execute that injected script. This class of vulnerability is called "
  "<b>XSS (Cross-Site Scripting)</b>.")
code('''function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c=>({
    '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
  }[c]));
}

// used everywhere untrusted text is inserted into HTML:
`<div class="fname">${escapeHtml(food.name)}</div>`''')
p("<font face='Courier'>escapeHtml()</font> converts the characters that give HTML its special meaning "
  "(<font face='Courier'>&lt; &gt; &amp; \" '</font>) into their harmless text equivalents "
  "(\"HTML entities\"), so <font face='Courier'>&lt;img&gt;</font> becomes the literal, inert text "
  "<font face='Courier'>&amp;lt;img&amp;gt;</font> instead of being parsed as a tag. This function is "
  "called on essentially every single piece of user-controlled or data-sourced text before it's woven into "
  "an HTML string anywhere in the app — food names, profile name, custom meal names, barcode numbers, all "
  "of it.")
sec("39.2 The Content-Security-Policy, revisited")
p("escapeHtml is the app's <i>first</i> line of defense — but defensive engineering means assuming a bug "
  "slips through anyway (a future edit that forgets to call it, say). Recall from Chapter 19.1 that "
  "build.py computes cryptographic hashes of the app's own two legitimate inline scripts and locks the "
  "browser down to <i>only</i> executing scripts matching those exact hashes. Even in the worst case — an "
  "attacker somehow gets an unescaped, malicious string containing a "
  "<font face='Courier'>&lt;script&gt;</font> tag into the page — the browser's own CSP enforcement would "
  "refuse to execute it, because its content wouldn't match either trusted hash. This is called "
  "<b>defense in depth</b>: multiple independent layers of protection, so that one layer failing doesn't "
  "mean total compromise.")
sec("39.3 Prototype pollution, revisited")
p("Covered in full in Chapter 24.2 — <font face='Courier'>mergeKnownFields()</font> ensures that loading "
  "saved state or an imported backup file can never inject unexpected properties (like "
  "<font face='Courier'>__proto__</font>) into the app's data, only ever the specific fields the app "
  "already knows about and expects.")

chapter("40. The Full Data Flow, End to End")
p("Putting every earlier chapter together, here is literally everything that happens, in order, when a "
  "user adds \"1.5 cups of rice\" to their lunch:")
bullets([
    "<b>1.</b> User taps <font face='Courier'>+ Add Lunch</font> &#8594; the click bubbles to "
    "<font face='Courier'>document</font> &#8594; <font face='Courier'>onClick</font> (Ch.36) matches "
    "<font face='Courier'>data-action=\"open-picker\"</font> &#8594; calls "
    "<font face='Courier'>openPicker({meal:'meal-2'})</font> (Ch.30).",
    "<b>2.</b> <font face='Courier'>openPicker</font> creates the picker state object and calls "
    "<font face='Courier'>renderPickerModal()</font>, which calls <font face='Courier'>renderListStep()</font> "
    "&#8594; returns an HTML string &#8594; <font face='Courier'>openModalHtml()</font> sets "
    "<font face='Courier'>#modalContent.innerHTML</font> and reveals the modal overlay.",
    "<b>3.</b> User types \"rice\" &#8594; fires an <font face='Courier'>input</font> event &#8594; "
    "<font face='Courier'>onInput</font> (Ch.36.1) updates <font face='Courier'>picker.query</font>, calls "
    "<font face='Courier'>filterFoods()</font> (Ch.22/30) against <font face='Courier'>FOOD_DB</font>, and "
    "replaces just the results list's <font face='Courier'>innerHTML</font>.",
    "<b>4.</b> User taps the \"Rice, cooked\" result &#8594; <font face='Courier'>onClick</font> matches "
    "<font face='Courier'>select-food</font> &#8594; sets <font face='Courier'>picker.activeRef</font> and "
    "<font face='Courier'>picker.step = 'serving'</font> &#8594; re-renders the modal, now showing "
    "<font face='Courier'>renderServingStep()</font>'s quantity screen.",
    "<b>5.</b> User sets amount to 1.5 &#8594; <font face='Courier'>onInput</font> recomputes "
    "grams/calories live via <font face='Courier'>computeGrams()</font> and "
    "<font face='Courier'>scaleNutrients()</font> (Ch.25) and updates just the preview numbers on screen.",
    "<b>6.</b> User taps <font face='Courier'>Add to list</font> &#8594; <font face='Courier'>onClick</font> "
    "matches <font face='Courier'>add-to-cart</font> &#8594; pushes the item into "
    "<font face='Courier'>picker.cart</font>, returns to the list step.",
    "<b>7.</b> User taps <font face='Courier'>Finish</font> &#8594; <font face='Courier'>onClick</font> "
    "matches <font face='Courier'>picker-finish</font> &#8594; for each cart item, computes its quantity "
    "and <font face='Courier'>getDay(dateKey)[meal].push({ref, qty})</font> — this is the moment "
    "<font face='Courier'>STATE</font> itself actually changes (Ch.26).",
    "<b>8.</b> Still inside that handler: <font face='Courier'>saveState()</font> serializes the whole "
    "<font face='Courier'>STATE</font> object to JSON and writes it to localStorage (Ch.24) — the data is "
    "now durable, surviving even if the tab is closed immediately.",
    "<b>9.</b> <font face='Courier'>closeModal()</font> hides the modal; <font face='Courier'>renderView()</font> "
    "(Ch.28) calls <font face='Courier'>renderToday()</font> (Ch.29) fresh — it calls "
    "<font face='Courier'>dayTotals()</font> (Ch.26), which now includes the new rice entry, recomputes the "
    "calorie ring's percentage, and returns brand-new HTML reflecting the updated total.",
    "<b>10.</b> That HTML replaces <font face='Courier'>#viewRoot</font>'s content; the browser repaints; "
    "the user sees the ring, the macro bars, and the lunch card all instantly reflect the new food — done.",
])
note("Every one of those ten steps is just a composition of small, individually simple functions covered "
     "earlier in this guide. There's no framework, no network request, no hidden magic anywhere in this "
     "chain — which is precisely the point being made in Chapter 38.")

# ================================================================
# PART 4 — INTERVIEW GUIDE
# ================================================================
part("PART 4<br/>Interview Guide")
p("You now understand every language this app uses and every significant piece of its code. This part "
  "turns that understanding into interview-ready answers. Read the question, try to answer it yourself "
  "first, then compare against the model answer.")

chapter("41. The 30-Second Pitch")
p("<i>\"Tiffin is a full-featured nutrition tracker — think Cronometer or MyFitnessPal — built as a single, "
  "self-contained, zero-dependency web app in vanilla JavaScript. It tracks 44 nutrients across a "
  "332-food built-in database with an Indian-and-international focus, supports barcode scanning, custom "
  "foods and recipes, weight tracking with charts, and BMR/TDEE-based goal calculation using the "
  "Mifflin-St Jeor formula. There's no backend and no account system — everything is stored client-side in "
  "localStorage, which means it's completely private and works offline. It ships as a website, and also as "
  "installable native iOS and Android apps via Capacitor, with both builds automated end-to-end through "
  "GitHub Actions.\"</i>")

chapter("42. Core Technical Q&A")
qa("Why vanilla JavaScript instead of React or another framework?",
   "For a single-user, client-only app of this size, a framework's main benefits — efficient re-rendering "
   "of huge, frequently-changing datasets, and managing complex component trees — aren't really needed. "
   "The tradeoff favored simplicity: zero build tooling required to run the app locally, one file that's "
   "fully auditable top to bottom, and no dependency updates to manage. The app still uses the same core "
   "idea frameworks are built on — 'the UI is a pure function of state' — just implemented by hand with "
   "template literals and full innerHTML replacement instead of a virtual DOM.")
qa("How does the app persist data without a server?",
   "It uses the browser's localStorage API, which is a simple key-value store that survives page reloads "
   "and browser restarts. The app's entire state — profile, goals, diary, custom foods, weight log — is "
   "one JavaScript object, serialized to a JSON string with JSON.stringify and written under one key. On "
   "load, it's read back with localStorage.getItem and parsed with JSON.parse. This means all data stays on "
   "the user's own device and never leaves it.")
qa("Walk me through what happens end to end when a user logs a food.",
   "See Chapter 40 for the full ten-step trace — in short: a click is caught by one delegated event "
   "listener, which mutates the central STATE object directly, immediately persists it to localStorage, "
   "then calls the render function for the current view, which reads the now-updated STATE and returns "
   "fresh HTML that replaces what's on screen.")
qa("Explain the event delegation pattern used here, and why.",
   "Instead of attaching a separate click listener to every button (which could be hundreds across all the "
   "screens), the app attaches exactly one listener to `document`. It relies on event bubbling — a click "
   "always propagates up through all of its ancestor elements — so a single top-level handler can inspect "
   "`event.target.closest('[data-action]')` to find out what was actually clicked, then dispatch based on "
   "that element's `data-action` attribute. This scales to any number of dynamically-created buttons with "
   "zero extra listener setup, which matters a lot here since almost the entire UI is regenerated from "
   "scratch on every state change.")
qa("What security measures does this app take, and why?",
   "Three layers: (1) escapeHtml() sanitizes any data-derived text before it's inserted into an HTML "
   "template, preventing XSS if a food name or similar field ever contained malicious markup; (2) a strict "
   "Content-Security-Policy, computed at build time from SHA-256 hashes of the app's own two legitimate "
   "inline scripts, means the browser will refuse to execute any script that doesn't match — a defense-in-"
   "depth backstop even if an escaping bug slipped through; (3) mergeKnownFields() guards against "
   "prototype pollution (CWE-1321) when loading saved or imported JSON data, by only ever copying keys the "
   "app already expects, rather than blindly merging an untrusted object's keys, which could otherwise let "
   "a key like '__proto__' corrupt the behavior of every object in the running app.")
qa("How does the app support both light and dark mode?",
   "Through CSS custom properties (variables). The entire color palette is defined once as variables under "
   ":root, and every other CSS rule references them via var(--name) instead of hardcoding colors. A dark-"
   "mode block simply redefines the same variable names with dark values, either automatically (via the "
   "prefers-color-scheme media query, following the OS setting) or explicitly (via a data-theme attribute "
   "the app sets on <html> based on the user's in-app choice). No individual CSS rule needs to know or "
   "branch on which theme is active.")
qa("How is the mobile app (iOS/Android) built from the same code as the website?",
   "Capacitor wraps the built web app (a single static HTML file produced by build.py) inside a native app "
   "shell for each platform — essentially a full-screen native WebView pointed at that file. The same "
   "JavaScript that runs in a desktop browser tab runs unmodified inside it. Two GitHub Actions workflows "
   "automate the whole pipeline on every push: build the web app, run `cap sync` to copy it into the native "
   "project, then run each platform's own native compiler (Gradle for Android, Xcode for iOS) to produce an "
   "installable .apk or .ipa file as a downloadable build artifact.")
qa("Why does the app store references to foods (type + id) in the diary instead of copies of the nutrition data?",
   "Two reasons: it keeps the diary lightweight, and — more importantly — it means editing a custom food's "
   "nutrition values later automatically updates every past diary entry that referenced it, since the "
   "nutrients are looked up fresh (resolveRefBase) every time totals are computed, rather than being frozen "
   "at the moment they were logged.")
qa("What's a tradeoff of the 'replace the whole innerHTML on every change' rendering approach?",
   "It's simple and easy to reason about, but it's not fine-grained — even a change affecting one small "
   "part of the screen regenerates and replaces the whole view's HTML. For an app of this size and a "
   "single user's dataset, that's imperceptibly fast on modern devices, so it's a reasonable trade for the "
   "simplicity gained. A framework with a virtual DOM would only touch the specific DOM nodes that actually "
   "changed, which matters more at larger scale.")

chapter("43. Deep-Dive Design Questions")
qa("Why is the food data (NUTRIENT_KEYS) represented as a list of strings that other code loops over, "
   "instead of just writing out each nutrient calculation by hand?",
   "It turns what would be ~44 nearly-identical lines of code (per function) into one small loop, in every "
   "function that touches nutrients: zeroing them out, scaling by quantity, adding two nutrient sets "
   "together. It also means the same list drives the Nutrients tab's display grouping and the custom-food "
   "form's generated fields — add a 45th nutrient to that one list, and (with matching data in food_db.json) "
   "it flows through the whole app automatically, rather than needing edits in a dozen different places.")
qa("Why does calcBMR() return null instead of, say, 0 or throwing an error, when profile data is missing?",
   "Returning null makes 'no answer is available yet' an explicit, checkable state, distinct from a "
   "legitimate calculated value (0 would be misleading — nobody's BMR is actually zero). Every caller "
   "checks `if (bmr == null)` and shows an appropriate fallback (like a prompt to fill in Profile) instead "
   "of either crashing or silently displaying a wrong number.")
qa("Why build a custom HTML file with 4 placeholder substitutions in Python, instead of using a real "
   "bundler like Webpack or Vite?",
   "The whole app deliberately has no npm-based build dependencies for its JavaScript — it's plain, "
   "unbundled, unminified JS designed to be read and audited directly. A real bundler would be overkill "
   "for combining exactly four static files into one; the ~85-line Python script does that one job "
   "directly, including computing the CSP script hashes a general-purpose bundler wouldn't know to do "
   "out of the box, with no extra dependencies of its own.")
qa("What would you change if this app needed to support multiple devices for the same user?",
   "The core blocker is that localStorage is local to one browser on one device — you'd need some remote "
   "storage a user's various devices could all read and write, which means introducing a backend and some "
   "form of authentication, likely a real API rather than the current 'no server' model. You'd also need "
   "a strategy for merging changes made offline on two devices (a sync/conflict-resolution problem), which "
   "the current single-device, single-writer model avoids entirely.")
qa("How would you test this codebase?",
   "The pure, render-function-per-view architecture (Ch.28) is actually quite testable in principle: most "
   "render functions are pure functions of STATE that return a string, so you could feed them a known "
   "STATE object and assert on the returned HTML string without needing a real browser. The nutrient math "
   "functions (scaleNutrients, addNutrients, dayTotals) are pure and trivially unit-testable. The harder "
   "parts to test are the event-delegation handlers, since they mix DOM reads, STATE mutation, and "
   "re-rendering together — those would benefit most from a browser-based testing tool (like Playwright) "
   "driving real clicks and asserting on the resulting DOM, since they're what's not currently covered.")

chapter("44. Glossary — Every Term Used in This Guide")
glossary = sorted([
    ("API", "A set of functions/rules that let one piece of software talk to another."),
    ("Array", "An ordered list of values, e.g. [1, 2, 3]."),
    ("Async/await", "JavaScript syntax for writing code that waits on slow operations without freezing the page."),
    ("Attribute", "Extra information on an HTML tag, written as name=\"value\"."),
    ("Bundler", "A build tool (e.g. Webpack, Vite) that combines many source files into fewer files for shipping."),
    ("Callback", "A function passed into another function, to be called later."),
    ("CDN", "Content Delivery Network — a server that hosts common public files (like libraries) for fast loading."),
    ("CI/CD", "Continuous Integration/Deployment — automatically building/testing code on every change."),
    ("Closure", "A function that remembers variables from the scope it was defined in, even after that scope ends."),
    ("Commit", "A saved snapshot of a project's files in Git, with a description of what changed."),
    ("Component", "A reusable, self-contained piece of UI (here: a function returning an HTML string)."),
    ("const", "A JavaScript variable declaration that can't be reassigned."),
    ("CSP", "Content-Security-Policy — a browser rule set restricting what scripts/styles are allowed to run."),
    ("CSS", "Cascading Style Sheets — the language that styles HTML's appearance."),
    ("CWE", "Common Weakness Enumeration — a standard catalog of software vulnerability types."),
    ("Data attribute", "A custom HTML attribute starting with data-, readable by JavaScript."),
    ("Destructuring", "JS syntax for unpacking values from an array/object into separate variables."),
    ("DOM", "Document Object Model — the browser's live, in-memory tree of a page's elements."),
    ("Event", "Something that happens on a page: a click, keystroke, form submit, etc."),
    ("Event bubbling", "A DOM behavior where an event fires on an element, then its parent, then its parent's parent, and so on."),
    ("Event delegation", "Listening for events on one shared ancestor instead of each individual element."),
    ("f-string", "Python's syntax for embedding variables directly in a string, e.g. f\"Hi {name}\"."),
    ("Flexbox", "A CSS layout system for arranging elements in a single row or column."),
    ("Function", "A named, reusable block of code."),
    ("Grid", "A CSS layout system for arranging elements in rows and columns at once."),
    ("HTML", "HyperText Markup Language — describes a page's structure using tags."),
    ("IIFE", "Immediately Invoked Function Expression — a function defined and called in one step, to create an isolated scope."),
    ("JSON", "JavaScript Object Notation — a text format for structured data."),
    ("let", "A JavaScript variable declaration that CAN be reassigned later."),
    ("localStorage", "A browser API for storing key-value data that persists across sessions."),
    ("Object", "A collection of named key-value pairs, e.g. {name: 'Alice'}."),
    ("Prototype pollution", "A vulnerability class (CWE-1321) where untrusted data corrupts a shared object prototype."),
    ("Render", "To convert data into HTML/UI and display it."),
    ("Selector", "A CSS pattern (like .class or #id) that picks which elements a rule applies to."),
    ("SHA-256", "A cryptographic function that produces a unique fingerprint (hash) of some data."),
    ("Single Page App (SPA)", "A web app that updates its content dynamically in place instead of loading new full HTML pages."),
    ("State", "The current data driving what an app displays."),
    ("String", "Text data, e.g. \"hello\"."),
    ("Template literal", "A backtick-quoted JS string that can embed expressions via ${...}."),
    ("Ternary operator", "A compact if/else expression: condition ? valueIfTrue : valueIfFalse."),
    ("Truthy/falsy", "JavaScript's rules for treating non-boolean values as true or false in a condition."),
    ("Web API", "A built-in browser capability beyond basic HTML/CSS/JS, e.g. camera access or clipboard access."),
    ("XSS", "Cross-Site Scripting — a vulnerability where untrusted text is executed as HTML/script."),
    ("YAML", "A simple, indentation-based text format often used for configuration files."),
])
for term, definition in glossary:
    story.append(Paragraph(f"<b>{term}</b> — {definition}", body))

spacer(20)
p(f"<b>Prepared:</b> {datetime.now().strftime('%B %d, %Y')} &nbsp;|&nbsp; "
  "<b>Project:</b> Tiffin — Nutrition Tracker &nbsp;|&nbsp; "
  "<b>Stack:</b> HTML, CSS, JavaScript, JSON, Python (build), Capacitor (mobile), GitHub Actions (CI/CD)")

# ================================================================
doc = SimpleDocTemplate("TIFFIN_INTERVIEW_GUIDE.pdf", pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch,
    title="Tiffin — Complete Beginner-to-Interview Guide")
doc.build(story)
print("Done: TIFFIN_INTERVIEW_GUIDE.pdf")
