#!/usr/bin/env python3
"""
Generate a complete, beginner-to-interview-ready PDF guide for the Tiffin app.
Part 1 teaches every language/technology used, from absolute zero, in real depth.
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
    Preformatted, KeepTogether
)
from reportlab.lib import colors
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
    spaceBefore=0, spaceAfter=18)

chapter_style = ParagraphStyle('Chapter', parent=styles['Heading1'], fontSize=18,
    textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold',
    spaceBefore=4, spaceAfter=12)

h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13.5,
    textColor=colors.HexColor('#2c3e50'), fontName='Helvetica-Bold',
    spaceBefore=13, spaceAfter=7)

h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11.5,
    textColor=colors.HexColor('#34495e'), fontName='Helvetica-Bold',
    spaceBefore=9, spaceAfter=5)

body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10.1,
    leading=14.5, spaceAfter=7, alignment=TA_LEFT)

bullet_style = ParagraphStyle('Bullet', parent=body, leftIndent=14, spaceAfter=4)

qa_q = ParagraphStyle('QAQuestion', parent=body, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#E8552F'), fontSize=10.6, spaceBefore=9, spaceAfter=4)
qa_a = ParagraphStyle('QAAnswer', parent=body, leftIndent=10, spaceAfter=9)

quiz_style = ParagraphStyle('Quiz', parent=body, leftIndent=10, spaceAfter=3,
    textColor=colors.HexColor('#444444'))
quiz_head = ParagraphStyle('QuizHead', parent=body, fontName='Helvetica-Bold',
    fontSize=10.1, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#5D7EA6'))
answer_style = ParagraphStyle('Answer', parent=body, leftIndent=10, spaceAfter=3,
    textColor=colors.HexColor('#3F9160'), fontName='Helvetica-Oblique')

code_font_style = ParagraphStyle('CodeInner', parent=styles['Normal'], fontName='Courier',
    fontSize=8.1, leading=10.4, textColor=colors.HexColor('#1a1a1a'))

note_style = ParagraphStyle('Note', parent=body, backColor=colors.HexColor('#FFF4E5'),
    borderColor=colors.HexColor('#E8B84A'), borderWidth=0.6, borderPadding=8,
    spaceBefore=6, spaceAfter=10)

toc_style = ParagraphStyle('TOC', parent=body, spaceAfter=2, fontSize=9.3)
toc_part_style = ParagraphStyle('TOCPart', parent=body, fontName='Helvetica-Bold',
    fontSize=11.5, textColor=colors.HexColor('#E8552F'), spaceBefore=10, spaceAfter=4)

story = []
toc = []  # (title, is_part) — collected automatically as chapters are added

def part(title):
    toc.append((title, True))
    story.append(PageBreak())
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(title, part_style))
    story.append(Spacer(1, 0.3*inch))

def chapter(title):
    toc.append((title, False))
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

def quiz(title, items):
    story.append(Paragraph("Check your understanding — " + title, quiz_head))
    for i, (q, a) in enumerate(items, 1):
        story.append(Paragraph(f"{i}. {q}", quiz_style))
        story.append(Paragraph("Answer: " + a, answer_style))

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

def simple_table(rows, col_widths):
    tt = Table(rows, colWidths=col_widths)
    tt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
        ('TEXTCOLOR',(0,0),(-1,0), colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTNAME',(0,1),(-1,-1),'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8.6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    story.append(tt)
    spacer(10)

# ================================================================
# COVER PAGE
# ================================================================
story.append(Spacer(1, 1.2*inch))
story.append(Paragraph("🍱 Tiffin", title_style))
story.append(Paragraph("The Complete Beginner-to-Interview Guide", cover_sub))
story.append(Spacer(1, 0.25*inch))
story.append(Paragraph(
    "A real, ground-up course in every language this app uses — HTML, CSS, JavaScript, JSON, "
    "Python, Git and GitHub Actions, Capacitor — followed by a line-by-line walkthrough of the entire "
    "codebase, then an interview-ready Q&amp;A guide.",
    body))
story.append(Spacer(1, 0.35*inch))
story.append(Paragraph(f"<b>Prepared:</b> {datetime.now().strftime('%B %Y')}", body))
story.append(Paragraph("<b>Audience:</b> Complete beginners with zero programming background", body))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph(
    "<b>How to use this document:</b> Part 1 is a genuine course — read it in order, work through the "
    "\"check your understanding\" questions at the end of each chapter before moving on, and don't skip "
    "sections even if they feel slow. Part 2 assumes you know everything in Part 1 and explains the real "
    "code. Part 4 is for interview prep once you're comfortable with the rest.",
    body))

# NOTE: the Table of Contents is inserted programmatically at the very end of this
# script (right after cover, before Part 1), once every chapter() call above has
# populated `toc`. See the bottom of this file.

print("Scaffold + cover ready — chapters appended by later edits.")

# ================================================================
# PART 1 — LEARN THE LANGUAGES, FROM ZERO
# ================================================================
part("PART 1<br/>Learn the Languages, From Zero")
p("This part is a real course, not a glossary. Every concept here gets a plain-language explanation, "
  "a working code example, and — at the end of each chapter — a short set of questions so you can check "
  "you actually absorbed it before moving on. If a chapter feels slow, that's fine; Part 2 will lean on "
  "every single one of these ideas.")

chapter("1. How Computers & the Web Work")
sec("1.1 What does it mean to \"run code\"?")
p("A computer's processor can only do extremely simple things — add two numbers, compare two numbers, "
  "move a piece of data from one place to another — but it does billions of them per second. A "
  "<b>program</b> (or \"code\") is just a long, precise list of these simple instructions, written in a "
  "form a computer can follow. \"Running\" a program means the computer executes that list, instruction "
  "by instruction, top to bottom (skipping around when told to by loops and conditionals).")
p("Humans don't write the raw instructions a processor understands directly — that's called "
  "<b>machine code</b>, and it's unreadable (streams of numbers). Instead, we write in a "
  "<b>programming language</b> — a human-readable set of rules for describing instructions — and a "
  "separate program (an <b>interpreter</b>, for languages like JavaScript and Python, or a "
  "<b>compiler</b>, for languages like C++) translates it into something the machine can actually run.")
sec("1.2 Files, folders, and extensions")
p("Everything on a computer — including every piece of this project — is stored as a <b>file</b>: a named "
  "chunk of data saved to disk. Files live inside <b>folders</b> (also called <b>directories</b>), which "
  "can themselves contain more folders, forming a tree. A file's <b>extension</b> — the letters after the "
  "final dot in its name, like <font face='Courier'>.html</font> or <font face='Courier'>.js</font> — is "
  "just a convention telling humans and programs what <i>kind</i> of content that file holds; the computer "
  "doesn't magically know a file is JavaScript just because it's named "
  "<font face='Courier'>app.js</font> — a program (like a browser, or Node.js) has to choose to interpret "
  "it that way.")
sec("1.3 Client and server")
p("Picture a restaurant. You (the <b>client</b>) don't go into the kitchen yourself — you ask a waiter for "
  "something, and the kitchen (the <b>server</b>) prepares it and sends it back. On the web, your browser "
  "is the client. When you type a web address, your browser sends a <b>request</b> out over the internet "
  "to a server — a computer, somewhere, that's always running and waiting for requests — asking for a "
  "specific file. The server sends back a <b>response</b>: usually an HTML file, plus whatever other files "
  "(CSS, JS, images) that HTML asks for.")
p("This request/response conversation happens using a shared set of rules called <b>HTTP</b> "
  "(HyperText Transfer Protocol) — the \"http://\" (or the more secure, encrypted "
  "\"https://\") at the start of a web address names exactly this protocol.")
note("Tiffin is unusual precisely because, after the very first page load, it stops needing this "
     "conversation entirely — every file it needs (HTML, CSS, JS, even its whole food database) is "
     "downloaded once, and everything after that runs locally in your browser with no further requests. "
     "We'll see exactly how and why across this guide.")
sec("1.4 What the browser actually does with a web page")
p("Once your browser has the HTML file, it works through a pipeline, roughly:")
bullets([
    "<b>Parse HTML</b> — read the tags and build the DOM (Document Object Model), the tree of elements "
    "described in Chapter 2.",
    "<b>Parse CSS</b> — read all the style rules and build a matching tree of \"what should each element "
    "look like.\"",
    "<b>Layout</b> — figure out the exact size and position, in pixels, of every element on the page.",
    "<b>Paint</b> — actually draw pixels to the screen based on that layout.",
    "<b>Run JavaScript</b> — execute any script, which can then read and modify the DOM, triggering the "
    "browser to redo layout and paint for whatever changed.",
])
p("This entire pipeline can re-run, partially, many times a second — every time JavaScript changes "
  "something, or you resize the window, or you scroll. Keeping this fast is a large part of why the way "
  "you write CSS and JavaScript matters for a smooth-feeling page.")
quiz("How the Web Works", [
    ("What's the difference between a compiler and an interpreter?",
     "A compiler translates an entire program into machine code ahead of time, before it runs. An "
     "interpreter reads and executes a program's instructions directly (or just-in-time), without a "
     "separate translation step first. JavaScript and Python are both normally interpreted (with some "
     "just-in-time compilation happening behind the scenes for speed)."),
    ("In the client/server model, which one is your web browser?",
     "The client — it sends requests and displays whatever response it gets back."),
    ("Name the five rough stages a browser goes through to show you a page.",
     "Parse HTML, parse CSS, layout, paint, and run JavaScript (which can then trigger layout/paint again)."),
])

chapter("2. HTML — Structure & Common Tags")
sec("2.1 What HTML is, and isn't")
p("HTML (HyperText Markup Language) is not a programming language — it has no math, no decisions, no "
  "loops. It's a <b>markup language</b>: you wrap text in tags to describe what that text <i>is</i> "
  "(a heading, a paragraph, a button), and the browser decides how to display each kind of thing.")
sec("2.2 Tags, elements, and nesting")
code('''<p>This is a paragraph.</p>

<div>
  <h2>A heading</h2>
  <p>A paragraph <strong>with some bold text</strong> inside it.</p>
</div>''')
p("A <b>tag</b> is the bracketed part, like <font face='Courier'>&lt;p&gt;</font>. An <b>element</b> is "
  "the tag plus everything between its opening and closing versions. Elements can contain other elements "
  "— this is called <b>nesting</b>, and it must be done in a strictly ordered way: whatever you open "
  "last, you must close first (like nested parentheses). The outer element here is "
  "<font face='Courier'>&lt;div&gt;</font>; <font face='Courier'>&lt;h2&gt;</font> and "
  "<font face='Courier'>&lt;p&gt;</font> are its <b>children</b>; <font face='Courier'>&lt;strong&gt;</font> "
  "is nested inside that <font face='Courier'>&lt;p&gt;</font>.")
sec("2.3 Block vs. inline elements")
p("Every HTML element has a default \"how does it take up space\" behavior (which CSS can override, "
  "Chapter 9): <b>block</b> elements always start on a new line and stretch to fill the available width "
  "(like <font face='Courier'>&lt;div&gt;</font>, <font face='Courier'>&lt;p&gt;</font>, "
  "<font face='Courier'>&lt;h1&gt;</font>); <b>inline</b> elements sit within a line of text, only as wide "
  "as their content (like <font face='Courier'>&lt;span&gt;</font>, <font face='Courier'>&lt;strong&gt;</font>, "
  "<font face='Courier'>&lt;a&gt;</font>).")
sec("2.4 Void elements — tags with no closing tag")
p("A handful of tags never wrap content, so they have no separate closing tag: "
  "<font face='Courier'>&lt;br&gt;</font> (line break), <font face='Courier'>&lt;img&gt;</font> (image), "
  "<font face='Courier'>&lt;input&gt;</font> (form field), <font face='Courier'>&lt;meta&gt;</font> "
  "(page metadata).")
sec("2.5 Lists and tables")
code('''<ul>                 <!-- unordered (bulleted) list -->
  <li>Rice</li>
  <li>Dal</li>
</ul>

<ol>                 <!-- ordered (numbered) list -->
  <li>Boil water</li>
  <li>Add rice</li>
</ol>

<table>
  <tr><th>Food</th><th>Calories</th></tr>
  <tr><td>Rice</td><td>200</td></tr>
</table>''')
sec("2.6 Links and images")
code('''<a href="https://example.com">Click here</a>   <!-- href = where it links to -->
<img src="photo.jpg" alt="A bowl of rice">          <!-- src = file location; alt = fallback/screen-reader text -->''')
sec("2.7 Semantic tags")
p("Beyond generic <font face='Courier'>&lt;div&gt;</font>s, HTML offers tags that describe the "
  "<i>meaning</i> of a section, which helps both accessibility tools (like screen readers) and search "
  "engines understand a page's structure:")
bullets([
    "<font face='Courier'>&lt;header&gt;</font> — introductory content, often navigation or a page title",
    "<font face='Courier'>&lt;nav&gt;</font> — a block of navigation links",
    "<font face='Courier'>&lt;main&gt;</font> — the primary content of the page",
    "<font face='Courier'>&lt;section&gt;</font> — a thematic grouping of content",
    "<font face='Courier'>&lt;footer&gt;</font> — closing content, like copyright or contact info",
])
p("Tiffin's shell.html uses <font face='Courier'>&lt;nav&gt;</font> for its sidebar/bottom bar and "
  "<font face='Courier'>&lt;main&gt;</font> for its content area — a small but real example of this in "
  "practice (Chapter 20 in Part 2).")
sec("2.8 Comments")
code('''<!-- This text is ignored by the browser entirely; it's just a note for humans -->''')
quiz("HTML", [
    ("What's the difference between a block element and an inline element?",
     "A block element starts on its own new line and stretches to fill the available width; an inline "
     "element flows within a line of text, taking up only as much width as its own content needs."),
    ("Why does &lt;img&gt; have no closing tag, but &lt;div&gt; does?",
     "&lt;img&gt; is a 'void' element — it never wraps any content (the image itself is specified via the src "
     "attribute), so there's nothing for a closing tag to close. &lt;div&gt; is a container meant to wrap other "
     "content, so it needs an opening AND closing tag to mark where that content begins and ends."),
    ("If you open &lt;div&gt;&lt;p&gt;, in what order must you close them?",
     "Innermost first: &lt;/p&gt; then &lt;/div&gt; — nesting must close in the reverse order it opened, like "
     "matching parentheses."),
])

chapter("3. HTML — Forms, Attributes & Accessibility")
sec("3.1 Attributes, revisited")
p("An attribute adds extra information to a tag, as <font face='Courier'>name=\"value\"</font> pairs "
  "inside the opening tag. Some attributes work on almost any element (<font face='Courier'>id</font>, "
  "<font face='Courier'>class</font>, any <font face='Courier'>data-*</font> attribute); others are "
  "specific to one tag (<font face='Courier'>href</font> only makes sense on "
  "<font face='Courier'>&lt;a&gt;</font>, <font face='Courier'>src</font> only on things that load an "
  "external file like <font face='Courier'>&lt;img&gt;</font>).")
sec("3.2 Forms — collecting user input")
p("A <font face='Courier'>&lt;form&gt;</font> groups related input fields so they can be handled — and, "
  "in a traditional server-driven website, submitted — together as one unit.")
code('''<form id="weightForm">
  <label for="weightInput">Weight (kg)</label>
  <input id="weightInput" type="number" name="weight" min="0" step="0.1" required>
  <button type="submit">Save</button>
</form>''')
p("<font face='Courier'>&lt;label for=\"weightInput\"&gt;</font> is linked to the input sharing that same "
  "<font face='Courier'>id</font> — clicking the label text then focuses that input automatically, and "
  "screen readers announce the label when the field receives focus. This is an accessibility best "
  "practice, not a decorative choice.")
sec("3.3 Common input types")
input_types = [
    ["type", "Produces"],
    ["text", "A single-line free text field"],
    ["number", "A numeric field, often with up/down steppers"],
    ["date", "A native date picker"],
    ["checkbox", "An on/off toggle"],
    ["radio", "One choice among a group sharing the same name"],
    ["file", "A button that opens the OS file picker"],
    ["password", "Like text, but the typed characters are masked"],
]
simple_table(input_types, [90, CONTENT_W-90])
sec("3.4 Validation attributes")
p("HTML can enforce basic rules on its own, with zero JavaScript, before a form is even allowed to "
  "submit: <font face='Courier'>required</font> (must not be empty), "
  "<font face='Courier'>min</font>/<font face='Courier'>max</font> (numeric bounds), "
  "<font face='Courier'>minlength</font>/<font face='Courier'>maxlength</font> (text length bounds), "
  "<font face='Courier'>pattern</font> (a regex the value must match, see Chapter 22).")
sec("3.5 Buttons: submit vs. button")
code('''<button type="submit">Save</button>    <!-- triggers the enclosing form's submit event -->
<button type="button">Cancel</button>    <!-- does nothing on its own; needs a JS click handler -->''')
p("This distinction matters throughout Tiffin's code: buttons meant to submit a form use "
  "<font face='Courier'>type=\"submit\"</font> (handled once, centrally, by the "
  "<font face='Courier'>submit</font> event, Chapter 25); buttons that should do something immediately on "
  "click, without any form involved, explicitly use <font face='Courier'>type=\"button\"</font> so they "
  "never accidentally trigger a nearby form's submission.")
sec("3.6 Why accessibility matters here, concretely")
p("Every icon-only button in this app (Chapter 2.8 in Part 2 will show the raw SVGs) also carries a "
  "<font face='Courier'>title</font> attribute describing what it does — this shows as a tooltip on hover "
  "for sighted mouse users, and gets read aloud by screen readers for users who can't see the icon at all.")
quiz("HTML Forms", [
    ("What does &lt;label for=\"x\"&gt; do, and why bother?",
     "It links a label to the input with id=\"x\", so clicking the label text focuses that input, and "
     "screen readers announce the label's text when that input receives focus — a real accessibility "
     "requirement, not just a nicety."),
    ("What's the practical difference between &lt;button type=\"submit\"&gt; and &lt;button type=\"button\"&gt;?",
     "type=\"submit\" inside a &lt;form&gt; triggers that form's submit event automatically; type=\"button\" "
     "does nothing by itself and needs an explicit JavaScript click handler to do anything."),
    ("Name two form validation rules you can enforce with plain HTML, no JavaScript.",
     "Any two of: required (non-empty), min/max (numeric range), minlength/maxlength (text length), "
     "pattern (must match a given regular expression)."),
])

chapter("4. CSS — Selectors, Cascade & Specificity")
sec("4.1 The rule shape, revisited")
code('''selector {
  property: value;
}''')
sec("4.2 Selector types")
sel_table = [
    ["Selector", "Matches"],
    ["p", "every <p> element"],
    [".btn", "every element with class=\"btn\" (classes: reusable, many elements can share one)"],
    ["#saveBtn", "the one element with id=\"saveBtn\" (ids: must be unique per page)"],
    [".card p", "every <p> INSIDE an element with class=\"card\" (a 'descendant' selector)"],
    [".card > p", "every <p> that is a DIRECT child of .card (not a grandchild)"],
    ["input[type=\"text\"]", "every <input> whose type attribute equals \"text\""],
    [".btn:hover", "a .btn element, only while the mouse hovers it"],
    [".a, .b", "anything matching .a OR .b (comma = 'or')"],
]
simple_table(sel_table, [140, CONTENT_W-140])
sec("4.3 The cascade — what happens when two rules conflict")
p("\"Cascading\" in the name is literal: when multiple CSS rules could apply to the same element and set "
  "the same property, the browser has to pick a winner. It does so using three tie-breakers, in order:")
bullets([
    "<b>Importance:</b> a declaration marked <font face='Courier'>!important</font> beats a normal one "
    "(used rarely — it's a blunt override that makes future overrides harder).",
    "<b>Specificity:</b> a more \"specific\" selector beats a less specific one — explained next.",
    "<b>Source order:</b> if importance and specificity are tied, whichever rule appears LATER in the "
    "stylesheet wins.",
])
sec("4.4 Specificity — how \"specific\" a selector is")
p("Specificity is roughly calculated by counting: ID selectors count the most, then class/attribute/"
  "pseudo-class selectors, then plain tag-name selectors count the least.")
code('''p { color: black; }        /* specificity: 0-0-1  (one tag name) */
.warning { color: red; }     /* specificity: 0-1-0  (one class) -- this wins over the rule above */
#alert { color: orange; }    /* specificity: 1-0-0  (one id) -- this wins over both rules above */''')
p("This is why Tiffin's CSS relies mostly on classes (<font face='Courier'>.btn-primary</font>, "
  "<font face='Courier'>.card</font>) rather than IDs for styling — classes are reusable and have a "
  "moderate, predictable specificity, whereas ID-based rules are hard to override later without resorting "
  "to even more specific (and messier) selectors.")
sec("4.5 Inheritance")
p("Some CSS properties — mostly text-related ones like <font face='Courier'>color</font>, "
  "<font face='Courier'>font-family</font>, <font face='Courier'>font-size</font> — automatically pass "
  "down from a parent element to its children, unless a child rule overrides them. Other properties "
  "(like <font face='Courier'>border</font> or <font face='Courier'>padding</font>) do NOT inherit — "
  "giving a <font face='Courier'>&lt;div&gt;</font> a border doesn't give its children one too. This is "
  "exactly how Tiffin sets <font face='Courier'>font-family</font> once on "
  "<font face='Courier'>body</font> (app.css line 48) and every piece of text on the page inherits it "
  "without every single element needing its own font-family rule.")
quiz("CSS Selectors & Cascade", [
    ("Which wins: .btn or #saveBtn, if both set color on the same element?",
     "#saveBtn — ID selectors have higher specificity than class selectors, regardless of source order."),
    ("What's the difference between .card p and .card &gt; p?",
     "'.card p' matches any &lt;p&gt; anywhere inside .card, at any nesting depth. '.card &gt; p' only matches a "
     "&lt;p&gt; that is a DIRECT child of .card, not a grandchild or deeper descendant."),
    ("Does `border` inherit from a parent element to its children by default?",
     "No — border does not inherit. Color, font-family, and font-size are examples of properties that DO "
     "inherit by default; most box-model/layout properties (border, padding, margin, width) do not."),
])

chapter("5. CSS — The Box Model & Units")
sec("5.1 The box model, in detail")
p("Every element is a rectangle made of four nested layers, from the inside out:")
bullets([
    "<b>content</b> — the actual text/image/whatever the element holds",
    "<b>padding</b> — transparent space between the content and the border, still \"inside\" the element "
    "(its background color fills the padding too)",
    "<b>border</b> — a visible (or invisible) line drawn around the padding",
    "<b>margin</b> — transparent space OUTSIDE the border, separating this element from its neighbors "
    "(never filled by background color)",
])
code('''.card {
  padding: 18px;    /* space inside, between border and content */
  border: 1px solid #E7DAC0;
  margin-bottom: 14px;   /* space below, pushing the next element away */
}''')
sec("5.2 box-sizing — a crucial, easy-to-miss detail")
p("By default, when you set <font face='Courier'>width: 200px</font>, that 200px applies only to the "
  "<i>content</i> — padding and border get added ON TOP, so the element's actual total width ends up "
  "larger than 200px. This surprises almost every beginner. The fix, used almost universally in modern "
  "CSS (and by this app, right at the top of app.css):")
code('''*, *::before, *::after {
  box-sizing: border-box;
}''')
p("<font face='Courier'>border-box</font> makes <font face='Courier'>width</font> include padding and "
  "border, so a 200px-wide element is ALWAYS 200px wide on screen, no matter how much padding/border you "
  "add — padding and border simply eat into the content area instead of adding extra width. The universal "
  "selector <font face='Courier'>*</font> matches every element on the page, so this one rule applies "
  "everywhere at once.")
sec("5.3 Units")
units_table = [
    ["Unit", "Meaning"],
    ["px", "pixels — an absolute, fixed size"],
    ["%", "a percentage of the PARENT element's corresponding size"],
    ["em", "relative to the current element's own font-size"],
    ["rem", "relative to the ROOT element's (<html>) font-size — more predictable than em"],
    ["vw / vh", "1% of the viewport's (browser window's) width / height"],
]
simple_table(units_table, [80, CONTENT_W-80])
p("Tiffin mixes these deliberately: pixel values for things that should stay a fixed, precise size "
  "(border widths, icon sizes), percentages for fluid layout (<font face='Courier'>width:100%</font> on "
  "inputs so they fill their container), and <font face='Courier'>vh</font> for "
  "<font face='Courier'>min-height:100%</font>-style full-screen layouts.")
sec("5.4 display: none vs. visibility: hidden")
p("Two different ways to hide an element, with an important difference: "
  "<font face='Courier'>display:none</font> removes it from the layout entirely — as if it weren't there "
  "at all, other elements shift to fill the gap. <font face='Courier'>visibility:hidden</font> makes it "
  "invisible but still reserves its space — other elements do NOT shift. Tiffin's responsive nav switch "
  "(Chapter 21 sidebar/bottomnav) uses <font face='Courier'>display:none</font>, since the hidden nav "
  "shouldn't leave an empty gap on the page.")
quiz("The Box Model", [
    ("With default box-sizing, if a &lt;div&gt; has width:200px, padding:20px, and border:2px solid, "
     "how wide does it actually render on screen?",
     "244px (200 + 20+20 padding + 2+2 border) — with default content-box sizing, padding and border ADD "
     "to the specified width."),
    ("Same question, but with box-sizing: border-box.",
     "Exactly 200px — border-box makes width include the padding and border, so they eat into the content "
     "area instead of adding extra size."),
    ("You hide an element with display:none. Do the elements around it shift to fill the gap?",
     "Yes — display:none removes the element from the layout entirely, as if it isn't there. "
     "(visibility:hidden, by contrast, would hide it but still reserve its space.)"),
])

chapter("6. CSS — Colors")
sec("6.1 Color formats")
code('''color: red;                     /* a small set of named colors */
color: #FF6B4A;                 /* hex: red, green, blue as 2-digit hex pairs, 00-FF each */
color: rgb(255, 107, 74);        /* same color, as decimal red/green/blue, 0-255 each */
color: rgba(255, 107, 74, 0.5);  /* like rgb, plus alpha (opacity): 0 = fully transparent, 1 = fully opaque */
color: hsl(11, 100%, 65%);        /* hue (0-360 on a color wheel), saturation %, lightness % */''')
p("Tiffin's app.css uses hex colors for its named design tokens "
  "(<font face='Courier'>--accent: #FF6B4A</font>) but switches to rgba for things needing transparency, "
  "like <font face='Courier'>rgba(36,28,18,.45)</font> for the modal's semi-transparent dark backdrop — "
  "hex alone can't express partial transparency without a less common 8-digit hex form, so rgba is the "
  "clearer choice there.")
sec("6.2 currentColor — a color that reads from context")
p("The special keyword <font face='Courier'>currentColor</font> refers to whatever that element's own "
  "<font face='Courier'>color</font> property currently is. This is how Tiffin's SVG icons "
  "(Chapter 23.2 in Part 2) automatically match whatever text color surrounds them — every icon's SVG "
  "markup uses <font face='Courier'>stroke=\"currentColor\"</font> instead of a hardcoded color, so the "
  "exact same icon markup renders in gray in an inactive nav item and orange in an active one, purely by "
  "inheriting the surrounding <font face='Courier'>color</font> CSS property (Chapter 4.5's inheritance, "
  "applied cleverly).")
quiz("CSS Colors", [
    ("Which color format lets you specify partial transparency: hex, rgb, or rgba?",
     "rgba — the fourth value (alpha) sets opacity from 0 (fully transparent) to 1 (fully opaque). Plain "
     "hex and rgb have no opacity channel."),
    ("What does the CSS keyword currentColor do?",
     "It resolves to whatever that element's own `color` property is currently set to (inherited or "
     "explicit) — useful for things like SVG icons that should always match the surrounding text color "
     "without needing their own hardcoded color value."),
])

chapter("7. CSS — Flexbox")
sec("7.1 The mental model")
p("Flexbox arranges a group of sibling elements along a single line — either a row or a column — and "
  "gives you powerful, simple control over how they share space, align, and wrap. You turn it on with "
  "<font face='Courier'>display:flex</font> on the PARENT; every property below then applies either to "
  "that parent (controlling its children as a group) or to an individual child.")
code('''.row {
  display: flex;
  flex-direction: row;        /* 'row' (default) or 'column' */
  justify-content: space-between;  /* spacing ALONG the main axis (row: horizontal) */
  align-items: center;             /* alignment ACROSS the main axis (row: vertical) */
  gap: 12px;                        /* space between every child */
  flex-wrap: wrap;                   /* allow children to wrap onto new lines if they don't fit */
}''')
sec("7.2 justify-content vs. align-items — the constant beginner mix-up")
p("Both control alignment, but along different axes, and which axis is which depends on "
  "<font face='Courier'>flex-direction</font>. In the default <font face='Courier'>row</font> direction: "
  "<font face='Courier'>justify-content</font> controls horizontal spacing/alignment (the \"main axis\"), "
  "and <font face='Courier'>align-items</font> controls vertical alignment (the \"cross axis\"). Common "
  "values for <font face='Courier'>justify-content</font>: <font face='Courier'>flex-start</font>, "
  "<font face='Courier'>center</font>, <font face='Courier'>space-between</font> (push children to the "
  "far ends, evenly spacing any in between), <font face='Courier'>space-around</font>. Common values for "
  "<font face='Courier'>align-items</font>: <font face='Courier'>flex-start</font>, "
  "<font face='Courier'>center</font>, <font face='Courier'>stretch</font> (default — children stretch to "
  "fill the row's full height).")
sec("7.3 flex — controlling how one child grows or shrinks")
code('''.sidebar { flex: none; width: 216px; }   /* never grow or shrink — stay exactly 216px */
.main     { flex: 1; }                     /* grow to consume all remaining space */''')
p("<font face='Courier'>flex:1</font> is one of the most common flexbox declarations in existence — it "
  "means \"take up any leftover space, sharing it equally with any other sibling that also has "
  "<font face='Courier'>flex:1</font>.\" Tiffin's own top-level layout uses exactly this pattern (Chapter "
  "21 in Part 2): the sidebar is fixed-width and <font face='Courier'>flex:none</font>, while the main "
  "content area is <font face='Courier'>flex:1</font>, automatically filling whatever width the sidebar "
  "doesn't use.")
quiz("Flexbox", [
    ("You set display:flex and flex-direction:row on a container. Which property controls horizontal "
     "alignment of its children — justify-content or align-items?",
     "justify-content — in the default row direction, the horizontal axis IS the main axis, which is "
     "exactly what justify-content controls. align-items would control the vertical (cross-axis) "
     "alignment in this same row layout."),
    ("What does flex:1 on a child element mean?",
     "Grow to fill any remaining space in the flex container, sharing it equally with any sibling that "
     "also has flex:1. It's commonly paired with a fixed-width sibling (flex:none) to make one panel "
     "fixed and another fill the rest."),
])

chapter("8. CSS — Grid")
sec("8.1 When to reach for Grid instead of Flexbox")
p("Flexbox is fundamentally one-dimensional — one row, or one column. Grid is two-dimensional — rows AND "
  "columns at the same time — which makes it the right tool whenever you're laying out something that's "
  "genuinely grid-shaped, like a photo gallery or (in this app) a row of side-by-side stat cards.")
code('''.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;   /* two columns, each taking an equal FRACTION of the space */
  gap: 14px;
}

.mini-stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* shorthand for "1fr 1fr 1fr" -- three equal columns */
  gap: 12px;
}''')
sec("8.2 The fr unit")
p("<font face='Courier'>fr</font> (\"fraction\") is a unit that only exists in Grid: it means \"one share "
  "of whatever space is left after fixed-size columns are accounted for.\" "
  "<font face='Courier'>grid-template-columns: 1fr 1fr</font> creates two equal-width columns; "
  "<font face='Courier'>200px 1fr</font> would create one fixed 200px column and one column that stretches "
  "to fill everything else — very similar in spirit to flexbox's <font face='Courier'>flex:1</font>, but "
  "for a full 2D grid.")
quiz("Grid", [
    ("What kind of layout problem calls for Grid over Flexbox?",
     "A genuinely two-dimensional layout — rows and columns at once, like a stat-card grid or photo "
     "gallery — as opposed to Flexbox's one-dimensional (single row OR column) model."),
    ("What does grid-template-columns: repeat(3, 1fr) produce?",
     "Three equal-width columns, each taking one equal fraction (1fr) of the available space — shorthand "
     "for writing '1fr 1fr 1fr' by hand."),
])

chapter("9. CSS — Positioning & Display")
sec("9.1 The position property")
pos_table = [
    ["Value", "Behavior"],
    ["static", "default — sits in normal document flow, top/left/etc. have no effect"],
    ["relative", "stays in normal flow, but top/left/etc. nudge it FROM where it'd normally be"],
    ["absolute", "removed from flow; positioned relative to its nearest positioned ANCESTOR"],
    ["fixed", "removed from flow; positioned relative to the VIEWPORT — stays put even when scrolling"],
    ["sticky", "normal flow until a scroll threshold, then behaves like fixed"],
]
simple_table(pos_table, [70, CONTENT_W-70])
p("<font face='Courier'>position:absolute</font> only makes sense paired with a positioned ancestor — an "
  "element with <font face='Courier'>position:relative</font> (or absolute/fixed/sticky) somewhere above "
  "it in the tree, which becomes the reference point absolute positioning measures "
  "<font face='Courier'>top</font>/<font face='Courier'>left</font>/etc. from. Without one, it falls back "
  "to positioning relative to the entire page.")
code('''.ring-wrap { position: relative; width: 220px; height: 220px; }
.ring-center {
  position: absolute;
  inset: 0;              /* shorthand for top:0; right:0; bottom:0; left:0 -- fills the parent exactly */
}''')
p("This is exactly the pattern Tiffin uses to overlay the calorie number in the CENTER of the SVG "
  "progress ring (Chapter 29 in Part 2): the ring's wrapper is <font face='Courier'>position:relative</font>, "
  "and the text sitting on top of it is <font face='Courier'>position:absolute; inset:0</font>, perfectly "
  "layering the number over the ring graphic underneath it.")
p("Tiffin also uses <font face='Courier'>position:fixed</font> for its floating scan button and its "
  "toast notifications, and <font face='Courier'>position:sticky</font> for its top bar and sidebar — "
  "sticky is what lets the sidebar stay visible while its content area scrolls independently.")
sec("9.2 The display property")
p("Every element has a <font face='Courier'>display</font> value controlling its fundamental layout "
  "behavior. We've already met <font face='Courier'>flex</font> and <font face='Courier'>grid</font>; the "
  "others worth knowing: <font face='Courier'>block</font>, <font face='Courier'>inline</font> (from "
  "Chapter 2.3), <font face='Courier'>inline-block</font> (inline flow, but you CAN set a width/height on "
  "it, unlike plain inline), and <font face='Courier'>none</font> (Chapter 5.4 — removed from layout "
  "entirely).")
quiz("Positioning & Display", [
    ("An element has position:absolute but no ancestor has position set at all. What does it "
     "position itself relative to?",
     "The whole page (technically the initial containing block) — absolute positioning always needs a "
     "positioned ancestor (relative/absolute/fixed/sticky) to be useful as a LOCAL reference point; "
     "without one, it falls back to positioning against the page itself."),
    ("What's the shorthand `inset: 0` equivalent to?",
     "top: 0; right: 0; bottom: 0; left: 0 — commonly used to make an absolutely-positioned element "
     "exactly fill its positioned parent."),
])

chapter("10. CSS — Responsive Design (Media Queries)")
sec("10.1 Why responsive design matters")
p("The same HTML/CSS has to look good on a phone screen (maybe 375px wide) and a desktop monitor (maybe "
  "1920px wide) — a fixed-width, fixed-layout design would either be cramped on mobile or absurdly "
  "sparse on desktop. Responsive design means writing CSS that adapts based on the available space.")
sec("10.2 Media queries, revisited and expanded")
code('''.sidenav { width: 216px; }          /* desktop default */
.bottomnav { display: none; }        /* hidden by default */

@media (max-width: 860px) {
  .sidenav { display: none; }         /* hide the desktop sidebar ... */
  .bottomnav { display: flex; }        /* ... and show a bottom tab bar instead */
}

@media (min-width: 861px) {
  .fab-scan { bottom: 32px; right: 24px; }   /* reposition a floating button on larger screens */
}''')
p("<font face='Courier'>max-width</font> means \"apply this when the viewport is AT MOST this wide\" "
  "(commonly used to target smaller screens); <font face='Courier'>min-width</font> means \"apply this "
  "when the viewport is AT LEAST this wide\" (commonly used to target larger screens). You can combine "
  "several conditions or write many separate <font face='Courier'>@media</font> blocks targeting "
  "different breakpoints — Tiffin deliberately keeps to just one breakpoint (860px) for simplicity, since "
  "its layout only really needs two states: \"mobile\" and \"desktop.\"")
sec("10.3 Mobile-first vs. desktop-first")
p("There are two philosophies for which styles are the \"default\" (outside any media query) and which "
  "are added inside one: <b>mobile-first</b> writes base styles for small screens, then uses "
  "<font face='Courier'>min-width</font> queries to add complexity for larger screens; "
  "<b>desktop-first</b> (what Tiffin does) writes base styles for the full desktop layout, then uses "
  "<font face='Courier'>max-width</font> queries to simplify/hide things for smaller screens. Neither is "
  "objectively correct — it's a matter of which is the more natural \"starting point\" for a given "
  "project.")
quiz("Responsive Design", [
    ("What's the difference between @media (max-width: 860px) and @media (min-width: 860px)?",
     "max-width:860px applies its rules when the viewport is 860px wide OR NARROWER (commonly used to "
     "target smaller/mobile screens). min-width:860px applies when the viewport is 860px OR WIDER "
     "(commonly used to target larger/desktop screens)."),
    ("Does Tiffin use a mobile-first or desktop-first approach, and how can you tell?",
     "Desktop-first — its base (non-media-query) CSS describes the full sidebar/desktop layout, and a "
     "single max-width:860px query then simplifies it down to a mobile bottom-tab-bar layout."),
])

chapter("11. CSS — Transitions & Animations")
sec("11.1 Transitions — smoothly animating a property change")
code('''.btn {
  background: var(--accent);
  transition: transform .08s ease, background .15s ease;
}
.btn:active { transform: scale(.97); }   /* transition makes this shrink SMOOTHLY, not instantly */''')
p("Without <font face='Courier'>transition</font>, a CSS property change (here, triggered by the "
  ":active pseudo-class from Chapter 3.6) would happen instantly, in a single frame — visually jarring. "
  "Adding <font face='Courier'>transition: property duration easing</font> tells the browser to "
  "automatically interpolate between the old and new values over that duration, producing a smooth "
  "animation with zero JavaScript.")
sec("11.2 Keyframe animations — for anything more complex than A-to-B")
code('''@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn .35s ease both; }''')
p("A transition only animates between two states (before/after a change); a "
  "<font face='Courier'>@keyframes</font> animation can define any number of intermediate steps "
  "(<font face='Courier'>from</font>/<font face='Courier'>to</font>, or percentages like "
  "<font face='Courier'>0%, 50%, 100%</font>) and, critically, can play automatically the moment an "
  "element appears — which is exactly what Tiffin's <font face='Courier'>.fade-in</font> class does every "
  "time a new view's HTML is inserted (Chapter 28 in Part 2), giving every screen transition a subtle, "
  "polished fade/slide-in instead of an abrupt pop.")
sec("11.3 Respecting reduced-motion preferences, revisited")
p("Recall from earlier that <font face='Courier'>@media (prefers-reduced-motion: reduce)</font> lets "
  "motion-sensitive users disable these effects system-wide; this is a real, standard accessibility "
  "feature, not a nice-to-have.")
quiz("Transitions & Animations", [
    ("What's the key difference between a CSS transition and a @keyframes animation?",
     "A transition only smoothly interpolates between two states — a property's old value and its new "
     "value after some change (like a hover or click). A @keyframes animation can define any number of "
     "intermediate steps and can play automatically on its own, without needing a state change to trigger it."),
])

chapter("12. CSS — Variables & Theming, In Depth")
sec("12.1 Defining and using custom properties")
p("Recall the syntax: define with two leading dashes inside a selector, read with "
  "<font face='Courier'>var(--name)</font>. Unlike a language variable, a CSS custom property is "
  "genuinely part of the cascade — it can be defined differently for different parts of the page, and "
  "child elements inherit whatever value is in effect for their nearest ancestor that set it.")
code(''':root {
  --accent: #FF6B4A;   /* the default, available everywhere */
}
.special-section {
  --accent: purple;     /* only elements INSIDE .special-section see this override */
}''')
sec("12.2 var() with a fallback")
code('''.thing { color: var(--maybe-undefined, black); }   /* uses black if --maybe-undefined was never set */''')
sec("12.3 Why this beats hardcoding colors everywhere")
p("Without variables, supporting dark mode would mean writing two nearly-identical copies of every "
  "single color-related rule in the whole stylesheet — one for light, one for dark — and keeping them in "
  "sync forever as the design evolves. With variables, as Chapter 21 in Part 2 will show in full, dark "
  "mode is implemented by redefining a couple dozen variable values ONE time, in one place — every rule "
  "elsewhere in the file that reads <font face='Courier'>var(--text)</font> or "
  "<font face='Courier'>var(--accent)</font> updates automatically, with no per-rule duplication at all.")
quiz("CSS Variables", [
    ("If .special-section redefines --accent to purple, does an element OUTSIDE .special-section see "
     "that new value?",
     "No — CSS custom properties follow the cascade and inheritance rules like any other property. Only "
     "elements INSIDE .special-section (that don't themselves override --accent again) see the purple "
     "value; everything outside still sees whatever --accent is set to at :root (or wherever else applies "
     "to them)."),
    ("Why does using CSS variables make supporting a dark theme drastically simpler than not using them?",
     "Because every rule in the stylesheet references the variable NAME (e.g. var(--text)) rather than a "
     "hardcoded value, switching themes only requires redefining what those variable names point to, "
     "once, in one place — not duplicating every color-related rule in the file for a second theme."),
])

chapter("13. JavaScript — Your First Lines of Code")
sec("13.1 What makes JavaScript different from HTML/CSS")
p("HTML describes structure and CSS describes appearance, but neither can make a decision, do math, "
  "repeat an action, or respond to something happening. JavaScript is a full <b>programming language</b>: "
  "it has variables (memory), logic (decisions), and control flow (repetition, sequencing) — the same "
  "core ingredients every programming language has, just with its own particular syntax (rules for how "
  "code must be written).")
sec("13.2 Statements and semicolons")
code('''console.log("Hello, world!");   // prints text to the browser's developer console
let x = 5;                       // a statement that creates a variable
x = x + 1;                        // a statement that changes it''')
p("A <b>statement</b> is one complete instruction. JavaScript statements are conventionally ended with a "
  "semicolon (though the language will often — not always — infer one for you if you omit it; this "
  "codebase always writes them explicitly, which is the safer habit). "
  "<font face='Courier'>console.log(...)</font> is how a developer prints values out for debugging — it "
  "doesn't show up on the actual page, only in the browser's developer tools.")
sec("13.3 Comments")
code('''// a single-line comment -- everything after // on this line is ignored

/* a multi-line comment
   can span several lines */''')
p("Comments are notes for humans; the JavaScript engine skips them entirely. This app's source is "
  "heavily commented in exactly the places where the WHY isn't obvious from the code alone (Part 2 will "
  "point out several real examples) — good practice is commenting sparingly, only where the reasoning "
  "behind a piece of code genuinely needs explaining.")
sec("13.4 Where JavaScript code lives")
p("In a browser, JavaScript can live inline inside a <font face='Courier'>&lt;script&gt;</font> tag, or "
  "in a separate <font face='Courier'>.js</font> file loaded via "
  "<font face='Courier'>&lt;script src=\"app.js\"&gt;&lt;/script&gt;</font>. It runs top to bottom, in "
  "order, exactly once per page load (though it can register things — like event listeners — that run "
  "again later, in response to something happening).")
quiz("First Lines of Code", [
    ("What's the difference between console.log(...) and something actually appearing on the web page?",
     "console.log prints a value only to the browser's developer console (a debugging tool) — it never "
     "appears anywhere on the visible page itself. To show something on the page, you have to modify the "
     "DOM directly (Chapter 24)."),
    ("Does the JavaScript engine execute the text inside /* ... */?",
     "No — that's a comment; everything between /* and */ (or after // on a line) is ignored entirely "
     "and exists purely for human readers."),
])

chapter("14. JavaScript — Variables & Primitive Types")
sec("14.1 const, let, and (avoid) var")
code('''const name = "Alice";    // cannot be reassigned -- attempting to will throw an error
let score = 100;          // CAN be reassigned
score = 150;                // fine

var old = "legacy";        // an older way to declare variables, with quirky scoping rules (Ch.19) --
                             // this codebase never uses it, and modern JS generally avoids it too''')
p("Best practice, followed throughout this codebase: default to <font face='Courier'>const</font>; only "
  "use <font face='Courier'>let</font> when a variable genuinely needs to be reassigned later. This isn't "
  "just style — it communicates intent to anyone reading the code, and lets the JavaScript engine (and "
  "your editor) catch a whole class of \"I didn't mean to change that\" bugs for free.")
sec("14.2 Primitive types, in depth")
p("A <b>primitive</b> is a basic, non-object value. JavaScript has seven: "
  "<font face='Courier'>number</font>, <font face='Courier'>string</font>, "
  "<font face='Courier'>boolean</font>, <font face='Courier'>null</font>, "
  "<font face='Courier'>undefined</font>, <font face='Courier'>symbol</font> (rare, not used here), and "
  "<font face='Courier'>bigint</font> (rare, not used here). Everything else — arrays, objects, functions "
  "— is technically an <b>object</b> under the hood, covered in Chapters 20-21.")
code('''typeof 42;           // "number"
typeof "hi";          // "string"
typeof true;           // "boolean"
typeof undefined;       // "undefined"
typeof null;             // "object"  -- a famous, long-standing quirk/bug in JS itself, kept for
                           // backwards compatibility; null is NOT actually an object''')

sec("14.3 Type coercion — JavaScript's automatic conversions")
p("JavaScript will sometimes silently convert one type to another to make an operation work, which is a "
  "common source of beginner confusion:")
code('''"5" + 3;      // "53"  -- + with a string on either side means CONCATENATE, so 3 becomes "3"
"5" - 3;       // 2     -- but - only makes sense for numbers, so "5" becomes 5
"5" == 5;       // true  -- == converts types before comparing (avoid this operator, see below)
"5" === 5;       // false -- === requires the SAME type AND value, no conversion at all
NaN === NaN;      // false -- NaN ("Not a Number") is the only value in JS that isn't equal to itself!
Number.isNaN(NaN); // true -- the correct, safe way to actually check for NaN''')
note("Always prefer <font face='Courier'>===</font> and <font face='Courier'>!==</font> over "
     "<font face='Courier'>==</font> and <font face='Courier'>!=</font>. The double-equals versions "
     "perform \"loose\" comparison with surprising coercion rules (<font face='Courier'>0 == ''</font> is "
     "true, <font face='Courier'>null == undefined</font> is true, but "
     "<font face='Courier'>null == 0</font> is false) that even experienced developers can't always "
     "predict from memory. This entire codebase uses <font face='Courier'>===</font> throughout.")
sec("14.4 Arrays and objects are NOT primitives")
p("A quick preview before their dedicated chapters: an array (<font face='Courier'>[1,2,3]</font>) and "
  "an object (<font face='Courier'>{name:'Alice'}</font>) both hold a <b>reference</b> to a location in "
  "memory, not the data itself directly the way a number or string does. This has a real, important "
  "consequence covered fully in Chapter 20: copying an array/object variable copies the reference, not "
  "the contents, so two variables can end up pointing at — and able to mutate — the exact same underlying "
  "data.")
quiz("Variables & Types", [
    ("What does \"5\" + 3 evaluate to, and why?",
     "\"53\" — the string \"5\" concatenated with 3 (converted to the string \"3\"). Whenever + has a "
     "string on either side, JavaScript treats it as string concatenation rather than arithmetic."),
    ("Why should you prefer === over == in this codebase (and generally)?",
     "== performs loose comparison, silently converting types before comparing, which produces "
     "surprising results (e.g. '' == 0 is true) that are easy to get wrong. === requires both the type "
     "and value to match exactly, with no hidden conversion, making code behavior far more predictable."),
    ("Is const name = \"Alice\" the same restriction as \"this string can never change\"?",
     "Not quite — const means the VARIABLE BINDING can't be reassigned to point at a different value. "
     "For a primitive like a string this amounts to the same thing (strings are themselves immutable in "
     "JS), but for an array or object declared with const, the variable can't be reassigned to a "
     "different array/object, yet its CONTENTS can still be mutated (see Chapter 20)."),
])

chapter("15. JavaScript — Operators & Expressions")
sec("15.1 Arithmetic operators")
code('''5 + 3;    // 8   addition
5 - 3;     // 2   subtraction
5 * 3;      // 15  multiplication
5 / 3;       // 1.6666...  division
5 % 3;        // 2   remainder ("modulo") -- how much is left over after dividing as many whole times as possible
5 ** 2;        // 25  exponentiation (5 squared)''')
p("The remainder operator, <font face='Courier'>%</font>, comes up constantly in real code for things "
  "like \"is this number even?\" (<font face='Courier'>n % 2 === 0</font>) or cycling through a fixed "
  "list of options, which is exactly how Tiffin cycles a meal's emoji through its palette of choices "
  "(Chapter 32 in Part 2): <font face='Courier'>(i + 1) % EMOJI_PALETTE.length</font> wraps back around to "
  "0 once it reaches the end of the list.")
sec("15.2 Comparison operators")
comp_table = [
    ["Operator", "Meaning"],
    ["===", "strictly equal (same type AND value) -- always prefer this"],
    ["!==", "strictly NOT equal -- always prefer this"],
    ["==  / !=", "loosely equal/unequal, with type coercion -- avoid"],
    [">  <", "greater than / less than"],
    [">=  <=", "greater than or equal / less than or equal"],
]
simple_table(comp_table, [90, CONTENT_W-90])
sec("15.3 Logical operators")
code('''true && false;    // false -- AND: both sides must be true
true || false;     // true  -- OR: at least one side must be true
!true;               // false -- NOT: flips a boolean

// short-circuit evaluation: && and || don't always evaluate BOTH sides
const a = user && user.name;   // if `user` is falsy (e.g. null), stops there -- never tries
                                  // to read .name on it, avoiding a crash
const b = savedName || 'Guest'; // if `savedName` is falsy/empty, falls back to 'Guest' ''')
p("This \"short-circuiting\" behavior of <font face='Courier'>&amp;&amp;</font> and "
  "<font face='Courier'>||</font> is used as a control-flow shortcut constantly throughout this codebase "
  "— for example, <font face='Courier'>opts = opts || {}</font> (\"if no options were passed, default to "
  "an empty object\") and <font face='Courier'>dbFoodById(id) || null</font> (Chapter 7.2's earlier "
  "example), which relies on OR to supply a fallback the moment the first value is falsy.")
sec("15.4 The ternary operator, revisited")
code('''const label = isOver ? 'over' : 'under';

// nested (use sparingly -- readability suffers fast with more than one level):
const size = weight > 100 ? 'large' : weight > 50 ? 'medium' : 'small';''')
sec("15.5 Assignment operators")
code('''let total = 0;
total += 5;    // same as: total = total + 5
total -= 2;     // same as: total = total - 2
total *= 3;      // same as: total = total * 3''')
quiz("Operators & Expressions", [
    ("What does 7 % 3 evaluate to, and what does the % operator actually compute?",
     "1 — % (modulo/remainder) gives you what's left over after dividing as many WHOLE times as possible: "
     "3 goes into 7 twice (6), leaving a remainder of 1."),
    ("In the expression `user && user.name`, what happens if `user` is null?",
     "The expression short-circuits and evaluates to null (or whatever falsy value `user` was) WITHOUT "
     "ever attempting to read `.name` — this pattern is a common, safe way to avoid a crash from trying "
     "to access a property on something that might not exist."),
    ("Rewrite `total = total + 5` using a shorthand assignment operator.",
     "total += 5"),
])

chapter("16. JavaScript — Control Flow (if/else/switch)")
sec("16.1 if / else if / else, revisited with more detail")
code('''const age = 15;

if (age >= 18) {
  console.log('adult');
} else if (age >= 13) {
  console.log('teen');
} else {
  console.log('child');
}
// Only ONE branch ever runs -- the first condition (top to bottom) that evaluates truthy.''')
sec("16.2 switch — choosing among many exact values")
code('''switch (action) {
  case 'nav':
    console.log('navigating');
    break;              // <-- without break, execution "falls through" into the NEXT case!
  case 'close-modal':
    console.log('closing');
    break;
  default:
    console.log('unknown action');
}''')
p("A <font face='Courier'>switch</font> is often used instead of a long if/else-if chain when you're "
  "comparing ONE value against many exact possibilities. Interestingly, this app deliberately does NOT "
  "use switch for its huge ~60-branch action dispatcher (Chapter 36 in Part 2) — it uses a long chain of "
  "<font face='Courier'>if (action === '...') { ...; return; }</font> statements instead, specifically "
  "because each branch there needs to <font face='Courier'>return</font> immediately afterward (skipping "
  "everything below), which an if-chain expresses more directly than a switch/break pattern would.")
sec("16.3 Truthy and falsy, revisited with the full list")
p("Exactly six values are \"falsy\" in JavaScript — treated as false inside an "
  "<font face='Courier'>if</font> condition — and this list is worth memorizing completely, since "
  "EVERYTHING else, including an empty array/object, is truthy:")
code('''false, 0, -0, 0n, "", null, undefined, NaN   // ALL of JavaScript's falsy values

if ([]) { console.log('this runs!'); }    // an empty array is truthy -- easy to get wrong
if ({}) { console.log('this runs too!'); } // an empty object is truthy too''')
quiz("Control Flow", [
    ("If you forget the `break` inside a switch case, what happens?",
     "Execution 'falls through' into the next case below it, running that code too, regardless of "
     "whether its own condition matches — a classic switch-statement bug."),
    ("Is an empty array, [], truthy or falsy in an if condition?",
     "Truthy — JavaScript's only falsy values are false, 0, -0, 0n, \"\" (empty string), null, undefined, "
     "and NaN. An empty array or empty object is NOT on that list, so both are truthy."),
])

chapter("17. JavaScript — Loops")
sec("17.1 The classic for loop")
code('''for (let i = 0; i < 5; i++) {
  console.log(i);   // prints 0, 1, 2, 3, 4
}
// the three parts: (1) run once before starting; (2) checked before EVERY iteration --
// loop stops the moment this is false; (3) runs after EVERY iteration''')
sec("17.2 while and do...while")
code('''let count = 0;
while (count < 3) {         // condition checked BEFORE each iteration -- may run zero times
  console.log(count);
  count++;
}

let n = 0;
do {
  console.log(n);            // condition checked AFTER each iteration -- always runs at least once
  n++;
} while (n < 3);''')
sec("17.3 for...of — the modern way to loop over an array's VALUES")
code('''const foods = ['rice', 'dal', 'roti'];
for (const food of foods) {
  console.log(food);   // 'rice', then 'dal', then 'roti'
}''')
sec("17.4 for...in — looping over an object's KEYS")
code('''const goals = { calorieGoal: 2000, proteinGoal: 100 };
for (const key in goals) {
  console.log(key, goals[key]);   // "calorieGoal 2000", then "proteinGoal 100"
}''')
note("In practice, this codebase almost never writes a raw for/while loop over an array or object — it "
     "uses array methods like <font face='Courier'>.map()</font>, <font face='Courier'>.forEach()</font>, "
     "and <font face='Courier'>.filter()</font> instead (Chapter 20), which is considered clearer, more "
     "modern style for array iteration specifically. Raw loops are still the right tool for things that "
     "AREN'T simply array iteration — a fixed number of repetitions, or looping backward through a range "
     "of dates, both of which this app's code does use a plain for loop for.")
sec("17.5 break and continue")
code('''for (let i = 0; i < 10; i++) {
  if (i === 5) break;      // exit the loop entirely, right now
  if (i % 2 === 0) continue; // skip the REST of this iteration, jump to the next one
  console.log(i);            // only prints odd numbers less than 5: 1, 3
}''')
quiz("Loops", [
    ("What's the key difference between while and do...while?",
     "while checks its condition BEFORE each iteration, so it might run zero times if the condition "
     "starts false. do...while checks its condition AFTER each iteration, so the loop body always runs "
     "at least once, even if the condition is false from the start."),
    ("What's the difference between for...of and for...in?",
     "for...of iterates over an array's (or other iterable's) VALUES directly. for...in iterates over an "
     "object's (or array's) enumerable KEYS/indices — using for...in on an array is generally discouraged "
     "in favor of for...of or array methods."),
    ("What does `continue` do differently from `break` inside a loop?",
     "continue skips the rest of the CURRENT iteration and jumps to the next one (the loop keeps going); "
     "break exits the loop entirely, immediately, with no further iterations at all."),
])

chapter("18. JavaScript — Functions, Deep Dive")
sec("18.1 Three ways to write a function")
code('''// 1. Function declaration -- "hoisted" (Ch.19): can be called even BEFORE this line runs
function add(a, b) {
  return a + b;
}

// 2. Function expression -- stored in a variable, NOT hoisted the same way
const subtract = function(a, b) {
  return a - b;
};

// 3. Arrow function -- shorter syntax, and handles `this` differently (see 18.4)
const multiply = (a, b) => {
  return a * b;
};''')
sec("18.2 Parameters, arguments, and defaults")
code('''function greet(name = 'friend') {   // 'friend' is used if no argument is passed at all
  return `Hello, ${name}`;
}
greet();          // "Hello, friend"
greet('Priya');    // "Hello, Priya"

function sum(...numbers) {          // "rest parameter" -- gathers any number of arguments into an array
  return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4);    // 10''')
sec("18.3 return — and what happens without one")
p("A function without an explicit <font face='Courier'>return</font> statement implicitly returns "
  "<font face='Courier'>undefined</font>. This is a common source of bugs: calling a function purely for "
  "its side effects (like <font face='Courier'>saveState()</font>, which just writes to localStorage) is "
  "fine, but forgetting to <font face='Courier'>return</font> from a function you MEANT to produce a "
  "value from will silently hand back <font face='Courier'>undefined</font> instead of erroring.")
sec("18.4 this inside a regular function vs. an arrow function")
p("<font face='Courier'>this</font> is a special keyword whose value depends on HOW a regular function is "
  "called (not where it's defined) — a notoriously confusing part of JavaScript. Arrow functions sidestep "
  "the confusion entirely: they don't have their own <font face='Courier'>this</font> at all — they "
  "simply use whatever <font face='Courier'>this</font> was in the surrounding code where they were "
  "written. This is a large part of why modern JavaScript (including every callback in this app's "
  "codebase) leans so heavily on arrow functions for short, inline callbacks.")
sec("18.5 Functions as values — the idea revisited")
p("Because a function is just another kind of value, it can be stored in a variable, put inside an array "
  "or object, and — most importantly for this app — passed as an argument into another function, to be "
  "called later. This is called a <b>callback</b>, and it's the entire mechanism behind event handling "
  "(Chapter 25) and array methods like <font face='Courier'>.map()</font> (Chapter 20).")
quiz("Functions", [
    ("What value does a function return if it has no explicit `return` statement?",
     "undefined — this is a silent, easy-to-miss bug source if you meant to compute and return something "
     "but forgot the return keyword."),
    ("What's a `callback`?",
     "A function passed as an argument into another function, to be called (invoked) by that other "
     "function later — the basis of how array methods like .map() and event listeners both work."),
    ("Why do arrow functions avoid a common source of `this`-related bugs that regular functions have?",
     "Arrow functions don't define their own `this` at all — they inherit whatever `this` was in the "
     "surrounding code where they were written, rather than having it depend on how/where the function "
     "gets CALLED, which is the confusing behavior regular functions have."),
])

chapter("19. JavaScript — Scope & Hoisting")
sec("19.1 What \"scope\" means")
p("Scope is the answer to \"from where in the code can I see this variable?\" JavaScript has three kinds:")
bullets([
    "<b>Global scope</b> — declared outside any function or block; visible EVERYWHERE in the file "
    "(the reason Tiffin wraps its entire app in an IIFE, Chapter 26, to avoid polluting this).",
    "<b>Function scope</b> — a variable declared inside a function is only visible inside that function "
    "(and any functions nested within it).",
    "<b>Block scope</b> — a variable declared with <font face='Courier'>const</font>/"
    "<font face='Courier'>let</font> inside a <font face='Courier'>{ }</font> block (an if, a loop, "
    "even a bare pair of braces) is only visible inside that block.",
])
code('''function example() {
  if (true) {
    const x = 5;    // block-scoped -- only exists inside this if-block
    let y = 10;       // also block-scoped
    var z = 15;         // FUNCTION-scoped, not block-scoped -- leaks out of the if-block!
  }
  console.log(z);   // 15 -- var "leaked" out of the block
  console.log(x);    // ReferenceError -- x doesn't exist out here
}''')
p("This is a major reason modern style avoids <font face='Courier'>var</font>: its function-level "
  "(rather than block-level) scoping is a frequent source of confusing bugs, especially inside loops. "
  "<font face='Courier'>const</font> and <font face='Courier'>let</font> were added to the language "
  "specifically to provide predictable, block-level scoping instead.")
sec("19.2 The scope chain")
p("When code references a variable, JavaScript looks for it in the current (innermost) scope first; if "
  "not found there, it looks in the next scope out, and so on, all the way to the global scope — this "
  "search path is called the <b>scope chain</b>. A function defined inside another function can always "
  "see (\"close over\") the outer function's variables — this is the foundation of closures, covered "
  "fully in Chapter 26.")
sec("19.3 Hoisting")
p("JavaScript processes a script in two conceptual passes: first it scans for declarations and sets up "
  "memory for them, THEN it runs the code top to bottom. This means <font face='Courier'>function</font> "
  "declarations (not expressions) are fully usable even before the line where they're written — this is "
  "called <b>hoisting</b>.")
code('''sayHi();               // works! "Hi" is printed -- function declarations are hoisted entirely

function sayHi() {
  console.log('Hi');
}

console.log(mystery);   // ReferenceError -- let/const are hoisted too, but left in an unusable
let mystery = 5;          // "temporal dead zone" until their actual declaration line runs''')
p("Because of this, this app's code always defines its functions before an event handler needs to call "
  "them — relying on hoisting for top-level function declarations is normal, expected JavaScript style, "
  "but relying on it for <font face='Courier'>let</font>/<font face='Courier'>const</font> variables would "
  "simply crash, so those are always declared before their first use.")
quiz("Scope & Hoisting", [
    ("A variable declared with `var` inside an if-block — is it visible outside that block, "
     "in the same function?",
     "Yes — var is function-scoped, not block-scoped, so it 'leaks' out of if/for/while blocks (though "
     "still not out of the enclosing function). const and let, by contrast, are genuinely block-scoped "
     "and would NOT be visible outside that same if-block."),
    ("Can you call a function declared with `function name() {...}` from a line of code ABOVE where "
     "it's written in the file?",
     "Yes — function declarations (not function expressions or arrow functions assigned to a variable) "
     "are fully hoisted, meaning the whole function is available throughout its scope even before the "
     "line that defines it actually executes."),
    ("What is the 'scope chain'?",
     "The ordered sequence of scopes JavaScript searches through to resolve a variable reference: current "
     "(innermost) scope first, then each enclosing scope outward, ending at the global scope. A nested "
     "function can always see variables from any scope that encloses it."),
])

chapter("20. JavaScript — Arrays, Deep Dive")
sec("20.1 Creating and accessing arrays")
code('''const fruits = ['apple', 'banana', 'cherry'];
fruits[0];            // 'apple'   -- indexes start at 0
fruits[fruits.length - 1];  // 'cherry'  -- the last item, using .length
fruits.length;          // 3''')
sec("20.2 Arrays hold REFERENCES, not copies")
code('''const a = [1, 2, 3];
const b = a;          // b now points to the SAME array in memory, not a new copy
b.push(4);
console.log(a);        // [1, 2, 3, 4]  -- a changed too! They're the same array.

const c = [...a];       // spread copies the array's CURRENT items into a brand new array
c.push(5);
console.log(a);          // still [1, 2, 3, 4] -- c is independent now''')
p("This is exactly why Tiffin writes <font face='Courier'>[...STATE.weightLog].sort(...)</font> rather "
  "than <font face='Courier'>STATE.weightLog.sort(...)</font> directly (Chapter 27, 32 in Part 2) — "
  "<font face='Courier'>.sort()</font> mutates the array it's called on IN PLACE, and sorting a plain "
  "reference to the real state array would silently reorder the actual stored data as a side effect of "
  "what's supposed to be a read-only \"give me this sorted for display\" operation.")
sec("20.3 Mutating vs. non-mutating methods — a crucial distinction")
mut_table = [
    ["Mutating (changes original)", "Non-mutating (returns a new array)"],
    ["push, pop, shift, unshift", "map, filter, slice"],
    ["splice, sort, reverse", "concat, join"],
]
simple_table(mut_table, [CONTENT_W/2, CONTENT_W/2])
code('''const arr = [1, 2, 3];
arr.push(4);       // arr is now [1, 2, 3, 4] -- MUTATED in place; push returns the new length, 4

const doubled = arr.map(n => n * 2);   // returns a BRAND NEW array: [2, 4, 6, 8]
console.log(arr);                        // arr itself is unchanged: [1, 2, 3, 4]''')
sec("20.4 The core methods used throughout this app")
sub(".map() — transform every item into something new, 1-to-1")
code('''const kcals = foods.map(food => food.kcal);
const html = foods.map(f => `<div>${f.name}</div>`).join('');   // build HTML strings from data''')
sub(".filter() — keep only items that pass a test")
code('''const indianFoods = foods.filter(f => f.category === 'Indian');''')
sub(".forEach() — do something with every item, without producing a new array")
code('''NUTRIENT_KEYS.forEach(key => {
  total[key] = (a[key] || 0) + (b[key] || 0);
});''')
sub(".find() — the first matching item, or undefined")
code('''function dbFoodById(id) {
  return FOOD_DB.find(f => f.id === id) || null;
}''')
sub(".reduce() — combine every item down into a single value")
code('''const total = [10, 20, 30].reduce((sum, n) => sum + n, 0);   // 60
// (sum, n) => ... runs once per item; `sum` carries forward between calls, starting at 0''')
sub("Other frequently useful methods")
code('''arr.includes(3);        // true if 3 is anywhere in the array
arr.indexOf(3);           // the index of the first 3, or -1 if not found
arr.some(n => n > 2);       // true if AT LEAST ONE item passes the test
arr.every(n => n > 0);        // true only if ALL items pass the test
arr.join(', ');                 // combine into one string: "1, 2, 3"
arr.slice(1, 3);                  // a NEW array containing items at index 1 up to (not including) 3
arr.splice(1, 1);                   // MUTATES: removes 1 item starting at index 1, returns the removed items''')
note("<font face='Courier'>.slice()</font> and <font face='Courier'>.splice()</font> look alike but "
     "behave very differently: slice is non-mutating (safe to use on data you don't want to change) and "
     "splice mutates in place. This app uses <font face='Courier'>.splice()</font> deliberately whenever "
     "it wants to remove an entry from the diary (e.g. deleting a logged food) — mutating "
     "<font face='Courier'>STATE</font> directly is exactly the intended behavior there.")
quiz("Arrays", [
    ("const a = [1,2]; const b = a; b.push(3); — does `a` now include the 3 as well?",
     "Yes — `b = a` copies the REFERENCE to the array, not the array's contents, so `a` and `b` point to "
     "the exact same array in memory. Mutating one mutates the other. To get an independent copy you'd "
     "need something like `const b = [...a]`."),
    ("Which of these mutate their array in place: .map(), .push(), .filter(), .splice()?",
     ".push() and .splice() mutate in place. .map() and .filter() do NOT mutate — they return a brand "
     "new array, leaving the original untouched."),
    ("What does .find() return if nothing in the array matches?",
     "undefined — which is why this codebase commonly writes `.find(...) || null` to turn that into an "
     "explicit, intentional null instead."),
])

chapter("21. JavaScript — Objects, Deep Dive")
sec("21.1 Object literals, revisited")
code('''const food = {
  name: 'Rice',
  kcal: 200,
  isVegetarian: true,
};''')
sec("21.2 Dot notation vs. bracket notation")
code('''food.name;          // 'Rice'  -- dot notation: the key name is written literally in the code
food['name'];         // 'Rice'  -- bracket notation: same result

const key = 'kcal';
food[key];              // 200 -- bracket notation lets the KEY itself be a variable/expression
food.key;                // undefined -- this looks for a property LITERALLY named "key", which doesn't exist!''')
p("Bracket notation with a variable is essential whenever a property name isn't known until the code "
  "runs. Recall Chapter 20's <font face='Courier'>NUTRIENT_KEYS</font> array of nutrient name strings — "
  "every nutrient-math function in Tiffin loops over that array and reads "
  "<font face='Courier'>food[key]</font> for each one, which is only possible with bracket notation "
  "(dot notation could never express \"look up whatever key this loop variable currently holds\").")
sec("21.3 Objects also hold references")
code('''const original = { x: 1 };
const alias = original;
alias.x = 99;
console.log(original.x);   // 99 -- same underlying object, same as arrays in Ch.20.2

const copy = { ...original };   // spread makes a shallow copy -- a NEW, independent object
copy.x = 5;
console.log(original.x);          // still 99 -- copy is independent''')
p("\"Shallow\" copy matters: <font face='Courier'>{...original}</font> copies "
  "<font face='Courier'>original</font>'s own top-level keys into a new object, but if one of those "
  "values is ITSELF an object or array, that nested value is still just a reference, shared between the "
  "original and the copy. Tiffin's <font face='Courier'>{...DEFAULT_GOALS}</font> pattern (Chapter 23 in "
  "Part 2) works safely here specifically because every value inside <font face='Courier'>DEFAULT_GOALS</font> "
  "is a primitive (a plain number or string), not a nested object — so a shallow copy is all that's "
  "needed to get a fully independent goals object per user.")
sec("21.4 Useful Object methods")
code('''Object.keys({a:1, b:2});             // ['a', 'b']            -- an array of just the keys
Object.values({a:1, b:2});            // [1, 2]                 -- an array of just the values
Object.entries({a:1, b:2});            // [['a',1], ['b',2]]     -- an array of [key, value] pairs
Object.assign({}, obj1, obj2);          // merges obj2's keys ONTO A COPY of obj1 (obj1 itself untouched)''')
sec("21.5 hasOwnProperty — checking if a key genuinely exists")
code('''const obj = { name: 'Alice' };
'name' in obj;                    // true
obj.hasOwnProperty('name');         // true -- checks the object's OWN keys specifically
Object.prototype.hasOwnProperty.call(obj, 'name'); // true, but safer -- doesn't rely on `obj`
                                                       // still having the normal Object prototype''')
p("That last, more defensive form appears verbatim in this app's "
  "<font face='Courier'>mergeKnownFields()</font> function (Chapter 24 in Part 2) — a real, deliberate "
  "security choice, not just a stylistic preference, explained fully there.")
quiz("Objects", [
    ("Given `const key = 'age'; const person = {age: 30};` — how do you read the age using the `key` "
     "variable?",
     "person[key] — bracket notation lets the property name be computed/dynamic. person.key would "
     "instead look for a literal property named \"key\", which doesn't exist here."),
    ("Does {...original} produce a fully independent, deep copy of a nested object?",
     "No — spread produces a SHALLOW copy: the object's own top-level keys are copied into a new object, "
     "but if any value is itself an object/array, that nested value is still a shared reference between "
     "the original and the copy."),
    ("What's the difference between Object.keys(obj) and Object.entries(obj)?",
     "Object.keys returns an array of just the property names. Object.entries returns an array of "
     "[key, value] pairs for every property — strictly more information."),
])

chapter("22. JavaScript — Strings & Basic Regex")
sec("22.1 Strings, revisited")
code('''const s = "Hello, World!";
s.length;              // 13
s.toUpperCase();          // "HELLO, WORLD!"
s.toLowerCase();           // "hello, world!"
s.trim();                    // removes whitespace from both ends
s.includes("World");           // true
s.slice(0, 5);                   // "Hello"  -- like array slice, works on characters
s.replace("World", "There");       // "Hello, There!"  -- replaces the FIRST match only
s.split(", ");                       // ["Hello", "World!"]  -- turns a string into an array''')
sec("22.2 Template literals, revisited in full")
code('''const name = "chicken curry", kcal = 350;
const msg = `Added ${name} (${kcal} kcal)`;    // embeds expressions directly

// can contain ANY expression, not just a variable name:
const status = `${kcal > 300 ? 'high' : 'normal'} calorie`;

// can span multiple lines -- exactly how this app builds multi-line HTML fragments:
const html = `<div class="food-row">
  <span>${name}</span>
  <span>${kcal} kcal</span>
</div>`;''')
sec("22.3 Regular expressions (regex) — pattern matching in text")
p("A regex is a compact, specialized mini-language for describing a PATTERN a string might match, rather "
  "than one exact literal string. Full regex syntax is a topic of its own, but a small amount goes a long "
  "way, and this app uses exactly one regex, worth understanding completely:")
code('''const pattern = /[&<>"']/g;
//               │       │
//               │       └─ 'g' flag: find ALL matches, not just the first
//               └───────── a character class: matches ANY ONE of these 5 characters

"Tom & Jerry".replace(pattern, c => '[' + c + ']');
// -> "Tom [&] Jerry"''')
p("<font face='Courier'>[...]</font> defines a <b>character class</b> — match any single character that "
  "appears inside the brackets. <font face='Courier'>[&lt;&gt;\"']</font> matches any one of "
  "<font face='Courier'>&amp; &lt; &gt; \" '</font> — precisely the five characters that are dangerous to "
  "leave unescaped inside HTML. The <font face='Courier'>g</font> (\"global\") flag after the closing "
  "slash means \"don't stop at the first match — replace EVERY occurrence in the whole string.\" This "
  "exact regex is the heart of Tiffin's <font face='Courier'>escapeHtml()</font> function, covered fully "
  "in Chapter 39 of Part 2.")
code('''function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}''')
p("<font face='Courier'>.replace(pattern, callback)</font> — when the second argument is a function "
  "instead of a plain replacement string, that function gets called once PER MATCH, receiving the "
  "matched character, and whatever it returns becomes the replacement. Here, the callback looks up each "
  "dangerous character in a small object and returns its safe HTML-entity equivalent.")
quiz("Strings & Regex", [
    ("What does \"Hello\".slice(0, 3) return?",
     "\"Hel\" — slice(start, end) returns characters from index `start` up to (but not including) index "
     "`end`, just like array slicing."),
    ("In the regex /[&<>\"']/g, what does the trailing g flag do?",
     "It makes the match/replace operate globally — finding and acting on EVERY occurrence in the string, "
     "not just stopping after the first one."),
    ("Why does escapeHtml's .replace() call pass a FUNCTION as its second argument instead of a "
     "plain string?",
     "Because the correct replacement is different depending on WHICH dangerous character was matched "
     "(& needs &amp;, < needs &lt;, etc.) — a function gets called once per match with that exact "
     "character, letting it look up and return the right replacement each time, rather than replacing "
     "every match with one single fixed string."),
])

chapter("23. JavaScript — Modern Syntax, In Depth")
sec("23.1 Destructuring, revisited with more forms")
code('''// Array destructuring
const [first, second] = ['a', 'b'];

// Skipping items
const [, , third] = ['a', 'b', 'c'];   // third = 'c'

// Object destructuring
const { name, age } = person;

// Renaming while destructuring
const { name: userName } = person;      // userName now holds person.name

// Default values if the property is missing
const { theme = 'system' } = settings;

// Nested destructuring
const { profile: { sex, age: userAge } } = STATE;''')
sec("23.2 Rest and spread, the full picture")
p("The same <font face='Courier'>...</font> syntax means two different (opposite) things depending on "
  "context: <b>spread</b> EXPANDS a collection outward; <b>rest</b> GATHERS remaining items inward.")
code('''// SPREAD -- expanding
const combined = [...arr1, ...arr2];        // one new array containing both arrays' items
const merged = { ...defaults, ...overrides }; // one new object, overrides' keys win on conflict

// REST -- gathering (opposite direction)
function sum(...numbers) { /* numbers is an array of every argument passed in */ }
const [head, ...tail] = [1, 2, 3, 4];         // head = 1, tail = [2, 3, 4]
const { kcal, ...otherNutrients } = food;       // kcal pulled out separately, everything else grouped''')
sec("23.3 Optional chaining (?.) and nullish coalescing (??)")
code('''const city = user?.address?.city;
// If `user` is null/undefined, OR `user.address` is null/undefined, this short-circuits
// to `undefined` immediately, instead of throwing "Cannot read property 'city' of undefined"

const goal = settings.calorieGoal ?? 2000;
// ?? only falls back if the left side is null or undefined SPECIFICALLY --
// unlike ||, it does NOT treat 0 or '' as "missing"
const goalOr = settings.calorieGoal || 2000;
// with ||, a legitimately-set calorieGoal of 0 would ALSO trigger the fallback to 2000 -- a real bug!''')
p("The distinction between <font face='Courier'>||</font> and <font face='Courier'>??</font> matters a "
  "lot for exactly the kind of numeric settings this app stores — a goal of <font face='Courier'>0</font> "
  "is a valid (if unusual) value a user might genuinely set, and <font face='Courier'>||</font> would "
  "incorrectly treat it as \"missing\" and silently override it, whereas <font face='Courier'>??</font> "
  "only treats <font face='Courier'>null</font>/<font face='Courier'>undefined</font> specifically as "
  "\"missing.\"")
quiz("Modern Syntax", [
    ("What's the difference between spread and rest, given they use the identical ... syntax?",
     "Spread expands an existing array/object OUT into individual elements/keys (e.g. building a new "
     "array from pieces of others). Rest does the opposite — it GATHERS multiple individual values INTO "
     "one array (e.g. collecting a function's extra arguments, or the 'remaining' items after "
     "destructuring some off the front)."),
    ("Why might `settings.calorieGoal || 2000` be a bug if calorieGoal is legitimately set to 0?",
     "Because 0 is falsy, || would treat a genuinely-set value of 0 as if it were missing and incorrectly "
     "fall back to 2000. The nullish coalescing operator, ??, avoids this — it only falls back when the "
     "left side is specifically null or undefined, treating 0 (and '') as valid, present values."),
    ("What does `user?.address?.city` evaluate to if `user.address` doesn't exist?",
     "undefined, safely — optional chaining short-circuits the moment it hits a null/undefined link in "
     "the chain, rather than throwing an error trying to read a property off of undefined."),
])

chapter("24. JavaScript — The DOM, In Depth")
sec("24.1 The DOM tree, revisited")
p("Recall from Part 1's earlier chapter that the DOM is the browser's live, in-memory tree of every "
  "element on the page. Each element is a JavaScript object with properties and methods you can read and "
  "call directly.")
sec("24.2 Every way to select an element")
code('''document.getElementById('viewRoot');       // the ONE element with this exact id
document.querySelector('.food-row');          // the FIRST element matching this CSS selector
document.querySelectorAll('.food-row');         // ALL matches, as a NodeList (array-like, not a real array)
document.querySelector('[data-action="nav"]');    // CSS attribute selectors work here too''')
sec("24.3 Traversing the tree from a known element")
code('''el.parentElement;      // the element directly containing this one
el.children;             // this element's direct child elements (a live HTMLCollection)
el.closest('.card');       // walks UP through ancestors until one matches, or returns null
el.querySelector('.icon');   // searches DOWN, only within this element's own descendants''')
p("<font face='Courier'>.closest()</font> is the single most-used traversal method in this app's entire "
  "codebase — it's the mechanism the whole event delegation system (Chapter 27) relies on to find \"which "
  "actionable element, if any, was this click inside of.\"")
sec("24.4 Reading and changing content")
code('''el.textContent;              // reads/sets PLAIN TEXT only -- safe, never parses HTML
el.textContent = 'Hello';

el.innerHTML;                  // reads/sets HTML -- browser PARSES whatever string you assign
el.innerHTML = '<b>Hi</b>';      // creates a real, bold <b> element -- powerful, but risky with
                                    // untrusted text (Chapter 39's XSS discussion)''')
sec("24.5 Attributes, classes, and inline styles")
code('''el.getAttribute('data-id');        // read any attribute's value
el.setAttribute('data-id', '123');   // set any attribute
el.dataset.id;                          // shortcut specifically for data-* attributes: reads data-id
el.dataset.action;                        // reads data-action

el.classList.add('active');
el.classList.remove('active');
el.classList.toggle('active');              // adds it if missing, removes it if present
el.classList.contains('active');             // true/false

el.style.width = '50%';                        // sets ONE inline CSS property directly''')
sec("24.6 Creating and inserting new elements")
code('''const div = document.createElement('div');
div.className = 'toast';
div.textContent = 'Saved!';
document.body.appendChild(div);        // adds it as the LAST child of <body>

el.remove();                              // removes an element from the page entirely''')
note("Tiffin's toast notifications (Chapter 24 in Part 2) are one of the few places this app builds an "
     "element with <font face='Courier'>createElement</font> + <font face='Courier'>appendChild</font> "
     "rather than an innerHTML string — almost everything else in the app is built as one big HTML "
     "string and inserted in a single <font face='Courier'>.innerHTML =</font> assignment instead, which "
     "is simpler when you're regenerating a whole section at once rather than adding one small element.")
quiz("The DOM", [
    ("What's the difference between el.textContent = '...' and el.innerHTML = '...'?",
     "textContent always treats the string as PLAIN TEXT, with no HTML parsing at all — safe by "
     "construction. innerHTML PARSES the string as HTML, creating real elements from any tags inside it — "
     "powerful, but risky if the string contains untrusted user data (see Chapter 39's XSS discussion)."),
    ("What does el.closest('.card') do?",
     "Starting from `el`, it walks UPWARD through ancestor elements (el itself, then its parent, then "
     "its parent's parent, etc.) until it finds one matching the given selector, or returns null if none "
     "match all the way to the document root."),
    ("How do you read the value of a data-action=\"delete\" attribute in JavaScript?",
     "el.dataset.action — the `dataset` property is a shortcut specifically for reading/writing any "
     "data-* attribute, converting the dash-separated name (data-action) into a camelCase property "
     "(dataset.action)."),
])

chapter("25. JavaScript — Events, In Depth")
sec("25.1 Listening for events, revisited")
code('''button.addEventListener('click', function(event) {
  console.log('clicked!', event.target);
});

button.removeEventListener('click', handlerFn);   // requires the SAME function reference to remove it''')
sec("25.2 Common event types")
event_table = [
    ["Event", "Fires when..."],
    ["click", "an element is clicked (mouse or, on touch devices, tapped)"],
    ["input", "a text field's value changes, on EVERY keystroke"],
    ["change", "a field's value is committed -- e.g. a file picker, dropdown, or checkbox"],
    ["submit", "a <form> is submitted (button click OR pressing Enter in a field)"],
    ["keydown / keyup", "a key is pressed down / released"],
    ["DOMContentLoaded", "the browser has finished parsing the initial HTML"],
    ["load", "a resource (image, whole page, etc.) has fully finished loading"],
]
simple_table(event_table, [130, CONTENT_W-130])
sec("25.3 The event object")
p("Every handler receives one argument — the event object — carrying details about what happened:")
code('''function onClick(e) {
  e.target;             // the EXACT element that was clicked (could be deep inside a button, e.g. an icon)
  e.currentTarget;        // the element the LISTENER was actually attached to
  e.type;                    // 'click'
  e.preventDefault();          // cancel the browser's default behavior for this event
  e.stopPropagation();           // stop this event from bubbling up to ancestor elements
}''')
sec("25.4 e.target vs. e.currentTarget — a frequent point of confusion")
p("If you click an <font face='Courier'>&lt;svg&gt;</font> icon sitting inside a "
  "<font face='Courier'>&lt;button&gt;</font>, and the listener is attached to "
  "<font face='Courier'>document</font> (as in this app's event delegation pattern, Chapter 27): "
  "<font face='Courier'>e.target</font> is the SVG itself (the innermost element actually clicked); "
  "<font face='Courier'>e.currentTarget</font> is <font face='Courier'>document</font> (where the "
  "listener lives). This is exactly why Tiffin's click handler uses "
  "<font face='Courier'>e.target.closest('[data-action]')</font> rather than "
  "<font face='Courier'>e.target</font> alone — clicking the icon needs to resolve back up to the "
  "actionable button that contains it.")
sec("25.5 preventDefault vs. stopPropagation — not the same thing")
p("These are commonly confused because both sound like \"stop this event.\" They stop two DIFFERENT "
  "things: <font face='Courier'>preventDefault()</font> cancels the BROWSER's own built-in behavior for "
  "this event (like a form actually submitting/reloading the page, or a link actually navigating) — the "
  "event still bubbles up normally afterward. <font face='Courier'>stopPropagation()</font> stops the "
  "event from bubbling any further UP through ancestor elements — it has nothing to do with the browser's "
  "default behavior at all. A handler can call either, both, or neither, depending on what it needs.")
sec("25.6 Event bubbling and capturing")
p("Recall from earlier: a DOM event fires first on the exact element clicked, then \"bubbles\" upward "
  "through every ancestor, all the way to <font face='Courier'>document</font>. (There's also a rarer "
  "\"capturing\" phase that runs top-down BEFORE bubbling, opted into with a third "
  "<font face='Courier'>addEventListener</font> argument — not used anywhere in this app.) Bubbling is "
  "the entire foundation event delegation (Chapter 27) is built on.")
quiz("Events", [
    ("A click lands on an <svg> icon inside a <button>. If a listener is attached to `document`, "
     "what is e.target -- the svg, the button, or document?",
     "The svg — e.target is always the exact, innermost element the event actually originated on, "
     "regardless of where the listener itself is attached."),
    ("What's the difference between event.preventDefault() and event.stopPropagation()?",
     "preventDefault() cancels the browser's own built-in behavior for that event (like a form actually "
     "submitting, or a link actually navigating) — the event still bubbles normally. stopPropagation() "
     "stops the event from bubbling further up to ancestor elements — it has no effect on the browser's "
     "default behavior."),
    ("What event fires on every keystroke inside a text input: input or change?",
     "input — it fires immediately on every keystroke/value change. change fires later, when the value "
     "is COMMITTED (e.g. the field loses focus, or — for things like file pickers/checkboxes — the "
     "moment a discrete choice is made)."),
])

chapter("26. JavaScript — Closures & Event Delegation")
sec("26.1 Closures, revisited in depth")
p("A closure is what you get whenever a function is defined inside another function: the inner function "
  "permanently \"remembers\" — closes over — the variables that were in scope around it, even after the "
  "outer function has already finished running and would normally have its local variables cleaned up.")
code('''function makeCounter() {
  let count = 0;                    // private to this specific call of makeCounter
  return function() {
    count = count + 1;                // this inner function "closes over" `count`
    return count;
  };
}

const counterA = makeCounter();
const counterB = makeCounter();          // a SEPARATE, independent `count` for this call
counterA();   // 1
counterA();    // 2
counterB();     // 1  -- counterA and counterB don't share state; each closure has its own `count`''')
p("Closures are how <font face='Courier'>picker</font>, <font face='Courier'>mealBuilder</font>, and "
  "every other piece of \"currently open modal's working state\" in Tiffin's codebase stays alive and "
  "accessible across many separate event-handler calls, without needing to be stored on the DOM itself — "
  "they're just variables declared once, near the top of the IIFE (Chapter 19.1's global-within-the-IIFE "
  "scope), that every handler function can see and mutate.")
sec("26.2 IIFEs, revisited")
code('''(function(){
  "use strict";
  // every const/let declared in here is invisible OUTSIDE this function
})();   // <-- the trailing () calls the function immediately, right where it's defined''')
p("This is the exact top-level wrapper around Tiffin's entire app.js. Because the function is anonymous "
  "and called immediately, it never leaves a named function lying around in global scope either — the "
  "whole ~1,700-line app contributes exactly nothing to the global namespace.")
sec("26.3 Event delegation, the complete explanation")
p("We've now covered every prerequisite: event bubbling (Ch.25.6), <font face='Courier'>e.target</font> "
  "(Ch.25.4), <font face='Courier'>.closest()</font> (Ch.24.3), and <font face='Courier'>data-*</font> "
  "attributes (Ch.3.1, Ch.24.5). Event delegation combines all four into one pattern:")
code('''document.addEventListener('click', function(e) {
  const el = e.target.closest('[data-action]');
  if (!el) return;                      // click landed somewhere with no action -- ignore it
  const action = el.dataset.action;

  if (action === 'delete-entry') { /* ... */ return; }
  if (action === 'add-water') { /* ... */ return; }
  // ...dozens more
});''')
p("Instead of attaching a separate listener to every one of potentially hundreds of buttons across every "
  "screen, ONE listener on <font face='Courier'>document</font> catches every click, anywhere on the "
  "page, forever — including on buttons that don't exist yet at page-load time and get created later by "
  "a render function. This last point is the biggest practical win: since Tiffin constantly replaces "
  "large chunks of the DOM via <font face='Courier'>innerHTML</font> (Chapter 28 in Part 2), any "
  "per-element listener would be destroyed along with the old HTML and would need to be manually "
  "re-attached after every single re-render. A delegated listener on <font face='Courier'>document</font> "
  "never needs re-attaching, because it was never attached to the elements that keep getting replaced in "
  "the first place.")
quiz("Closures & Event Delegation", [
    ("In the makeCounter() example, why does calling counterB() return 1, not 3, even after "
     "counterA() had already been called twice?",
     "Each call to makeCounter() creates a brand NEW, independent `count` variable via its own closure — "
     "counterA and counterB each close over their own separate count, so they don't share state at all."),
    ("Why is event delegation especially well-suited to an app like Tiffin that constantly replaces "
     "big chunks of the DOM via innerHTML?",
     "A listener attached directly to an individual button gets destroyed the moment that button's HTML "
     "is replaced, and would need to be manually re-attached after every re-render. A single delegated "
     "listener on `document` is never attached to the elements being replaced, so it keeps working "
     "automatically for any new HTML inserted later, with zero extra setup."),
    ("What does el.closest('[data-action]') return if the clicked element has no such ancestor "
     "at all, not even itself?",
     "null — which is exactly why the very first line inside the handler is `if (!el) return;`, to "
     "safely ignore clicks that didn't land on anything actionable."),
])

chapter("27. JavaScript — Error Handling")
sec("27.1 try / catch / finally")
code('''try {
  const data = JSON.parse(someText);   // this line MIGHT throw, if someText isn't valid JSON
  console.log(data);
} catch (err) {
  console.log('Failed to parse:', err.message);   // runs ONLY if something in try{} threw
} finally {
  console.log('This always runs, error or not.');   // optional -- cleanup code goes here
}''')
p("Code that might fail goes inside <font face='Courier'>try</font>. If any line inside it throws an "
  "error, execution immediately jumps to <font face='Courier'>catch</font> — none of the remaining lines "
  "in <font face='Courier'>try</font> run. Without a surrounding try/catch, a thrown error would crash "
  "the whole script (specifically, unwind up the call stack until nothing catches it, then get logged as "
  "an uncaught error and stop that entire chain of execution).")
sec("27.2 throw — raising your own errors")
code('''function requireName(name) {
  if (!name) {
    throw new Error('Name is required');
  }
  return name;
}''')
sec("27.3 Where this app actually uses try/catch, and why")
p("Tiffin wraps exactly the operations that can genuinely fail for reasons outside its control: "
  "<font face='Courier'>JSON.parse()</font> on a user-supplied backup file (which might not even be valid "
  "JSON at all — Chapter 24 &amp; 35 in Part 2), and <font face='Courier'>localStorage.setItem()</font> "
  "(which can throw if storage is disabled or full, Chapter 24). In both cases, the "
  "<font face='Courier'>catch</font> block sets a flag or shows a friendly toast message instead of "
  "letting the whole app crash over one bad file or one storage quirk.")
code('''function importFromFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      // ...apply it...
    } catch (e) {
      toast("That file couldn't be read as a Tiffin backup.");   // graceful failure, not a crash
    }
  };
  reader.readAsText(file);
}''')
quiz("Error Handling", [
    ("If a try block's second line throws an error, does the try block's third line still run?",
     "No — the moment an error is thrown, execution immediately jumps out of the try block and into the "
     "matching catch block; any remaining lines in try are skipped entirely."),
    ("What happens if a thrown error is never caught by any try/catch?",
     "It propagates ('unwinds') up through every calling function until it either finds a catch block "
     "somewhere, or reaches the top with none — at which point it becomes an uncaught error, gets logged "
     "to the console, and execution of that particular call chain stops."),
    ("Why does Tiffin wrap JSON.parse() in a try/catch when importing a backup file, specifically?",
     "Because the file's content is entirely outside the app's control — a user could select any file, "
     "including one that isn't valid JSON at all, which would make JSON.parse throw. Catching that lets "
     "the app show a friendly error message instead of crashing the whole page over one bad file."),
])

chapter("28. JavaScript — Async JavaScript")
sec("28.1 The problem: some things take time")
p("Asking for camera access, reading a file, waiting for a network response — these can't complete "
  "instantly. If JavaScript simply paused and waited (\"blocked\") for each one, the entire page would "
  "freeze — no scrolling, no clicking, nothing — until it finished. Browsers avoid this with "
  "<b>asynchronous</b> (async) programming: code that starts a slow operation, then keeps the page "
  "responsive while it's in progress, and runs some follow-up code once it eventually finishes.")
sec("28.2 Callbacks — the original approach")
code('''setTimeout(function() {
  console.log('3 seconds later...');
}, 3000);
console.log('This prints FIRST, immediately -- setTimeout does not block.');''')
p("A callback is simply a function handed to another function, to be called later once something "
  "finishes. This works, but nesting many async steps this way (\"do this, and when it's done, do that, "
  "and when THAT's done...\") produces deeply nested, hard-to-read code nicknamed \"callback hell\" — "
  "which is exactly the problem Promises were introduced to solve.")
sec("28.3 Promises")
p("A <b>Promise</b> is an object representing a value that isn't ready yet, but will be at some point "
  "(or will fail). It has two possible outcomes you can attach handlers for: "
  "<font face='Courier'>.then()</font> (runs on success, with the resulting value) and "
  "<font face='Courier'>.catch()</font> (runs on failure, with the error).")
code('''scanDetector.detect(video)
  .then(codes => { if (codes.length) handleBarcode(codes[0].rawValue); })
  .catch(() => { /* detection failed this frame -- just try again next frame */ });''')
p("This exact <font face='Courier'>.then()</font>/<font face='Courier'>.catch()</font> pattern appears "
  "in Tiffin's barcode-scanning loop (Chapter 34 in Part 2), where "
  "<font face='Courier'>BarcodeDetector.detect()</font> returns a Promise each time it examines one video "
  "frame.")
sec("28.4 async/await — Promises with synchronous-looking syntax")
code('''async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    showMessage("Camera access isn't available here.");
  }
}''')
p("Marking a function <font face='Courier'>async</font> lets you use <font face='Courier'>await</font> "
  "inside it. <font face='Courier'>await somePromise</font> PAUSES that function at that exact line — "
  "without freezing the page, other code keeps running — and resumes it with the resolved value once the "
  "Promise finishes. This is really just different-looking syntax for the exact same "
  "<font face='Courier'>.then()</font> mechanism underneath; it's popular because it reads top-to-bottom "
  "like ordinary, synchronous code, and — critically — lets you use an ordinary try/catch (Chapter 27) "
  "around it for error handling, instead of a separate <font face='Courier'>.catch()</font> chain.")
sec("28.5 requestAnimationFrame — a special-purpose async scheduling tool")
code('''function scanLoop() {
  if (!scanning) return;
  scanDetector.detect(video).then(codes => {
    if (codes.length) { handleBarcode(codes[0].rawValue); }
    else { requestAnimationFrame(scanLoop); }   // check again right before the next repaint
  });
}''')
p("<font face='Courier'>requestAnimationFrame(fn)</font> schedules <font face='Courier'>fn</font> to run "
  "once, right before the browser's next screen repaint (typically ~60 times per second). Calling it "
  "again from inside itself, as above, creates a self-sustaining loop that automatically paces itself to "
  "the screen's refresh rate, and — as a bonus — automatically pauses when the browser tab isn't visible, "
  "unlike a fixed <font face='Courier'>setInterval</font> timer would.")
quiz("Async JavaScript", [
    ("Why doesn't `await somePromise` freeze the whole page while it's waiting?",
     "await only pauses the execution of the SPECIFIC async function it's inside — the rest of the page "
     "(other event handlers, rendering, user interaction) keeps working normally in the meantime. It's "
     "cooperative pausing of one function, not a full-page freeze."),
    ("What are the two things you can attach to a Promise to handle its eventual outcome?",
     ".then(onSuccess) for when it resolves successfully, and .catch(onError) for when it fails/rejects."),
    ("Is async/await a completely different mechanism from Promises, or built on top of them?",
     "Built on top of them — async/await is syntax that makes working with Promises read more like "
     "ordinary synchronous code (and lets you use try/catch for errors), but under the hood it's the "
     "exact same Promise mechanism."),
])

chapter("29. JSON — The Data Format, In Depth")
sec("29.1 JSON syntax rules, precisely")
p("JSON (JavaScript Object Notation) looks almost exactly like JavaScript object/array literals, but "
  "with stricter rules — these are exactly the mistakes that make a JSON file invalid:")
bullets([
    "Every key MUST be wrapped in double quotes — <font face='Courier'>{name: \"Rice\"}</font> is invalid "
    "JSON (even though it's valid JS); it must be <font face='Courier'>{\"name\": \"Rice\"}</font>.",
    "Strings must use double quotes, never single quotes.",
    "No comments are allowed anywhere — not <font face='Courier'>//</font>, not "
    "<font face='Courier'>/* */</font>.",
    "No trailing commas — <font face='Courier'>[1, 2, 3,]</font> is invalid; the comma after the last "
    "item must be removed.",
    "Only these value types are allowed: string, number, boolean, null, array, or another (nested) "
    "object — no functions, no <font face='Courier'>undefined</font>, no dates as a real type (dates get "
    "stored as plain strings by convention).",
])
code('''{
  "id": "rice-cooked-white",
  "name": "Rice, cooked (Chawal, white)",
  "kcal": 200,
  "isVegetarian": true,
  "allergens": null,
  "tags": ["staple", "gluten-free"],
  "nested": { "servingGrams": 150 }
}''')
sec("29.2 Converting between JSON text and live JavaScript values")
code('''const data = { name: "Alice", age: 30 };

const text = JSON.stringify(data);           // '{"name":"Alice","age":30}'  -- now a STRING
const text2 = JSON.stringify(data, null, 2);   // same, but pretty-printed with 2-space indentation

const back = JSON.parse(text);                  // { name: "Alice", age: 30 }  -- a live object again
JSON.parse("not valid json{{{");                   // throws a SyntaxError -- always wrap in try/catch
                                                       // when parsing anything not written by your own code''')
sec("29.3 The three separate jobs JSON does in this project")
bullets([
    "<b>food_db.json</b> — a static, 332-item database shipped with the app (Chapter 22 in Part 2).",
    "<b>localStorage persistence</b> — the user's live STATE object is JSON.stringify'd to save, and "
    "JSON.parse'd to load (Chapter 24 in Part 2) — this is JSON acting as a serialization format for an "
    "in-memory JavaScript value, not a file someone hand-writes.",
    "<b>Configuration files</b> — package.json and capacitor.config.json are JSON files that tools "
    "(npm, Capacitor) read to configure themselves; you edit these directly as text.",
])
quiz("JSON", [
    ("Is {name: 'Rice'} (single quotes, unquoted key) valid JSON?",
     "No — JSON requires double quotes for both keys and string values, with no exceptions. That exact "
     "object would need to be written {\"name\": \"Rice\"} to be valid JSON (though it IS valid as a "
     "plain JavaScript object literal, which has looser rules)."),
    ("What does JSON.stringify(obj, null, 2) do differently from JSON.stringify(obj)?",
     "The third argument (2) tells it to pretty-print the output with 2-space indentation, producing "
     "human-readable, multi-line JSON text, rather than one dense, unindented line."),
    ("Why should JSON.parse() almost always be wrapped in a try/catch when the input isn't something "
     "your own code just generated?",
     "Because JSON.parse throws a SyntaxError if given text that isn't valid JSON — and any input coming "
     "from outside your own program (a user-selected file, pasted text, etc.) can't be trusted to always "
     "be well-formed."),
])

chapter("30. Browser Storage — localStorage, sessionStorage & Cookies")
sec("30.1 localStorage, revisited")
code('''localStorage.setItem('key', 'value');   // save (value MUST be a string)
localStorage.getItem('key');               // load, or null if never set
localStorage.removeItem('key');              // delete one key
localStorage.clear();                          // delete everything for this site''')
sec("30.2 How localStorage compares to its alternatives")
storage_table = [
    ["", "localStorage", "sessionStorage", "Cookies"],
    ["Persists after tab closes?", "Yes", "No", "Yes (until expiry)"],
    ["Shared across tabs?", "Yes", "No (per-tab)", "Yes"],
    ["Typical size limit", "~5-10 MB", "~5-10 MB", "~4 KB"],
    ["Sent to the server automatically?", "Never", "Never", "Yes, every request!"],
]
tt5 = Table(storage_table, colWidths=[130, (CONTENT_W-130)/3, (CONTENT_W-130)/3, (CONTENT_W-130)/3])
tt5.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#E8552F')),
    ('TEXTCOLOR',(0,0),(-1,0), colors.white),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica'),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
    ('FONTSIZE',(0,0),(-1,-1),8.6),
    ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F7F7F7')]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(tt5)
spacer(10)
p("localStorage is the right choice for Tiffin specifically because it persists indefinitely and never "
  "gets automatically transmitted anywhere — cookies, by contrast, get attached to every single request a "
  "browser sends to a matching server, which is exactly why they're the traditional mechanism for "
  "server-side logins, but would be pure unnecessary overhead (and a very cramped 4KB limit) for an app "
  "with no server to send anything to in the first place.")
sec("30.3 Same-origin: storage is scoped per website")
p("localStorage is isolated per <b>origin</b> (protocol + domain + port) — a page on "
  "<font face='Courier'>example.com</font> can never read localStorage written by "
  "<font face='Courier'>other-site.com</font>. This is a fundamental browser security boundary, not "
  "something Tiffin has to implement itself.")
quiz("Browser Storage", [
    ("Your data needs to survive the user closing and reopening their browser tomorrow. "
     "localStorage or sessionStorage?",
     "localStorage — sessionStorage is cleared the moment its tab closes, while localStorage persists "
     "indefinitely until explicitly cleared."),
    ("Why would cookies be a poor fit for storing Tiffin's ~40-field settings object, even ignoring "
     "size limits?",
     "Cookies are automatically sent to the server with EVERY matching request — but Tiffin has no server "
     "to send anything to at all, so that behavior would be pure wasted overhead with zero benefit, on "
     "top of cookies' much smaller (~4KB) typical size limit."),
])

chapter("31. Browser & Web APIs")
sec("31.1 What a 'Web API' is")
p("Beyond the core DOM (Chapter 24), browsers expose dozens of additional built-in capabilities — "
  "collectively called Web APIs — that JavaScript can call into. None of these require any external "
  "library; they're simply available as global objects/functions the moment your script runs in a "
  "browser.")
sec("31.2 BarcodeDetector")
p("Scans a video frame (or image) for barcodes and reports what it finds, entirely built into supporting "
  "browsers — no external barcode-scanning library needed. Not universally supported, so real code always "
  "feature-detects first:")
code('''if ('BarcodeDetector' in window) {
  // safe to use it
} else {
  // fall back to manual entry
}''')
sec("31.3 MediaDevices.getUserMedia")
p("Requests permission to access the camera and/or microphone, returning a live \"MediaStream\" that can "
  "be piped into a <font face='Courier'>&lt;video&gt;</font> element for display. This ALWAYS requires "
  "explicit user permission — the browser shows its own native \"Allow camera access?\" prompt, which "
  "JavaScript cannot bypass or auto-approve.")
sec("31.4 FileReader")
p("Reads the contents of a local file the user has selected (via a file-input element), asynchronously "
  "via an <font face='Courier'>onload</font> callback, so reading a large file doesn't freeze the page.")
code('''const reader = new FileReader();
reader.onload = () => {
  const text = reader.result;   // the file's full text content, once loading finishes
};
reader.readAsText(file);          // starts the (async) read''')
sec("31.5 Clipboard API")
code('''navigator.clipboard.writeText('some text')
  .then(() => console.log('copied!'))
  .catch(() => console.log('clipboard access was denied'));''')
sec("31.6 Chart.js — a third-party library, not a Web API")
p("Worth distinguishing clearly: Chart.js is NOT built into the browser — it's an external, open-source "
  "JavaScript library that has to be downloaded (Tiffin fetches it from a CDN, Chapter 28 in Part 2) "
  "before its <font face='Courier'>Chart</font> object becomes available to use, unlike everything else "
  "in this chapter, which is simply always present.")
quiz("Browser & Web APIs", [
    ("Why does code always check `if ('BarcodeDetector' in window)` before using it, rather than "
     "just calling it directly?",
     "Because it's not supported in every browser — feature-detecting first lets the app gracefully fall "
     "back to a manual-entry alternative instead of crashing with an error in browsers that lack support."),
    ("Can JavaScript silently grant itself camera access without the user seeing a permission prompt?",
     "No — getUserMedia always requires the browser's own native permission prompt, which the user must "
     "explicitly approve; there is no way for a website's JavaScript to bypass or auto-approve this."),
    ("Is Chart.js a browser built-in Web API, or a separate library that has to be loaded?",
     "A separate, third-party library — it has to be fetched (e.g. from a CDN) and loaded as a script "
     "before its functionality becomes available, unlike true Web APIs like FileReader or "
     "BarcodeDetector, which are simply always present in a supporting browser."),
])

chapter("32. Python — From Zero")
sec("32.1 Why a second language at all?")
p("Recall from the project tour (Part 2 will cover this fully): this codebase uses Python for exactly "
  "one small job — a build script that glues the app's source files together. Python and JavaScript are "
  "different languages with different syntax, but the underlying programming CONCEPTS (variables, "
  "functions, loops, conditionals) are the same ideas you already learned in Chapters 14-19 — only the "
  "punctuation changes.")
sec("32.2 Indentation instead of curly braces")
p("This is Python's single most distinctive feature: instead of <font face='Courier'>{ }</font> marking "
  "a block of code, Python uses consistent INDENTATION (spaces) itself to mark where a block starts and "
  "ends. Getting indentation wrong is a real syntax error in Python, not just a style nitpick.")
code('''# JavaScript:
if (age >= 18) {
    console.log("adult");
} else {
    console.log("minor");
}

# The same logic in Python:
if age >= 18:
    print("adult")
else:
    print("minor")
# Note: no curly braces, no semicolons -- the colon (:) starts a block,
# and everything indented beneath it belongs to that block.''')
sec("32.3 Variables and types")
code('''name = "Alice"          # no `let`/`const` -- Python variables are just assigned directly
age = 30                  # int
height = 5.6                # float
is_active = True              # bool -- capitalized True/False, unlike JS's lowercase true/false
nothing = None                  # Python's equivalent of JS's null''')
sec("32.4 Lists and dictionaries — Python's arrays and objects")
code('''fruits = ["apple", "banana", "cherry"]   # a LIST -- like a JS array
fruits[0]                                    # "apple"
fruits.append("date")                          # like JS's .push()
len(fruits)                                      # like JS's .length, but it's a FUNCTION, not a property

person = {"name": "Alice", "age": 30}         # a DICT -- like a JS object
person["name"]                                  # "Alice" -- Python ALWAYS uses bracket notation,
                                                    # there's no dot-notation shortcut like JS has
person.get("age")                                 # 30 -- safer than [] if the key might not exist''')
sec("32.5 Functions")
code('''def add(a, b):              # `def` instead of `function`
    return a + b

def greet(name="friend"):      # default parameter value, same idea as JS
    return f"Hello, {name}"     # an f-string -- Python's equivalent of a JS template literal''')
p("<font face='Courier'>f\"Hello, {name}\"</font> is Python's direct equivalent of JavaScript's "
  "<font face='Courier'>`Hello, ${name}`</font> — the <font face='Courier'>f</font> prefix before the "
  "opening quote is what tells Python to evaluate the <font face='Courier'>{...}</font> expressions "
  "inside the string.")
sec("32.6 Loops")
code('''for fruit in fruits:            # like JS's for...of
    print(fruit)

for i in range(5):                # like a classic for(let i=0; i<5; i++) loop
    print(i)                        # prints 0, 1, 2, 3, 4

count = 0
while count < 3:                  # works exactly like JS's while
    print(count)
    count += 1                      # Python HAS +=, but no ++ shorthand -- must write count += 1''')
sec("32.7 Importing code from other modules")
code('''import pathlib          # brings in Python's built-in "pathlib" module, used as pathlib.Path(...)
import hashlib            # used for computing hashes (like SHA-256)
import base64               # used for base64 encoding/decoding
import argparse                # used for parsing command-line arguments

from pathlib import Path         # imports just ONE specific name directly, so you can write Path(...)
                                     # instead of pathlib.Path(...)''')
p("This is conceptually the same idea as JavaScript's <font face='Courier'>&lt;script src=\"...\"&gt;</font> "
  "or, in more modern JS, <font face='Courier'>import</font> statements — pulling in code someone else "
  "already wrote so you don't have to reimplement it. Python ships with a huge standard library of these "
  "built-in modules; <font face='Courier'>pathlib</font>, <font face='Courier'>hashlib</font>, "
  "<font face='Courier'>base64</font>, and <font face='Courier'>argparse</font> are all part of it — "
  "build.py needs no separate installation step for any of them.")
sec("32.8 Reading and writing files")
code('''from pathlib import Path

text = Path("app.js").read_text(encoding="utf-8")     # read an entire file as one string
Path("output.txt").write_text("hello", encoding="utf-8")  # overwrite a file with new content''')
p("<font face='Courier'>encoding=\"utf-8\"</font> specifies exactly how the file's bytes should be "
  "interpreted as text — UTF-8 is the standard, universal text encoding capable of representing every "
  "character in every language, and specifying it explicitly (rather than relying on a possibly "
  "inconsistent system default) is considered best practice for reliable, portable code.")
quiz("Python Basics", [
    ("What defines a block of code in Python, if not curly braces?",
     "Consistent indentation (whitespace) — everything indented at the same level beneath a line ending "
     "in a colon (like `if x:` or `def f():`) belongs to that block. Inconsistent indentation is a real "
     "syntax error."),
    ("What's the Python equivalent of a JavaScript object literal, {name: 'Alice'}?",
     "A dict (dictionary): {\"name\": \"Alice\"} — read with person[\"name\"] (Python always uses bracket "
     "notation for dicts; there's no dot-notation shortcut the way JS objects have)."),
    ("What does the f before a string like f\"Hello, {name}\" do?",
     "It marks the string as an f-string, telling Python to evaluate any {expression} inside it and "
     "substitute the result — the direct Python equivalent of a JavaScript template literal's ${...}."),
])

chapter("33. Python Applied — Reading build.py With Full Understanding")
p("With Chapter 32's vocabulary in hand, build.py — covered in full architectural detail in Chapter 19 "
  "of Part 2 — is now fully readable. A quick preview of its shape:")
code('''import argparse, base64, hashlib, pathlib

ROOT = pathlib.Path(__file__).parent    # the folder this script itself lives in

def sha256_b64(text):                     # a function, just like JS -- `def` instead of `function`
    return base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode("ascii")

def build(output_path):
    shell = (ROOT / "shell.html").read_text(encoding="utf-8")   # read a file's text (Ch.32.8)
    css = (ROOT / "app.css").read_text(encoding="utf-8")
    ...
    out = (
        shell.replace("__CSP__", csp)          # find-and-replace, like JS's .replace() with a
             .replace("/*__CSS__*/", css)         # PLAIN STRING (not a regex) as the search target
             .replace("/*__FOODDB__*/", fooddb)
             .replace("/*__APPJS__*/", appjs)
    )
    output_path = pathlib.Path(output_path)
    output_path.write_text(out, encoding="utf-8")    # write the assembled file out (Ch.32.8)

if __name__ == "__main__":                   # only runs when this file is executed directly
    parser = argparse.ArgumentParser()          # (not when imported as a module elsewhere)
    parser.add_argument("-o", "--output", default="dist/tiffin.html")
    args = parser.parse_args()
    build(args.output)''')
p("<font face='Courier'>ROOT / \"shell.html\"</font> is Python's <font face='Courier'>pathlib</font> "
  "module cleverly overloading the <font face='Courier'>/</font> operator to mean \"join a path "
  "segment\" — <font face='Courier'>ROOT / \"shell.html\"</font> builds a full file path regardless of "
  "whether the underlying operating system uses forward or backward slashes, which is exactly the kind of "
  "small cross-platform detail a purpose-built module like pathlib handles for you.")
p("<font face='Courier'>if __name__ == \"__main__\":</font> is a very common Python idiom worth "
  "recognizing on sight: it's Python's way of saying \"only run the code below if this specific file was "
  "the one directly executed (e.g. via <font face='Courier'>python3 build.py</font>), not if some OTHER "
  "script merely imported functions from this file.\" It has no direct JavaScript equivalent, since "
  "browser scripts don't have quite the same \"run directly vs. imported\" distinction.")
quiz("build.py", [
    ("What does ROOT / \"shell.html\" actually do?",
     "It joins the ROOT path with the filename \"shell.html\" to build a full file path, using pathlib's "
     "overloaded / operator — a cross-platform-safe way to combine path segments without manually "
     "worrying about forward vs. backward slashes."),
    ("What is `.replace(\"__CSP__\", csp)` doing, in terms you already know from JavaScript?",
     "Exactly the same thing as JavaScript's string .replace() method with a plain string as the search "
     "argument: find the first occurrence of the literal text \"__CSP__\" and substitute it with the "
     "value of the `csp` variable."),
])

chapter("34. Git — Version Control Basics")
sec("34.1 The problem Git solves")
p("Without version control, tracking changes to a project means either manually copying files "
  "(\"app_v2_final_FINAL.js\") or simply losing track of what changed and why. Git solves this by "
  "recording a complete, navigable HISTORY of every change ever made to a project.")
sec("34.2 The core concepts")
bullets([
    "<b>Repository (\"repo\")</b> — a project folder Git is tracking the history of.",
    "<b>Commit</b> — a saved snapshot of the entire project at one point in time, with a message "
    "describing what changed and why.",
    "<b>Branch</b> — an independent line of development; you can make commits on a branch without "
    "affecting the project's main, stable line of history until you're ready to combine them.",
    "<b>Remote</b> — a copy of the repository hosted elsewhere (commonly on GitHub), that your local "
    "copy can sync with.",
])
sec("34.3 The everyday command sequence")
code('''git status              # what's changed since the last commit?
git add app.js            # stage a specific file's changes, marking them "ready to commit"
git commit -m "Fix streak calculation off-by-one"   # save a snapshot of everything staged
git push origin main         # upload local commits to the remote (here, a branch named "main")
git pull origin main           # download and merge new commits FROM the remote
git log                          # view commit history
git diff                           # see exactly what changed, line by line, not yet committed''')
sec("34.4 Branching and merging")
code('''git branch                     # list local branches
git checkout -b new-feature       # create AND switch to a new branch in one step
git checkout main                    # switch back to the main branch
git merge new-feature                  # bring new-feature's commits into whatever branch you're on now''')
p("Branches let multiple lines of work — a bug fix, a new feature, an experiment — proceed "
  "independently without interfering with each other, then be combined (merged) once ready.")
sec("34.5 Git vs. GitHub — a common point of confusion")
p("<b>Git</b> is the version-control TOOL itself — it works entirely on your own computer and needs no "
  "internet connection or external account. <b>GitHub</b> is a separate, unrelated COMPANY'S hosting "
  "SERVICE for Git repositories — it stores a remote copy of your repo, provides a web interface for "
  "browsing it, and adds collaboration features on top (like pull requests, covered next, and GitHub "
  "Actions, Chapter 35) that have nothing to do with Git itself. You could use Git your entire life and "
  "never touch GitHub; other hosting services (GitLab, Bitbucket) exist too.")
sec("34.6 Pull requests")
p("A <b>pull request</b> (PR) is a GitHub feature (not a Git concept) proposing that the commits on one "
  "branch be merged into another — typically used to have someone else review a change before it joins "
  "the main line of the project. This project's own workflow (referenced throughout the setup that "
  "generated the automated Android/iOS builds) is exactly this: work happens on a feature branch, and a "
  "PR proposes merging it into <font face='Courier'>main</font>.")
quiz("Git", [
    ("What's the difference between `git add` and `git commit`?",
     "git add stages specific changes, marking them as ready to be included in the next commit. "
     "git commit actually saves a permanent snapshot of everything currently staged, along with a message "
     "describing the change."),
    ("Is GitHub a part of Git itself, or a separate product?",
     "A separate, unrelated hosting service built on top of Git — Git works entirely locally with no "
     "internet or account needed; GitHub is one of several companies that host remote copies of Git "
     "repositories and add extra features (pull requests, Actions, issue tracking) on top."),
    ("Why use branches instead of just making every commit directly on the main line of history?",
     "Branches let independent lines of work (a feature, a fix, an experiment) proceed without "
     "interfering with the stable main branch, and let that work be reviewed (e.g. via a pull request) "
     "before it's merged in."),
])

chapter("35. GitHub Actions — CI/CD Basics")
sec("35.1 What CI/CD means")
p("<b>Continuous Integration</b> (CI) means automatically building and testing code every time it "
  "changes, catching problems immediately rather than discovering them later. <b>Continuous Deployment/"
  "Delivery</b> (CD) extends this to automatically packaging and shipping the result. GitHub Actions is "
  "GitHub's own built-in tool for both.")
sec("35.2 YAML — the configuration format these workflows are written in")
p("YAML is a plain-text format for structured configuration, using indentation for nesting (similar in "
  "spirit to Python, Chapter 32.2) and a simple <font face='Courier'>key: value</font> syntax. A dash "
  "(<font face='Courier'>-</font>) at the start of a line marks an item in a list.")
code('''name: Build Android App        # a key: value pair

on:                                # `on` is a key whose value is a nested object
  push:
    branches: [ main, my-branch ]     # a key whose value is a LIST, written inline with [ ]

jobs:                                # `jobs` is a key whose value is a nested object of named jobs
  build:
    runs-on: ubuntu-latest              # this job runs on a fresh Ubuntu Linux virtual machine
    steps:                                # a LIST of steps, each starting with `- `
      - uses: actions/checkout@v4           # step 1: use someone else's prebuilt "action"
      - run: npm install                      # step 2: run a raw shell command
      - run: npm run build''')
sec("35.3 The core vocabulary")
bullets([
    "<b>Workflow</b> — one complete YAML file describing an automated process (this project has two: one "
    "for Android, one for iOS).",
    "<b>Trigger</b> (the <font face='Courier'>on:</font> key) — what causes the workflow to run; most "
    "commonly <font face='Courier'>push</font> (code was pushed) or <font face='Courier'>pull_request</font> "
    "(a PR was opened/updated).",
    "<b>Job</b> — a set of steps that all run together on one freshly-provisioned virtual machine "
    "(the <b>runner</b>).",
    "<b>Step</b> — one action within a job: either <font face='Courier'>run:</font> (an arbitrary shell "
    "command) or <font face='Courier'>uses:</font> (a reusable, prebuilt \"action\" someone else "
    "published, referenced like <font face='Courier'>actions/checkout@v4</font>).",
    "<b>Artifact</b> — a file (or folder) produced by a workflow run that gets saved and made downloadable "
    "afterward — this is exactly how the compiled <font face='Courier'>.apk</font> and "
    "<font face='Courier'>.ipa</font> files become available once a build finishes.",
])
sec("35.4 Why this matters for a project with no dedicated build server")
p("Without CI/CD, producing a signed Android build would require someone to manually install Android "
  "Studio, the right SDK versions, and run the build locally, every single time — slow, error-prone, and "
  "impossible to do from, say, a phone. GitHub Actions instead spins up a brand-new, identically-"
  "configured virtual machine for every single run, runs the exact same recipe every time, and throws the "
  "machine away afterward — this determinism is a large part of CI/CD's value: it eliminates \"works on my "
  "machine\" inconsistency entirely.")
quiz("GitHub Actions", [
    ("In YAML, how do you represent a list of items, like several branch names?",
     "Either inline with square brackets, e.g. branches: [ main, dev ], or as multiple lines each "
     "starting with a dash (-), indented under the key."),
    ("What's the difference between a workflow's `run:` step and its `uses:` step?",
     "run: executes an arbitrary raw shell command you write yourself. uses: invokes a reusable, "
     "prebuilt 'action' that someone else already published (like actions/checkout, which handles "
     "downloading the repo's code) — you don't need to write that logic yourself."),
    ("Why does a fresh virtual machine get created for every single workflow run, rather than reusing "
     "one machine repeatedly?",
     "To guarantee a clean, identical, reproducible environment every time, eliminating 'works on my "
     "machine' inconsistencies where leftover state from a previous run might cause a build to succeed or "
     "fail unpredictably."),
])

chapter("36. Capacitor — Turning a Website into a Phone App")
sec("36.1 Native vs. web vs. hybrid apps")
p("A <b>native</b> app is written directly in a platform's own language and frameworks (Swift/Kotlin, "
  "typically) and can access every device feature directly, but must be written and maintained twice — "
  "once per platform. A <b>web</b> app is just a website, worked with entirely through the vocabulary of "
  "this whole guide, but can't be installed from an app store or (traditionally) access certain device "
  "features. A <b>hybrid</b> app is a middle path: write it once as a web app, then wrap that web app "
  "inside a thin native shell for each platform, getting app-store installability with a single shared "
  "codebase.")
sec("36.2 What a WebView actually is")
p("A WebView is a native, embeddable browser component that any native app can include as part of its "
  "own interface — essentially a full-screen browser tab with no address bar or browser chrome visible "
  "around it. Capacitor generates a minimal native app, for each platform, whose entire screen is just "
  "one WebView pointed at your built web app's HTML file. Your JavaScript runs inside that WebView "
  "exactly as it would in a normal browser tab — the same DOM, the same events, the same "
  "<font face='Courier'>localStorage</font>.")
sec("36.3 The Capacitor workflow, concretely")
code('''// capacitor.config.json
{
  "appId": "com.example.tiffin",
  "appName": "Tiffin",
  "webDir": "dist"      // <-- the folder containing the already-built web app''')
bullets([
    "1. <font face='Courier'>npm run build</font> assembles the single dist/index.html file (Chapter 19).",
    "2. <font face='Courier'>npx cap sync android</font> (or <font face='Courier'>ios</font>) copies that "
    "file into a native project template Capacitor generated once, ahead of time.",
    "3. The platform's own native compiler — Gradle for Android, Xcode for iOS — builds an actual, "
    "installable native app from that template, with the WebView pointed at your file.",
])
sec("36.4 Why this required almost no extra code for Tiffin specifically")
p("Because Tiffin already ran entirely client-side with zero server dependency (Chapter 38 of Part 2 "
  "covers this decision in full), wrapping it in a WebView changed essentially nothing about how the app "
  "behaves — the exact same <font face='Courier'>localStorage</font>-based persistence, the exact same "
  "JavaScript logic, works completely unmodified inside the native shell. An app that DID depend on a "
  "server would need to keep working through the WebView's networking exactly as it does in a normal "
  "browser too, which is usually fine, but would be one more thing to verify.")
quiz("Capacitor", [
    ("What is a WebView, concretely?",
     "A native, embeddable browser component — essentially a full-screen browser tab with no visible "
     "address bar or browser UI around it — that a native app can include as part of its own interface."),
    ("Why did wrapping Tiffin with Capacitor require almost no code changes, specifically?",
     "Because Tiffin already had zero server dependency and stored everything in localStorage — exactly "
     "the same behavior that already worked in a normal desktop browser tab continues to work completely "
     "unmodified inside a WebView, since a WebView provides the same DOM, JavaScript engine, and "
     "localStorage that any browser tab does."),
    ("Name the three broad categories of mobile app (native / web / hybrid) and which one Capacitor "
     "produces.",
     "Native (platform-specific code, e.g. Swift/Kotlin), web (a website, not installable from an app "
     "store), and hybrid (a web app wrapped in a thin native shell) — Capacitor produces hybrid apps."),
])

part("PART 2<br/>The App, Explained End to End")
p("With that vocabulary in hand, we can now read every file in this project and understand exactly what "
  "it does and why. We'll go file by file, then work through app.js — the largest and most important file "
  "— section by section, in the order it's actually written.")

chapter("37. Project Tour — Every File and What It's For")
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
  "browser. This single decision shapes nearly everything else about the project (Chapter 57).")

chapter("38. The Build Pipeline — build.py Deep Dive")
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
sec("38.1 The Content-Security-Policy (CSP) — a security feature")
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
  "<font face='Courier'>&lt;script&gt;</font> tag into the page (Chapter 58 explains how that could even "
  "happen), its hash wouldn't match, and the browser would simply refuse to execute it. This is a strong, "
  "defense-in-depth security measure explained fully in Chapter 58.")

chapter("39. shell.html Deep Dive")
p("Once you strip out the placeholders, shell.html is almost nothing — deliberately so:")
code('''<div class="topbar">...</div>                <!-- mobile-only top bar -->
<div class="app">
  <nav class="sidenav" id="sideNav"></nav>       <!-- EMPTY -- JS fills this -->
  <main class="main">
    <div id="viewRoot"></div>                     <!-- EMPTY -- JS fills this -->
  </main>
</div>
<nav class="bottomnav" id="bottomNav"></nav>       <!-- EMPTY -- JS fills this -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal" id="modalContent"></div>       <!-- EMPTY -- JS fills this -->
</div>
<div class="toast-wrap" id="toastWrap"></div>        <!-- EMPTY -- JS fills this -->''')
p("Five containers, each with an <font face='Courier'>id</font>, and every single one starts completely "
  "empty. This is the hallmark of a JavaScript-driven single page app: HTML provides only the <i>slots</i>; "
  "JavaScript generates 100% of what actually appears inside them, and keeps regenerating it as the app's "
  "data changes. We'll see exactly how in Chapter 44.")

chapter("40. app.css Deep Dive")
sec("40.1 Design tokens and dark mode, revisited")
p("Recall from Part 1 that CSS variables let you name a value once and reuse it everywhere. app.css "
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
     is explicitly "dark" -- regardless of the OS setting */
  --paper: #161210; --text: #F5ECDF; --accent: #FF7D5E;
}''')
p("Three theme states are supported: <b>system</b> (follow the OS's light/dark preference automatically, "
  "via the <font face='Courier'>@media (prefers-color-scheme: dark)</font> query), or an explicit "
  "<b>light</b> / <b>dark</b> override, applied by JavaScript setting a "
  "<font face='Courier'>data-theme</font> attribute on the <font face='Courier'>&lt;html&gt;</font> element "
  "(Chapter 54 shows the JS side of this). Not one other CSS rule in the whole file needs to know or care "
  "which theme is active — they all just say <font face='Courier'>color: var(--text)</font>, and the "
  "variable's current value does the rest.")
sec("40.2 Mobile vs desktop layout")
p("Recall the media query pattern from Part 1. app.css uses exactly one breakpoint, 860px, to switch "
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
sec("40.3 Reduced motion accessibility")
code('''@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .001ms !important;
    transition-duration: .001ms !important;
  }
}''')
p("Some users configure their OS to minimize animations (often for motion-sensitivity/vestibular reasons). "
  "This query respects that system preference by effectively disabling all CSS animations and transitions "
  "for them, app-wide, in one rule.")

chapter("41. food_db.json Deep Dive")
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
  ... (continues through all 44 nutrients -- vitamins, minerals, fats, etc.)
}''')
bullets([
    "<font face='Courier'>id</font> — a unique, human-readable identifier (used to reference this food from the diary, never the display name, since names could change).",
    "<font face='Courier'>category</font> — 'Indian' or 'International', used for the filter chips in the Foods tab.",
    "<font face='Courier'>servingLabel</font> / <font face='Courier'>servingGrams</font> — a human-friendly serving description (\"1 cup\") paired with its weight in grams, so any other serving size can be computed proportionally.",
    "Every other key matches one entry in the app's own <font face='Courier'>NUTRIENT_KEYS</font> list (Chapter 42) — this consistency is what lets the same generic nutrient-math functions work identically on every food.",
])
note("This file is loaded once, embedded directly as a JS array literal via build.py's "
     "<font face='Courier'>__FOODDB__</font> placeholder (Chapter 38) — there's no network request to fetch "
     "it at runtime, which is why the app works completely offline.")

chapter("42. app.js Part 1 — Setup & The Shape of the Data")
p("Everything from here through Chapter 56 walks through app.js top to bottom. Line numbers refer to the "
  "actual file in this repository.")
sec("42.1 The wrapper (lines 1-8)")
code('''(function(){
"use strict";''')
p("As explained in Part 1's closures/IIFE chapter, this is an IIFE: it isolates every name the app "
  "defines from the rest of the page, and turns on JavaScript's strict mode.")
sec("42.2 Icons (lines 9-27)")
p("An object literal, <font face='Courier'>ICON</font>, mapping short names like "
  "<font face='Courier'>home</font>, <font face='Courier'>flame</font>, <font face='Courier'>x</font> to "
  "raw SVG markup strings. Recall from Part 1 that <font face='Courier'>&lt;svg&gt;</font> draws vector "
  "graphics directly in markup — no image files are downloaded for any icon in this app; they're all just "
  "text, embedded directly into whatever HTML string needs them, e.g. <font face='Courier'>${ICON.flame}</font>.")
sec("42.3 Constants (lines 29-114)")
code('''const STORAGE_KEY = 'tiffin_state_v1';   // the localStorage key everything is saved under

const NUTRIENT_KEYS = [
  'kcal','protein','carbs','fat','satFat','fiber','sugar','sodium', ...  // all 44, by name
];''')
p("<font face='Courier'>NUTRIENT_KEYS</font> is the single source of truth for \"what nutrients does this "
  "app track?\" — every nutrient-math function (Chapter 44) loops over this list rather than hardcoding "
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
  "list drives both the Nutrients tab (Chapter 48) and the custom-food-entry form (Chapter 50) — define a "
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
  "energy formula (Chapter 46). <font face='Courier'>DEFAULT_GOALS</font> is what a brand-new user starts "
  "with before they customize anything in Profile.")
sec("42.4 Default-state factory functions (lines 116-133)")
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
  "everywhere, every new user (and the \"Reset all data\" feature, Chapter 54) would end up sharing and "
  "accidentally mutating the exact same object in memory. Calling a function guarantees a brand new, "
  "independent copy every time — recall Part 1's chapter on arrays/objects holding references, not copies.")
p("This block also defines the complete shape of the app's data: goals (calorie/macro targets), profile "
  "(the user's body stats), diary (a dictionary of date &#8594; meals eaten), weightLog (an array of "
  "weigh-ins), customFoods / customMeals (anything the user created themselves), barcodeMap (barcode "
  "numbers linked to specific foods), and mealSlots (the user's customizable list of meal names, replacing "
  "a fixed \"Breakfast/Lunch/Dinner\" scheme).")

chapter("43. app.js Part 2 — Storage & Security")
sec("43.1 Loading and saving (lines 150-190)")
code('''let STATE = loadState();   // <-- the app's ENTIRE data lives in this one variable

function saveState(){
  try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(STATE)); }
  catch(e){ storageOk = false; }
}''')
p("This is the localStorage pattern from Part 1, applied to the whole app's data at once. Every single "
  "place in app.js that changes something — adding a food, logging weight, changing a setting — calls "
  "<font face='Courier'>saveState()</font> immediately afterward. There is no \"Save\" button for the app "
  "as a whole; changes are persisted the instant they happen.")
p("The <font face='Courier'>try/catch</font> matters because <font face='Courier'>localStorage</font> can "
  "fail — private/incognito browsing sometimes disables it entirely, or storage could be full. Rather than "
  "crash, the app sets a flag (<font face='Courier'>storageOk = false</font>) and later warns the user "
  "their data won't be saved, so they know to back it up manually (Chapter 54).")
sec("43.2 mergeKnownFields — a security-conscious loader")
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
  "with to no longer inherit the normal Object prototype (recall Part 1's Object chapter); calling the "
  "trusted, original method explicitly sidesteps that.")
p("This function is used in two places: loading state from localStorage on startup (which, strictly, is "
  "data the app itself wrote, so lower risk) and importing a backup file the user selects (Chapter 54) — "
  "the more realistic risk, since backup files could be shared, edited, or come from an untrusted source.")
sec("43.3 Legacy data migration")
p("loadState() also contains a one-time migration for users who had the app before \"meal slots\" became "
  "customizable, converting their old fixed <font face='Courier'>breakfast/lunch/dinner/snacks</font> keys "
  "into the new generic <font face='Courier'>meal-1/meal-2/...</font> scheme automatically, so nobody's "
  "existing diary history is lost when the app is updated.")

chapter("44. app.js Part 3 — Utility & Math Functions")
sec("44.1 General-purpose helpers (lines 193-210)")
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
    "<font face='Courier'>escapeHtml()</font> is Tiffin's central XSS defense — full explanation in Chapter 58.",
])
sec("44.2 Date helpers")
code('''function toKey(d){ return d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate()); }
function todayKey(){ return toKey(new Date()); }
function addDaysKey(key, delta){ const d = keyToDate(key); d.setDate(d.getDate()+delta); return toKey(d); }''')
p("The whole app represents a date not as a JavaScript Date object, but as a plain string key like "
  "<font face='Courier'>'2024-09-17'</font>. This makes it trivially usable as an object key (for the diary, "
  "see Chapter 45) and easy to compare/sort as plain strings, while still allowing arithmetic (\"give me "
  "yesterday\") by briefly converting back to a real Date object, changing it, and converting back to a key.")
sec("44.3 Nutrient math — the core arithmetic of the whole app")
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
  "perfect example of the <font face='Courier'>NUTRIENT_KEYS</font> list paying off: instead "
  "of 44 lines of <font face='Courier'>o.protein = a.protein + b.protein; o.carbs = a.carbs + b.carbs; ...</font>, "
  "one loop handles every current and future nutrient identically — Part 1's Arrays chapter covered "
  "exactly this <font face='Courier'>.forEach()</font> pattern.")
bullets([
    "<font face='Courier'>zeroNutrients()</font> — an empty starting point (everything 0), used as the "
    "running total before summing a day's meals.",
    "<font face='Courier'>scaleNutrients(base, qty)</font> — multiplies every nutrient by a quantity, e.g. "
    "\"1.5 servings of rice\" scales rice's per-serving nutrients by 1.5.",
    "<font face='Courier'>addNutrients(a, b)</font> — adds two nutrient sets together, key by key, e.g. "
    "combining breakfast's total with lunch's total.",
])
sec("44.4 Resolving a \"reference\" into actual nutrition data")
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

chapter("45. app.js Part 4 — The Diary & Meal System")
p("Recall that <font face='Courier'>STATE.diary</font> is an object mapping date-key "
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
  "later still works for old diary days that were created before that slot existed — "
  "<font face='Courier'>getDay()</font> patches it in automatically.")
code('''function dayTotals(key){
  const d = getDay(key);
  let total = zeroNutrients();
  STATE.mealSlots.forEach(s=>{
    (d[s.id]||[]).forEach(entry=>{ total = addNutrients(total, entryNutrients(entry)); });
  });
  return total;
}''')
p("<font face='Courier'>dayTotals()</font> combines everything from Chapter 44: for every meal slot, for "
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
  "thing in the morning before you've had a chance to log breakfast. This is exactly the kind of "
  "<font face='Courier'>while</font> loop from Part 1's Loops chapter, applied to real data.")

chapter("46. app.js Part 5 — Energy Calculations (BMR/TDEE)")
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
  "coefficient. Note the guard clauses at the top — recall Part 1's Objects/Functions chapters — if any "
  "required profile field is missing, the function returns <font face='Courier'>null</font> rather than "
  "calculating with garbage/missing data, and every caller of this function is expected to check for that "
  "<font face='Courier'>null</font> before using the result (Chapter 52 shows the UI's fallback message "
  "when it's missing).")
code('''function calcTDEE(){
  const bmr = calcBMR(); if(bmr == null) return null;
  const mult = ACTIVITY_MULT[STATE.profile.activityLevel || 'moderate'];
  return bmr * mult;
}''')
p("TDEE (Total Daily Energy Expenditure) scales BMR up by an activity multiplier (from "
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
  "(\"Calculate my targets\", Chapter 52). It uses the well-known approximation that roughly 7,700 kcal of "
  "sustained surplus or deficit corresponds to about 1 kg of body weight change, to translate a user's "
  "desired weekly rate of loss/gain into a daily calorie adjustment. It sets protein higher (per kg of "
  "bodyweight) during a \"cut\" (calorie deficit) than during maintenance or a \"bulk,\" reflecting real "
  "nutrition guidance to preserve muscle while losing fat. Fat and carbs are then derived from what's left "
  "of the calorie budget, using the standard calorie-per-gram figures (9 kcal/g fat, 4 kcal/g carbs/protein). "
  "Note the safety floor: <font face='Courier'>Math.max(1200, ...)</font> refuses to ever suggest a "
  "dangerously low calorie target, regardless of what the math alone would produce.")

chapter("47. app.js Part 6 — The Rendering System")
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
  "<font face='Courier'>${...}</font> interpolations (Part 1's template literals chapter), and hands it "
  "back. Nothing inside <font face='Courier'>renderToday()</font>, for instance, ever touches the DOM "
  "directly; it just returns text. The <i>caller</i> — <font face='Courier'>renderView()</font> — is the "
  "only place that actually assigns to <font face='Courier'>.innerHTML</font>, replacing everything "
  "inside <font face='Courier'>#viewRoot</font> in one shot.")
sec("47.1 The render cycle — how a click becomes a screen update")
p("This five-step loop happens every single time the user does anything at all in this app:")
bullets([
    "<b>1.</b> User clicks/types/submits something.",
    "<b>2.</b> The event delegation system (Chapter 55) figures out what action that corresponds to.",
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
     "This is a real, defensible trade-off — see Chapter 57.")
sec("47.2 Lazy-loading Chart.js")
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
  "<font face='Courier'>&lt;script&gt;</font> element pointed at a CDN URL and inserting it into the page "
  "(exactly the DOM-creation pattern from Part 1's DOM chapter). It tracks loading state so simultaneous "
  "or repeated requests don't trigger duplicate downloads, and handles the failure case (no internet) "
  "gracefully by still calling the callback, which then shows a \"chart unavailable\" fallback instead of "
  "crashing.")

chapter("48. app.js Part 7 — The Today View & Nutrients Tab")
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
sec("48.1 The SVG progress ring")
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
sec("48.2 The Nutrients tab")
code('''function renderNutrientsView(){
  const totals = dayTotals(currentDate);
  const G = Object.assign({}, FIXED_TARGETS, STATE.goals);
  const groups = NUTRIENT_GROUPS.map(grp=>{
    const rows = grp.rows.map(([key,label,unit,goalKey,isLimit])=>{
      const goal = goalKey ? G[goalKey] : null;
      return barRow(label, totals[key]||0, goal, ' '+unit, {isLimit});
    }).join('');
    return `<div class="nutrient-group-title">${grp.title}</div><div>${rows}</div>`;
  }).join('');
  return `${dateNavHtml()}<div class="card">...${groups}...</div>`;
}''')
p("This function is a great example of Part 1's Object/Array chapters paying off directly: "
  "<font face='Courier'>Object.assign({}, FIXED_TARGETS, STATE.goals)</font> merges the app-wide default "
  "targets with whatever the user has personally customized (the user's own values winning any overlap), "
  "and the array destructuring on each row — "
  "<font face='Courier'>([key,label,unit,goalKey,isLimit])</font> — unpacks each nutrient's metadata "
  "tuple directly in the <font face='Courier'>.map()</font> callback's parameter list.")

chapter("49. app.js Part 8 — The Food Picker Flow")
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
  "render function — the exact same \"render function reads state, returns HTML\" pattern from Chapter 47, "
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
  "(used when linking a scanned barcode to an existing food, Chapter 53, where picking a food should link "
  "it rather than log it).")

chapter("50. app.js Part 9 — Custom Foods & Custom Meals")
p("A custom food form dynamically generates one input field per nutrient, reusing "
  "<font face='Courier'>NUTRIENT_GROUPS</font> so the form's organization exactly matches "
  "the Nutrients tab's organization:")
code('''function customFoodNutrientFieldsHtml(){
  return NUTRIENT_GROUPS.map(grp=>{
    const rows = grp.rows.filter(([key])=> !CUSTOM_FOOD_PRIMARY_KEYS.includes(key));
    ...
    return `<details class="settings-group"><summary>${grp.title}</summary>${pairsHtml}</details>`;
  }).join('');
}''')
p("(<font face='Courier'>&lt;details&gt;</font>/<font face='Courier'>&lt;summary&gt;</font> is a native "
  "HTML element pair — from Part 1's HTML chapters — that creates a collapsible section with zero "
  "JavaScript needed. Calories, protein, carbs, and fat are excluded from this generated list because "
  "they're always shown as separate, prominent fields at the top of the form — everything else (all ~40 "
  "vitamins/minerals/fat-subtypes) is generated.")
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
p("<font face='Courier'>FormData</font> is a built-in browser API (Part 1's Forms/Browser-APIs chapters) "
  "that reads every named input inside a <font face='Courier'>&lt;form&gt;</font> at once, keyed by each "
  "input's <font face='Courier'>name</font> attribute — much simpler than manually querying and reading "
  "dozens of individual input elements. The small inline arrow function "
  "<font face='Courier'>num(k, d)</font> parses a field as a number and falls back to a default "
  "<font face='Courier'>d</font> if it's empty or invalid, so a nutrient field left blank quietly becomes "
  "0 rather than <font face='Courier'>NaN</font> corrupting later math.")
sec("50.1 Custom meals (recipes)")
p("A custom meal is built interactively: search for an ingredient, tap it to add it to the recipe, repeat, "
  "then save. Recall that a meal reference resolves recursively (Chapter 44) — so once saved, a custom "
  "meal behaves exactly like any other loggable food everywhere else in the app, including being usable as "
  "an ingredient in searches, but not nestable inside another custom meal (the picker explicitly filters "
  "meal-type items out of the ingredient search to prevent that).")

chapter("51. app.js Part 10 — Progress View & Charts")
p("The weight-trend chart is a thin wrapper around the Chart.js library, lazy-loaded via the mechanism "
  "from Chapter 47.2:")
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
  "optional goal-line dataset is added conditionally using the array-spread trick from Part 1's Modern "
  "Syntax chapter — <font face='Courier'>...(goal!=null ? [{...}] : [])</font> spreads in either one extra "
  "dataset object or nothing at all, cleanly avoiding an <font face='Courier'>if</font> statement in the "
  "middle of an object literal (which isn't syntactically possible in JavaScript).")
p("The chart's colors are read directly from the current CSS variables (via a small "
  "<font face='Courier'>css()</font> helper) so the chart automatically matches whichever "
  "theme — light or dark — is currently active, without any separate \"chart theme\" configuration.")

chapter("52. app.js Part 11 — Profile View")
p("The Profile view is the largest single render function in the app, but structurally it's just several "
  "independent <font face='Courier'>&lt;form&gt;</font> elements stacked together — each with its own "
  "<font face='Courier'>id</font>, handled separately in <font face='Courier'>onSubmit</font> (Chapter 55). "
  "A few UI details worth noting:")
bullets([
    "Height can be entered in cm or ft/in — internally, the app <i>always</i> stores height as centimeters "
    "(<font face='Courier'>heightCm</font>); the ft/in inputs are converted on the way in and out, so all "
    "downstream math (like <font face='Courier'>calcBMR</font>) only ever has to deal with one unit.",
    "Similarly, weight is always stored internally in kilograms, with <font face='Courier'>toDisplayWeight()</font> "
    "/ <font face='Courier'>fromDisplayWeight()</font> converting to/from pounds only at the point of "
    "display or input, based on the user's chosen unit preference.",
    "The micronutrient goal-editing section is wrapped in a collapsible &lt;details&gt; element (Chapter "
    "50) since most users won't want to micromanage 40 individual targets.",
])
p("Notice the design principle here — introduced back in Part 1's units discussion: pick ONE canonical "
  "internal representation (centimeters, kilograms) and convert only at the boundary where a human reads "
  "or types a value, rather than letting multiple units leak into the actual math anywhere in the codebase.")

chapter("53. app.js Part 12 — Barcode Scanning")
p("This feature combines three ideas already covered in Part 1: the "
  "<font face='Courier'>BarcodeDetector</font> and <font face='Courier'>MediaDevices</font> browser APIs, "
  "<font face='Courier'>async</font>/<font face='Courier'>await</font>, and a recursive polling loop using "
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
  "specifically, since that's the one normally used for scanning things.")
p("When a code is found, <font face='Courier'>handleBarcode()</font> looks it up in "
  "<font face='Courier'>STATE.barcodeMap</font> (Chapter 42); if it's already linked to a food, it offers "
  "to log that food directly; if it's a never-before-seen barcode, it offers to either link it to an "
  "existing food or create a brand new custom food for it — after which future scans of that same barcode "
  "resolve instantly.")

chapter("54. app.js Part 13 — Export / Import / Theme")
sec("54.1 Backup export")
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
p("<font face='Courier'>JSON.stringify(STATE, null, 2)</font> — from Part 1's JSON chapter — pretty-"
  "prints with 2-space indentation, making the exported file human-readable if someone opens it directly. "
  "The function first tries an optional platform-specific save-file API (available when running inside "
  "certain host environments), and falls back to simply displaying the raw JSON text in a read-only "
  "textbox with a \"copy to clipboard\" button when that's not available — always giving the user "
  "<i>some</i> way to get their data out, regardless of environment.")
sec("54.2 Backup import")
code('''function importFromFile(file){
  const reader = new FileReader();
  reader.onload = ()=>{
    try{
      const parsed = JSON.parse(reader.result);
      const s = defaultState();
      s.goals = mergeKnownFields(DEFAULT_GOALS, parsed.goals);       // <-- security, Ch.43.2
      s.profile = mergeKnownFields(defaultProfile(), parsed.profile); // <-- security, Ch.43.2
      ...
      STATE = s;
      saveState(); applyTheme(); renderApp();
    }catch(e){ toast("That file couldn't be read as a Tiffin backup."); }
  };
  reader.readAsText(file);
}''')
p("This is exactly the loader logic from <font face='Courier'>loadState()</font> (Chapter 43), reused for "
  "an imported file — and it's the more important of the two places <font face='Courier'>"
  "mergeKnownFields</font> gets used, since an imported file is more plausibly something a user downloaded, "
  "shared, or hand-edited, rather than something the app wrote itself.")
sec("54.3 Theme switching")
code('''function applyTheme(){
  const t = STATE.goals.theme || 'system';
  if(t === 'system') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
}''')
p("This is the JavaScript half of the dark-mode system introduced in Chapter 40.1: setting or removing the "
  "<font face='Courier'>data-theme</font> attribute on the root <font face='Courier'>&lt;html&gt;</font> "
  "element is the ONLY thing this function does — every visual consequence is handled entirely by the CSS "
  "variable rules already defined in app.css reacting to that attribute changing.")

chapter("55. app.js Part 14 — The Event System (the app's heart)")
p("Everything explained so far describes functions that <i>could</i> run — this section is what actually "
  "decides <i>when</i> they run. Recall the event delegation pattern from Part 1 (Chapter 26); this is its "
  "full, real implementation.")
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
  "<font face='Courier'>dataset</font> (Part 1's DOM chapter), mutate <font face='Courier'>STATE</font> or "
  "another module-level variable accordingly, then <font face='Courier'>return</font> immediately — the "
  "early <font face='Courier'>return</font> after every branch is what makes an otherwise 60-branch "
  "if-chain readable: once one matches, nothing below it is even checked.")
p("<font face='Courier'>e.stopPropagation()</font>, seen in the delete-entry branch, prevents this click "
  "from also bubbling up and triggering a <i>different</i> data-action on a parent element (in this "
  "specific case, the delete (×) icon sits inside a row that itself has its own "
  "<font face='Courier'>data-action=\"edit-entry\"</font> for opening the edit screen — without "
  "<font face='Courier'>stopPropagation()</font>, clicking delete would also immediately trigger edit — "
  "exactly the distinction Part 1's Events chapter drew between stopPropagation and preventDefault).")
sec("55.1 Three sibling listeners for three other event types")
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
  "URL, exactly what a no-backend app must never let happen (recall Part 1's forms chapter). Note also "
  "that <font face='Courier'>onInput</font>'s live-search handler deliberately updates <i>only</i> the "
  "small results-list element (<font face='Courier'>document.getElementById('foodsList').innerHTML = ...</font>) "
  "rather than calling the full <font face='Courier'>renderView()</font> — re-rendering the entire page on "
  "every single keystroke of a search box would be needlessly wasteful and could even steal focus away "
  "from the input the user is actively typing in.")

chapter("56. app.js Part 15 — Startup")
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
  "kicks off: apply the saved theme, attach the four delegated event listeners from Chapter 55 exactly "
  "once, wire up \"click the dark overlay behind a modal to close it,\" and finally call "
  "<font face='Courier'>renderApp()</font> for the very first time, painting the initial screen from "
  "whatever <font face='Courier'>STATE</font> was loaded at the very top of the file (Chapter 43).")
p("The <font face='Courier'>inited</font> guard flag exists because of the two lines at the very bottom: "
  "<font face='Courier'>DOMContentLoaded</font> (Part 1's Events chapter) fires once, when the browser "
  "finishes parsing the HTML — but if the script happens to load and execute <i>after</i> that event "
  "already fired (a real possibility depending on exactly how/when the script tag runs), the listener "
  "would simply never fire at all, and the app would never start. The second line, checking "
  "<font face='Courier'>document.readyState</font>, catches that case by calling "
  "<font face='Courier'>init()</font> immediately if the document has already finished loading. The guard "
  "flag ensures that if <i>both</i> paths somehow end up running, <font face='Courier'>init()</font> "
  "still only ever truly executes once.")

part("PART 3<br/>Architecture &amp; Design Decisions")

chapter("57. Why No Framework, No Backend?")
sec("57.1 No framework (no React / Vue / Angular)")
p("This app achieves everything a framework normally provides — a render-on-state-change loop, reusable "
  "\"components,\" event handling — using nothing but the patterns from Chapters 47 and 55: template "
  "literals for components, one delegated listener for events, and full-innerHTML-replacement for updates.")
bullets([
    "<b>Pro:</b> Zero dependencies, zero build step needed to develop (only to bundle for shipping), and a "
    "single ~1,700-line file that a reader can genuinely hold in their head — nothing hides behind an "
    "abstraction layer or framework \"magic.\"",
    "<b>Con:</b> No fine-grained DOM diffing (a framework only updates the exact DOM nodes that actually "
    "changed; this app replaces whole chunks of HTML every time), no built-in component reuse/composition "
    "tooling, and the burden of avoiding bugs like memory leaks (Chapter 51's chart cleanup) falls entirely "
    "on the developer instead of the framework.",
    "<b>Why it's a reasonable choice here:</b> the app's total data size is small (one user's diary, not "
    "millions of rows), so the performance cost of \"just re-render everything\" never becomes noticeable, "
    "and the simplicity payoff — no build tooling required to even run the app locally, trivial to audit "
    "for security since every line of logic is visible in one file — is worth it for a project this size.",
])
sec("57.2 No backend, no server, no database")
p("Every user's data lives only in their own browser's localStorage (Part 1, Chapter 30). There is no "
  "login, no account, no API calls that send personal data anywhere.")
bullets([
    "<b>Pro:</b> Perfect privacy by construction (nothing to breach — there's no server holding anyone's "
    "data), zero server hosting cost, and the app works fully offline once loaded, since even the food "
    "database is baked directly into the page (Chapter 41).",
    "<b>Con:</b> No cross-device sync (your diary on your phone and your laptop are two separate, "
    "unconnected datasets), and clearing browser data destroys everything unless a backup was manually "
    "exported (Chapter 54).",
    "<b>Why it's a reasonable choice here:</b> a personal nutrition tracker's core value doesn't strictly "
    "require sync or accounts, and trading that away buys meaningful simplicity and privacy.",
])

chapter("58. Security: XSS, CSP, Prototype Pollution")
sec("58.1 XSS (Cross-Site Scripting) and escapeHtml")
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
p("<font face='Courier'>escapeHtml()</font> — the exact regex from Part 1's Strings &amp; Regex chapter — "
  "converts the characters that give HTML its special meaning (<font face='Courier'>&lt; &gt; &amp; \" '</font>) "
  "into their harmless text equivalents (\"HTML entities\"), so <font face='Courier'>&lt;img&gt;</font> "
  "becomes the literal, inert text <font face='Courier'>&amp;lt;img&amp;gt;</font> instead of being parsed "
  "as a tag. This function is called on essentially every single piece of user-controlled or data-sourced "
  "text before it's woven into an HTML string anywhere in the app — food names, profile name, custom meal "
  "names, barcode numbers, all of it.")
sec("58.2 The Content-Security-Policy, revisited")
p("escapeHtml is the app's <i>first</i> line of defense — but defensive engineering means assuming a bug "
  "slips through anyway (a future edit that forgets to call it, say). Recall from Chapter 38.1 that "
  "build.py computes cryptographic hashes of the app's own two legitimate inline scripts and locks the "
  "browser down to <i>only</i> executing scripts matching those exact hashes. Even in the worst case — an "
  "attacker somehow gets an unescaped, malicious string containing a "
  "<font face='Courier'>&lt;script&gt;</font> tag into the page — the browser's own CSP enforcement would "
  "refuse to execute it, because its content wouldn't match either trusted hash. This is called "
  "<b>defense in depth</b>: multiple independent layers of protection, so that one layer failing doesn't "
  "mean total compromise.")
sec("58.3 Prototype pollution, revisited")
p("Covered in full in Chapter 43.2 — <font face='Courier'>mergeKnownFields()</font> ensures that loading "
  "saved state or an imported backup file can never inject unexpected properties (like "
  "<font face='Courier'>__proto__</font>) into the app's data, only ever the specific fields the app "
  "already knows about and expects.")

chapter("59. The Full Data Flow, End to End")
p("Putting every earlier chapter together, here is literally everything that happens, in order, when a "
  "user adds \"1.5 cups of rice\" to their lunch:")
bullets([
    "<b>1.</b> User taps <font face='Courier'>+ Add Lunch</font> &#8594; the click bubbles to "
    "<font face='Courier'>document</font> &#8594; <font face='Courier'>onClick</font> (Ch.55) matches "
    "<font face='Courier'>data-action=\"open-picker\"</font> &#8594; calls "
    "<font face='Courier'>openPicker({meal:'meal-2'})</font> (Ch.49).",
    "<b>2.</b> <font face='Courier'>openPicker</font> creates the picker state object and calls "
    "<font face='Courier'>renderPickerModal()</font>, which calls <font face='Courier'>renderListStep()</font> "
    "&#8594; returns an HTML string &#8594; <font face='Courier'>openModalHtml()</font> sets "
    "<font face='Courier'>#modalContent.innerHTML</font> and reveals the modal overlay.",
    "<b>3.</b> User types \"rice\" &#8594; fires an <font face='Courier'>input</font> event &#8594; "
    "<font face='Courier'>onInput</font> (Ch.55.1) updates <font face='Courier'>picker.query</font>, calls "
    "<font face='Courier'>filterFoods()</font> against <font face='Courier'>FOOD_DB</font>, and "
    "replaces just the results list's <font face='Courier'>innerHTML</font>.",
    "<b>4.</b> User taps the \"Rice, cooked\" result &#8594; <font face='Courier'>onClick</font> matches "
    "<font face='Courier'>select-food</font> &#8594; sets <font face='Courier'>picker.activeRef</font> and "
    "<font face='Courier'>picker.step = 'serving'</font> &#8594; re-renders the modal, now showing "
    "<font face='Courier'>renderServingStep()</font>'s quantity screen.",
    "<b>5.</b> User sets amount to 1.5 &#8594; <font face='Courier'>onInput</font> recomputes "
    "grams/calories live via <font face='Courier'>computeGrams()</font> and "
    "<font face='Courier'>scaleNutrients()</font> (Ch.44) and updates just the preview numbers on screen.",
    "<b>6.</b> User taps <font face='Courier'>Add to list</font> &#8594; <font face='Courier'>onClick</font> "
    "matches <font face='Courier'>add-to-cart</font> &#8594; pushes the item into "
    "<font face='Courier'>picker.cart</font>, returns to the list step.",
    "<b>7.</b> User taps <font face='Courier'>Finish</font> &#8594; <font face='Courier'>onClick</font> "
    "matches <font face='Courier'>picker-finish</font> &#8594; for each cart item, computes its quantity "
    "and <font face='Courier'>getDay(dateKey)[meal].push({ref, qty})</font> — this is the moment "
    "<font face='Courier'>STATE</font> itself actually changes (Ch.45).",
    "<b>8.</b> Still inside that handler: <font face='Courier'>saveState()</font> serializes the whole "
    "<font face='Courier'>STATE</font> object to JSON and writes it to localStorage (Ch.43) — the data is "
    "now durable, surviving even if the tab is closed immediately.",
    "<b>9.</b> <font face='Courier'>closeModal()</font> hides the modal; <font face='Courier'>renderView()</font> "
    "(Ch.47) calls <font face='Courier'>renderToday()</font> (Ch.48) fresh — it calls "
    "<font face='Courier'>dayTotals()</font> (Ch.45), which now includes the new rice entry, recomputes the "
    "calorie ring's percentage, and returns brand-new HTML reflecting the updated total.",
    "<b>10.</b> That HTML replaces <font face='Courier'>#viewRoot</font>'s content; the browser repaints; "
    "the user sees the ring, the macro bars, and the lunch card all instantly reflect the new food — done.",
])
note("Every one of those ten steps is just a composition of small, individually simple functions covered "
     "earlier in this guide. There's no framework, no network request, no hidden magic anywhere in this "
     "chain — which is precisely the point being made in Chapter 57.")

part("PART 4<br/>Interview Guide")
p("You now understand every language this app uses and every significant piece of its code. This part "
  "turns that understanding into interview-ready answers. Read the question, try to answer it yourself "
  "first, then compare against the model answer.")

chapter("60. The 30-Second Pitch")
p("<i>\"Tiffin is a full-featured nutrition tracker — think Cronometer or MyFitnessPal — built as a single, "
  "self-contained, zero-dependency web app in vanilla JavaScript. It tracks 44 nutrients across a "
  "332-food built-in database with an Indian-and-international focus, supports barcode scanning, custom "
  "foods and recipes, weight tracking with charts, and BMR/TDEE-based goal calculation using the "
  "Mifflin-St Jeor formula. There's no backend and no account system — everything is stored client-side in "
  "localStorage, which means it's completely private and works offline. It ships as a website, and also as "
  "installable native iOS and Android apps via Capacitor, with both builds automated end-to-end through "
  "GitHub Actions.\"</i>")

chapter("61. Core Technical Q&A")
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
   "See Chapter 59 for the full ten-step trace — in short: a click is caught by one delegated event "
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

chapter("62. Deep-Dive Design Questions")
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
   "The pure, render-function-per-view architecture (Ch.47) is actually quite testable in principle: most "
   "render functions are pure functions of STATE that return a string, so you could feed them a known "
   "STATE object and assert on the returned HTML string without needing a real browser. The nutrient math "
   "functions (scaleNutrients, addNutrients, dayTotals) are pure and trivially unit-testable. The harder "
   "parts to test are the event-delegation handlers, since they mix DOM reads, STATE mutation, and "
   "re-rendering together — those would benefit most from a browser-based testing tool (like Playwright) "
   "driving real clicks and asserting on the resulting DOM, since they're what's not currently covered.")

chapter("63. Glossary — Every Term Used in This Guide")
glossary = sorted([
    ("API", "A set of functions/rules that let one piece of software talk to another."),
    ("Array", "An ordered list of values, e.g. [1, 2, 3]."),
    ("Async/await", "JavaScript syntax for writing code that waits on slow operations without freezing the page."),
    ("Attribute", "Extra information on an HTML tag, written as name=\"value\"."),
    ("Block scope", "Variables (const/let) visible only within the { } block they're declared in."),
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
    ("Hoisting", "JavaScript's behavior of making function/variable declarations usable before the line that defines them."),
    ("HTML", "HyperText Markup Language — describes a page's structure using tags."),
    ("IIFE", "Immediately Invoked Function Expression — a function defined and called in one step, to create an isolated scope."),
    ("JSON", "JavaScript Object Notation — a text format for structured data."),
    ("let", "A JavaScript variable declaration that CAN be reassigned later."),
    ("localStorage", "A browser API for storing key-value data that persists across sessions."),
    ("Object", "A collection of named key-value pairs, e.g. {name: 'Alice'}."),
    ("Prototype pollution", "A vulnerability class (CWE-1321) where untrusted data corrupts a shared object prototype."),
    ("Regex", "Regular expression — a pattern language for matching text."),
    ("Render", "To convert data into HTML/UI and display it."),
    ("Scope", "The region of code from which a given variable is visible/accessible."),
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
# BUILD (TOC gets spliced in right before this runs)
# ================================================================
def _finalize_and_build():
    toc_flowables = [PageBreak(), Paragraph("Table of Contents", chapter_style)]
    for title, is_part in toc:
        toc_flowables.append(Paragraph(title, toc_part_style if is_part else toc_style))
    # cover page content is the first N flowables (everything added before this point
    # that isn't a chapter/part) -- we simply insert TOC right after the cover, i.e.
    # at index 1 (index 0 is the cover's first Spacer). Since `part()`/`chapter()`
    # always start with PageBreak(), and the cover has none, we insert before the
    # FIRST PageBreak in `story`.
    insert_at = len(story)
    for i, flow in enumerate(story):
        if isinstance(flow, PageBreak):
            insert_at = i
            break
    story[insert_at:insert_at] = toc_flowables

    doc = SimpleDocTemplate("TIFFIN_INTERVIEW_GUIDE.pdf", pagesize=letter,
        rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch,
        title="Tiffin — Complete Beginner-to-Interview Guide")
    doc.build(story)
    print(f"Done: TIFFIN_INTERVIEW_GUIDE.pdf ({len(toc)} chapters/parts)")

if __name__ == '__main__':
    _finalize_and_build()
