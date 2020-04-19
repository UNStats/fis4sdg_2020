import os
import re
import utils
import set_schema


def available_series_areas(folder, regex, i_series, i_geo):
    '''Catalog of available series-area datasets
        - <folder>: the directory in which to search for dataset files
        - <regex>: regular expression establishing how to find 
                   series and refArea codes within the file name
        - <i_series>: position of the group that contains the series code
                      within the regex
        - <i_geo>: position of the group that contains the refARea code
                   within the regex

        Example: 
            folder = 'data/raw/2019.Q4.G.01/'
            regex = r'Series_(.*?)_RefArea_(.*?).txt'
            i_series = 1
            i_geo = 2

            available_series_areas(folder, regex, i_series, i_geo)


    '''
    files = os.listdir(folder)

    series_area = []

    for f in files:

        d = dict()

        search_results = re.search(regex, f)
        d['seriesCode'] = search_results.group(i_series)
        d['geoAreaCode'] = search_results.group(i_geo)

        series_area.append(d)

    return series_area


def available_series_by_geo(folder, regex, i_series, i_geo):
    '''Catalog of available series for each geographic area.
        - <folder>: the directory in which to search for dataset files
        - <regex>: regular expression establishing how to find 
                   series and refArea codes within the file name
        - <i_series>: position of the group that contains the series code
                      within the regex
        - <i_geo>: position of the group that contains the refARea code
                   within the regex

        Example: 
            folder = 'data/raw/2019.Q4.G.01/'
            regex = r'Series_(.*?)_RefArea_(.*?).txt'
            i_series = 1
            i_geo = 2
    '''

    series_area = available_series_areas(folder, regex, i_series, i_geo)

    areas = utils.unique_dicts(
        utils.subdict_list(series_area, ['geoAreaCode']))

    for g in areas:
        g['series'] = []
        for sa in series_area:
            if g['geoAreaCode'] == sa['geoAreaCode']:
                g['series'].append(sa['seriesCode'])

    return areas


def available_geo_by_series(folder, regex, i_series, i_geo):
    '''Catalog of geographic areas that have data available for each series.
        - <folder>: the directory in which to search for dataset files
        - <regex>: regular expression establishing how to find 
                   series and refArea codes within the file name
        - <i_series>: position of the group that contains the series code
                      within the regex
        - <i_geo>: position of the group that contains the refARea code
                   within the regex

        Example: 
            folder = 'data/raw/2019.Q4.G.01/'
            regex = r'Series_(.*?)_RefArea_(.*?).txt'
            i_series = 1
            i_geo = 2
    '''

    series_area = available_series_areas(folder, regex, i_series, i_geo)

    series = utils.unique_dicts(
        utils.subdict_list(series_area, ['seriesCode']))

    for s in series:
        s['geoAreaCodes'] = []
        for sa in series_area:
            if s['seriesCode'] == sa['seriesCode']:
                s['geoAreaCodes'].append(sa['geoAreaCode'])

    return series


def available_geo(folder, regex, i_series, i_geo):
    '''Catalog of available areas
        - <folder>: the directory in which to search for dataset files
        - <regex>: regular expression establishing how to find 
                   series and refArea codes within the file name
        - <i_series>: position of the group that contains the series code
                      within the regex
        - <i_geo>: position of the group that contains the refARea code
                   within the regex

        Example: 
            folder = 'data/raw/2019.Q4.G.01/'
            regex = r'Series_(.*?)_RefArea_(.*?).txt'
            i_series = 1
            i_geo = 2
    '''
    series_area = available_series_areas(folder, regex, i_series, i_geo)

    areas = utils.unique_dicts(
        utils.subdict_list(series_area, ['geoAreaCode']))

    return [x['geoAreaCode'] for x in areas]


def available_series(folder, regex, i_series, i_geo):
    '''Catalog of available series
        - <folder>: the directory in which to search for dataset files
        - <regex>: regular expression establishing how to find 
                   series and refArea codes within the file name
        - <i_series>: position of the group that contains the series code
                      within the regex
        - <i_geo>: position of the group that contains the refARea code
                   within the regex

        Example: 
            folder = 'data/raw/2019.Q4.G.01/'
            regex = r'Series_(.*?)_RefArea_(.*?).txt'
            i_series = 1
            i_geo = 2
    '''
    series_area = available_series_areas(folder, regex, i_series, i_geo)

    series = utils.unique_dicts(
        utils.subdict_list(series_area, ['seriesCode']))

    return [x['seriesCode'] for x in series]


def available_time_series(series, release):
    ''' Obtain the available time series that exist for each
        data series.
    '''

    schema = set_schema.set_schema()

    file = 'data/interim/' + release + '/series/Series_' + series + '.txt'

    x = utils.tsv2dictlist(file)

    dim_other = [k for k in x[0].keys() if k not in schema['dim_series'] + schema['dim_geo'] +
                 schema['dim_time'] + schema['measure'] + schema['attr_main'] + schema['attr_measure']]

    ts_keys = utils.unique_dicts(utils.subdict_list(
        x, schema['dim_series'] + schema['dim_geo'] + dim_other))

    for ts_k in ts_keys:

        ts = utils.select_dict(x, ts_k)

        years = [int(float(i['timePeriod'])) for i in ts]

        ts_k['years'] = years
        ts_k['min_year'] = min(years)
        ts_k['max_year'] = max(years)
        ts_k['n_years'] = len(years)

    return ts_keys
