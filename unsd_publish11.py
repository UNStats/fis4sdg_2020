from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

import utils_arcgis
import json
import requests
import utils
import set_release
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# This script reads metadata card of the items published in SDG hub and
# and creates a table with the arcGIS item is corresponding to each
# SDG data series. The output is stored in ..data/external/hub_items_[release]
# ----------------------------------------------------------------------


release = set_release.set_release()

# Establish ArcGIS connection
online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(gis_online_connection)

open_data_group_prod_id_01 = '66d8595b381440afb5e320a9265c3fe1'  # UNSD_SDG01
open_data_group_prod_id_02 = '065896a584ca4ceb920fbdd3892bee05'  # UNSD_SDG02
open_data_group_prod_id_03 = 'a5552356ddd04e6fb05905bf931e9e54'  # UNSD_SDG03
open_data_group_prod_id_04 = 'c15ae34432ee46b49e3533668ae63d79'  # UNSD_SDG04
open_data_group_prod_id_05 = '25e04240b93f498e96427bd633b98dbc'  # UNSD_SDG05
open_data_group_prod_id_06 = 'e03793e08ed849be8e8b3abebf7ec983'  # UNSD_SDG06
open_data_group_prod_id_07 = 'c7e2215476e14a1a84e6990934275048'  # UNSD_SDG07
open_data_group_prod_id_08 = '1c8f53673a514f83bf932b1f8a1e9ec5'  # UNSD_SDG08
open_data_group_prod_id_09 = '688e20ebffb74d43b40ffbf297e3cf72'  # UNSD_SDG09
open_data_group_prod_id_10 = '2b3548cac5bf4cd2941d41751b45e992'  # UNSD_SDG10
open_data_group_prod_id_11 = '2455ce9284e5452a855576aad64e5a75'  # UNSD_SDG11
open_data_group_prod_id_12 = '713a738b9851495aba305483fba820ca'  # UNSD_SDG12
open_data_group_prod_id_13 = 'a334f601cbce43e4b47b0de8aa1a5b38'  # UNSD_SDG13
open_data_group_prod_id_14 = 'b3cc3fd1f58e46df8aaaa9616186f7c7'  # UNSD_SDG14
open_data_group_prod_id_15 = '157221a102d3405eb15430aff5204ad8'  # UNSD_SDG15
open_data_group_prod_id_16 = '4452219ecc1c4573a4384b6b05a9b5b5'  # UNSD_SDG16
open_data_group_prod_id_17 = 'dd0676a1809b40309c1302e9ba64bd89'  # UNSD_SDG17

online_username_admin = 'unstats_admin'

# ----
open_data_group_prod_01 = gis_online_connection.groups.get(
    open_data_group_prod_id_01)
open_data_group_prod_02 = gis_online_connection.groups.get(
    open_data_group_prod_id_02)
open_data_group_prod_03 = gis_online_connection.groups.get(
    open_data_group_prod_id_03)
open_data_group_prod_04 = gis_online_connection.groups.get(
    open_data_group_prod_id_04)
open_data_group_prod_05 = gis_online_connection.groups.get(
    open_data_group_prod_id_05)
open_data_group_prod_06 = gis_online_connection.groups.get(
    open_data_group_prod_id_06)
open_data_group_prod_07 = gis_online_connection.groups.get(
    open_data_group_prod_id_07)
open_data_group_prod_08 = gis_online_connection.groups.get(
    open_data_group_prod_id_08)
open_data_group_prod_09 = gis_online_connection.groups.get(
    open_data_group_prod_id_09)
open_data_group_prod_10 = gis_online_connection.groups.get(
    open_data_group_prod_id_10)
open_data_group_prod_11 = gis_online_connection.groups.get(
    open_data_group_prod_id_11)
open_data_group_prod_12 = gis_online_connection.groups.get(
    open_data_group_prod_id_12)
open_data_group_prod_13 = gis_online_connection.groups.get(
    open_data_group_prod_id_13)
open_data_group_prod_14 = gis_online_connection.groups.get(
    open_data_group_prod_id_14)
open_data_group_prod_15 = gis_online_connection.groups.get(
    open_data_group_prod_id_15)
open_data_group_prod_16 = gis_online_connection.groups.get(
    open_data_group_prod_id_16)
open_data_group_prod_17 = gis_online_connection.groups.get(
    open_data_group_prod_id_17)


admin_user = gis_online_connection.users.get(online_username_admin)

sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

item_list = []

for g in sdg_meta:

    # if g['code'] not in ['1']:
    #     continue

    goal_code = g['code']

    user_items = admin_user.items(
        folder='Open Data - SDG '+goal_code.zfill(2), max_items=800)

    for item in user_items:
        if item.type == 'Feature Service':

            soup = BeautifulSoup(item.description, "html.parser")
            list_items = soup.findAll('li')
            series = list_items[1].text.replace('Series Code: ', '')

            item_list.append(
                {'goal': g['code'], 'series': series, 'id': item.id})

file_out = 'data/external/hub_items_' + release + '.txt'

# It thas to be tab-delimited, in order to be able to deal with commans within strings.
utils.dictList2tsv(item_list, file_out)
