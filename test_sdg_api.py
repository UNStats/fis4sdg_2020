import sdg_api
import utils
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# for t in sdg_api.geoAreaTree():
#    code = str(t["geoAreaCode"])
#    name = t["geoAreaName"]
# print(f'root={code}:{name}')


# print(sdg_api.geoAreaTree(1))

# geoAreaTree_flat = utils.traverse_tree(sdg_api.geoAreaTree(1),
#                                       parentCode=None,
#                                       parentName=None,
#                                       itemCode='geoAreaCode',
#                                       itemName='geoAreaName')

# print(geoAreaTree_flat)


#missing_areas = utils.tsv2dict('data/geography/missingAreas.txt')
# print(missing_areas)

# add missing areas to geoAreaTree_flat:
# for d in missing_areas:
#     new_d = dict()
#     for k1 in geoAreaTree_flat[0].keys():
#         if k1 in d.keys():
#             new_d[k1] = d[k1]
#         else:
#             new_d[k1] = None
#     geoAreaTree_flat.append(new_d)

# print(geoAreaTree_flat)

# Verify how many pages need to be requested to get all the data for a specific series from the SDG API.
#print(sdg_api.series_request_details('SL_EMP_INJUR', '2019.Q4.G.01'))

# Explore the code lists of the attributes and dimensions of a series
# print(sdg_api.series_code_lists('SL_EMP_INJUR', '2019.Q4.G.01'))

# collect data for a specific series from the global SDG API
#x = sdg_api.series_data('SL_EMP_INJUR', '2019.Q4.G.01')

#y = sdg_api.flat_series_data('SL_EMP_INJUR', '2019.Q4.G.01')

# print(y[0:5])

#sdg_api.series_data_to_json('SL_EMP_INJUR', '2019.Q4.G.01')

# sdg_api.series_data_to_json('SL_EMP_INJUR', '2019.Q4.G.01')

seriesCode = 'VC_DSR_MISS'
release = '2019.Q4.G.01'
sdg_api.seriesData2json(seriesCode, release)


 
 