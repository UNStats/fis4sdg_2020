import utils
import csv

x = utils.get_json_from_web(
    'https://unstats.un.org/SDGAPI/v1/sdg/GeoArea/Tree')

# print(x[0])

y = utils.traverse_tree(x[0], parentCode=None, parentName=None, itemCode='geoAreaCode',
                        itemName='geoAreaName', itemChildren='children')

print(len(y))
print(y[0])

print('-----------------------')

z = utils.tsv2dict('data/geography/refAreas.txt')
print(len(z))
print(z[0])


print('-----------------------')

yz = utils.merge_dict_lists(y, z, ['geoAreaCode'], ['M49'], how='inner')
print(yz[0:10])

metadata = utils.open_json('data/external/metadata.json')
print(metadata[0]['targets'][0]['indicators'][0]['series'][0])
