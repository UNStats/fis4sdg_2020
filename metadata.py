import utils
import sdg_api
import copy
import json
import re
import csv


# ---------------------------------------
# Read tags for series


def read_tags(tags_file, tags_seriesCodeCol, tags_tagsListCol):
    ''' Read tags template from tab-delimited txt file.
        File must include two columns:
            - seriesCodeCol
            - tagsListCol
        Tags in the tagsList column must be separated by commas. 
        Tags can be wrapped in brackets and sinqle quote marks. 
        
        Example: read_tags('data/external/tagsTemplate2019.Q3.G.01.txt', 'seriesCode', 'TAGS')
        
    '''
    tags_list = []
    
    for i in utils.tsv2dictlist(tags_file):
        tags_dict = dict()
        tags_dict['seriesCode'] = i[tags_seriesCodeCol]
        tags_dict['tags'] = re.sub('[\[\]\']', '', i[tags_tagsListCol]).split(', ')
        tags_list.append(tags_dict)
    return tags_list

# print(tags_list[0])


# ---------------------------------------
# Get goals, targets, and indicators from global indicator framework, as captured in local file,
    
def read_indicator_framework(framework_file, goals_sheet, targets_sheet, indicators_sheet, tierClassification_sheet):
    ''' Read goals, targets, indicators, and tier classification from 
        local xlsx framework_file
        
        Example: 
            read_indicator_framework('data/external/GlobalIndicatorFramework2019_EN_ES_FR.xlsx',
            'Goals','Targets','Indicators', 'TierClassification')
    '''
    
    goals = utils.xlsx2dict(framework_file, goals_sheet)
    
    for g in goals:
        for k,v in g.items():
            g[k] = utils.clean_str(v)
    
            
    targets = utils.xlsx2dict(framework_file, targets_sheet)
    
    for t in targets:
        for k,v in t.items():
            t[k] = utils.clean_str(v)
    
    indicators = utils.xlsx2dict(framework_file, indicators_sheet)
    
    for i in indicators:
        for k,v in i.items():
            i[k] = utils.clean_str(v)
    
    tiers = utils.xlsx2dict(framework_file, tierClassification_sheet)
    
    for r in tiers:
        for k,v in r.items():
            r[k] = utils.clean_str(v)
    
    return {'goals': goals,
            'targets': targets,
            'indicators': indicators,
            'tiers': tiers}

# ---------------------------------------
# Add colors to goals:
    
def build_sdg_tree_metadata(framework_file, goals_sheet, targets_sheet, indicators_sheet, tierClassification_sheet,
                            sdgColors_file,
                            tags_file, tags_seriesCodeCol, tags_tagsListCol, release):
    ''' Read sdg framework and sdg colors from local sdg files; add series from sdg_api call.
    
        Example call:
            build_sdg_tree_metadata('data/external/GlobalIndicatorFramework2019_EN_ES_FR.xlsx',
                                    'Goals','Targets','Indicators', 'TierClassification',
                                    'data/external/sdgColors.json',
                                    'data/external/tagsTemplate2019.Q4.G.01.txt','seriesCode', 'seriesTags','2019.Q4.G.01')
    
    '''

    framework =  read_indicator_framework(framework_file, 
                                          goals_sheet, 
                                          targets_sheet, 
                                          indicators_sheet, 
                                          tierClassification_sheet)
    
    tags_list = read_tags(tags_file, tags_seriesCodeCol, tags_tagsListCol)
    

    with open(sdgColors_file) as json_file:
        sdgColors = json.load(json_file)['ColorScheme']
    
    for g in framework['goals']:
        col_scheme = utils.select_dict(
            sdgColors, {'GoalCode': int(g['code'])})[0]
        g['hex'] = col_scheme['hex']
        g['rgb'] = col_scheme['rgb']
        g['ColorScheme'] = col_scheme['ColorScheme']
    
    
    # ---------------------------------------
    # Add series to indicators
    sdg_api_tree = sdg_api.sdg_tree()
    
    
    # create a goals/targets/indicators tree
    for g in framework['goals']:
        
        g['targets'] = []
        
        api_goal = utils.select_dict(sdg_api_tree, {'code': g['code']})[0]
        
        #print(f'Goal: {g["code"]}')
        
        for t in framework['targets']:
            
            if t['parentCode'] == g['code']:
                
                target = copy.deepcopy(t)
                del target['parentCode']
                target['indicators'] = []
                #print(f'   Target: {target["code"]}')
    
                api_target = utils.select_dict(api_goal['targets'], 
                                               {'code': target['code']})[0]
                        
                for i in framework['indicators']:
                    
                    if i['parentCode'] == target['code']:
                        
                        indicator = copy.deepcopy(i)
                        del indicator['parentCode']
                        #print(f'      Indicator: {indicator["reference"]}')
                                                
                        api_indicator = utils.select_dict(api_target['indicators'], 
                                                          {'code': indicator['reference']})                        
                        
                        if len(api_indicator) == 1:                
                            series = utils.subdict_list(utils.select_dict(api_indicator[0]['series'], 
                                                                          {'release': release}), 
                                                        ['code','description','release'])
                            for s in series:
                                s_tags = utils.select_dict(tags_list,{'seriesCode' : s['code']})
                                if len(s_tags)> 0: 
                                    s['tags'] = s_tags[0]['tags']
                                else:
                                    s['tags'] = []
                        else:
                            series = []
                            
                        indicator['series'] = series
                                                    
                    
                        target['indicators'].append(indicator)
                
                g['targets'].append(target)
            
    
    new_metadata_template  = []
    for g in framework['goals']:
        for t in g['targets']:
            for i in t['indicators']:
                for s in i['series']:
                    r = dict()
                    r['goalCode'] =  g['code']
                    r['goalLabelEN'] = g['labelEN']
                    r['goalDescEN'] = g['descEN']
                    r['targetCode'] = t['code']
                    r['targetDescEN'] = t['descEN']
                    r['indicatorCode'] = i['code']
                    r['indicatorRef'] = i['reference']
                    r['seriesCode'] = s['code']
                    r['seriesDescEN'] = s['description']
                    r['seriesRelease'] = s['release']
                    r['seriesTags'] = s['tags']
                    new_metadata_template.append(r)
                    
    with open('data/interim/interim_tags_template_'+release+'.txt', 'w', encoding="utf-8", newline='') as f1:
        writer = csv.DictWriter(f1, fieldnames=new_metadata_template[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(new_metadata_template)      

    print('Created file \'data/interim/interim_tags_template_'+release+'.txt\'')
    
    
    with open('data/interim/interim_metadata_'+release+'.json', 'w', encoding="utf-8") as f:
        json.dump(framework['goals'], f, indent=4)
        
    print('created file \'data/interim/interim_metadata_'+release+'.json\'')
        
    return framework['goals']
    
