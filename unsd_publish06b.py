import set_release
import set_schema
import utils
import availability
import json

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

filters = []

for s in series_list:

    # if s != 'EG_ELC_ACCS':
    #     continue

    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'

    x = utils.tsv2dictlist(file_ts)
    dim_other = [k for k in x[0].keys() if k not in schema['dim_series'] +
                 schema['dim_geo'] + ['years', 'max_year', 'min_year', 'n_years'] +
                 ['timeCoverage', 'geoInfoUrl'] + 
                 ['cities_code', 'cities_desc', 
                  'observationStatus_code', 'observationStatus_desc',
                  'samplingStations_code','samplingStations_desc']]

    ts_keys = utils.unique_dicts(utils.subdict_list( x, ['series'] + dim_other))

    if len(ts_keys)>1:

        filter_dict = dict()   

        filter_k = [key for key in ts_keys[0].keys() if key.endswith('_code')]
        filter_l = [key for key in ts_keys[0].keys() if key.endswith('_desc')]

        if 'age_desc' in filter_l:
            for d in ts_keys:
                if d['age_code'] == '_U':
                    d['age_desc'] = 'Unknown age' 
        
        views_k = utils.subdict_list(ts_keys, filter_k )
        views_l = utils.subdict_list(ts_keys, filter_l )

        views_labels = []
        
        for view in utils.subdict_list(ts_keys, filter_l ):

            view_label = []
            for i in filter_l:
                view[i].replace('\n', '').replace('\r', '')
                view_label.append(view[i])

            
            views_labels.append('; '.join(view_label))
    
        filter_dict['series'] = s
        filter_dict['filters'] = views_k
        filter_dict['labels'] = views_labels

    else:
        
        filter_dict = dict()   
        filter_dict['series'] = s
        filter_dict['filters'] = None
        filter_dict['labels'] = None
    
    filters.append(filter_dict)

    outputfile = 'data/interim/' + release + \
        '/TS/timeSeriesCat_' + s + '.txt'

    utils.dictList2tsv(ts_keys, outputfile)

    print(f'--finished series {s}/n')

outputfile2 = 'data/interim/' + release + \
    '/TS/views_.json'

import json
with open(outputfile2, 'w') as fout:
    json.dump(filters, fout,  indent=4)