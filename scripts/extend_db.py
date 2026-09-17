import json, re

with open('food_db.json') as f:
    BASE = json.load(f)

# ---------- Extended nutrient rule engine ----------
# Precise per-food lab values for ~40 nutrients across hundreds of foods are not
# realistically available from memory. Instead we derive most extended fields from
# each food's existing macro profile using defensible nutrition-science heuristics,
# and override with specific literature-cited approximations only where a nutrient
# is genuinely significant for that food (fatty fish -> omega-3, dairy/egg/meat -> B12,
# leafy greens -> vitamin K/folate, nuts/seeds/oils -> fat subtypes, coffee/tea -> caffeine).

def clamp0(x):
    return max(0.0, round(x, 3))

def extend(food, tags):
    fat = food['fat']; sat = food['satFat']; unsat = max(0.0, fat - sat)
    protein = food['protein']; carbs = food['carbs']; fiber = food['fiber']
    sugar = food['sugar']; sodium = food['sodium']

    mufa_frac, pufa_frac = tags.get('fat_split', (0.45, 0.35))
    mufa = unsat * mufa_frac
    pufa = unsat * pufa_frac

    ala = tags.get('ala', 0.0)
    epa = tags.get('epa', 0.0)
    dha = tags.get('dha', 0.0)
    la = tags.get('la', clamp0(pufa * 0.75 - ala * 0.2))

    addedSugar = sugar if tags.get('added_sugar') else clamp0(sugar * tags.get('added_sugar_frac', 0.0))

    vitD = tags.get('vitD', 0.0)
    vitE = tags.get('vitE', clamp0(unsat * 0.5) if unsat > 1 else 0.05)
    vitK = tags.get('vitK', 0.0)

    b12 = tags.get('b12', 0.0)
    folate = tags.get('folate', clamp0(4 + fiber * 3))
    b6 = tags.get('b6', clamp0(0.03 + protein * 0.012))
    b1 = tags.get('b1', clamp0(0.02 + carbs * 0.0025 + protein * 0.004))
    b2 = tags.get('b2', clamp0(0.02 + protein * 0.01))
    b3 = tags.get('b3', clamp0(0.15 + protein * 0.16))
    b5 = tags.get('b5', clamp0(0.08 + protein * 0.02))
    b7 = tags.get('b7', 0.3)

    magnesium = tags.get('magnesium', clamp0(4 + fiber * 5 + protein * 1.4))
    phosphorus = tags.get('phosphorus', clamp0(8 + protein * 13))
    chloride = clamp0(sodium * 1.5)
    zinc = tags.get('zinc', clamp0(protein * 0.05))
    copper = tags.get('copper', clamp0(0.02 + fiber * 0.02))
    manganese = tags.get('manganese', clamp0(fiber * 0.06))
    selenium = tags.get('selenium', clamp0(protein * 0.35))
    iodine = tags.get('iodine', 0.0)
    chromium = tags.get('chromium', 0.0)
    molybdenum = tags.get('molybdenum', 0.0)
    choline = tags.get('choline', clamp0(4 + protein * 2))
    caffeine = tags.get('caffeine', 0.0)
    solubleFiber = clamp0(fiber * tags.get('soluble_frac', 0.3))
    creatine = tags.get('creatine', 0.0)

    out = dict(food)
    out.update({
        'addedSugar': round(addedSugar, 1),
        'mufa': round(mufa, 2), 'pufa': round(pufa, 2),
        'omega3Ala': round(ala, 2), 'omega3Epa': round(epa, 2), 'omega3Dha': round(dha, 2),
        'omega6La': round(la, 2),
        'vitD': round(vitD, 2), 'vitE': round(vitE, 2), 'vitK': round(vitK, 1),
        'vitB1': round(b1, 2), 'vitB2': round(b2, 2), 'vitB3': round(b3, 2), 'vitB5': round(b5, 2),
        'vitB6': round(b6, 2), 'vitB7': round(b7, 1), 'vitB9': round(folate, 1), 'vitB12': round(b12, 2),
        'magnesium': round(magnesium, 1), 'phosphorus': round(phosphorus, 1), 'chloride': round(chloride, 1),
        'zinc': round(zinc, 2), 'copper': round(copper, 2), 'manganese': round(manganese, 2),
        'selenium': round(selenium, 1), 'iodine': round(iodine, 1), 'chromium': round(chromium, 1),
        'molybdenum': round(molybdenum, 1), 'choline': round(choline, 1), 'caffeine': round(caffeine, 1),
        'solubleFiber': round(solubleFiber, 2), 'creatine': round(creatine, 1),
    })
    return out

# tag overrides keyed by food id (only where a nutrient is genuinely notable)
OVERRIDES = {}
def T(*ids, **tags):
    for i in ids:
        OVERRIDES.setdefault(i, {}).update(tags)

# --- Fish / seafood: omega-3, vitamin D, iodine, B12, creatine ---
T('salmon-cooked', fat_split=(0.4,0.35), epa=0.35, dha=1.1, vitD=11, b12=3.2, iodine=25, selenium=28, creatine=450, choline=90)
T('tuna-canned-in-water', epa=0.15, dha=0.2, vitD=1, b12=2.5, iodine=17, selenium=68, creatine=400)
T('shrimp-cooked', epa=0.1, dha=0.1, iodine=35, b12=1.2, selenium=38, creatine=150, choline=65)
T('fish-curry', epa=0.2, dha=0.5, vitD=4, b12=2, iodine=20, creatine=350)

# --- Meat / poultry: B12, zinc, creatine, choline ---
for i in ['chicken-breast-grilled','chicken-thigh-cooked','chicken-tikka','tandoori-chicken','chicken-curry','butter-chicken']:
    T(i, b12=0.3, zinc=1, creatine=350, choline=70, b3=9, selenium=20)
for i in ['ground-beef-85-lean-cooked','beef-steak-grilled','mutton-curry','keema-mince-curry']:
    T(i, b12=2.2, zinc=5, creatine=430, choline=80, b3=6, selenium=22, fat_split=(0.45,0.06))
T('pork-chop-cooked', b12=0.7, zinc=2, creatine=400, choline=90, selenium=30)
T('bacon', b12=0.4, zinc=1, creatine=250, choline=25, caffeine=0)
T('turkey-breast-cooked', b12=0.3, zinc=1.4, creatine=350, choline=65, selenium=25)
T('egg-boiled', b12=0.6, choline=147, vitD=1, b7=10, iodine=24, selenium=15, fat_split=(0.4,0.15))
T('omelette-indian-style-2-eggs', b12=1.0, choline=260, vitD=1.8, b7=18, iodine=40)
T('egg-curry', b12=1.0, choline=220, vitD=1.6, b7=16, iodine=35)

# --- Dairy: B12, iodine, vitD trace, calcium already present ---
for i in ['curd-dahi-plain','buttermilk-chaas','greek-yogurt-plain-nonfat','milk-whole','milk-skim',
          'cheddar-cheese','mozzarella-cheese','cottage-cheese','lassi-sweet','kheer','shrikhand',
          'paneer-raw','paneer-butter-masala','palak-paneer']:
    T(i, b12=0.4, iodine=20, choline=15)
T('milk-whole', vitD=1.2, b2=0.18)
T('ghee', vitD=0, vitA_note=None)
T('butter', vitD=0.2)

# --- Legumes: folate, molybdenum, soluble fiber, magnesium ---
for i in ['dal-tadka-toor','moong-dal','dal-makhani','rajma','chana-masala-chole','sambar',
          'lentils-cooked','chickpeas-cooked','black-beans-cooked','kidney-beans-cooked','sprouts-salad']:
    T(i, folate=90, molybdenum=25, soluble_frac=0.35, manganese=0.4, copper=0.25)

# --- Leafy greens & vegetables: vitamin K, folate ---
T('spinach-cooked', vitK=480, folate=145, manganese=0.9, magnesium=78)
T('kale-raw', vitK=700, folate=60, manganese=0.5)
T('methi-thepla', vitK=30, folate=25)
T('broccoli-steamed', vitK=100, folate=55, choline=18)
T('bhindi-masala', vitK=25, folate=30)
T('baingan-bharta', vitK=15)
T('kachumber-salad', vitK=15)
T('mixed-vegetable-curry', vitK=20, folate=25)
T('aloo-gobi', vitK=60, folate=40)

# --- Nuts / seeds / oils: fat subtype splits, vitamin E, magnesium ---
T('almonds', fat_split=(0.62,0.24), vitE=7.3, magnesium=76, manganese=0.6, copper=0.3, la=3.4)
T('walnuts', fat_split=(0.14,0.72), ala=2.5, vitE=0.2, magnesium=45, la=10.8, copper=0.4, manganese=1)
T('cashews', fat_split=(0.55,0.18), vitE=0.3, magnesium=83, zinc=1.6, copper=0.6, manganese=0.5)
T('peanut-butter', fat_split=(0.5,0.28), vitE=2.4, magnesium=50, la=4.5, manganese=0.6, b3=4.2)
T('peanuts-roasted', fat_split=(0.5,0.28), vitE=2.4, magnesium=48, la=4.2, folate=42, manganese=0.5)
T('olive-oil', fat_split=(0.73,0.08), vitE=1.9, vitK=8.1, la=1.1)
T('chia-seeds', fat_split=(0.08,0.85), ala=1.9, magnesium=27, calcium_note=None, manganese=0.2, phosphorus=79)
T('flax-seeds', fat_split=(0.18,0.75), ala=2.2, magnesium=39, manganese=0.2, la=0.5)
T('avocado', fat_split=(0.67,0.13), vitE=2.1, vitK=21, folate=81, choline=14)

# --- Coffee / tea / chocolate: caffeine ---
T('coffee-black', caffeine=95, b3=0.5, b2=0.18)
T('tea-black-no-sugar', caffeine=40)
T('masala-chai-with-milk-sugar', caffeine=25)
T('chocolate-dark-70', caffeine=25, magnesium=63, copper=0.5, manganese=0.5, fat_split=(0.35,0.03))
T('chocolate-milk', caffeine=6, added_sugar=True)
T('soda-cola', caffeine=30, added_sugar=True)

# --- Oats / grains: soluble fiber, B1, manganese ---
for i in ['oats-rolled-dry','oatmeal-cooked']:
    T(i, soluble_frac=0.45, manganese=0.9, b1=0.2, magnesium=32)
for i in ['pasta-white-cooked','pasta-whole-wheat-cooked','quinoa-cooked','bread-white','bread-whole-wheat',
          'rice-cooked-white','rice-cooked-brown','roti-chapati-whole-wheat','naan','bagel-plain']:
    T(i, b1=0.15, manganese=0.5)

# --- Fruits: soluble fiber ---
for i in ['apple','orange','banana','mango-sliced','strawberries','blueberries','grapes','sweet-potato-baked']:
    T(i, soluble_frac=0.4)

# --- Added sugar: sweets, desserts, sweetened drinks/snacks ---
for i in ['gulab-jamun','jalebi','rasgulla','besan-ladoo','kaju-barfi','gajar-ka-halwa','kheer','shrikhand',
          'lassi-sweet','peanut-chikki','ice-cream-vanilla','soda-cola','chocolate-milk','granola-bar',
          'apple-juice','orange-juice','ketchup']:
    T(i, added_sugar=True)
for i in ['masala-chai-with-milk-sugar','pav-bhaji','bhel-puri','pani-puri-6-pieces']:
    T(i, added_sugar_frac=0.6)

food_ext = [extend(f, OVERRIDES.get(f['id'], {})) for f in BASE]

# ---------- New items: Indian market / branded-generic packaged foods + more dishes ----------
NEW_ROWS = [
# name, category, servingLabel, servingGrams, kcal, protein, carbs, fat, satFat, fiber, sugar, sodium, potassium, calcium, iron, vitA, vitC, tags
("Milk, toned (packaged, 3% fat)","Indian","1 glass",250,120,8,12,3,0,0,12,105,340,300,0.1,60,0,{'b12':0.5,'iodine':20,'vitD':0.3}),
("Milk, full cream (packaged, 6% fat)","Indian","1 glass",250,170,8,12,10,6,0,12,105,340,290,0.1,100,0,{'b12':0.5,'iodine':20,'vitD':0.3}),
("Milk, double toned (1.5% fat, packaged)","Indian","1 glass",250,100,8,12,1.5,0.9,0,12,105,340,300,0.1,30,0,{'b12':0.5,'iodine':20}),
("Milk, skimmed (packaged)","Indian","1 glass",250,88,9,12,0.2,0.1,0,12,110,350,310,0.1,10,0,{'b12':0.5,'iodine':20}),
("Curd, packaged (full fat)","Indian","100 g",100,65,3.3,4.7,3.3,2.1,0,4.5,45,150,120,0.1,25,0.5,{'b12':0.4}),
("Curd, packaged (low fat)","Indian","100 g",100,45,4,5,1,0.6,0,4.8,48,150,130,0.1,10,0.5,{'b12':0.4}),
("Paneer, packaged (branded)","Indian","100 g",100,265,18,4,20,13,0,2,20,120,480,0.5,150,0,{'b12':0.4}),
("Tofu, packaged (Indian brand)","Indian","100 g",100,144,15,3,9,1.3,2,0.6,12,120,200,2.7,0,0,{}),
("Protein oats, chocolate (branded)","Indian","40 g",40,155,10,20,3.5,1,4,4,120,160,40,2,0,0,{'soluble_frac':0.4,'manganese':0.8,'added_sugar_frac':0.5}),
("Muesli, fruit & nut (branded)","Indian","40 g",40,160,4,28,3.5,0.8,5,7,60,150,25,1.5,0,0,{'soluble_frac':0.3}),
("Whey protein, chocolate (branded, India)","Indian","1 scoop (30 g)",30,120,24,3,1.5,0.8,0.5,1.5,60,160,110,0.2,0,0,{'b12':0.3,'choline':10}),
("Plant protein, pea/rice blend (branded)","Indian","1 scoop (30 g)",30,115,21,4,2,0.3,2,1,150,180,20,3,0,0,{'folate':20,'zinc':2}),
("Soy milk, packaged (unsweetened)","Indian","1 glass",250,90,7,4,4.5,0.6,1.5,1,55,300,25,1.4,0,0,{'folate':10,'la':2}),
("Buttermilk, packaged (branded, salted)","Indian","1 glass",200,45,2,4,1.8,1.1,0,3.5,220,130,90,0.1,10,0,{'b12':0.2}),
("Amul-style butter (packaged)","Indian","1 tbsp",14,100,0.1,0,11.4,7.5,0,0,90,3,3,0,95,0,{'vitD':0.2}),
("Sweetened flavoured yogurt (branded)","Indian","100 g",100,95,3.5,14,2.5,1.6,0,13,55,150,120,0.1,20,0.5,{'added_sugar':True,'b12':0.3}),
("Cheese slice, processed (branded)","Indian","1 slice",20,60,3,1.5,4.5,3,0,1.2,220,25,150,0.1,50,0,{'b12':0.2}),
("Multigrain atta bread (branded)","Indian","1 slice",30,80,3.5,14,1.2,0.2,2.2,1.3,140,60,20,1,0,0,{'soluble_frac':0.35}),
("Brown bread (branded)","Indian","1 slice",30,75,3,14,1,0.2,1.8,1.2,135,55,20,0.9,0,0,{}),
("Rusk, plain (branded)","Indian","2 pieces",20,85,2,15,2,0.8,1,3,90,30,15,0.6,0,0,{'added_sugar_frac':0.6}),
("Digestive biscuits (branded, 2 pc)","Indian","2 pieces",20,90,1.5,13,3.5,1.7,0.6,3,80,30,10,0.5,0,0,{'added_sugar':True}),
("Marie biscuits (branded, 4 pc)","Indian","4 pieces",24,105,2,18,3,1.4,0.6,5,90,25,10,0.5,0,0,{'added_sugar':True}),
("Cream-filled biscuits (branded, 3 pc)","Indian","3 pieces",30,150,1.5,20,7,4,0.4,10,70,25,10,0.4,0,0,{'added_sugar':True}),
("Instant noodles, masala (branded)","Indian","1 pack cooked",115,350,7,48,15,7,3,4,1200,150,20,2,10,1,{'added_sugar_frac':0.1}),
("Poha mix, instant (branded)","Indian","1 pack cooked",180,260,5,42,7,1.5,3,3,320,140,20,1.6,50,6,{}),
("Sev, namkeen (branded)","Indian","30 g",30,160,5,14,10,2,1,1,280,90,20,1.2,0,0,{'la':1.5}),
("Bhujia, namkeen (branded)","Indian","30 g",30,165,6,13,10,2,1.5,1,320,100,20,1.5,0,0,{'la':1.5}),
("Banana chips, fried (branded)","Indian","30 g",30,150,1,17,9,4,1.5,8,90,180,5,0.3,5,3,{}),
("Roasted makhana (fox nuts, branded)","Indian","30 g",30,105,3,20,0.3,0.1,2,0.5,90,150,25,1.5,0,0,{'manganese':0.4}),
("Protein bar, chocolate (branded, India)","Indian","1 bar (40 g)",40,160,15,14,6,3,3,4,110,140,60,1,0,0,{'added_sugar_frac':0.5}),
("Multigrain khakhra (branded, 2 pc)","Indian","2 pieces",30,120,3,20,3,0.5,2,1,150,90,15,1,10,0,{}),
("Ready-to-eat dal makhani (branded, tetra pack)","Indian","1 katori",150,220,8,20,12,6,5,3,480,300,70,2,50,1,{}),
("Ready-to-eat rajma (branded, tetra pack)","Indian","1 katori",150,190,8,26,5,1.2,7,3,420,380,55,2.6,10,3,{}),
("Frozen paratha, plain (branded, cooked)","Indian","1 piece",70,200,4,26,9,4,2,0.5,260,90,15,1.3,15,0,{}),
("Frozen samosa, cooked (branded)","Indian","1 piece",90,230,4,25,13,3,2.5,2,340,200,18,1,15,4,{}),
("Ragi flour porridge (finger millet)","Indian","1 bowl",200,180,5,35,2,0.4,4,2,60,150,220,3.5,20,0,{'manganese':1.4,'calcium':220}),
("Bajra roti (pearl millet)","Indian","1 medium",50,140,4,26,2.5,0.5,3,0.5,80,180,25,2.5,10,0,{'magnesium':60,'manganese':0.8}),
("Jowar roti (sorghum)","Indian","1 medium",50,130,3.5,27,1.5,0.3,3,0.4,70,170,15,1.8,5,0,{}),
("Sprout & vegetable chaat","Indian","1 bowl",150,140,9,20,3,0.4,5,6,180,320,40,2,20,25,{'folate':60}),
("Dahi vada","Indian","2 pieces",150,220,8,24,9,4,2,7,350,220,150,1.2,20,2,{'b12':0.3}),
("Undhiyu (mixed vegetable, Gujarati)","Indian","1 katori",150,210,5,20,12,3,5,6,320,380,50,1.5,80,20,{'vitK':40}),
("Litti chokha","Indian","2 pieces + chokha",200,340,9,45,13,4,6,3,420,380,40,2.5,40,15,{}),
("Misal pav","Indian","1 plate",300,380,14,50,12,3,9,6,600,480,80,3.5,60,20,{'folate':60}),
("Idiyappam (string hoppers)","Indian","3 pieces",120,170,3,38,0.5,0.1,1,0.3,150,60,10,0.8,0,0,{}),
("Appam, plain","Indian","1 piece",70,120,2,22,2,0.6,0.5,2,90,50,10,0.5,0,0,{}),
("Malabar parotta","Indian","1 piece",90,280,5,38,12,5,2,1,320,90,20,1.5,10,0,{}),
("Egg biryani","Indian","1 plate",320,480,18,55,20,5,3,4,600,340,70,2.8,120,4,{'b12':0.8,'choline':120}),
("Fish fry (Indian style)","Indian","100 g",100,220,20,8,13,3,0.5,1,380,340,40,1,20,3,{'epa':0.15,'dha':0.3,'vitD':3}),
("Prawn curry","Indian","1 katori",150,210,18,8,12,3,1,3,400,300,80,1.2,15,5,{'epa':0.1,'dha':0.1,'iodine':30}),
("Mutton biryani","Indian","1 plate",320,540,24,55,24,9,3,4,680,340,50,3,30,3,{'creatine':300}),
("Chicken 65","Indian","100 g",100,260,20,10,16,4,0.5,3,480,260,30,1.3,15,4,{}),
("Paneer tikka","Indian","100 g",100,230,14,8,17,9,0.5,3,380,220,220,1,120,6,{}),
("Rava upma with vegetables","Indian","1 cup",200,270,6,42,9,1.5,4,3,380,180,30,1.9,80,10,{}),
("Coconut chutney","Indian","2 tbsp",30,60,1,3,5,4,1.5,1,90,60,10,0.3,0,3,{}),
("Green chutney (mint-coriander)","Indian","2 tbsp",30,20,1,3,0.5,0.1,1,1,120,90,15,0.6,30,10,{}),
("Tamarind chutney","Indian","2 tbsp",30,45,0.3,11,0.1,0,0.5,9,120,60,8,0.4,0,1,{'added_sugar':True}),
]

def slug(name):
    s = name.lower()
    out = []
    for ch in s:
        if ch.isalnum(): out.append(ch)
        elif ch in " -/,()&%": out.append("-")
    s = "".join(out)
    while "--" in s: s = s.replace("--", "-")
    return s.strip("-")

existing_ids = set(f['id'] for f in food_ext)
new_food_ext = []
for row in NEW_ROWS:
    name, category, servingLabel, servingGrams, kcal, protein, carbs, fat, satFat, fiber, sugar, sodium, potassium, calcium, iron, vitA, vitC, tags = row
    base = slug(name)
    fid = base
    n = 1
    while fid in existing_ids:
        n += 1
        fid = f"{base}-{n}"
    existing_ids.add(fid)
    food = {
        "id": fid, "name": name, "category": category, "servingLabel": servingLabel, "servingGrams": servingGrams,
        "kcal": kcal, "protein": protein, "carbs": carbs, "fat": fat, "satFat": satFat, "fiber": fiber, "sugar": sugar,
        "sodium": sodium, "potassium": potassium, "calcium": calcium, "iron": iron, "vitA": vitA, "vitC": vitC,
    }
    new_food_ext.append(extend(food, tags))

ALL = food_ext + new_food_ext
print("Total foods:", len(ALL))
print("Fields per food:", len(ALL[0]))
ids = [f['id'] for f in ALL]
dupes = [i for i in set(ids) if ids.count(i) > 1]
print("Duplicate ids:", dupes)

with open('food_db.json', 'w') as f:
    json.dump(ALL, f, separators=(',', ':'))
print("Written. Size bytes:", len(json.dumps(ALL)))
