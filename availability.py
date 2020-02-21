import os
import re
import utils

def available_series_areas(folder):
    '''Catalog of available series
    '''
    files = os.listdir(folder)
    
    series_area =[]
    
    for f in files:
 
        d = dict()
        
        search_results = re.search(r'Series_(.*?)_RefArea_(.*?).txt', f)
        d['seriesCode'] = search_results.group(1)
        d['geoAreaCode'] = search_results.group(2)
    
        series_area.append(d)
        
    return series_area


def available_series_by_geo(folder):
    '''Catalog of available series for each geographic area.
    '''
    
    series_area = available_series_areas(folder)
        
    areas = utils.unique_dicts(utils.subdict_list(series_area, ['geoAreaCode']))
    
    for g in areas:
        g['series'] = []
        for sa in series_area:
            if g['geoAreaCode'] == sa['geoAreaCode']:
                g['series'].append(sa['seriesCode'])
    
    return areas
                
    
def available_geo_by_series(folder):
    '''Catalog of geographic areas that have data available for each series.
    '''
    
    series_area = available_series_areas(folder)
        
    series = utils.unique_dicts(utils.subdict_list(series_area, ['seriesCode']))
    
    for s in series:
        s['geoAreaCodes'] = []
        for sa in series_area:
            if s['seriesCode'] == sa['seriesCode']:
                s['geoAreaCodes'].append(sa['geoAreaCode'])
    
    return series

def available_geo(folder):
    '''Catalog of available areas
    '''
    series_area = available_series_areas(folder)
        
    areas = utils.unique_dicts(utils.subdict_list(series_area, ['geoAreaCode']))
    
    return [x['geoAreaCode'] for x in areas]
                

def available_series(folder):
    '''Catalog of available seires
    '''
    series_area = available_series_areas(folder)
    
    series = utils.unique_dicts(utils.subdict_list(series_area, ['seriesCode']))
        
    return [x['seriesCode'] for x in series]
                          