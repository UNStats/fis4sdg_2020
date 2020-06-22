import set_release
import metadata
import utils


# *******************************************************************
# Write final csv files to data/processed
# *******************************************************************

release = set_release.set_release()

sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

# print(sdg_meta[0].keys())

for g in sdg_meta:

    # if g['code'] != '1':
    #     continue

    goal_code = g['code']
    goal_labelEN = g['labelEN']
    goal_descEN = g['descEN']

    for t in g['targets']:

        # if t['code'] != '1.1':
        #     continue

        target_code = t['code']
        target_descEN = t['descEN']

        for i in t['indicators']:

            # if i['reference'] != '1.1.1':
            #     continue

            indicator_code = utils.clean_str(i['code'])
            indicator_reference = utils.clean_str(i['reference'])
            indicator_descEN = utils.clean_str(i['descEN'])

            for s in i['series']:

                # Use this for release 2020.Q1.G.01
                # if s['code'] == 'SE_ADT_ACTS':
                #    continue

                series_code = utils.clean_str(s['code'])
                series_description = utils.clean_str(s['description'])
                series_release = utils.clean_str(s['release'])
                series_tags = utils.clean_str(s['tags'])

                file_pivot = 'data/interim/' + release + \
                    '/pivot/PivotSeries_' + series_code + '.txt'

                data = utils.tsv2dictlist(file_pivot)

                new_data = []

                for r in data:

                    d = dict()
                    d['goal_code'] = goal_code
                    d['goal_labelEN'] = goal_labelEN
                    d['goal_descEN'] = goal_descEN
                    d['target_code'] = target_code
                    d['target_descEN'] = target_descEN
                    d['indicator_code'] = indicator_code
                    d['indicator_reference'] = indicator_reference
                    d['indicator_descEN'] = indicator_descEN
                    d['series_release'] = series_release
                    d['series_tags'] = series_tags
                    for k, v in r.items():
                        d[k] = utils.clean_str(v)
                    new_data.append(d)

                # print(new_data[0])

                # Note: ArcGIS only accepts .csv extension (even if it's tab-delimited)
                file_out = 'data/processed/' + release + '/Indicator_' + \
                    indicator_reference.replace(
                        '.', '_') + '__Series_' + series_code + '.csv'

                utils.dictList2csv(new_data, file_out)

                print(f'--finished processing file {file_out}')
