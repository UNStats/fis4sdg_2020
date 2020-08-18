from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

import utils_arcgis
import json
import requests
import utils
import set_release


historic_folder = 'Historic Data 2020Q1G02'

release = set_release.set_release()


global open_data_group
global open_data_group_prod
global online_username
global online_username_admin
global gis_online_connection

# Establish ArcGIS connection
online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(gis_online_connection)

# open_data_group_id:
# open_data_group_stage_id = '967dbf64d680450eaf424ac4a38799ad' #Travis
open_data_group_stage_id = 'ad013d2911184063a0f0c97d252daf32'  # Luis
open_data_group_prod_id = '15c1671f5fbc4a00b1a359d51ea6a546'  # SDG Open Data
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

print(online_username_admin)
print(online_username)

# ----
open_data_group_prod = gis_online_connection.groups.get(
    open_data_group_prod_id)
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

# --------------------

# Production Site Changes
#  Search all the Items in Production Open Data Group
user = gis_online_connection.users.get(online_username)
admin_user = gis_online_connection.users.get(online_username_admin)

print(user)
print(admin_user)

sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

for g in sdg_meta:

    # if g['code'] not in ['1']:
    #    continue

    goal_code = g['code']

    user_items = admin_user.items(
        folder='Open Data - SDG '+goal_code.zfill(2), max_items=800)

    for item in user_items:
        #  Move these items into Archive folder under the Admin User
        print('Moving ' + item.title + ' to archive folder')
        item.move(folder="Historic Data 2019Q3G01",
                  owner=online_username_admin)

        #  Unshare the Items from Open Data Group (Production)
        print('unsharing item ' + item.title + " from the open data group")

        item.unshare(open_data_group_prod["id"])
        if goal_code == '1':
            item.unshare(open_data_group_prod_01["id"])
        elif goal_code == '2':
            item.unshare(open_data_group_prod_02["id"])
        elif goal_code == '3':
            item.unshare(open_data_group_prod_03["id"])
        elif goal_code == '4':
            item.unshare(open_data_group_prod_04["id"])
        elif goal_code == '5':
            item.unshare(open_data_group_prod_05["id"])
        elif goal_code == '6':
            item.unshare(open_data_group_prod_06["id"])
        elif goal_code == '7':
            item.unshare(open_data_group_prod_07["id"])
        elif goal_code == '8':
            item.unshare(open_data_group_prod_08["id"])
        elif goal_code == '9':
            item.unshare(open_data_group_prod_09["id"])
        elif goal_code == '10':
            item.unshare(open_data_group_prod_10["id"])
        elif goal_code == '11':
            item.unshare(open_data_group_prod_11["id"])
        elif goal_code == '12':
            item.unshare(open_data_group_prod_12["id"])
        elif goal_code == '13':
            item.unshare(open_data_group_prod_13["id"])
        elif goal_code == '14':
            item.unshare(open_data_group_prod_14["id"])
        elif goal_code == '15':
            item.unshare(open_data_group_prod_15["id"])
        elif goal_code == '16':
            item.unshare(open_data_group_prod_16["id"])
        elif goal_code == '17':
            item.unshare(open_data_group_prod_17["id"])

        #  Update Tags (Remove Current add Historic)
        item_properties = {}
        item_properties["tags"] = item.tags
        if 'Current' in item_properties["tags"]:
            item_properties["tags"] = item_properties["tags"].remove(
                'Current')

        item_properties["tags"].append('Historic')
        item.update(item_properties=item_properties)

        # Mark this item as depracated

        utils_arcgis.set_content_status(
            gis_online_connection, item, authoratative=False)

    # -----------------------------------------------------------
    # Staging Site Changes
    #  Get all the Items in the Open Data Folder
    # -----------------------------------------------------------

    user_items = user.items(
        folder='Open Data SDG' + goal_code.zfill(2), max_items=800)

    # Move all the CSV Files to the Open Data Folder of the Admin User
    # This will also move the Feature Service Layer!!!!
    for item in user_items:
        if item.type == 'CSV':
            # Assign Item to the Admin User
            print('reassigning item ' + item.title + ' from ' +
                  online_username + ' to ' + online_username_admin)
            item.reassign_to(online_username_admin,
                             'Open Data - SDG ' + goal_code.zfill(2))

    # -----------------------------------------------------------
    # Update the Items in the Open Data Folder of the Admin User
    # -----------------------------------------------------------

    user_items = admin_user.items(
        folder='Open Data - SDG ' + goal_code.zfill(2), max_items=800)

    # Update Sharing to Public, Share with Open Data Group
    for item in user_items:
        if item.type != 'CSV':
            print('updating sharing for item ' + item.title)
            if goal_code == '1':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_01["id"], allow_members_to_edit=False)
            elif goal_code == '2':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_02["id"], allow_members_to_edit=False)
            elif goal_code == '3':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_03["id"], allow_members_to_edit=False)
            elif goal_code == '4':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_04["id"], allow_members_to_edit=False)
            elif goal_code == '5':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_05["id"], allow_members_to_edit=False)
            elif goal_code == '6':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_06["id"], allow_members_to_edit=False)
            elif goal_code == '7':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_07["id"], allow_members_to_edit=False)
            elif goal_code == '8':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_08["id"], allow_members_to_edit=False)
            elif goal_code == '9':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_09["id"], allow_members_to_edit=False)
            elif goal_code == '10':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_10["id"], allow_members_to_edit=False)
            elif goal_code == '11':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_11["id"], allow_members_to_edit=False)
            elif goal_code == '12':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_12["id"], allow_members_to_edit=False)
            elif goal_code == '13':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_13["id"], allow_members_to_edit=False)
            elif goal_code == '14':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_14["id"], allow_members_to_edit=False)
            elif goal_code == '15':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_15["id"], allow_members_to_edit=False)
            elif goal_code == '16':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_16["id"], allow_members_to_edit=False)
            elif goal_code == '17':
                item.share(
                    everyone=True, org=True, groups=open_data_group_prod_17["id"], allow_members_to_edit=False)

            # Disable Editing on the Feature Service
            print('disable editing for ' + item.title)
            item_flc = FeatureLayerCollection.fromitem(item)
            update_dict2 = {"capabilities": "Query, Extract"}
            item_flc.manager.update_definition(update_dict2)

        #  Unshare from Staging Group
        #print('unsharing item ' + item.title + " from the staging group")
        # item.unshare(open_data_group["id"])

        print('enabling delete protection for: ' + item.title)
        item.protect(enable=True)

        # Tag as Current
        print('updating item properties for ' + item.title)
        item_properties = dict()
        item_properties["tags"] = item.tags.append('Current')
        item.update(item_properties=item_properties)

        # Mark this item as authoratative
        print('marking item ' + item.title + " as authortative")

        utils_arcgis.set_content_status(
            gis_online_connection, item, authoratative=True)
