# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 20:32:23 2018

@author: Sean Howard

Summary
-------
This script requires the user to input the the directory path for the shopify
theme. The script will automatically grab the settings_data.json and
settings_schema.json file from the config folder within the directory. The
ids listed in the settings_schema.json are used as the master id roster. For
each preset group the ids are checked against the master. Any unmatched ids
are removed.

Currently this script does not clean up "sections" within each preset group.

Dependencies
------------
json
re
numpy

Parameters
----------
the full path the theme folder

Return
------
The script will print some diagnostics to the console about number of good and
bad ids by presets group.

The file settings_data.json is replaced with the unmatched ids removed. For
safety the orignal a copy of of the original is also output as
settings_data_bak.json
"""

import json
import re
import numpy as np

# get file path from user.
FILE_DATA = input("Provide full path to theme config data file:")
BAK = input("Would you like to create a backup [Y/N]:")
if BAK.upper() != "Y":
    print("Are you sure you don't want a backup?")
    BAK = input("Say yes to backups [Y/N]:")

# it is assumed that \config\settings_data.json exists
FILE_SCHEMA = FILE_DATA.replace('_data', '_schema')

# import json files and save as a dictoinary
with open(FILE_DATA, "r") as file:
    SETTINGS_DATA = json.loads(file.read())
with open(FILE_SCHEMA, "r") as file:
    FIN = file.read()

# create a backup of the settings_data.json
if BAK.upper() == 'Y':
    FILE_BAK = FILE_DATA.replace('_data', '_data_bak')
    with open(FILE_BAK, "w") as file:
        file.truncate()
        json.dump(SETTINGS_DATA, file, indent=2)

# the list of ids from schema
MATCH_PATTERN = r'"id": ".*"'
GENERAL_IDS = re.findall(MATCH_PATTERN, FIN)
GENERAL_IDS = [re.sub('"id": "', "", i) for i in GENERAL_IDS]
GENERAL_IDS = [re.sub('"', "", i) for i in GENERAL_IDS]
GENERAL_IDS = np.unique(np.array(GENERAL_IDS))
print("There are " + str(len(GENERAL_IDS)) + " unique confirmed ids")
print("------------------------------------------------------------------")

# get the list of keys for presets
KEY_NAMES = list(SETTINGS_DATA["presets"].keys())

# dictionary for unmatched by preset
UNMATCHED_OUT = {}

# loop through each key name and match against general_ids list
for name in KEY_NAMES:
    # get the unmatched keys between the schema and data settings
    IDS = np.unique(np.array(list(SETTINGS_DATA["presets"][name].keys()))[:-2])
    NOT_MATCHED = list(set(IDS) - set(GENERAL_IDS))
    NOT_MATCHED.sort()
    UNMATCHED_OUT.update({name: NOT_MATCHED})

    # loop through non-matched ids and remove from dictionary
    for kill in NOT_MATCHED:
        del SETTINGS_DATA["presets"][name][kill]

    # report what has happend to the user
    not_good = str(len(NOT_MATCHED))
    print("There were " + not_good + " unmatched ids from " + name + " removed")

    # minus 2 because of sections and content_for_index
    good = str(len(SETTINGS_DATA["presets"][name].keys())-2)
    print(name + " contains " + good + " confirmed ids")
    print("------------------------------------------------------------------")

# write output
with open(FILE_DATA, "w") as file:
    file.truncate()
    json.dump(SETTINGS_DATA, file, indent=2)

print("------------------------------------------------------------------")
