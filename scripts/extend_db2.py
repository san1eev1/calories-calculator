import json, re

with open('food_db.json') as f:
    CURRENT = json.load(f)  # 221 items, already fully extended (45 nutrient fields)

# ---------- reuse the same rule engine from extend_db.py ----------
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

# ---------- new rows: name, category, servingLabel, servingGrams, kcal, protein, carbs, fat, satFat, fiber, sugar, sodium, potassium, calcium, iron, vitA, vitC, tags ----------
NEW = [
# --- raw eggs / meats / fish ---
("Egg, raw (Anda)","Indian","1 large",50,72,6.3,0.4,4.8,1.6,0,0.2,71,69,28,0.9,80,0,{'b12':0.5,'choline':140,'vitD':1,'b7':10,'iodine':22,'fat_split':(0.4,0.15)}),
("Egg yolk, raw (Anda ki jardi)","Indian","1 yolk",17,55,2.7,0.6,4.5,1.6,0,0.1,8,19,22,0.5,65,0,{'b12':0.3,'choline':115,'vitD':1,'b7':8}),
("Chicken, raw (whole, with skin)","Indian","100 g",100,215,18,0,15,4.3,0,0,70,190,11,0.9,15,0,{'b12':0.3,'creatine':350,'choline':65}),
("Chicken breast, raw (boneless, skinless)","Indian","100 g",100,120,22.5,0,2.6,0.6,0,0,45,220,5,0.4,5,0,{'b12':0.3,'creatine':350,'choline':65}),
("Mutton, raw (bakri/goat meat)","Indian","100 g",100,143,21,0,6,2,0,0,65,385,12,3.3,0,0,{'b12':2,'creatine':400,'choline':75,'fat_split':(0.45,0.06)}),
("Fish, raw (Rohu)","Indian","100 g",100,97,17,0,2.7,0.6,0,0,45,300,20,0.7,10,0,{'epa':0.1,'dha':0.2,'vitD':2,'b12':2,'iodine':20,'creatine':350}),
("Fish, raw (Pomfret)","Indian","100 g",100,130,19,0,5.5,1.4,0,0,60,320,25,0.5,5,0,{'epa':0.15,'dha':0.3,'vitD':3,'b12':1.5,'iodine':22,'creatine':350}),
("Prawns, raw (Jhinga)","Indian","100 g",100,85,18,0.5,1,0.3,0,0,150,220,50,0.3,0,0,{'iodine':30,'b12':1,'selenium':30,'creatine':120}),
# --- cooking oils ---
("Mustard oil (Sarson ka tel)","Indian","1 tbsp",14,124,0,0,14,1.6,0,0,0,1,0,0.1,0,0,{'fat_split':(0.6,0.21),'ala':0.8,'vitE':2.2}),
("Groundnut oil (Peanut oil)","Indian","1 tbsp",14,119,0,0,13.5,2.3,0,0,0,0,0,0,0,0,{'fat_split':(0.46,0.32),'vitE':1.9}),
("Sunflower oil","Indian","1 tbsp",14,120,0,0,13.6,1.4,0,0,0,0,0,0,0,0,{'fat_split':(0.2,0.65),'la':6,'vitE':5.6}),
("Coconut oil (Nariyal tel)","Indian","1 tbsp",14,121,0,0,13.5,11.8,0,0,0,0,0,0,0,0,{'fat_split':(0.06,0.02),'vitE':0.1}),
("Sesame oil (Til ka tel)","Indian","1 tbsp",14,120,0,0,13.6,1.9,0,0,0,0,0,0,0,0,{'fat_split':(0.4,0.42),'la':5.6,'vitE':1.9}),
("Vanaspati (hydrogenated fat, Dalda)","Indian","1 tbsp",14,115,0,0,13,3.5,0,0,0,0,0,0,0,0,{'fat_split':(0.5,0.15)}),
("Rice bran oil","Indian","1 tbsp",14,120,0,0,13.6,2.7,0,0,0,0,0,0,0,0,{'fat_split':(0.4,0.35),'vitE':3.5}),
# --- raw grains / flours / dals (dry) ---
("Wheat flour, whole (Atta), raw","Indian","100 g",100,340,12,72,2,0.3,11,2,5,340,35,3.6,0,0,{'b1':0.45,'manganese':3.5,'magnesium':140}),
("Maida (refined flour), raw","Indian","100 g",100,350,10,76,1,0.2,2.7,1,5,105,15,3.5,0,0,{}),
("Besan (gram flour), raw","Indian","100 g",100,360,22,58,6,0.6,11,5,10,780,60,5.2,0,0,{'folate':180,'magnesium':160}),
("Rava / Sooji (semolina), raw","Indian","100 g",100,360,12,74,1,0.4,3,5,10,190,20,3.5,0,0,{}),
("Rice, raw (uncooked, white)","Indian","100 g",100,365,7,80,0.7,0.2,1.3,0.1,5,115,28,0.8,0,0,{}),
("Rice, raw (uncooked, brown)","Indian","100 g",100,370,7.9,77,2.9,0.6,3.5,0.4,5,220,23,1.5,0,0,{'manganese':3.7}),
("Toor dal, raw (dry, Arhar)","Indian","100 g",100,335,22,57,1.7,15,8,5,1000,73,3.6,0,0,0,{'folate':450,'molybdenum':100,'magnesium':180}),
("Moong dal, raw (dry, split)","Indian","100 g",100,347,24,59,1.2,16,6,5,1000,75,4.4,0,0,0,{'folate':550,'molybdenum':100,'magnesium':190}),
("Chana dal, raw (dry)","Indian","100 g",100,360,20,61,5,17,11,15,900,90,5,0,0,0,{'folate':480,'molybdenum':100,'magnesium':115}),
("Urad dal, raw (dry, whole)","Indian","100 g",100,340,25,59,1.6,18,4,5,980,140,7.6,0,0,0,{'folate':540,'molybdenum':100,'magnesium':270}),
("Masoor dal, raw (dry)","Indian","100 g",100,340,25,60,1.1,11,3,5,900,55,7.6,0,0,0,{'folate':480,'molybdenum':100,'magnesium':120}),
("Poha, raw (flattened rice, dry)","Indian","100 g",100,356,6.6,77,1.2,1,2,5,90,20,3.5,0,0,0,{}),
("Vermicelli (Semiya), raw","Indian","100 g",100,348,10,74,0.6,2.7,3,5,120,20,2.5,0,0,0,{}),
("Sabudana (Sago/Tapioca pearls), raw","Indian","100 g",100,350,0.2,86,0.1,0.9,3,10,15,20,1.9,0,0,0,{}),
("Ragi flour (finger millet), raw","Indian","100 g",100,320,7,72,1.3,3.6,1,5,410,340,3.9,0,0,0,{'calcium':340,'manganese':2}),
# --- raw vegetables (Indian names) ---
("Bitter gourd, raw (Karela)","Indian","100 g",100,17,1,3.7,0.2,0,2.8,2,5,296,19,0.4,25,84,{}),
("Bottle gourd, raw (Lauki)","Indian","100 g",100,14,0.6,3.4,0.1,0,0.5,2,2,150,20,0.2,0,10,{}),
("Ridge gourd, raw (Turai)","Indian","100 g",100,20,1.2,4.4,0.2,0,1.6,3,5,140,20,0.4,15,12,{}),
("Drumstick, raw (Moringa/Sahjan)","Indian","100 g",100,37,2.1,8.5,0.2,0,3.2,4,40,460,30,0.4,10,141,{'folate':40}),
("Brinjal / Eggplant, raw (Baingan)","Indian","100 g",100,25,1,6,0.2,0,3,4,5,230,9,0.2,5,2.2,{}),
("Cabbage, raw (Patta gobi)","Indian","100 g",100,25,1.3,6,0.1,0,2.5,3,20,170,40,0.5,5,37,{'vitK':76}),
("Cauliflower, raw (Phool gobi)","Indian","100 g",100,25,2,5,0.1,0,2,2,15,300,22,0.4,0,48,{'folate':57}),
("Fenugreek leaves, raw (Methi saag)","Indian","100 g",100,49,4.4,6,0.9,0,5,1,75,350,180,1.9,190,52,{'vitK':230,'folate':57}),
("Green peas, raw (Matar)","Indian","100 g",100,81,5.4,14,0.4,0,5.7,6,5,240,25,1.5,35,40,{'folate':65}),
("Taro root, raw (Arbi)","Indian","100 g",100,112,1.5,26,0.2,0,3.4,0.4,10,590,40,0.6,0,4.5,{}),
("Pointed gourd, raw (Parwal)","Indian","100 g",100,20,1.2,4,0.3,0,2,2,10,150,15,0.7,15,10,{}),
("Ivy gourd, raw (Tindora/Tendli)","Indian","100 g",100,17,1,3.6,0.1,0,1.6,2,5,150,40,1.3,25,3,{}),
("Cluster beans, raw (Gawar)","Indian","100 g",100,33,3.2,6.3,0.2,0,4.6,2,10,240,130,1.5,20,49,{}),
("Amaranth leaves, raw (Chaulai saag)","Indian","100 g",100,23,2.5,4,0.3,0,2.1,2,20,610,215,2.3,120,43,{'vitK':1140,'folate':85}),
# --- fruits ---
("Guava, raw (Amrud)","Indian","1 medium",100,68,2.6,14,1,0.3,5.4,9,2,417,18,0.3,10,228,{'soluble_frac':0.4}),
("Papaya, raw (Papita)","Indian","1 cup cubed",145,62,0.7,16,0.4,0.1,2.5,11,10,270,24,0.1,60,87,{'soluble_frac':0.4}),
("Watermelon, raw (Tarbooz)","Indian","1 cup",150,46,0.9,11.5,0.2,0,0.6,9,2,170,11,0.3,45,12,{}),
("Pomegranate, raw (Anar)","Indian","1/2 cup arils",87,72,1.5,16,1,0.1,3.5,12,3,205,9,0.3,0,9,{'soluble_frac':0.4}),
("Custard apple, raw (Sitaphal)","Indian","1 medium",150,150,2.5,36,0.6,0.3,6.8,28,10,430,25,0.7,0,36,{}),
("Chikoo, raw (Sapodilla)","Indian","1 medium",100,83,0.4,20,1.1,0.1,5.3,14,12,190,21,0.8,0,15,{'soluble_frac':0.4}),
("Jackfruit, raw (Kathal, ripe)","Indian","1 cup",150,143,2,34,0.5,0.2,2.4,29,3,440,34,0.7,15,10,{}),
("Lychee, raw (Litchi)","Indian","10 pieces",100,66,0.8,17,0.4,0.1,1.3,15,1,171,5,0.3,0,72,{}),
("Muskmelon, raw (Kharbuja)","Indian","1 cup",170,60,1.5,14,0.3,0.1,1.4,13,25,430,17,0.4,300,37,{}),
("Sweet lime, raw (Mosambi)","Indian","1 medium",100,43,0.8,10,0.2,0,1.9,8,2,180,30,0.1,5,50,{}),
("Jamun (Java plum), raw","Indian","100 g",100,60,0.7,14,0.2,0,0.6,10,26,55,19,1.2,3,14,{}),
# --- beverages ---
("Nimbu pani (lemonade, sweetened)","Indian","1 glass",250,95,0.2,24,0,0,0.2,22,5,30,5,0.1,0,15,{'added_sugar':True}),
("Jaljeera","Indian","1 glass",200,30,0.5,7,0.1,0,0.3,1,300,90,10,0.5,0,3,{}),
("Aam panna","Indian","1 glass",200,90,0.4,22,0.1,0,0.5,18,60,110,10,0.3,20,15,{'added_sugar_frac':0.7}),
("Badam milk (sweetened almond milk drink)","Indian","1 glass",200,180,6,22,7,2.5,1,20,90,220,180,0.6,15,0,{'added_sugar':True,'vitE':3}),
("Filter coffee, South Indian (with milk & sugar)","Indian","1 cup",100,60,1.5,8,2.5,1.5,0,7,20,80,50,0.1,10,0,{'caffeine':40,'added_sugar_frac':0.8}),
("Rooh Afza sharbat","Indian","1 glass",200,130,0.2,32,0,0,0,30,10,20,5,0.1,0,0,{'added_sugar':True}),
("Coconut water, raw (Nariyal pani)","Indian","1 glass",240,46,1.7,9,0.5,0,2.6,6,105,600,58,0.7,0,6,{}),
# --- dairy ---
("Khoya / Mawa","Indian","100 g",100,421,15,24,31,20,0,20,90,300,650,0.7,180,1,{'b12':0.4}),
("Condensed milk, sweetened","Indian","1 tbsp",20,65,1.6,11,1.7,1,0,11,25,75,60,0,10,0.5,{'added_sugar':True,'b12':0.1}),
("Milk powder, whole","Indian","100 g",100,496,26,38,27,17,0,38,370,1330,900,0.5,300,3,{'b12':1.5,'vitD':1}),
# --- spices / condiments ---
("Turmeric powder (Haldi)","Indian","1 tsp",3,10,0.2,2,0.1,0,0.7,0.1,1,80,6,1.6,0,0.6,{'manganese':0.6}),
("Cumin seeds (Jeera)","Indian","1 tsp",2,8,0.4,1,0.5,0.1,0.2,0,1,38,8,1,0,0.1,{}),
("Coriander powder (Dhania)","Indian","1 tsp",2,5,0.2,1,0.3,0.6,0,0,1,26,13,0.3,0,0.4,{}),
("Garam masala","Indian","1 tsp",2,7,0.3,1.2,0.3,0.4,0.1,1,25,10,6,0.6,0,0.2,{}),
("Red chilli powder (Lal mirch)","Indian","1 tsp",2,6,0.3,1,0.3,0.5,0.1,1,44,30,3,0.3,10,1.4,{}),
("Hing (asafoetida)","Indian","1 pinch",0.5,2,0.1,0.4,0,0,0,0,25,2,1,0,0,0,{}),
("Salt, table (Namak)","Indian","1 tsp",6,0,0,0,0,0,0,0,2360,1,0,0,0,0,{}),
("Sugar, white (Cheeni)","Indian","1 tsp",4,16,0,4,0,0,0,4,0,0,0,0,0,0,{'added_sugar':True}),
("Jaggery (Gur)","Indian","1 tbsp",10,38,0,10,0,0,0,10,5,80,8,0.4,0,0,{'added_sugar_frac':0.9,'magnesium':2,'manganese':0.2}),
# --- more dishes ---
("Sarson ka saag","Indian","1 katori",150,160,5,12,10,2,5,4,320,420,150,2,400,30,{'vitK':250}),
("Makki di roti","Indian","1 piece",60,150,3,28,3,0.6,3,0.5,80,90,15,1,10,0,{}),
("Handvo (Gujarati savoury cake)","Indian","1 piece",80,180,6,22,7,1.5,3,2,280,150,40,1.5,20,3,{}),
("Puran poli","Indian","1 piece",80,220,5,38,6,2,3,15,120,150,30,1.5,10,0,{'added_sugar_frac':0.7}),
("Modak, steamed","Indian","1 piece",40,100,2,18,2.5,1.5,1,10,15,60,20,0.5,10,0,{'added_sugar':True}),
("Sandesh (Bengali sweet)","Indian","1 piece",30,90,3,13,3,1.8,0.2,11,15,50,60,0.1,20,0.5,{'added_sugar':True}),
("Mishti doi","Indian","100 g",100,150,4,22,5,3,0,20,50,180,140,0.1,30,0.5,{'added_sugar':True,'b12':0.3}),
("Rasmalai","Indian","1 piece",70,180,5,22,8,4.5,0,18,45,150,150,0.2,40,1,{'added_sugar':True,'b12':0.3}),
("Kulfi","Indian","1 piece",60,130,3,16,6,3.5,0,14,35,120,90,0.1,40,0.5,{'added_sugar':True}),
("Falooda","Indian","1 glass",250,280,5,50,7,4,1,40,60,200,150,0.5,20,2,{'added_sugar':True}),
("Dal fry","Indian","1 katori",150,180,8,24,6,1,6,2,380,320,35,2.2,15,3,{'folate':70,'molybdenum':20}),
("Egg bhurji","Indian","1 serving (2 eggs)",130,220,13,4,17,4.5,0.3,2,260,150,60,1.6,150,4,{'b12':1,'choline':240}),
("Aloo tikki","Indian","1 piece",80,160,2.5,22,7,1.5,1,1,220,320,20,0.9,10,10,{}),
("Gobi paratha","Indian","1 piece",90,220,4.5,32,8,3.5,2,1,260,180,25,1.4,15,10,{}),
("Paneer paratha","Indian","1 piece",100,260,9,30,11,5,2,1,300,150,150,1.4,60,3,{'b12':0.2}),
("Chicken seekh kebab","Indian","100 g",100,250,22,4,16,5,0.3,2,420,300,25,1.5,15,3,{'b12':0.3,'creatine':300}),
("Fish tikka","Indian","100 g",100,180,22,3,8,2,0.3,2,380,320,25,1,10,3,{'epa':0.1,'dha':0.2,'b12':1.5}),
("Malai kofta","Indian","1 katori",150,320,7,20,24,11,1.5,7,420,260,150,1.2,80,8,{}),
("Navratan korma","Indian","1 katori",150,240,5,18,16,7,2.5,9,380,280,90,1.3,150,15,{}),
("Vegetable korma","Indian","1 katori",150,220,4,16,15,6.5,3,7,360,260,80,1.2,120,15,{}),
("Pesarattu (moong dal dosa)","Indian","1 piece",100,150,7,24,3,0.5,3,1,220,200,30,1.5,10,2,{'folate':40}),
("Set dosa","Indian","3 pieces",150,240,6,44,4,0.6,2,2,280,110,20,1.6,0,0,{}),
("Neer dosa","Indian","2 pieces",100,140,3,28,1.5,0.3,1,0.5,180,60,10,0.8,0,0,{}),
("Lemon rice","Indian","1 cup",180,260,4,42,9,1,2,3,420,180,30,1.3,20,10,{}),
("Tamarind rice (Puliyodarai)","Indian","1 cup",180,280,5,45,9,1,3,5,450,210,35,1.8,15,3,{}),
("Coconut rice","Indian","1 cup",180,290,4,42,12,8,2,2,320,160,25,1.2,0,0,{'fat_split':(0.06,0.02)}),
("Puttu","Indian","1 cup",100,150,3,32,1,0.2,1,0.5,150,60,15,1,0,0,{}),
("Thattai / Chakli","Indian","30 g",30,150,2.5,16,8.5,1.5,1,1,220,80,15,0.9,0,0,{}),
("Murukku","Indian","30 g",30,155,2.5,17,8.5,1.5,1,1,230,80,15,0.9,0,0,{}),
("Mathri","Indian","30 g",30,145,3,16,7.5,2,1,1,180,60,15,0.8,10,0,{}),
("Shakarpara","Indian","30 g",30,140,2,20,6,2,1,8,60,40,10,0.5,5,0,{'added_sugar':True}),
("Boondi, sweet","Indian","30 g",30,120,2,18,5,1,0.5,12,15,40,15,0.4,5,0,{'added_sugar':True}),
("Dabeli","Indian","1 piece",120,260,5,40,9,2,3,7,420,280,40,1.6,15,5,{}),
("Veg frankie / kathi roll","Indian","1 roll",150,320,8,45,12,3,3,5,480,320,80,2,60,15,{}),
("Chicken frankie / kathi roll","Indian","1 roll",170,380,18,42,15,4,2.5,5,560,360,60,2.2,50,12,{'b12':0.3,'creatine':150}),
("Sabudana vada","Indian","2 pieces",80,220,3,28,11,2,1,1,280,150,20,0.7,10,3,{}),
("Sol kadhi","Indian","1 glass",200,60,1,6,3.5,2.5,0.1,3,180,120,60,0.2,0,2,{}),
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

existing_ids = set(f['id'] for f in CURRENT)
new_ext = []
for row in NEW:
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
    new_ext.append(extend(food, tags))

# ---------- patch a handful of existing staples to include their common Hindi name ----------
NAME_PATCH = {
    "rice-cooked-white": "Rice, cooked (Chawal, white)",
    "rice-cooked-brown": "Rice, cooked (Chawal, brown)",
    "potato-boiled": "Potato, boiled (Aloo)",
    "onion-raw": "Onion, raw (Pyaz)",
    "tomato-raw": "Tomato, raw (Tamatar)",
    "garlic-raw": "Garlic, raw (Lehsun)",
    "cucumber-raw": "Cucumber, raw (Kheera)",
    "bell-pepper-raw": "Bell pepper, raw (Shimla Mirch)",
    "carrot-raw": "Carrot, raw (Gajar)",
    "spinach-cooked": "Spinach, cooked (Palak)",
    "sweet-potato-baked": "Sweet potato, baked (Shakarkandi)",
}
for f in CURRENT:
    if f['id'] in NAME_PATCH:
        f['name'] = NAME_PATCH[f['id']]

ALL = CURRENT + new_ext
print("Total foods now:", len(ALL))
ids = [f['id'] for f in ALL]
dupes = [i for i in set(ids) if ids.count(i) > 1]
print("Duplicate ids:", dupes)
print("Fields per food:", len(ALL[0]))

with open('food_db.json', 'w') as f:
    json.dump(ALL, f, separators=(',', ':'))
print("Written. Size bytes:", len(json.dumps(ALL)))
