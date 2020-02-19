import utils
import metadata
import sdg_api
import pandas as pd
import os
import urllib3
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------
# Set input parameters
# ---------------------------------------------

release = '2019.Q4.G.01'

# ******************************************************************************
# SDG INDICATORS TREE AND METADATA
# ******************************************************************************

# ---------------------------------------------
# Read or update sdg metadata file
# ---------------------------------------------

tags_template = {'file': 'data/external/tagsTemplate2019.Q4.G.01.txt',
                 'seriesCodeCol': 'seriesCode',
                 'seriesTagsCol': 'seriesTags'}


sdg_meta = metadata.build_sdg_tree_metadata('data/external/GlobalIndicatorFramework2019_EN_ES_FR.xlsx',
                                            'Goals', 'Targets', 'Indicators', 'TierClassification',
                                            'data/external/sdgColors.json',
                                            tags_template['file'],
                                            tags_template['seriesCodeCol'],
                                            tags_template['seriesTagsCol'],
                                            release)


series_missing_tags = []
for g in sdg_meta:
    for t in g['targets']:
        for i in t['indicators']:
            for s in i['series']:
                if len(s['tags']) == 0:
                    series_missing_tags.append(s['code'])

series_missing_tags = list(set(series_missing_tags))

print(f'{len(series_missing_tags)} series are missing tags. \n {series_missing_tags}')

# Run the above to generate a new tags Template. After editing the tags tamplate, save it as a new txt file under data/external/
# and re-run the same command (changing the name of the tagsTemplate file if necessary).

edit_tags = utils.query_yes_no("Do you want to edit the tags template?")

if edit_tags:
    sys.exit('Run this script again after editing the tags template')

    # ******************************************************************************
    # GEOGRAPHY
    # ******************************************************************************

    # ---------------------------------------------
    # Read geographic areas tree and flatten it to
    # a parent-child relationship
    # ---------------------------------------------
geo = utils.traverse_tree(sdg_api.geoAreaTree(rootCode=1)[0],
                          parentCode=None,
                          parentName=None,
                          itemCode='geoAreaCode',
                          itemName='geoAreaName',
                          itemChildren='children',
                          hierarchy=[],
                          traverse_level=1)

# ---------------------------------------------
# Add missing areas to geo
# ---------------------------------------------

geo_missing = utils.tsv2dictlist('data/geography/missingAreas.txt')

for gm in geo_missing:

    new_dict = dict()

    new_dict['level'] = 1
    new_dict['parentCode'] = None
    new_dict['parentName'] = None
    new_dict['geoAreaCode'] = gm['geoAreaCode']
    new_dict['geoAreaName'] = gm['geoAreaName']
    new_dict['type'] = 'Group'

    geo.append(new_dict)

# ---------------------------------------------
# Merge coordinates and list of geographic areas
# ---------------------------------------------

xy_geo = utils.tsv2dictlist('data/geography/refAreas.txt')

geo = utils.merge_dict_lists(geo, xy_geo, ['geoAreaCode'], ['M49'], how='left')


# ******************************************************************************
# GET DATA FOR EACH SERIES FROM THE API
# Save as tab-delimited files for each indicator-country dataset in the
# ..data/raw/<release>/ directory
# ******************************************************************************


series = []
for g in sdg_meta:
    for t in g['targets']:
        for i in t['indicators']:
            if 'series' in i.keys():
                for s in i['series']:
                    series.append(s['code'])
series = list(set(series))

# If some series have already bene processed, skip them:
files = os.listdir('data/raw/'+release)

series_done = []
for f in files:
    f_s = re.search(r'Series_(.*?)_RefArea_(.*?).txt', f).group(1)
    if f_s in series:
        series.remove(f_s)
        series_done.append(f_s)

print(f'{len(series_done)} have already been processed')
print(f'{len(series)} remain')

for s in series:
    sdg_api.seriesData2tsv(s, release)
