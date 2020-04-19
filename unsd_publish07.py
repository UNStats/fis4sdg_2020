import set_release
import set_schema
import utils
import availability

# *******************************************************************
# Obtain latest data point for each available time series
# *******************************************************************

schema = set_schema.set_schema()

release = set_release.set_release()

folder = 'data/raw/' + release
regex = r'Series_(.*?)_RefArea_(.*?).txt'
i_series = 1
i_geo = 2

series_list = availability.available_series(folder, regex, i_series, i_geo)

for s in series_list:

    if s != 'EG_ELC_ACCS':
        continue

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    x = utils.tsv2dictlist(file_ts)

    # Obtain list of unique years included in dataset:

    years_string = utils.subdict_list(x, ['years'])
    years = set()
    for y in years_string:
        years = years.union(
            set(map(str.strip, y['years'][1:-1].split(","))))
    years = list(years)
    years.sort()
    print(years)

    # Identify dimensions that are not:
    # - series dimension
    # - geography dimension
    # - time attributes

    dim_other = [k for k in x[0].keys() if k not in schema['dim_series'] +
                 schema['dim_geo'] + ['years', 'max_year', 'min_year', 'n_years']]

    ts_keys = utils.subdict_list(
        x, schema['dim_series'] +
        schema['dim_geo'] +
        ['years', 'max_year', 'min_year', 'n_years'] +
        dim_other)

    print(f'Length of \'ts_keys\' is: {len(ts_keys)}')
    print(f'Example of \'ts_keys\':\n{ts_keys[0]}')

    # Get Series file (with all the data):
    file_data = 'data/interim/' + release + '/series/Series_' + s + '.txt'
    y = utils.tsv2dictlist(file_data)

    print(y[0])


#     latest_year = utils.merge_dict_lists(ts_keys,
#                                          y,
#                                          schema['dim_series'] +
#                                          schema['dim_geo'] +
#                                          dim_other + ['year'],
#                                          schema['dim_series'] +
#                                          schema['dim_geo'] +
#                                          dim_other + ['year'],
#                                          how='left')
#
#     xy = utils.subdict_list(latest_year, ['max_year'], exclude=True)
#
#     outputfile = 'data/interim/' + release + '/latest_data/LatestDataPoints_' + s + '.txt'
#
#     utils.dictList2tsv(xy, outputfile)
#
#     print(f'--finished series {s}')
