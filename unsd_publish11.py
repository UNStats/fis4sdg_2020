import availability
import set_schema
import utils
import set_release

release = set_release.set_release()


# *******************************************************************
# Create country-profile builder
# *******************************************************************

schema = set_schema.set_schema()
ts_columns = ['timeCoverage', 'geoInfoUrl',
              'years', 'min_year', 'max_year', 'n_years']


folder = 'data/raw/' + release
regex = r'Series_(.*?)_RefArea_(.*?).txt'
i_series = 1
i_geo = 2

series_list = availability.available_series(folder, regex, i_series, i_geo)

all_dimensions = []

for s in series_list:

    # if s != 'IS_RDP_PFVOL':
    #    continue

    # if s[0:2] != 'AG':
    #    continue

    # print(f'--started processing series {s}')

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)

    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns]

    all_dimensions = list(set(all_dimensions) | set(dimensions_ts))

counts = {}
for i in all_dimensions:
    counts[i] = 0

for s in series_list:
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)
    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns]
    for i in dimensions_ts:
        counts[i] = counts[i] + 1

all_dimensions = [x for _, x in sorted(
    zip(list(counts.values()), list(counts.keys())), reverse=True)]

# ---------------------------------

country_profile_builder = []

for s in series_list:

    # if s != 'IS_RDP_PFVOL':
    #     continue

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    data = utils.tsv2dictlist(file_ts)

    dimensions_ts = [x for x in data[0].keys(
    ) if x not in schema['dim_series'] + schema['dim_geo'] + ts_columns]

    # List of unique countries:
    '''
    series	seriesDescription	geoAreaCode	geoAreaName	level	parentCode	parentName
    type	X	Y	ISO3	UN_Member	Country_Profile	timeCoverage	geoInfoUrl
    age_code	age_desc	sex_code	sex_desc	years	min_year	max_year	n_years
    '''

    x = utils.unique_dicts(
        utils.subdict_list(
            utils.select_dict(
                data, {'type': 'Country', 'Country_Profile': '1'}),
            schema['dim_series'] + ['geoAreaCode', 'geoAreaName'] + ['years', 'min_year', 'max_year', 'n_years'] + dimensions_ts))

    y = utils.unique_dicts(utils.subdict_list(
        x, schema['dim_series'] + dimensions_ts))

    for i in y:

        select_ts = {}
        for t in dimensions_ts:
            select_ts[t] = i[t]

        z = utils.select_dict(
            x, select_ts)

        min_year = []
        max_year = []
        n_years = []

        for j in z:
            min_year.append(int(j['min_year']))
            max_year.append(int(j['max_year']))
            n_years.append(int(j['n_years']))

        d = {}
        d['n_countries'] = len(z)
        d['series'] = i['series']
        d['seriesDescription'] = i['seriesDescription']
        d['min_year'] = min(min_year)
        d['max_year'] = max(max_year)
        d['min_n_years'] = min(n_years)
        d['max_n_years'] = max(n_years)
        d['n_disaggregations'] = len(dimensions_ts) / 2

        for k in all_dimensions:
            if k in i.keys():
                d[k] = i[k]
            else:
                d[k] = None
        country_profile_builder.append(d)


file_out = 'data/interim/' + release + '/CountryProfileBuilder.txt'

utils.dictList2tsv(country_profile_builder, file_out)

print(f'--finished country_profile_builder')
