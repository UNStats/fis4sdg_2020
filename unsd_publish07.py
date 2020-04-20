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

    print(f'--started processing series {s}')

    # if s != 'AG_PRD_ORTIND':
    #     continue

    # Get Time Series file (with time series keys):
    file_ts = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'
    x = utils.tsv2dictlist(file_ts)

    # Get Series file (with all the data):
    file_data = 'data/interim/' + release + '/series/Series_' + s + '.txt'
    y = utils.tsv2dictlist(file_data)

    # Determine whether UP/LB are present:

    up = utils.unique_dicts(utils.subdict_list(y, ['upperBound']))
    if len(up) == 1 and up[0]['upperBound'] == '':
        has_up = False
    else:
        has_up = True

    lb = utils.unique_dicts(utils.subdict_list(y, ['lowerBound']))
    if len(lb) == 1 and lb[0]['lowerBound'] == '':
        has_lb = False
    else:
        has_lb = True

    # Select unique time periods among all records:
    temp = set()
    timePeriods = []

    for ts in x:

        y_list = [int(float(x)) for x in [x.strip()
                                          for x in ts['years'][1:-1].split(",")]]

        temp = temp.union(set(y_list))

    timePeriods = list(temp)
    timePeriods.sort()

    # print(timePeriods)

    data_new = []

    for ts in x:

        # print('====================')
        # print(ts)
        # print('====================')

        # select records in y corresponding to timeseries ts:

        exclude_keys = ['level',
                        'parentCode',
                        'parentName',
                        'type',
                        'X',
                        'Y',
                        'ISO3',
                        'UN_Member',
                        'Country_Profile',
                        'years',
                        'min_year',
                        'max_year',
                        'n_years',
                        ]
        ts_keys = {k: ts[k] for k in ts.keys() if k not in exclude_keys}

        slice_data_wide = ts.copy()
        slice_keys = slice_data_wide.keys()

        data = utils.select_dict(y, ts_keys, keep=True)

        slice_footnotes = []
        slice_sources = []
        slice_timeDetails = []
        slice_nature = []
        slice_years = []
        slice_unitsCode = []
        slice_unitsDesc = []
        slice_unitMultiplier = []
        slice_reportingTypeCode = []
        slice_reportingTypeDesc = []
        slice_basePeriod = []
        slice_valueDetails = []
        if has_lb:
            slice_lowerBoundDetails = []
        if has_up:
            slice_upperBoundDetails = []

        for r in data:
            if 'footnotes' in r.keys():
                slice_footnotes.append(r['footnotes'])
            if 'source' in r.keys():
                slice_sources.append(r['source'])
            if 'time_detail' in r.keys():
                slice_timeDetails.append(r['time_detail'])
            if 'nature_code' in r.keys():
                slice_nature.append(
                    r['nature_code'] + ': ' + r['nature_desc'])
            if 'timePeriod' in r.keys():
                slice_years.append(r['timePeriod'])
            if 'units_code' in r.keys():
                slice_unitsCode.append(r['units_code'])
            if 'units_desc' in r.keys():
                slice_unitsDesc.append(r['units_desc'])
            if 'reportingType_code' in r.keys():
                slice_reportingTypeCode.append(
                    r['reportingType_code'])
            if 'reportingType_desc' in r.keys():
                slice_reportingTypeDesc.append(
                    r['reportingType_desc'])
            if 'basePeriod' in r.keys():
                slice_basePeriod.append(r['basePeriod'])
            if 'value_detail' in r.keys() and r['value_detail'] != '':
                slice_valueDetails.append(r['value_detail'])
            if has_lb:
                if 'lowerBound_detail' in r.keys() and r['lowerBound_detail'] != '' and r['lowerBound_detail'] != 'NA':
                    slice_lowerBoundDetails.append(r['lowerBound_detail'])
            if has_up:
                if 'upperBound_detail' in r.keys() and r['upperBound_detail'] != '' and r['upperBound_detail'] != 'NA':
                    slice_upperBoundDetails.append(r['upperBound_detail'])

        slice_footnotes = list(set(slice_footnotes))
        slice_sources = list(set(slice_sources))
        slice_timeDetails = list(set(slice_timeDetails))
        slice_nature = list(set(slice_nature))
        slice_basePeriod = list(set(slice_basePeriod))
        slice_valueDetails = list(set(slice_valueDetails))
        if has_lb:
            slice_upperBoundDetails = list(set(slice_upperBoundDetails))
            # print('----')
            # print(slice_upperBoundDetails)
            # print('----')

        if has_up:
            slice_lowerBoundDetails = list(set(slice_lowerBoundDetails))

        slice_unitsCode = ' // '.join(list(set(slice_unitsCode)))
        slice_unitsDesc = ' // '.join(list(set(slice_unitsDesc)))
        slice_reportingTypeCode = ' // '.join(
            list(set(slice_reportingTypeCode)))
        slice_reportingTypeDesc = ' // '.join(
            list(set(slice_reportingTypeDesc)))

        slice_data_wide['unitsCode'] = slice_unitsCode
        slice_data_wide['unitsDesc'] = slice_unitsDesc
        slice_data_wide['reportingTypeCode'] = slice_reportingTypeCode
        slice_data_wide['reportingTypeDesc'] = slice_reportingTypeDesc

        for yy in timePeriods:

            slice_data_wide['value_' + str(yy)] = None

            if has_lb:
                slice_data_wide['lowerbound_' + str(yy)] = None

            if has_up:
                slice_data_wide['upperbound_' + str(yy)] = None

        # ======================================================

        for yy in slice_years:

            slice_data_yy = utils.subdict_list(utils.select_dict(
                data, {'timePeriod': yy}, keep=True),
                ['value', 'upperBound', 'lowerBound'])

            if len(slice_data_yy) == 1:
                slice_data_wide['value_'+yy] = slice_data_yy[0]['value']
                if has_lb:
                    slice_data_wide['lowerbound_' +
                                    yy] = slice_data_yy[0]['lowerBound']
                if has_up:
                    slice_data_wide['upperbound_' +
                                    yy] = slice_data_yy[0]['upperBound']

                if yy == slice_data_wide['max_year']:
                    latest_value = slice_data_yy[0]['value']

        slice_data_wide['latest_value'] = latest_value

        # ======================================================

        slice_basePeriod_join = []
        counter = 0
        for fn in slice_basePeriod:
            counter += 1
            fn_years = []
            for r in data:
                if 'basePeriod' in r.keys():
                    if fn == r['basePeriod']:
                        fn_years.append(r['timePeriod'])
            if fn:
                if len(slice_basePeriod) > 1:
                    slice_basePeriod_join.append(
                        '['+utils.year_intervals(fn_years)+']: ' + fn)
                if len(slice_basePeriod) == 1:
                    slice_basePeriod_join.append(fn)

        slice_basePeriod_join.sort()
        slice_basePeriod_join = ' // '.join(
            slice_basePeriod_join)

        slice_data_wide['basePeriod'] = slice_basePeriod_join

        # ----------------------------

        slice_valueDetails_join = []
        counter = 0
        for fn in slice_valueDetails:
            counter += 1
            fn_years = []
            for r in data:
                if 'value_detail' in r.keys():
                    if fn == r['value_detail']:
                        fn_years.append(r['timePeriod'])
            if fn:
                if len(slice_valueDetails) > 1:
                    slice_valueDetails_join.append(
                        '['+utils.year_intervals(fn_years)+']: ' + fn)
                if len(slice_valueDetails) == 1:
                    slice_valueDetails_join.append(fn)

        slice_valueDetails_join.sort()
        slice_valueDetails_join = ' // '.join(
            slice_valueDetails_join)

        slice_data_wide['valueDetails'] = slice_valueDetails_join

        # ----------------------------
        if has_lb:
            slice_lowerBoundDetails_join = []
            counter = 0
            for fn in slice_lowerBoundDetails:
                counter += 1
                fn_years = []
                for r in data:
                    if 'lowerBound_detail' in r.keys():
                        if fn == r['lowerBound_detail']:
                            fn_years.append(r['timePeriod'])
                if fn:
                    if len(slice_lowerBoundDetails) > 1:
                        slice_lowerBoundDetails_join.append(
                            '['+utils.year_intervals(fn_years)+']: ' + fn)

                    if len(slice_lowerBoundDetails) == 1:
                        slice_lowerBoundDetails_join.append(fn)

            slice_lowerBoundDetails_join.sort()
            slice_lowerBoundDetails_join = ' // '.join(
                slice_lowerBoundDetails_join)

            slice_data_wide['lowerBoundDetails'] = slice_lowerBoundDetails_join

        # ----------------------------
        if has_up:
            slice_upperBoundDetails_join = []
            counter = 0
            for fn in slice_upperBoundDetails:
                counter += 1
                fn_years = []
                for r in data:
                    if 'upperBound_detail' in r.keys():
                        if fn == r['upperBound_detail']:
                            fn_years.append(r['timePeriod'])
                if fn:
                    if len(slice_upperBoundDetails) > 1:
                        slice_upperBoundDetails_join.append(
                            '['+utils.year_intervals(fn_years)+']: ' + fn)
                    if len(slice_upperBoundDetails) == 1:
                        slice_upperBoundDetails_join.append(fn)

            slice_upperBoundDetails_join.sort()
            slice_upperBoundDetails_join = ' // '.join(
                slice_upperBoundDetails_join)

            slice_data_wide['upperBoundDetails'] = slice_upperBoundDetails_join

        # ----------------------------

        slice_footnote_join = []
        counter = 0
        for fn in slice_footnotes:
            counter += 1
            fn_years = []
            for r in data:
                if 'footnotes' in r.keys():
                    if fn == r['footnotes']:
                        fn_years.append(r['timePeriod'])
            if fn:
                if len(slice_footnotes) > 1:
                    slice_footnote_join.append(
                        '['+utils.year_intervals(fn_years)+']: ' + fn)
                if len(slice_footnotes) == 1:
                    slice_footnote_join.append(fn)

        slice_footnote_join.sort()
        slice_footnote_join = ' // '.join(
            slice_footnote_join)

        slice_data_wide['footnotes'] = slice_footnote_join

        # -----------------------

        slice_sources_join = []
        counter = 0

        for src in slice_sources:
            counter += 1
            src_years = []
            for r in data:
                if src == r['source']:
                    src_years.append(r['timePeriod'])

            if src:
                if len(slice_sources) > 1:
                    slice_sources_join.append(
                        '['+utils.year_intervals(src_years)+']: ' + src)

                if len(slice_sources) == 1:
                    slice_sources_join.append(src)

        slice_sources_join.sort()
        slice_sources_join = ' // '.join(slice_sources_join)

        slice_data_wide['sources'] = slice_sources_join

        # ------------------------

        slice_timeDetail_join = []
        counter = 0
        for td in slice_timeDetails:
            counter += 1
            td_years = []
            for r in data:
                if td == r['time_detail']:
                    td_years.append(r['timePeriod'])
            if td:
                if len(slice_timeDetails) > 1:
                    slice_timeDetail_join.append(
                        '['+utils.year_intervals(td_years)+']: ' + td)
                if len(slice_timeDetails) == 1:
                    slice_timeDetail_join.append(td)

        slice_timeDetail_join.sort()
        slice_timeDetail_join = ' // '.join(
            slice_timeDetail_join)

        slice_data_wide['timeDetails'] = slice_timeDetail_join

        # ------------------------

        slice_nature_join = []
        counter = 0
        for n in slice_nature:
            counter += 1
            n_years = []
            for r in data:
                if n == r['nature_code'] + ': ' + r['nature_desc']:
                    n_years.append(r['timePeriod'])
            if n:
                if len(slice_nature) > 1:
                    slice_nature_join.append(
                        '['+utils.year_intervals(n_years)+']: ' + n)
                if len(slice_nature) == 1:
                    slice_nature_join.append(n)

        slice_nature_join.sort()

        slice_nature_join = ' // '.join(slice_nature_join)

        slice_data_wide['nature'] = slice_nature_join

        data_new.append(slice_data_wide)

    file_out = 'data/interim/' + release + '/pivot/PivotSeries_' + s + '.txt'

    # print(data_new)

    utils.dictList2tsv(data_new, file_out)

    print(f'--finished processing file {file_out}')
