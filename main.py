from queue import Empty
import pandas as pd
from tabula import read_pdf

file_name = "./RAW_nutrition_data/US_Nutrition_July2022.pdf"



SKIP_LIST = [
    'SANDWICHES', 
    'SALADS', 
    'BREAKFAST & PIZZA & SLIDERS', 
    'BREADS & CONDIMENTS', 
    'DESSERTS & SIDES', 
    'U.S. NUTRITION INFORMATION\rJuly 2022', 
    'Values include bread, cheese and all the select vegetables.   Double values for footlong nutrition information (one footlong=two Make any Sandwich into a 6" Fresh Melt Lmited Time Offer/Regional\r6" servings)',
    'Values include lettuce, spinach, tomatoes, onions, green peppers, cucumbers and olives.  Values do not include dressing unless\rMake any Sandwich into a Salad\rnoted.',
    ['Values include lettuce, spinach, tomatoes, onions, green peppers, cucumbers and olives.  Values do not include dressing unless\rMake any Sandwich into a Salad Limited Time Offer/Regional\rnoted']
]

CATAGORIES = [
    '6" Subway Series Sandwiches',
    '6" Build Your Own Sandwiches',
    '6" Limited Time Offer/Regional Subs**',
    '6" Subway Series SandwichesDouble values for footlong nutrition information (one footlong=two 6" servings)',
    'Individual ProteinsAmount on 6" sub or salad, double values for footlong or wrap',
    'Footlong Pro Subway Series Sandwiches',
    'Footlong Pro Build Your Own Sandwiches',
    'Footlong Pro Limited Time Offer/Regional Footlong Pro Subs**',
    "Kids' Mini Sub",
    'Make any Build Your Own Sandwich into a Wrap',
    'Make any Sandwich into a Wrap Limited Time Offer/Regional Wrap',
    'Make any Sandwich into a 6" Fresh Melt',
    'Make any Sandwich into a 6" Fresh Melt Lmited Time Offer/Regional',
    'Make any Sandwich into a Salad',
    'Make any Sandwich into a Salad Limited Time Offer/Regional',
    'Make any Footlong a Protein Bowl Limited Time Offer/Regional',
    '6" Build Your Own SandwichesDouble values for footlong nutrition information (one footlong=two 6" servings)',
    '6" Limited Time Offer/Regional Subs**Double values for footlong nutrition information (one footlong=two 6" servings)',
    'Footlong Pro Subway Series SandwichesValues include footlong portions of vegetables and cheese and double footlong portion of protein',
    'Footlong Pro Build Your Own SandwichesValues include footlong portions of vegetables and cheese and double footlong portion of protein',
    'Footlong Pro Limited Time Offer/Regional Footlong Pro Subs**Values include footlong portions of vegetables and cheese and double footlong portion of protein',
    'Make any Build Your Own Sandwich into a WrapValues include suggested wrap, select fresh vegetables and footlong meat portion',
    'Make any Sandwich into a Wrap Limited Time Offer/Regional WrapValues include suggested wrap, select fresh vegetables and footlong meat portion',
    'Make any Sandwich into a 6" Fresh Melt',
    'Make any Sandwich into a 6" Fresh Melt Lmited Time Offer/Regional',
    'Omelet on 6" Artisan Flatbread (with Egg White)**',
    'Omelet on 6" Artisan Flatbread (with Regular Egg)**',
    'Omelet on 6" Artisan Italian (with Egg White)**',
    'Omelet on 6" Artisan Italian (with Regular Egg)**',
    'Omelet on Plain Wrap (with Egg White)**',
    'Omelet on Plain Wrap (with Regular Egg)**',
    'Flatizza ®**',
    '8" Pizza**',
    'Sliders',
    'Breads',
    'Sandwich Condiments and Toppings',
    'Seasonings and Spices',
    'Vegetables',
    'Cheese',
    'Individual Proteins',
    'Cookies & Desserts',
    'Soup** (8 oz. bowl)',
    'Values include bread, cheese and all the select vegetables. Double values for footlong nutrition information (one footlong=two 6" servings)',
    '6" servings)dwich into a 6" Fresh Meltd all the select vegetables.   Double values for footlong nutrition information (one footlong=two',
    'Values include bread, cheese and all the select vegetables.   Double values for footlong nutrition information (one footlong=two\rMake any Sandwich into a 6" Fresh Melt\r6" servings)',
    'Values include lettuce, spinach, tomatoes, onions, green peppers, cucumbers and olives.  Values do not include dressing unless\rMake any Sandwich into a Salad\rnoted.',
    'Values include lettuce, spinach, tomatoes, onions, green peppers, cucumbers and olives. Values do not include dressing unless noted'
]

FIELDS = [
    "Entry",
    "Serving Size (g)",
    "Calories",
    "Total Fat (g)",
    "Sat. Fat (g)",
    "Trans Fat (g)",
    "Chol. (mg)",
    "Sodium (mg)",
    "Carbohydrate(g)",
    "Dietary Fiber (g)",
    "Sugars (g)",
    "Added Sugars (g)",
    "Protein(g)",
    ]

nutrition_json = read_pdf(file_name, output_format="json", pages="all", lattice=True)
nutrition_list = []

for item in nutrition_json:
    for line in item['data']:
        nutrition_list.append(line)

section_list = []
for this_list in nutrition_list:
    item_list = []
    for item in this_list:
        if(
            item['text'] == '' or
            'A Registered Dietitian compile' in item['text'] or
            item['text'] in CATAGORIES or
            item['text'] in SKIP_LIST
            ):
            pass
        else:
            #print(f"ITEM: {item['text']}")
            item_list.append(item['text'])

        #print(f"ITEM_LIST: {item_list}")
        if (len(item_list) == 0):
            pass
        else:
            section_list.append(item_list)
        #pause_btn = input("Press Enter")


list_of_dicts = []
for food in section_list:
    this_dict = {}
    if(len(food) < 13):
        pass
    else:
        #print(f"RECORD: {food}")
        for field in FIELDS:
            #print(f"{field}: {food[FIELDS.index(field)]}")
            this_dict[field] = food[FIELDS.index(field)]
        list_of_dicts.append(this_dict)

for item in list_of_dicts:
    for key, value in item.items():
        print(f"{key}: {value}")


#print(section_list)
# df = pd.DataFrame( section_list )
# df.columns = FIELDS
# df.index.name = "entry"

# print(df.iloc[1])






