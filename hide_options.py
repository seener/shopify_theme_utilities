# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 09:45:22 2019

@author: Sean Howard

Summary
-------
This script requires the user to input the the directory path for the shopify
theme. The script will automatically grab the settings_schema.json and
all liquid files in the sections folder. Any instances where the id attribute
of a settings object has '~' as the first character will be removed.

This is currently meant has a proof of concept.

Dependencies
------------
json
os

Parameters
----------
the full path the theme folder

Return
------
The script will print some diagnostics to the console about the json objects
removed from each file.

the settings_schema.json and liquid files in sections are overwritten with
appropriate json objects removed. Backup version of all files are created with
the suffix _bak.
"""


import json
import os

# =============================================================================
# Process \config\settings_schema.json
# =============================================================================

DIRECTORY = input("Directory for Shopify theme: ")

# get files for input
FILE_SCHEMA = DIRECTORY + r"\config\settings_schema.json"
FILE_SCHEMA_NAME = FILE_SCHEMA.split("\\")[-1]

# import schema data
with open(FILE_SCHEMA, "r") as f:
    SCHEMA_DATA = json.loads(f.read())

# create a backup of the settings_schema.json
BAK = "Y"
if BAK.upper() != "Y":
    print("Are you sure you don't want a backup?")
    BAK = input("Say yes to backups [Y/N]:")
if BAK.upper() == 'Y':
    FILE_BAK = FILE_SCHEMA.replace('_schema', '_schema_bak')
    with open(FILE_BAK, "w") as file:
        file.truncate()
        json.dump(SCHEMA_DATA, file, indent=2)

# iterate through json object and find cases where first character of id = "~"
# and remove from the json object
NUM_REMOVED = 0
for i, element in enumerate(SCHEMA_DATA):
    if 'settings' in element.keys():
        for j, sub_element in enumerate(element['settings']):
            if 'id' in sub_element.keys():
                if sub_element['id'][0] == '~':
                    NUM_REMOVED += 1
                    print()
                    print("From {0} removing:".format(FILE_SCHEMA_NAME))
                    print(SCHEMA_DATA[i]['settings'][j])
                    SCHEMA_DATA[i]['settings'].pop(j)

print("")
print("There was {0} json elements removed from {1}".format(str(NUM_REMOVED), FILE_SCHEMA_NAME))

# write output
with open(FILE_SCHEMA.replace("_schema", "_schema_test"), "w") as file:
    file.truncate()
    json.dump(SCHEMA_DATA, file, indent=2)

# =============================================================================
# deal with liquid files in sections
# =============================================================================

DIRECTORY_LIQUID = DIRECTORY + r"\\sections"
# get the list of liquid files to be processed
LIQUID_FILES = os.listdir(DIRECTORY_LIQUID)
FILE_LIQUID = DIRECTORY_LIQUID + '\\' + LIQUID_FILES[0]
FILE_LIQUID_NAME = LIQUID_FILES[0]

# import schema data
with open(FILE_LIQUID, "r") as f:
    LIQUID_IN = f.read()

# create a backup of the settings_schema.json
BAK = "Y"
if BAK.upper() != "Y":
    print("Are you sure you don't want a backup?")
    BAK = input("Say yes to backups [Y/N]:")
if BAK.upper() == 'Y':
    FILE_BAK = FILE_LIQUID.replace('.liquid', '_bak.liquid')
    with open(FILE_BAK, "w") as file:
        file.truncate()
        json.dump(LIQUID_IN, file, indent=2)

START_JSON = LIQUID_IN.index('{% schema %}') + len('{% schema %}')
END_JSON = len(LIQUID_IN) - len('{% endschema %}')
LIQUID_SCHEMA = LIQUID_IN[START_JSON:END_JSON]
LIQUID = LIQUID_IN[:START_JSON]
LIQUID_DATA = json.loads(LIQUID_SCHEMA)

# process settings and remove any json objects with '~' as the first character
# of the id.
NUM_REMOVED = 0
for j, sub_element in enumerate(LIQUID_DATA['settings']):
    if 'id' in sub_element.keys():
        if sub_element['id'][0] == '~':
            NUM_REMOVED += 1
            print()
            print("From {0}.settings removing:".format(FILE_SCHEMA_NAME))
            print(LIQUID_DATA['settings'][j])
            LIQUID_DATA['settings'].pop(j)

# iterate through the 'blocks' object and remove any json object with '~' as
# the first character of the id
for i, element in enumerate(LIQUID_DATA['blocks']):
    if 'settings' in element.keys():
        for j, sub_element in enumerate(element['settings']):
            if 'id' in sub_element.keys():
                if sub_element['id'][0] == '~':
                    NUM_REMOVED += 1
                    print()
                    print("From {0}.blocks removing:".format(FILE_LIQUID_NAME))
                    print(LIQUID_DATA['blocks'][i]['settings'][j])
                    LIQUID_DATA['blocks'][i]['settings'].pop(j)

print("")
print("There was {0} json elements removed from {1}".format(str(NUM_REMOVED), FILE_LIQUID_NAME))

# write output
with open(FILE_LIQUID.replace(".liquid", "_test.liquid"), "w") as file:
    file.truncate()
    file.write(LIQUID+"\n\n")
    json.dump(LIQUID_DATA, file, indent=2)
    file.write('\n\n{% endschema %}')
