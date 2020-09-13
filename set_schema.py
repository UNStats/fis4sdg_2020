def set_schema():

    schema = dict()

    schema['dim_series'] = ['series', 'seriesDescription']

    schema['dim_geo'] = ['geoAreaCode', 'geoAreaName',
                         'level', 'parentCode', 'parentName', 'type', 'X', 'Y',
                         'ISO3', 'UN_Member', 'Country_Profile']

    schema['dim_time'] = ['timePeriod', 'time_detail']

    schema['measure'] = ['value',
                         'upperBound',
                         'lowerBound']

    schema['attr_main'] = ['basePeriod', 'source', 'footnotes',
                           'nature_code', 'nature_desc',
                           'units_code', 'units_desc',
                           'reportingType_code', 'reportingType_desc',
                           'observationStatus_code', 'observationStatus_desc'
                           ]

    schema['attr_measure'] = ['value_detail',
                              'lowerBound_detail',
                              'upperBound_detail']

    return schema
