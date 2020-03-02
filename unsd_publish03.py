import utils
import sdg_api
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

xy_geo = utils.tsv2dictlist('data/geography/refAreas.txt', encoding='latin-1')

geo = utils.merge_dict_lists(geo, xy_geo, ['geoAreaCode'], ['M49'], how='left')

geo = utils.subdict_list(geo, ['M49', 'areaName'], exclude=True)

utils.dictList2tsv(geo, 'data/geography/geo_tree.txt')
