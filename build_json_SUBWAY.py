from tabula import read_pdf
import json

file_name = "./RAW_nutrition_data/subway/US_Nutrition_July2022.pdf"

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
    "Serving Size",
    "Calories",
    "Total Fat",
    "Sat. Fat",
    "Trans Fat",
    "Cholesterol",
    "Sodium",
    "Carbohydrate",
    "Fiber",
    "Sugars",
    "Added Sugars",
    "Protein",
    "Restaurant"
    ]

# Read PDF file into a JSON variable
nutrition_json = read_pdf(file_name, output_format="json", pages="all", lattice=True)
nutrition_list = []

# Remove metadata
for item in nutrition_json:
    for line in item['data']:
        nutrition_list.append(line)

# Build Nutritional List
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
            item_list.append(item['text'])
    if (len(item_list) == 0):
        pass
    else:
        restaurant_item = 'Subway'
        item_list.append(restaurant_item)
        section_list.append(item_list)

# Convert to Dictionary and place in a list of those dictionaries
list_of_dicts = []
for food in section_list:
    this_dict = {}
    if(len(food) < 13):
        pass
    else:
        for field in FIELDS:
            if(field == 'Restaurant'):
                this_dict[field] = 'Subway'
            else:
                this_dict[field] = food[FIELDS.index(field)]
        list_of_dicts.append(this_dict)

# CORRECTIONS
correction_index = next((index for (index, d) in enumerate(list_of_dicts) if d["Entry"] == "Rotisserie-Style Chicken on Plain Wrap"), None)
list_of_dicts[correction_index] = {
    "Entry": "Rotisserie-Style Chicken on Plain Wrap",
    "Serving Size": "335",
    "Calories": "500",
    "Total Fat": "14",
    "Sat. Fat": "3",
    "Trans Fat": "0",
    "Cholesterol": "75",
    "Sodium": "1440",
    "Carbohydrate": "58",
    "Fiber": "3",
    "Sugars": "7",
    "Added Sugars": "0",
    "Protein": "38",
    "Restaurant": "Subway"
  }

# Save to file
with open("subway_nutrition.json", "w") as final:
    json.dump(list_of_dicts, final)
