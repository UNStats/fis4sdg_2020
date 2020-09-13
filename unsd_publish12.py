import availability
import set_schema
import utils
import set_release
import copy

release = set_release.set_release()


# *******************************************************************
# Create country-profile builder
# *******************************************************************

# Read list of hub items for each series (created in Script unsd_publish11.py):
hub_items = utils.tsv2dictlist('data/external/hub_items_' + release + '.txt')

# Read metadata file:
sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

temp_builder = []

# Add Goal, Target and Indicator to each series:
for hub_item in hub_items:

    s = hub_item['series']
    g = hub_item['goal']
    h = hub_item['id']

    for m_g in sdg_meta:
        if int(m_g['code']) != int(g):
            continue
        g_code = m_g['code']

        for m_t in m_g['targets']:
            t_code = m_t['code']

            for m_i in m_t['indicators']:
                i_code = m_i['code']
                i_ref = m_i['reference']

                for m_s in m_i['series']:

                    if m_s['code'] != s:
                        continue
                    s_code = s

                    d = {}
                    d['goal'] = g_code
                    d['target'] = t_code
                    d['indicator_code'] = i_code
                    d['indicator_ref'] = i_ref
                    d['series'] = s_code
                    d['hub_id'] = h

                    temp_builder.append(d)

# Obtain the list of all dimensions used across all series
schema = set_schema.set_schema()

ts_columns = ['timeCoverage', 'geoInfoUrl',
              'years', 'min_year', 'max_year', 'n_years']

all_dimensions = []
for i in temp_builder:
    s = i['series']

    # if s != 'IS_RDP_PFVOL':
    #    continue

    # if s[0:2] != 'AG':
    #    continue

    # print(f'--started processing series {s}')

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)

    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns + schema['dim_geo']+schema['attr_main']]

    all_dimensions = list(set(all_dimensions) | set(dimensions_ts))


# Sort the list of dimensions, putting the most frequent ones at the beginning:

counts = {}
for i in all_dimensions:
    counts[i] = 10000

for i in temp_builder:
    s = i['series']
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)
    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns + schema['attr_main']]
    for j in dimensions_ts:
        counts[j] = counts[j] - 1

all_dimensions = [x for _, x in sorted(
    zip(list(counts.values()), list(counts.keys())), reverse=False)]

# print(all_dimensions)

# ---------------------------------------------

country_profiles_builder = []

for i in temp_builder:

    i['target'] = "'" + i['target']

    s = i['series']

    # if s != 'IS_RDP_PFVOL':
    #     continue

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)

    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns + schema['attr_main']]

    x = utils.unique_dicts(
        utils.subdict_list(
            utils.select_dict(
                data, {'type': 'Country', 'Country_Profile': '1'}),
            schema['dim_series'] + ['geoAreaCode', 'geoAreaName'] + ['years', 'min_year', 'max_year', 'n_years'] + dimensions_ts))

    y = utils.unique_dicts(utils.subdict_list(
        x, schema['dim_series'] + dimensions_ts))

    for j in y:

        select_ts = {}
        for t in dimensions_ts:
            select_ts[t] = j[t]

        z = utils.select_dict(
            x, select_ts)

        min_year = []
        max_year = []
        n_years = []

        for k in z:
            min_year.append(int(k['min_year']))
            max_year.append(int(k['max_year']))
            n_years.append(int(k['n_years']))

        d = copy.deepcopy(i)

        d['n_countries'] = len(z)
        d['series'] = j['series']
        d['seriesDescription'] = j['seriesDescription']
        d['min_year'] = min(min_year)
        d['max_year'] = max(max_year)
        d['min_n_years'] = min(n_years)
        d['max_n_years'] = max(n_years)
        d['n_disaggregations'] = len(dimensions_ts) / 2

        for l in all_dimensions:
            if l in j.keys():
                d[l] = j[l]
            else:
                d[l] = None

        country_profiles_builder.append(d)


file_out = 'data/interim/' + release + '/CountryProfileBuilder2.txt'

utils.dictList2tsv(country_profiles_builder, file_out)

print(f'--finished country_profile_builder')
