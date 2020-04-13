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

    # if s != 'EG_ELC_ACCS':
    #    continue

    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    file_data = 'data/interim/' + release + '/series/Series_' + s + '.txt'

    x = utils.tsv2dictlist(file_ts)
    dim_other = [k for k in x[0].keys() if k not in schema['dim_series'] +
                 schema['dim_geo'] + ['years', 'max_year', 'min_year', 'n_years']]
    ts_keys = utils.subdict_list(
        x, schema['dim_series'] + schema['dim_geo'] + ['max_year'] + dim_other)
    for i in ts_keys:
        i['year'] = int(float(i['max_year']))
        i.pop('max_year')

    y = utils.tsv2dictlist(file_data)
    for i in y:
        i['year'] = int(float(i['timePeriodStart']))
        i.pop('timePeriodStart')

    latest_year = utils.merge_dict_lists(ts_keys,
                                         y,
                                         schema['dim_series'] +
                                         schema['dim_geo'] +
                                         dim_other + ['year'],
                                         schema['dim_series'] +
                                         schema['dim_geo'] +
                                         dim_other + ['year'],
                                         how='left')

    xy = utils.subdict_list(latest_year, ['max_year'], exclude=True)

    outputfile = 'data/interim/' + release + '/latest_data/LatestDataPoints_' + s + '.txt'

    utils.dictList2tsv(xy, outputfile)

    print(f'--finished series {s}')
