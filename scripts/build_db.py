import json

# Fields: name, category, servingLabel, servingGrams,
# kcal, protein, carbs, fat, satFat, fiber, sugar, sodium(mg), potassium(mg), calcium(mg), iron(mg), vitA(mcg), vitC(mg)

rows = [
# --- Indian staples & grains ---
("Rice, cooked (white)","Indian","1 cup",150,200,4.2,44,0.4,0.1,0.6,0.1,2,55,16,0.4,0,0),
("Rice, cooked (brown)","Indian","1 cup",150,170,3.5,36,1.3,0.3,1.6,0.5,5,84,15,0.6,0,0),
("Roti / Chapati (whole wheat)","Indian","1 medium",40,120,3.6,24,0.7,0.1,3,0.6,95,90,10,1.1,0,0),
("Naan","Indian","1 piece",90,260,8,45,5,1,2,3,430,110,50,2,0,0),
("Paratha, plain","Indian","1 piece",60,210,4,27,9,4,2,0.5,190,80,15,1.2,20,0),
("Aloo paratha","Indian","1 piece",90,260,5,35,11,5,3,1,320,220,25,1.5,15,4),
("Methi thepla","Indian","1 piece",50,130,3,18,5,1,2,1,180,120,30,1,50,2),
("Idli","Indian","1 piece",35,58,2,12,0.2,0.05,0.5,0.2,80,35,5,0.3,0,0),
("Rava idli","Indian","1 piece",40,70,2,13,1,0.2,0.6,0.5,120,50,10,0.5,5,0),
("Dosa, plain","Indian","1 medium",80,133,3.5,22,3.5,0.5,1,0.5,190,60,10,0.9,0,0),
("Uttapam","Indian","1 piece",100,160,4,28,3.5,0.5,1.5,1,220,90,15,1,10,2),
("Poha","Indian","1 cup",150,250,4,45,6,1,2,3,300,120,20,1.5,50,8),
("Upma","Indian","1 cup",200,260,6,40,9,1.5,3,2,380,150,25,1.8,60,5),
("Khichdi","Indian","1 bowl",250,280,10,45,6,1,4,2,350,220,35,2.5,40,3),
("Vegetable pulao","Indian","1 cup",200,280,6,45,8,1.5,3,3,320,150,30,1.5,80,10),
("Chicken biryani","Indian","1 plate",300,490,22,58,18,4,3,3,650,320,50,2.5,60,4),
("Vegetable biryani","Indian","1 plate",300,420,9,65,14,2.5,4,4,580,280,45,2,100,8),
("Curd rice","Indian","1 bowl",200,220,6,35,5,2.5,1,4,250,180,120,0.6,30,2),
("Sabudana khichdi","Indian","1 bowl",150,260,3,40,10,1.5,1,1,180,160,20,0.8,20,3),
("Bisi bele bath","Indian","1 bowl",250,320,9,50,9,1.5,5,4,420,260,50,2.5,70,6),
# --- Indian legumes & curries ---
("Dal tadka (toor)","Indian","1 katori",150,150,8,20,4,0.7,5,2,320,320,30,2.2,20,2),
("Moong dal","Indian","1 katori",150,130,8,18,2.5,0.4,5,1.5,280,300,25,2,10,1),
("Dal makhani","Indian","1 katori",150,280,10,25,16,7,7,3,420,350,80,2.5,60,2),
("Rajma","Indian","1 katori",150,210,9,30,6,1.5,8,4,380,420,60,3,15,5),
("Chana masala / Chole","Indian","1 katori",150,220,9,32,6,1,8,5,400,380,60,3,20,8),
("Sambar","Indian","1 bowl",200,150,6,22,4,0.5,5,4,450,280,40,1.5,30,4),
("Rasam","Indian","1 bowl",200,60,2,10,1.5,0.2,1.5,3,380,180,20,0.8,15,6),
("Kadhi","Indian","1 bowl",200,160,5,18,7,3,1,6,400,220,120,0.6,20,2),
("Palak paneer","Indian","1 katori",150,230,10,10,17,8,3,3,380,320,220,2,300,15),
("Paneer butter masala","Indian","1 katori",150,320,11,14,25,12,2,6,450,250,200,1,150,8),
("Butter chicken","Indian","1 katori",150,330,18,10,24,11,1.5,5,480,280,60,1,100,3),
("Chicken curry","Indian","1 katori",150,240,20,8,14,4,1.5,3,380,300,30,1.5,40,3),
("Egg curry","Indian","1 katori (2 eggs)",200,260,14,10,18,5,2,4,400,260,80,2,150,5),
("Fish curry","Indian","1 katori",150,220,18,8,13,3,1.5,3,350,320,40,1,30,5),
("Mutton curry","Indian","1 katori",150,320,20,8,22,8,1.5,3,400,300,30,2.5,20,3),
("Keema (mince curry)","Indian","1 katori",100,250,17,6,17,6,1,2,380,260,25,2,15,3),
("Aloo gobi","Indian","1 katori",150,150,3,18,7,1,4,4,280,380,40,1,30,25),
("Baingan bharta","Indian","1 katori",150,130,2.5,14,7,1,5,5,300,320,25,0.8,20,8),
("Bhindi masala","Indian","1 katori",150,130,3,12,8,1,4,3,260,300,60,1,40,15),
("Mixed vegetable curry","Indian","1 katori",150,140,3,16,7,1,4,5,280,300,40,1,60,20),
# --- Indian snacks / street food ---
("Samosa","Indian","1 piece",100,260,4,28,15,3,3,2,380,220,20,1.2,20,5),
("Pakora, mixed vegetable","Indian","100 g",100,280,6,25,18,3,3,3,350,250,30,1.5,40,8),
("Vada, medu","Indian","1 piece",60,150,4,16,8,1,2,1,220,120,15,0.8,5,1),
("Dhokla","Indian","100 g",100,160,5,25,4,0.5,2,3,350,120,25,1,5,1),
("Vada pav","Indian","1 piece",150,340,7,45,15,3,3,4,480,280,40,1.8,10,3),
("Pav bhaji","Indian","1 plate",300,420,9,55,18,8,7,10,650,480,80,2.5,120,25),
("Chole bhature","Indian","1 plate",350,620,15,75,28,10,10,8,700,520,80,4,30,10),
("Puri","Indian","1 piece",30,100,1.8,11,5.5,1,0.8,0.3,90,40,5,0.5,0,0),
("Papad, roasted","Indian","1 piece",10,35,2,5,0.5,0.1,0.8,0.2,280,60,5,0.4,0,0),
("Bhel puri","Indian","1 plate",150,250,6,40,8,1,4,8,480,320,30,1.5,20,15),
("Pani puri (6 pieces)","Indian","6 pieces",120,180,4,30,5,0.8,2,4,420,220,15,1,10,10),
("Kachori","Indian","1 piece",70,220,4,24,12,2.5,2,2,320,150,15,1,5,2),
("Momos, vegetable (6 pc)","Indian","6 pieces",150,260,6,40,7,1,3,4,420,250,30,1.5,30,6),
("Momos, chicken (6 pc)","Indian","6 pieces",150,300,14,35,10,2,2,3,450,280,25,1.5,10,3),
# --- Indian sweets ---
("Gulab jamun","Indian","1 piece",40,150,2,18,8,4,0.2,17,40,40,50,0.2,10,0),
("Jalebi","Indian","1 piece",30,110,0.8,18,4,1.5,0.1,16,20,15,10,0.2,0,0),
("Rasgulla","Indian","1 piece",40,90,2,17,1,0.5,0.1,16,15,25,30,0.1,0,0),
("Besan ladoo","Indian","1 piece",30,130,2.5,14,7,3,0.8,10,20,50,15,0.6,10,0),
("Kaju barfi","Indian","1 piece",20,100,1.5,10,6,2.5,0.3,9,10,40,10,0.4,0,0),
("Gajar ka halwa","Indian","1 katori",100,240,4,28,13,7,2,22,60,220,120,0.5,600,3),
("Kheer","Indian","1 katori",150,200,5,30,7,4,0.3,26,60,180,150,0.3,40,1),
("Shrikhand","Indian","1 katori",100,220,6,32,7,4,0.1,30,40,150,150,0.1,30,1),
# --- Indian dairy / beverages / misc ---
("Curd / Dahi, plain","Indian","100 g",100,60,3.5,4.5,3,2,0,4.5,45,150,120,0.1,25,0.5),
("Buttermilk / Chaas","Indian","1 glass",200,40,2,4,1.5,1,0,4,180,120,80,0.1,10,0),
("Paneer, raw","Indian","100 g",100,265,18,4,20,13,0,2,20,120,480,0.5,150,0),
("Ghee","Indian","1 tbsp",13,115,0,0,13,8,0,0,0,0,0,0,90,0),
("Masala chai (with milk & sugar)","Indian","1 cup",150,90,2.5,12,3.5,2,0,11,30,100,80,0.1,15,0),
("Lassi, sweet","Indian","1 glass",250,180,6,26,6,3.5,0,24,80,260,200,0.1,30,1),
("Pickle / Achar, mixed","Indian","1 tbsp",15,35,0.3,3,2.5,0.3,0.5,1,400,20,5,0.3,10,0),
("Roasted chana","Indian","1 handful",30,120,7,18,2,0.2,5,3,5,220,20,1.5,0,0),
("Peanut chikki","Indian","1 piece",25,115,3.5,12,6,1.5,1,9,15,90,15,0.5,0,0),
("Moong dal chilla","Indian","1 piece",80,130,7,18,3,0.4,3,2,220,220,25,1.5,10,2),
("Besan chilla","Indian","1 piece",80,140,6,16,5,0.6,3,2,230,180,20,1.3,10,1),
("Raita","Indian","1 katori",100,70,3,6,3.5,2,0.5,5,150,140,100,0.2,20,3),
("Kachumber salad","Indian","1 katori",100,45,1.5,9,0.3,0,2,5,150,220,25,0.5,40,20),
("Sprouts salad","Indian","1 katori",100,90,7,14,1,0.2,4,3,120,220,25,1.5,10,10),
("Chicken tikka","Indian","100 g",100,190,26,4,8,2,0.5,2,420,320,30,1.2,15,3),
("Tandoori chicken","Indian","100 g",100,170,25,3,6,1.5,0.3,1,400,320,20,1,10,2),
("Omelette, Indian style (2 eggs)","Indian","1 serving",120,220,14,4,17,4,0.5,2,280,180,60,1.8,150,10),
# --- International: proteins ---
("Chicken breast, grilled","International","100 g",100,165,31,0,3.6,1,0,0,74,256,15,1,9,0),
("Chicken thigh, cooked","International","100 g",100,209,26,0,11,3,0,0,90,240,12,1.3,20,0),
("Salmon, cooked","International","100 g",100,208,20,0,13,3,0,0,59,363,9,0.3,50,0),
("Tuna, canned in water","International","100 g",100,116,26,0,1,0.3,0,0,247,237,10,1,20,0),
("Egg, boiled","International","1 large",50,78,6.3,0.6,5.3,1.6,0,0.6,62,63,25,0.6,80,0),
("Egg white","International","1 large",33,17,3.6,0.2,0.05,0,0,0.2,55,54,2,0,0,0),
("Ground beef, 85% lean, cooked","International","100 g",100,250,26,0,17,6.5,0,0,75,270,15,2.5,0,0),
("Beef steak, grilled","International","100 g",100,271,25,0,19,7.5,0,0,60,320,10,2.6,0,0),
("Pork chop, cooked","International","100 g",100,231,26,0,14,5,0,0,62,320,10,0.7,5,0),
("Bacon","International","2 slices",16,90,6,0.2,7,2.5,0,0,300,90,2,0.2,0,0),
("Turkey breast, cooked","International","100 g",100,135,30,0,1,0.3,0,0,55,260,10,1,0,0),
("Shrimp, cooked","International","100 g",100,99,24,0.2,0.3,0.1,0,0,111,220,70,0.5,0,0),
("Tofu, firm","International","100 g",100,144,15,3,9,1.3,2,0.6,12,120,200,2.7,0,0),
# --- International: dairy ---
("Greek yogurt, plain (nonfat)","International","100 g",100,59,10,3.6,0.4,0.1,0,3.2,36,141,110,0.1,0,0),
("Milk, whole","International","1 glass",250,150,8,12,8,4.5,0,12,105,350,280,0.1,110,0),
("Milk, skim","International","1 glass",250,90,9,12,0.5,0.3,0,12,105,380,300,0.1,150,0),
("Almond milk, unsweetened","International","1 glass",250,40,1.5,1.5,3,0,1,0,180,180,450,0.5,110,0),
("Cheddar cheese","International","1 slice",30,120,7,0.5,10,6,0,0.1,180,25,200,0.2,90,0),
("Mozzarella cheese","International","30 g",30,85,6,0.6,6.3,3.7,0,0.3,175,20,150,0.1,60,0),
("Cottage cheese","International","100 g",100,98,11,3.4,4.3,2.7,0,2.7,364,104,83,0.1,37,0),
("Butter","International","1 tbsp",14,100,0.1,0,11.4,7.3,0,0,90,3,3,0,95,0),
# --- International: grains / breads ---
("Oats, rolled (dry)","International","40 g",40,150,5,27,3,0.5,4,0.5,0,140,20,1.7,0,0),
("Oatmeal, cooked","International","1 bowl",230,150,5,27,3,0.5,4,0.5,10,140,20,1.7,0,0),
("Bread, white","International","1 slice",28,75,2.5,14,1,0.2,0.8,1.5,150,30,40,0.8,0,0),
("Bread, whole wheat","International","1 slice",28,70,3.5,12,1,0.2,2,1.5,130,55,20,0.9,0,0),
("Bagel, plain","International","1 piece",95,245,9,48,1.5,0.2,2,4,430,110,50,3,0,0),
("Croissant","International","1 piece",60,230,5,26,12,7,1.5,6,280,70,20,1.2,50,0),
("Pasta, white, cooked","International","1 cup",150,220,8,43,1.3,0.2,2.5,1,3,60,10,1,0,0),
("Pasta, whole wheat, cooked","International","1 cup",150,200,8,40,1.5,0.3,5,1,5,90,20,1.5,0,0),
("Quinoa, cooked","International","1 cup",150,180,6.5,32,3,0.3,4,1,10,240,20,2,5,0),
("Sweet potato, baked","International","1 medium",150,130,2.3,30,0.2,0,4.5,9,55,540,45,1,1400,20),
("Potato, boiled","International","1 medium",150,130,2.7,30,0.2,0,2.7,1.5,6,510,12,0.5,0,15),
("Corn flakes cereal","International","1 cup",30,110,2,25,0.3,0,1,2,200,30,1,4,150,15),
("Granola bar","International","1 bar",40,180,4,26,7,3,3,10,110,120,30,1,0,0),
("Pancake","International","1 medium",60,150,4,20,6,1.5,0.6,5,300,90,80,1,20,0),
("Waffle","International","1 piece",75,220,5,27,10,2,1,5,380,110,150,1.5,20,0),
# --- International: vegetables ---
("Broccoli, steamed","International","100 g",100,35,2.4,7,0.4,0,3.3,1.7,33,290,47,0.7,31,65),
("Spinach, cooked","International","100 g",100,23,2.9,3.6,0.3,0,2.4,0.4,70,466,136,3.6,469,10),
("Kale, raw","International","100 g",100,49,4.3,9,0.9,0.1,3.6,2.3,38,491,150,1.5,500,120),
("Carrot, raw","International","100 g",100,41,0.9,10,0.2,0,2.8,4.7,69,320,33,0.3,835,5.9),
("Tomato, raw","International","100 g",100,18,0.9,3.9,0.2,0,1.2,2.6,5,237,10,0.3,42,14),
("Cucumber, raw","International","100 g",100,15,0.7,3.6,0.1,0,0.5,1.7,2,147,16,0.3,5,3),
("Bell pepper, raw","International","100 g",100,31,1,6,0.3,0,2.1,4.2,4,211,7,0.4,157,128),
("Onion, raw","International","100 g",100,40,1.1,9.3,0.1,0,1.7,4.2,4,146,23,0.2,0,7.4),
("Garlic, raw","International","10 g",10,15,0.6,3.3,0.05,0,0.2,0.1,2,40,18,0.2,0,3),
# --- International: fruits ---
("Banana","International","1 medium",120,105,1.3,27,0.4,0.1,3.1,14,1,422,6,0.3,4,10),
("Apple","International","1 medium",180,95,0.5,25,0.3,0,4.4,19,2,195,11,0.2,5,8.4),
("Orange","International","1 medium",130,62,1.2,15,0.2,0,3.1,12,0,237,52,0.1,14,70),
("Mango, sliced","International","1 cup",165,99,1.4,25,0.6,0.1,2.6,23,2,277,18,0.3,89,60),
("Grapes","International","1 cup",150,104,1.1,27,0.2,0.1,1.4,23,3,288,15,0.5,5,5),
("Strawberries","International","1 cup",150,49,1,12,0.5,0,3,7,2,220,24,0.6,1,90),
("Blueberries","International","1 cup",150,84,1.1,21,0.5,0,3.6,15,1,114,9,0.4,3,14),
("Avocado","International","100 g",100,160,2,8.5,15,2.1,6.7,0.7,7,485,12,0.6,7,10),
# --- International: nuts / seeds / fats ---
("Almonds","International","28 g (handful)",28,164,6,6,14,1.1,3.5,1.2,0,200,76,1,0,0),
("Walnuts","International","28 g (handful)",28,185,4.3,3.9,18.5,1.7,1.9,0.7,1,125,28,0.8,0,0.4),
("Cashews","International","28 g (handful)",28,157,5.2,8.6,12.4,2.2,0.9,1.7,3,187,10,1.9,0,0),
("Peanut butter","International","2 tbsp",32,190,8,7,16,3,2,3,150,190,15,0.6,0,0),
("Olive oil","International","1 tbsp",14,119,0,0,13.5,1.9,0,0,0,0,0,0.1,0,0),
("Chia seeds","International","1 tbsp",12,58,2,5,3.7,0.4,4.1,0,1,44,63,0.9,0,0),
("Flax seeds","International","1 tbsp",10,55,1.9,3,4.3,0.4,2.8,0.2,3,81,26,0.6,0,0),
("Peanuts, roasted","International","28 g (handful)",28,166,7,6,14,2,2.4,1.3,5,190,15,0.7,0,0),
# --- International: legumes ---
("Lentils, cooked","International","1 cup",150,173,13,30,0.6,0.1,12,2.7,4,477,29,4.9,4,3),
("Chickpeas, cooked","International","1 cup",150,246,12,41,4,0.4,10,7,10,340,60,4,2,2),
("Black beans, cooked","International","1 cup",150,170,11,31,0.6,0.2,11,0.4,2,460,35,2.6,1,0),
("Kidney beans, cooked","International","1 cup",150,170,11,30,0.6,0.1,10,0.6,2,440,40,3.2,0,2),
# --- International: packaged / fast food ---
("Pizza, cheese","International","1 slice",110,285,12,36,10,4.5,2.5,4,600,180,190,2,80,2),
("Burger, beef, plain","International","1 burger",200,500,25,40,26,10,2,7,700,380,80,4,20,2),
("French fries","International","100 g",100,312,3.4,41,15,2.3,3.8,0.3,210,580,15,0.7,0,10),
("Potato chips","International","1 small bag",28,152,2,15,10,3,1.2,0.1,150,360,7,0.5,0,8),
("Chocolate, dark 70%","International","28 g",28,170,2.2,13,12,7,3.1,7,6,200,22,3.4,3,0),
("Chocolate, milk","International","28 g",28,150,2,17,8.5,5,1,15,25,130,60,0.4,10,0),
("Ice cream, vanilla","International","100 g",100,207,3.5,24,11,6.8,0.7,21,80,199,128,0.1,110,0.6),
("Whey protein powder","International","1 scoop",30,120,24,3,1.5,0.8,0.5,1.5,50,150,120,0.2,0,0),
("Hummus","International","2 tbsp",30,70,2,6,4.5,0.6,2,0.2,120,70,20,0.6,0,1),
("Popcorn, air-popped","International","1 cup",30,110,3.5,22,1.3,0.2,4,0.1,1,90,3,0.9,20,0),
# --- Condiments / beverages ---
("Mayonnaise","International","1 tbsp",14,94,0.1,0.1,10.3,1.6,0,0.1,88,2,1,0,10,0),
("Ketchup","International","1 tbsp",17,19,0.2,4.7,0.05,0,0.1,3.7,167,60,3,0.1,3,2),
("Mustard","International","1 tsp",5,3,0.2,0.3,0.2,0,0.2,0.1,55,7,4,0.1,0,0),
("Soy sauce","International","1 tbsp",15,8,1.3,0.8,0,0,0.1,0.1,900,30,1,0.1,0,0),
("Coffee, black","International","1 cup",240,2,0.3,0,0,0,0,0,5,116,5,0,0,0),
("Tea, black, no sugar","International","1 cup",240,2,0,0.7,0,0,0,0,5,66,0,0,0,0),
("Orange juice","International","1 glass",250,110,1.7,26,0.5,0,0.5,21,2,470,25,0.5,10,120),
("Apple juice","International","1 glass",250,115,0.2,28,0.3,0,0.3,24,10,220,20,0.6,0,2),
("Soda, cola","International","1 can",330,140,0,39,0,0,0,39,45,5,10,0,0,0),
("Beer","International","1 can",355,150,1.6,13,0,0,0,0,14,96,14,0,0,0),
("Wine, red","International","1 glass",150,125,0.1,4,0,0,0,1,6,140,9,0.4,0,0),
]

def slug(name):
    s = name.lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/,()":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")

foods = []
seen = {}
for r in rows:
    (name, category, servingLabel, servingGrams, kcal, protein, carbs, fat, satFat,
     fiber, sugar, sodium, potassium, calcium, iron, vitA, vitC) = r
    base = slug(name)
    n = seen.get(base, 0)
    seen[base] = n + 1
    fid = base if n == 0 else f"{base}-{n+1}"
    foods.append({
        "id": fid,
        "name": name,
        "category": category,
        "servingLabel": servingLabel,
        "servingGrams": servingGrams,
        "kcal": kcal,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "satFat": satFat,
        "fiber": fiber,
        "sugar": sugar,
        "sodium": sodium,
        "potassium": potassium,
        "calcium": calcium,
        "iron": iron,
        "vitA": vitA,
        "vitC": vitC,
    })

print(f"Total foods: {len(foods)}")
ids = [f["id"] for f in foods]
dupes = set([i for i in ids if ids.count(i) > 1])
print(f"Duplicate ids: {dupes}")

with open("/home/claude/food_db.json", "w") as f:
    json.dump(foods, f, indent=None, separators=(",", ":"))

print("Written food_db.json, size bytes:", len(json.dumps(foods)))
