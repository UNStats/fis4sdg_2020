import set_release
import availability
import utils
import sdg_api
import urllib3
import copy
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# *******************************************************************
# Add sdmx codes and description of coded concepts in each dataset
# Remove brackets and quotes from footnotes field
# Eliminate "NA" and "NV" values
# Extract numeric part of non-numeric values (e.g., "<2.4" -> 2.4)
# *******************************************************************

release = set_release.set_release()

folder = 'data/raw/'+release
regex = r'Series_(.*?)_RefArea_(.*?).txt'
i_series = 1
i_geo = 2

catalog = availability.available_geo_by_series(folder, regex, i_series, i_geo)

geo_tree = utils.tsv2dictlist('data/geography/geo_tree.txt')


# read dataset:
for entry in catalog:

    series = entry['seriesCode']

    # if series[0:2] != 'AG':
    #    continue

    codes = sdg_api.series_code_lists(series, release)

    concepts = [x['concept'] for x in codes]

    series_data = []

    for geo in entry['geoAreaCodes']:

        # if geo not in ['426', '410']:
        #    continue

        file = folder + '/Series_' + series + '_RefArea_' + geo + '.txt'

        dataset = utils.tsv2dictlist(file, encoding='latin2')

        colNames = [utils.camel_case(x) for x in dataset[0].keys()]

        new_dataset = copy.deepcopy(dataset)

        # Remove brackets and single quotes that are wrapping footnote field,
        # as well as new line characters within any field:
        for r in new_dataset:
            fn = re.search(r'\[\'(.*?)\'\]', r['footnotes'])
            if fn:
                r['footnotes'] = fn.group(1)

            for k, v in r.items():
                r[k] = v.replace('\n', ' ').replace('\t', ' ')

        # Transcoding:
        for k in dataset[0].keys():

            if utils.camel_case(k) in concepts:

                codelist_k = copy.deepcopy(utils.select_dict(
                    codes, {'concept': utils.camel_case(k)})[0]['codes'])

                # Rename the keys of codelist_k dictionary:
                for code in codelist_k:
                    code[utils.camel_case(k)+'_code'] = code.pop('sdmx')
                    code[utils.camel_case(k)+'_desc'] = code.pop('description')
                    code['x'] = code.pop('code')

                new_dataset = utils.merge_dict_lists(
                    new_dataset, codelist_k, [k], ['x'], how='left')

                new_dataset = utils.subdict_list(
                    new_dataset, [k, 'x'], exclude=True)

        series_data = series_data + new_dataset

    # Remove records where value is NA:
    series_data = utils.select_dict(series_data, {'value': 'NA'}, keep=False)

    # Remove records where value is NV:
    # In some instaneces, FAO reports: "NV = The figure has not been validated by the national statistical
    # system for global reporting."
    series_data = utils.select_dict(series_data, {'value': 'NV'}, keep=False)

    # Remove records where value is nan (e.g., in series AG_FPA_COMM):
    series_data = utils.select_dict(series_data, {'value': 'nan'}, keep=False)

    # Remove records where value is nan (e.g., in series AG_FPA_COMM):
    series_data = utils.select_dict(series_data, {'value': 'NaN'}, keep=False)
    # Rename 'timePeriodStart' to 'timePeriod' and replace non-numeric values
    # (i.e., truncated values) with its numeric part, and store the full,
    # non-numeric value as a "value detail" column

    for r in series_data:

        r['timePeriod'] = int(float(r.pop('timePeriodStart')))

        try:
            r['value_detail'] = None
            r['value'] = float(r['value'])
            r.pop('valueType')
        except ValueError:
            r['value_detail'] = copy.deepcopy(r['value'])
            r['value'] = utils.numeric_part(r['value'])
            r.pop('valueType')

        try:
            r['lowerBound_detail'] = None
            r['lowerBound'] = float(r['lowerBound'])
        except ValueError:
            r['lowerBound_detail'] = copy.deepcopy(r['lowerBound'])
            r['lowerBound'] = utils.numeric_part(r['lowerBound'])

        try:
            r['upperBound_detail'] = None
            r['upperBound'] = float(r['upperBound'])
        except ValueError:
            r['upperBound_detail'] = copy.deepcopy(r['upperBound'])
            r['upperBound'] = utils.numeric_part(r['upperBound'])

    # Join geographic coordinates (XY) and other geo attributes
    series_data = utils.merge_dict_lists(series_data, geo_tree, ['geoAreaCode'], [
        'geoAreaCode'], how='left')

    file_out = 'data/interim/' + release + '/series/Series_' + series + '.txt'

    utils.dictList2tsv(series_data, file_out)

    print(f'--finished processing file {file_out}')
