#!/usr/bin/env python3
"""
Generate comprehensive educational PDF for the Tiffin nutrition tracker app.
Teaches JavaScript fundamentals and gradually builds to app code explanation.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def create_tutorial_pdf():
    doc = SimpleDocTemplate("TIFFIN_TUTORIAL.pdf", pagesize=letter,
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=4,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=0
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#d63384'),
        backColor=colors.HexColor('#f8f9fa'),
        leftIndent=20
    )

    # ========== COVER PAGE ==========
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("🍱 Tiffin", title_style))
    story.append(Paragraph("Complete JavaScript Tutorial & Code Explanation", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("A Full-Stack Web App for Nutrition Tracking", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>Created:</b> {datetime.now().strftime('%B %Y')}", normal_style))
    story.append(Paragraph("<b>For:</b> Complete Beginners to Advanced Developers", normal_style))
    story.append(PageBreak())

    # ========== TABLE OF CONTENTS ==========
    story.append(Paragraph("Table of Contents", heading_style))
    toc_items = [
        "Module 1: JavaScript Foundations",
        "Module 2: The Document Object Model (DOM)",
        "Module 3: Events & Interactivity",
        "Module 4: State Management",
        "Module 5: Data Structures",
        "Module 6: The Tiffin App Architecture",
        "Module 7: Deep Dive: Core Functions",
        "Module 8: UI Rendering System",
        "Appendix: Complete Glossary"
    ]
    for item in toc_items:
        story.append(Paragraph(f"• {item}", normal_style))
    story.append(PageBreak())

    # ========== MODULE 1: JAVASCRIPT FOUNDATIONS ==========
    story.append(Paragraph("Module 1: JavaScript Foundations", heading_style))

    story.append(Paragraph("1.1 What is JavaScript?", subheading_style))
    story.append(Paragraph(
        "JavaScript is a programming language that runs in web browsers. Unlike HTML (structure) and CSS (styling), "
        "JavaScript makes web pages interactive and dynamic. In Tiffin, JavaScript handles all the logic: storing data, "
        "calculating nutrients, and updating the display.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("1.2 Variables: Storing Data", subheading_style))
    story.append(Paragraph(
        "Variables are containers for storing information. Think of them as labeled boxes—each box holds a value.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>const</b> - A constant (cannot change):<br/>"
                          "<font face='Courier' color='#d63384'>const name = 'Alice';</font><br/>"
                          "<font face='Courier' color='#d63384'>const age = 25;</font>",
                          normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>let</b> - A variable (can change):<br/>"
                          "<font face='Courier' color='#d63384'>let score = 100;<br/>"
                          "score = 150;</font>",
                          normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("1.3 Data Types", subheading_style))
    data_types = [
        ("Number", "123, 45.67, -10"),
        ("String", "'hello' or \"world\""),
        ("Boolean", "true or false"),
        ("Array", "[1, 2, 3, 'apple']"),
        ("Object", "{name: 'Alice', age: 25}"),
        ("null", "Intentional absence of value"),
    ]

    for dtype, example in data_types:
        story.append(Paragraph(f"<b>{dtype}:</b> {example}", normal_style))

    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("1.4 Operations & Operators", subheading_style))
    ops = [
        ("Addition", "5 + 3 = 8"),
        ("Comparison", "5 > 3 is true"),
        ("String concatenation", "'Hello' + ' ' + 'World'"),
        ("Logical AND", "true && false = false"),
        ("Logical OR", "true || false = true"),
    ]

    for op_name, example in ops:
        story.append(Paragraph(f"<b>{op_name}:</b> {example}", normal_style))

    story.append(PageBreak())

    # ========== MODULE 2: DOM ==========
    story.append(Paragraph("Module 2: The Document Object Model (DOM)", heading_style))

    story.append(Paragraph("2.1 What is the DOM?", subheading_style))
    story.append(Paragraph(
        "The DOM is a tree of all HTML elements on a page. JavaScript uses the DOM to read and modify HTML. "
        "When you update the DOM, the browser automatically re-renders the page.",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2.2 Selecting Elements", subheading_style))
    story.append(Paragraph(
        "<b>Get an element by ID:</b><br/>"
        "<font face='Courier' color='#d63384'>const btn = document.getElementById('myButton');</font><br/><br/>"
        "<b>Get elements by class:</b><br/>"
        "<font face='Courier' color='#d63384'>const items = document.querySelectorAll('.food-item');</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2.3 Modifying HTML", subheading_style))
    story.append(Paragraph(
        "<b>Change text:</b><br/>"
        "<font face='Courier' color='#d63384'>element.textContent = 'New text';</font><br/><br/>"
        "<b>Change HTML:</b><br/>"
        "<font face='Courier' color='#d63384'>element.innerHTML = '&lt;b&gt;Bold&lt;/b&gt;';</font><br/><br/>"
        "<b>Add a CSS class:</b><br/>"
        "<font face='Courier' color='#d63384'>element.classList.add('active');</font>",
        normal_style))
    story.append(PageBreak())

    # ========== MODULE 3: EVENTS ==========
    story.append(Paragraph("Module 3: Events & Interactivity", heading_style))

    story.append(Paragraph("3.1 What are Events?", subheading_style))
    story.append(Paragraph(
        "Events are things that happen on a page: clicks, typing, scrolling. JavaScript can listen for events "
        "and run code in response.",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("3.2 Listening for Events", subheading_style))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>button.addEventListener('click', function() {<br/>"
        "&nbsp;&nbsp;console.log('Button clicked!');<br/>"
        "});</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("3.3 Common Events", subheading_style))
    events = ["click", "change", "submit", "keydown", "mouseover", "scroll"]
    for e in events:
        story.append(Paragraph(f"• <b>{e}:</b> Triggered when user {e.lower()}", normal_style))

    story.append(PageBreak())

    # ========== MODULE 4: STATE MANAGEMENT ==========
    story.append(Paragraph("Module 4: State Management", heading_style))

    story.append(Paragraph("4.1 What is Application State?", subheading_style))
    story.append(Paragraph(
        "State is the current data of your app. In Tiffin, state includes: user profile, nutrition goals, "
        "meals logged, weight history, etc. State changes when users interact with the app.",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("4.2 The State Object in Tiffin", subheading_style))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>let STATE = {<br/>"
        "&nbsp;&nbsp;goals: { calorieGoal: 2000, proteinGoal: 100, ... },<br/>"
        "&nbsp;&nbsp;profile: { name: '', sex: null, age: null, ... },<br/>"
        "&nbsp;&nbsp;diary: { '2024-09-17': { 'meal-1': [...], ... } },<br/>"
        "&nbsp;&nbsp;customFoods: [...],<br/>"
        "&nbsp;&nbsp;weightLog: [...],<br/>"
        "};</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("4.3 localStorage: Persistent Storage", subheading_style))
    story.append(Paragraph(
        "localStorage is browser storage that persists across sessions. Tiffin saves state to localStorage "
        "so data survives page refreshes.<br/><br/>"
        "<font face='Courier' color='#d63384'>// Save state<br/>"
        "localStorage.setItem('tiffin_state_v1', JSON.stringify(STATE));<br/><br/>"
        "// Load state<br/>"
        "const saved = localStorage.getItem('tiffin_state_v1');<br/>"
        "STATE = JSON.parse(saved);</font>",
        normal_style))

    story.append(PageBreak())

    # ========== MODULE 5: DATA STRUCTURES ==========
    story.append(Paragraph("Module 5: Data Structures", heading_style))

    story.append(Paragraph("5.1 Understanding Nutrients", subheading_style))
    story.append(Paragraph(
        "Tiffin tracks 44 nutrients: macronutrients (protein, carbs, fat), micronutrients (vitamins, minerals), "
        "and more. Each food has a nutrient object:",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>{<br/>"
        "&nbsp;&nbsp;kcal: 100,<br/>"
        "&nbsp;&nbsp;protein: 10,<br/>"
        "&nbsp;&nbsp;carbs: 5,<br/>"
        "&nbsp;&nbsp;fat: 2,<br/>"
        "&nbsp;&nbsp;fiber: 1,<br/>"
        "&nbsp;&nbsp;...<br/>"
        "}</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("5.2 Food Items Structure", subheading_style))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>{<br/>"
        "&nbsp;&nbsp;id: 'food-123',<br/>"
        "&nbsp;&nbsp;name: 'Chicken Breast',<br/>"
        "&nbsp;&nbsp;servingLabel: '100g',<br/>"
        "&nbsp;&nbsp;servingGrams: 100,<br/>"
        "&nbsp;&nbsp;category: 'Proteins',<br/>"
        "&nbsp;&nbsp;kcal: 165, protein: 31, carbs: 0, fat: 3.6,<br/>"
        "&nbsp;&nbsp;...(all 44 nutrients)<br/>"
        "}</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("5.3 Diary Structure (Daily Log)", subheading_style))
    story.append(Paragraph(
        "The diary stores meals for each day. Date keys are strings like '2024-09-17':<br/>"
        "<font face='Courier' color='#d63384'>diary: {<br/>"
        "&nbsp;&nbsp;'2024-09-17': {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'meal-1': [<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{ ref: {type: 'db', id: 'food-123'}, qty: 1.5 },<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;],<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;water: 2000,<br/>"
        "&nbsp;&nbsp;}<br/>"
        "}</font>",
        normal_style))

    story.append(PageBreak())

    # ========== MODULE 6: ARCHITECTURE ==========
    story.append(Paragraph("Module 6: The Tiffin App Architecture", heading_style))

    story.append(Paragraph("6.1 Overall Flow", subheading_style))
    story.append(Paragraph(
        "<b>1. User Opens App:</b> app.js loads, STATE is loaded from localStorage<br/>"
        "<b>2. Render Phase:</b> JavaScript generates HTML for the current view<br/>"
        "<b>3. User Interacts:</b> Click, type, submit—events trigger handler functions<br/>"
        "<b>4. Update Phase:</b> Handler modifies STATE<br/>"
        "<b>5. Save & Re-render:</b> STATE is saved to localStorage, page updates",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("6.2 Main Components", subheading_style))
    components = [
        ("Food Database (FOOD_DB)", "Pre-loaded JSON with 3000+ foods and nutrients"),
        ("State (STATE)", "Current app data: profile, goals, diary, etc."),
        ("Rendering Functions", "Generate HTML (renderToday, renderFoodsView, etc.)"),
        ("Handler Functions", "Respond to user events (addFood, logMeal, updateProfile, etc.)"),
        ("Utility Functions", "Helpers: calculate nutrients, format dates, etc."),
    ]

    for comp, desc in components:
        story.append(Paragraph(f"<b>{comp}:</b> {desc}", normal_style))

    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("6.3 Key Views", subheading_style))
    views = [
        ("Home/Today", "Log meals for today, see daily summary"),
        ("Foods", "Search/browse foods, create custom foods"),
        ("Progress", "Track weight, view charts, see streaks"),
        ("Nutrients", "See detailed breakdown of all nutrients"),
        ("Profile", "Set personal info, goals, targets"),
    ]

    for view_name, desc in views:
        story.append(Paragraph(f"<b>{view_name}:</b> {desc}", normal_style))

    story.append(PageBreak())

    # ========== MODULE 7: CORE FUNCTIONS ==========
    story.append(Paragraph("Module 7: Deep Dive—Core Functions", heading_style))

    story.append(Paragraph("7.1 Utility Functions", subheading_style))
    story.append(Paragraph(
        "<b>uid():</b> Generate unique IDs<br/>"
        "<font face='Courier' color='#d63384'>const id = uid(); // Returns 'a3c2f1x'</font><br/><br/>"
        "<b>toKey(date):</b> Convert Date to string key<br/>"
        "<font face='Courier' color='#d63384'>const key = toKey(new Date()); // Returns '2024-09-17'</font><br/><br/>"
        "<b>zeroNutrients():</b> Create empty nutrient object<br/>"
        "<font face='Courier' color='#d63384'>const empty = zeroNutrients(); // All nutrients = 0</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("7.2 Nutrient Math", subheading_style))
    story.append(Paragraph(
        "<b>scaleNutrients(base, qty):</b> Multiply nutrients by quantity<br/>"
        "<font face='Courier' color='#d63384'>// If eating 1.5 servings of rice<br/>"
        "const nutrients = scaleNutrients(riceNutrients, 1.5);</font><br/><br/>"
        "<b>addNutrients(a, b):</b> Sum two nutrient objects<br/>"
        "<font face='Courier' color='#d63384'>// Total daily nutrients<br/>"
        "const total = addNutrients(mealTotals, snackTotals);</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("7.3 Diary Functions", subheading_style))
    story.append(Paragraph(
        "<b>getDay(dateKey):</b> Get or create diary entry for a date<br/>"
        "<font face='Courier' color='#d63384'>const day = getDay('2024-09-17');</font><br/><br/>"
        "<b>dayTotals(dateKey):</b> Sum all nutrients for a day<br/>"
        "<font face='Courier' color='#d63384'>const total = dayTotals('2024-09-17');</font><br/><br/>"
        "<b>mealTotal(dateKey, mealId):</b> Sum nutrients for one meal<br/>"
        "<font face='Courier' color='#d63384'>const mealNutrients = mealTotal('2024-09-17', 'meal-1');</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("7.4 Energy Calculations", subheading_style))
    story.append(Paragraph(
        "<b>calcBMR():</b> Basal Metabolic Rate (calories at rest)<br/>"
        "<b>calcTDEE():</b> Total Daily Energy Expenditure (with activity multiplier)<br/>"
        "<b>calculateTargetsFromProfile():</b> Auto-calculate macro goals based on profile and goals",
        normal_style))

    story.append(PageBreak())

    # ========== MODULE 8: RENDERING ==========
    story.append(Paragraph("Module 8: The UI Rendering System", heading_style))

    story.append(Paragraph("8.1 Render Functions", subheading_style))
    story.append(Paragraph(
        "Rendering functions generate HTML as strings. They take data and return HTML. The main render function "
        "updates the page:",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>function renderApp() {<br/>"
        "&nbsp;&nbsp;renderShell(); // Navigation, sidebar<br/>"
        "&nbsp;&nbsp;renderView(); // Current view (today, foods, etc.)<br/>"
        "}</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("8.2 View Rendering Functions", subheading_style))
    story.append(Paragraph(
        "<b>renderToday():</b> Home view—meals, daily totals<br/>"
        "<b>renderFoodsView():</b> Food search and custom food creation<br/>"
        "<b>renderProgressView():</b> Weight tracking and charts<br/>"
        "<b>renderNutrientsView():</b> Detailed nutrient breakdown<br/>"
        "<b>renderProfileView():</b> User profile and goal settings",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("8.3 Building HTML with Data", subheading_style))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>function renderFoodItem(food) {<br/>"
        "&nbsp;&nbsp;return `<div class=\"food-item\"><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&lt;strong&gt;${escapeHtml(food.name)}&lt;/strong&gt;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&lt;span&gt;${food.kcal} kcal&lt;/span&gt;<br/>"
        "&nbsp;&nbsp;&lt;/div&gt;`;<br/>"
        "}<br/><br/>"
        "// Render many items<br/>"
        "const html = foods.map(f => renderFoodItem(f)).join('');<br/>"
        "document.getElementById('foodList').innerHTML = html;</font>",
        normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("8.4 The Render Cycle", subheading_style))
    story.append(Paragraph(
        "<b>Step 1:</b> User clicks button, event handler fires<br/>"
        "<b>Step 2:</b> Handler modifies STATE<br/>"
        "<b>Step 3:</b> Handler calls saveState() (localStorage update)<br/>"
        "<b>Step 4:</b> Handler calls renderView() or renderApp()<br/>"
        "<b>Step 5:</b> New HTML replaces old HTML in DOM<br/>"
        "<b>Step 6:</b> Browser re-renders the page (user sees update)",
        normal_style))

    story.append(PageBreak())

    # ========== EVENT HANDLERS ==========
    story.append(Paragraph("8.5 Event Handlers", subheading_style))
    story.append(Paragraph(
        "Event handlers respond to user actions. They live in main.html &lt;script&gt; tag. Example:",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<font face='Courier' color='#d63384'>document.addEventListener('click', function(e) {<br/>"
        "&nbsp;&nbsp;if(e.target.dataset.action === 'add-food') {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;const foodId = e.target.dataset.foodId;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;const qty = parseFloat(e.target.dataset.qty);<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;const mealId = e.target.dataset.mealId;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;addFoodToMeal(foodId, mealId, qty);<br/>"
        "&nbsp;&nbsp;}<br/>"
        "});</font>",
        normal_style))

    story.append(PageBreak())

    # ========== COMPLETE EXAMPLE ==========
    story.append(Paragraph("8.6 Complete Example: Adding a Food", subheading_style))
    story.append(Paragraph(
        "<b>User clicks 'Add Food' button for Chicken (1 serving)</b><br/><br/>"
        "1. Event handler reads food ID and meal ID<br/>"
        "2. Creates entry: <font face='Courier'>{ref: {type: 'db', id: 'chicken'}, qty: 1}</font><br/>"
        "3. Adds entry to STATE.diary['2024-09-17']['meal-1']<br/>"
        "4. Calls saveState() → saves to localStorage<br/>"
        "5. Calls renderView() → re-renders meals<br/>"
        "6. User sees chicken added to today's log",
        normal_style))

    story.append(PageBreak())

    # ========== APPENDIX ==========
    story.append(Paragraph("Appendix: Glossary", heading_style))

    glossary_items = [
        ("API", "Application Programming Interface—set of functions/rules for code interaction"),
        ("Array", "Ordered collection of items: [1, 2, 3]"),
        ("Boolean", "true or false"),
        ("Callback", "Function passed to another function, called later"),
        ("const", "Constant—variable that cannot be reassigned"),
        ("DOM", "Document Object Model—tree of HTML elements"),
        ("Event", "Something that happens: click, type, scroll"),
        ("Function", "Reusable block of code"),
        ("JSON", "JavaScript Object Notation—text format for data"),
        ("localStorage", "Browser storage for persistent data"),
        ("Object", "Collection of key-value pairs: {name: 'Alice', age: 25}"),
        ("Render", "Convert data to HTML and update the page"),
        ("State", "Current data of the application"),
        ("String", "Text: 'hello' or \"world\""),
        ("Template Literals", "Strings with variables: `Hello ${name}`"),
    ]

    for term, definition in sorted(glossary_items):
        story.append(Paragraph(f"<b>{term}:</b> {definition}", normal_style))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        f"<b>Created:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
        "<b>App:</b> Tiffin - Nutrition Tracker<br/>"
        "<b>Technology:</b> Vanilla JavaScript, HTML5, CSS3, localStorage",
        normal_style))

    # Build the PDF
    doc.build(story)
    print("✅ PDF created: TIFFIN_TUTORIAL.pdf")

if __name__ == '__main__':
    create_tutorial_pdf()
