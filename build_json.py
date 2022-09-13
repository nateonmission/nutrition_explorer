import json
import pandas as pd

FILE_NAME = "temp_Subway_pg4.json"
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

with open(FILE_NAME) as json_file:
    data = json.load(json_file)



    section_list = []
for item in data:
    item_list = []
    for field in FIELDS:
        # line_item = f'{field}: {item[FIELDS.index(field)]["text"]}'
        item_list.append(item[FIELDS.index(field)]["text"])
        print("")
    print(" ")
    section_list.append(item_list)

df = pd.DataFrame( section_list )
df.columns = FIELDS
df.index.name = "entry"

print(df.iloc[1])

#df_json = df.to_json()



