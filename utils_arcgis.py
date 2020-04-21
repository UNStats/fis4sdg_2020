from arcgis.gis import GIS
import sys
import json
import getpass
import os
import utils
import copy
import requests


def connect_to_arcGIS():
    """Open connection to ArcGIS Online Organization"""

    online_username = input('Username: ')
    online_password = getpass.getpass('Password: ')
    online_connection = "https://www.arcgis.com"
    gis_online_connection = GIS(online_connection,
                                online_username,
                                online_password)

    return online_username, gis_online_connection


def open_data_group(gis_online_connection, id):
    """Explore existing open data gruop"""

    open_data_group = gis_online_connection.groups.get(id)
    return (open_data_group)


def cleanup_staging_folder(user_items):
    """ Cleanup staging folder for Open Data (delete everything in the staging folder for Open Data)"""

    if input('Do you want to cleanup your staging folder for Open Data? (y/n)') == 'y':
        if input('Are you sure? (y/n)') == 'y':
            for item in user_items:
                print('deleting item ' + item.title)
                item.delete()
        else:
            print('Cleanup of staging forlder for Open Data was canceled')
    else:
        print('Cleanup of staging forlder for Open Data was canceled')


def build_series_card(g, t, i, s):
    """ Build series metadata card """

    try:
        s_card = dict()
        title = 'Indicator ' + i['reference'] + ': ' + \
            s['description'].replace('%', 'percent')
        s_card['title'] = (title[:250] + '..') if len(title) > 250 else title
        s_card['layer_title'] = s['description'].replace(
            '%', 'percent').replace(',', ' ').replace('/', ' ')

        s_card['snippet'] = s_card['title']

        #s_card['snippet'] = (snippet[:250] + '..') if len(snippet) > 250 else snippet
        s_card['description'] =  \
            '<div style="background-color: #' + g['hex'] + '; color:#fff; padding: 15px">' + \
            '<ul style="list-style: none;">' + \
            '<li><strong> Series Name:</strong> ' + s['description'].replace(',', ' ').replace('/', ' ') + '</li>' + \
            '<li><strong>Series Code:</strong> ' + s['code'] + '</li>' + \
            '<li><strong>Release Version:</strong> ' + s['release'] + '</li>' + \
            '</ul>' + \
            '</div>' + \
            '<div style="background-color: #f4f4f4; padding: 15px">' + \
            '<p> This dataset is the part of the Global SDG Indicator Database compiled ' + \
            'through the UN System in preparation for the Secretary-General\'s annual report on <em>Progress towards the Sustainable Development Goals</em>.' + \
            '</p>' + \
            '<p><strong>Indicator ' + i['reference'] + ': </strong>' + i['descEN'] + \
            '</p>' + \
            '<p><strong>Target ' + t['code'] + ': </strong>' + t['descEN'] + \
            '</p>' + \
            '<p><strong>Goal ' + g['code'] + ': </strong>' + g['descEN'] + \
            '</p>' +  \
            '<p><em>For more information on the compilation methodology of this dataset, ' +\
            ' see <a href="https://unstats.un.org/sdgs/metadata/" target="_blank">https://unstats.un.org/sdgs/metadata/' + \
            '</a></em></p>' + \
            '</div>'

        series_tags = s['tags'][:]
        series_tags.append(s['release'])

        s_card['tags'] = series_tags

        return s_card
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None


def find_online_item(title, owner, gis_online_connection, force_find=True):

    try:

        # Search for this ArcGIS Online Item
        query_string = "title:'{}' AND owner:{}".format(title, owner)
        print('Searching for ' + title)
        # The search() method returns a list of Item objects that match the
        # search criteria
        search_results = gis_online_connection.content.search(query_string)

        if search_results:
            for item in search_results:
                if item['title'] == title:
                    print(' -- Item ' + title + ' found (simple find)')
                    return item

        if force_find:
            user = gis_online_connection.users.get(owner)
            user_items = user.items(folder='Open Data', max_items=800)
            for item in user_items:
                if item['title'] == title:
                    print(' -- Item ' + title + ' found (force find)')
                    return item
            print(' -- Item ' + title + ' not found (force find)')
            return None

        print(' -- Item ' + title + ' not found (simple find)')
        return None

    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None


def generate_renderer_infomation(feature_item,
                                 statistic_field,
                                 layer_info,
                                 color=None):
    try:
        if len(color) == 3:
            color.append(130)  # ---specifies the alpha channel of the color

        visual_params = layer_info['layerInfo']
        definition_item = feature_item.layers[0]

        # get the min/max values
        out_statistics = [{'statisticType': 'max',
                           'onStatisticField': statistic_field,
                           'outStatisticFieldName': statistic_field + '_max'},
                          {'statisticType': 'min',
                           'onStatisticField': statistic_field,
                           'outStatisticFieldName': statistic_field + '_min'}]
        # This fails:
        feature_set = definition_item.query(
            where='1=1', out_statistics=out_statistics)

        max_value = feature_set.features[0].attributes[statistic_field + '_max']
        min_value = feature_set.features[0].attributes[statistic_field + '_min']

        visual_params['drawingInfo']['renderer']['visualVariables'][0]['minDataValue'] = min_value
        visual_params['drawingInfo']['renderer']['visualVariables'][0]['maxDataValue'] = max_value

        visual_params['drawingInfo']['renderer']['authoringInfo']['visualVariables'][0]['minSliderValue'] = min_value
        visual_params['drawingInfo']['renderer']['authoringInfo']['visualVariables'][0]['maxSliderValue'] = max_value

        visual_params['drawingInfo']['renderer']['classBreakInfos'][0]['symbol']['color'] = color
        visual_params['drawingInfo']['renderer']['transparency'] = 25

        definition_update_params = definition_item.properties
        definition_update_params['drawingInfo']['renderer'] = visual_params['drawingInfo']['renderer']
        if 'editingInfo' in definition_update_params:
            del definition_update_params['editingInfo']
        definition_update_params['capabilities'] = 'Query, Extract, Sync'
        print('Update Feature Service Symbology')
        definition_item.manager.update_definition(definition_update_params)

        return
    except:
        print('Unexpected error in generate_renderer_infomation:',
              sys.exc_info()[0])
        return None


def publish_csv(g, t, i, s,
                item_properties,
                thumbnail,
                layer_info,
                gis_online_connection,
                data_dir,
                online_username,
                statistic_field='latest_value',
                property_update_only=False,
                color=[169, 169, 169]):

    # Check if service name is available; if not, update the link
    service_title = s['code'] + '_' + \
        i['reference'].replace('.', '_') + '_' + s['release'].replace('.', '')

    # display(service_title)

    service_title_num = 1

    while not gis_online_connection.content.is_service_name_available(service_name=service_title,
                                                                      service_type='featureService'):
        service_title = s['code'] + '_' + i['reference'].replace('.', '_') + '_' + s['release'].replace('.', '') + \
            '_' + str(service_title_num)
        service_title_num += 1

    # display(service_title_num)

    # csv file to be uploaded:
    file = os.path.join(data_dir, 'Indicator_' +
                        i['reference'].replace('.', '_') + '__Series_' + s['code'] + '.csv')

    print(file)

    if os.path.isfile(file):
        csv_item_properties = copy.deepcopy(item_properties)
        csv_item_properties['name'] = service_title
        csv_item_properties['title'] = service_title
        csv_item_properties['type'] = 'CSV'
        csv_item_properties['url'] = ''

        # display(csv_item_properties)

        # Does this CSV already exist
        csv_item = find_online_item(
            csv_item_properties['title'], online_username, gis_online_connection)

        if csv_item is None:
            print('Adding CSV File to ArcGIS Online....')

            # display(gis_online_connection)
            # display(thumbnail)

            csv_item = gis_online_connection.content.add(item_properties=csv_item_properties,
                                                         thumbnail=thumbnail,
                                                         data=file)

            if csv_item is None:
                return None

            print('Analyze Feature Service....')
            publish_parameters = analyze_csv(
                csv_item['id'], gis_online_connection)
            if publish_parameters is None:
                return None
            else:
                publish_parameters['name'] = csv_item_properties['title']
                publish_parameters['layerInfo']['name'] = csv_item_properties['layer_title']
                print('Publishing Feature Service....')
                csv_lyr = csv_item.publish(
                    publish_parameters=publish_parameters, overwrite=True)

                # Update the layer infomation with a basic rendering based on the Latest Value
                # use the hex color from the SDG Metadata for the symbol color

                print('.......call generate renderer within publish_csv')
                generate_renderer_infomation(feature_item=csv_lyr,
                                             statistic_field=statistic_field,
                                             layer_info=layer_info,
                                             color=color)

        else:
            # Update the Data file for the CSV File
            csv_item.update(item_properties=csv_item_properties,
                            thumbnail=thumbnail, data=file)
            # Find the Feature Service and update the properties
            csv_lyr = find_online_item(
                csv_item_properties['title'], online_username, gis_online_connection)

        # Move to the Open Data Folder
        if csv_item['ownerFolder'] is None:
            print('Moving CSV to Open Data Folder')
            csv_item.move('Open Data SDG' + g['code'].zfill(2))

        if csv_lyr is not None:
            print('Updating Feature Service metadata....')
            csv_lyr.update(item_properties=item_properties,
                           thumbnail=thumbnail)

            if csv_lyr['ownerFolder'] is None:
                print('Moving Feature Service to Open Data Folder')
                csv_lyr.move('Open Data SDG' + g['code'].zfill(2))

            return csv_lyr
        else:
            return None
    else:
        return None


def analyze_csv(item_id, gis_online_connection):
    try:
        sharing_url = gis_online_connection._url + \
            '/sharing/rest/content/features/analyze'
        analyze_params = {'f': 'json',
                          'token': gis_online_connection._con.token,
                          'sourceLocale': 'en-us',
                          'filetype': 'csv',
                          'itemid': item_id}
        r = requests.post(sharing_url, data=analyze_params)
        analyze_json_data = json.loads(r.content.decode('UTF-8'))
        for field in analyze_json_data['publishParameters']['layerInfo']['fields']:
            field['alias'] = set_field_alias(field['name'])

            # display(field['name'])
            # display(field['type'])
            # display(field['sqlType'])
            # print('---')

            # IndicatorCode is coming in as a date Field make the correct
            if field['name'] == 'indicator_reference':
                field['type'] = 'esriFieldTypeString'
                field['sqlType'] = 'sqlTypeNVarchar'

            if field['name'] == 'target_code':
                field['type'] = 'esriFieldTypeString'
                field['sqlType'] = 'sqlTypeNVarchar'

            if field['name'] == 'min_year':
                field['type'] = 'esriFieldTypeInteger'
                field['sqlType'] = 'sqlTypeInt'

            if field['name'] == 'max_year':
                field['type'] = 'esriFieldTypeInteger'
                field['sqlType'] = 'sqlTypeInt'

            if field['name'] == 'n_years':
                field['type'] = 'esriFieldTypeInteger'
                field['sqlType'] = 'sqlTypeInt'

            if field['name'] == 'valueDetails':
                field['type'] = 'esriFieldTypeString'
                field['sqlType'] = 'sqlTypeNVarchar'

            elif field['name'].startswith('value'):
                field['type'] = 'esriFieldTypeDouble'
                field['sqlType'] = 'sqlTypeFloat'

        # set up some of the layer information for display
        analyze_json_data['publishParameters']['layerInfo']['displayField'] = 'geoAreaName'
        return analyze_json_data['publishParameters']
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None


def set_field_alias(field_name):

    if field_name == 'goal_code':
        return 'Goal Code'
    if field_name == 'goal_labelEN':
        return 'Goal Label'
    if field_name == 'goal_descEN':
        return 'Goal Description '
    if field_name == 'target_code':
        return 'Target Code'
    if field_name == 'target_descEN':
        return 'Target Description'
    if field_name == 'indicator_code':
        return 'Indicator Code'
    if field_name == 'indicator_reference':
        return 'Indicator Reference'
    if field_name == 'indicator_tier':
        return 'Tier'
    if field_name == 'indicator_custodians':
        return 'Custodian Agency'
    if field_name == 'indicator_descEN':
        return 'Indicator Description'
    if field_name == 'series_release':
        return 'Series Release'
    if field_name == 'series_tags':
        return 'Tags'
    if field_name == 'series':
        return 'Series Code'
    if field_name == 'seriesDescription':
        return 'Series Description'
    if field_name == 'geoAreaCode':
        return 'Geographic Area Code'
    if field_name == 'geoAreaName':
        return 'Geographic Area Name'
    if field_name == 'level':
        return 'Geographic Area Level'
    if field_name == 'parentCode':
        return 'Parent Geographic Area Code'
    if field_name == 'parentName':
        return 'Parent Geographic Area Name'
    if field_name == 'type':
        return 'Geographic Area Type'
    if field_name == 'ISO3':
        return 'ISO Code'
    if field_name == 'UN_Member':
        return 'Is UN Member'
    if field_name == 'Country_Profile':
        return 'Has Country Proile'
    if field_name == 'years':
        return 'Available Years'
    if field_name == 'min_year':
        return 'Earliest Year Available'
    if field_name == 'max_year':
        return 'Latest Year Available'
    if field_name == 'n_years':
        return 'Number of Years Available'
    if field_name == 'unitsCode':
        return 'Measurement Unit Code'
    if field_name == 'unitsDesc':
        return 'Measurement Unit Description'
    if field_name == 'reportingTypeCode':
        return 'Reporting Type Code'
    if field_name == 'reportingTypeDesc':
        return 'Reporting Type Description'
    if field_name == 'basePeriod':
        return 'Base Period'
    if field_name == 'valueDetails':
        return 'Value Details'
    if field_name == 'footnotes':
        return 'Footnotes'
    if field_name == 'sources':
        return 'Sources'
    if field_name == 'timeDetails':
        return 'Time Period Details'
    if field_name == 'nature':
        return 'Nature'
    else:
        return utils.camel_case_split(field_name.replace('_', ' ')).replace(' Desc', ' Description').title()


def update_item_categories(item, goal, target, gis_online_connection):
    update_url = gis_online_connection._url + "/sharing/rest/content/updateItems"
    items = [{item["id"]:{"categories": [
        "/Categories/Goal " + str(goal) + "/Target " + str(target)]}}]
    update_params = {'f': 'json',
                     'token': gis_online_connection._con.token,
                     'items': json.dumps(items)}
    r = requests.post(update_url, data=update_params)
    update_json_data = json.loads(r.content.decode("UTF-8"))
    print(update_json_data)
