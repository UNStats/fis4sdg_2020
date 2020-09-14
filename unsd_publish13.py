import set_release
import utils
import json

# Read list of main time series

release = set_release.set_release()

main_ts = utils.tsv2dictlist(
    'data/external/mainTimeSeries_' + release + '.txt')

# Build a ts selector (specify code value for key dimensions of each Time Seires):
ts_selector = []


for i in main_ts:
    s = dict()
    s['goal'] = i['goal']
    s['target'] = i['target']
    s['indicator_code'] = i['indicator_code']
    s['indicator_ref'] = i['indicator_ref']
    s['series'] = i['series']
    s['hub_id'] = i['hub_id']
    s['seriesDescription'] = i['seriesDescription']
    s['ts_description'] = i['TimeSeriesDescription']
    s['ts_unit'] = i['unit']
    s['ts_filter'] = dict()
    for k in [k for k in i.keys() if k.endswith('_code')]:
        if k == 'indicator_code':
            continue
        if i[k] == '':
            continue
        s['ts_filter'][k] = i[k]

    ts_selector.append(s)

# ---------------------------------

profiles_data = []

country_codes = []


for ts in ts_selector:

    # if ts['series'] != 'SN_ITK_DEFC':
    #     continue

    ts_data = utils.select_dict(utils.select_dict(utils.tsv2dictlist(
        'data/processed/' + release +
        '/Indicator_' + ts['indicator_ref'].replace('.', '_') +
        '__Series_' + ts['series'] + '.csv'),
        ts['ts_filter']),
        {'type': 'Country'})

    # print(ts['indicator_ref'].replace('.', '_'))
    # print(ts['series'])

    for r in ts_data:

        #print(r['geoAreaCode'] + ': ' + r['geoAreaName'])

        country_codes.append(r['geoAreaCode'])

        d = dict()
        d['release'] = release
        d['country_code'] = r['geoAreaCode']
        d['country_name'] = r['geoAreaName']
        d['indicator_code'] = r['indicator_code']
        d['indicator_reference'] = r['indicator_reference']
        d['seriesCode'] = r['series']
        d['seriesDescription'] = r['seriesDescription']
        d['timeSeriesTitle'] = ts['ts_description']
        d['timeSeriesUnit'] = ts['ts_unit']
        d['hub'] = ts['hub_id']
        d['dashboard'] = ''
        d['slice_dimensions'] = ts['ts_filter']
        years = r['years'][1:-1].replace(" ", "").split(',')
        d['data_values'] = []
        d['data_years'] = []
        d['data_is_censored'] = []
        d['data_numeric_part'] = []
        for y in years:

            #print(r['value_' + y])
            try:
                d['data_numeric_part'].append(float(r['value_' + y]))
                d['data_values'].append(r['value_' + y])
                # This needs to be double checked:
                d['data_years'].append(int(y))
                # ---------------------------------
                d['data_is_censored'].append(False)
            except ValueError:
                pass

        d['preferred_visualization'] = None

        if len(d['data_years']) > 0:
            profiles_data.append(d)

    country_codes = list(set(country_codes))


# Get list of unique country codes

country_codes.sort(key=float)

for c in country_codes:
    x = utils.select_dict(profiles_data, {'country_code': c}, keep=True)
    file_out = 'data/interim/' + release + \
        '/country_profiles/country_profile_data_' + c + '.json'

    with open(file_out, 'w', encoding="utf-8") as f:
        json.dump(x, f, indent=4)

    print(f'Profile for country {c} has {len(x)} time series')
