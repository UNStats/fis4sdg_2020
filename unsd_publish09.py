import set_release
import metadata
import utils
import os
import utils_arcgis

import requests
from arcgis.gis import GIS

# ====================================
# Upload to ArcGIS into staging folder
# ====================================

release = set_release.set_release()

series_metadata = utils.open_json(
    'data/external/metadata_' + release + '.json')

goal_properties = list(series_metadata[0].keys())
target_properties = list(series_metadata[1]['targets'][0].keys())
indicator_properties = list(
    series_metadata[1]['targets'][0]['indicators'][0].keys())
series_properties = list(
    series_metadata[1]['targets'][0]['indicators'][0]['series'][0].keys())

# Layer info template
layer_info = utils.open_json('data/external/layerinfo.json')
# print(layer_info)

layer_info_properties = list(layer_info.keys())

# ----------------------------------------
# Setup global information and variables
# ----------------------------------------

# ArcGIS group with which the data will be shared
global open_data_group
# Variable to keep track of any csv file that cannot be staged
global failed_series
# ArcGIS credentials
global online_username
# ArcGIS connection
global gis_online_connection
# Information pertaining to the layer template
global layer_json_data
# Collection of items owned by user
global user_items

# ----------------------------------------
# User parameters
# ----------------------------------------

property_update_only = False
update_symbology = True
update_sharing = True

# -----------------------------------------
# Set path to data
# -----------------------------------------

data_files = os.listdir('data/processed/'+release)

data_dir = 'data/processed/'+release

failed_series = []

# Establish ArcGIS connection
online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()
print(gis_online_connection)

# Get open data group
open_data_group = utils_arcgis.open_data_group(
    gis_online_connection, 'ad013d2911184063a0f0c97d252daf32')  # Luis
# open_data_group = open_data_group(
#     gis_online_connection, '967dbf64d680450eaf424ac4a38799ad')  # Travis

print(gis_online_connection)


# ==============================

sdgTree = series_metadata.copy()  # Produces a shallow copy of series_metadata

print(sdgTree[0].keys())
print(sdgTree[0]['code'])

for g in sdgTree:

    if g['code'] not in ['14', '15', '16', '17']:
        continue

    for t in g['targets']:
        # if t['code'] not in ['1.1']:
        #     continue

        for i in t['indicators']:
            # if i['reference'] not in ['1.1.1', '1.3.1']:
            #     continue

            if 'series' in i.keys():
                for s in i['series']:

                    # if s['code'] != 'SI_COV_POOR':
                    #     continue

                    print('\nProcessing series code:',
                          i['reference'], s['code'])

                    this_g = {k: g[k]
                              for k in g.keys() if k not in ['targets']}

                    this_t = {k: t[k]
                              for k in t.keys() if k not in ['indicators']}

                    this_i = {k: i[k] for k in i.keys() if k not in ['series']}

                    s_card = utils_arcgis.build_series_card(
                        this_g, this_t, this_i, s)

                    online_item = utils_arcgis.publish_csv(this_g,
                                                           this_t,
                                                           this_i,
                                                           s,
                                                           item_properties=s_card,
                                                           thumbnail=this_g['thumbnail'],
                                                           layer_info=layer_info,
                                                           gis_online_connection=gis_online_connection,
                                                           online_username=online_username,
                                                           data_dir=data_dir,
                                                           statistic_field='latest_value',
                                                           property_update_only=False,
                                                           color=this_g['rgb'])

                    # Only set the sharing when updating or publishing
                    if online_item is not None:
                        if update_sharing:
                            # Share this content with the open data group
                            online_item.share(everyone=False,
                                              org=True,
                                              groups=open_data_group["id"],
                                              allow_members_to_edit=False)

                        # display(online_item)
                        # Update the Group Information with Data from the Indicator and targets
                        utils_arcgis.update_item_categories(online_item,
                                                            g["code"],
                                                            t["code"],
                                                            gis_online_connection)

                        # open_data_group.update(tags=open_data_group["tags"] + [series["code"]])
                    else:
                        failed_series.append(s["code"])
