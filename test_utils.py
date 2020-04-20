import utils
import re


# # -----------------------------------------------

# # Test data:
# d1 = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964
# }
# d2 = {
#     "brand": "VW",
#     "model": "Beetle",
#     "year": 1965
# }
# d_list = [d1, d2]

# # -----------------------------------------------

# # camel_case
# print(utils.camel_case('this is camel case'))

# # -----------------------------------------------
# # numeric_part
# x = '<-0.01'
# print(f'The numeric part of {x} is {utils.numeric_part(x)}')

# # -----------------------------------------------
# # dict_hash

# print(d1)
# print(f'The hash of {d1} is {utils.dict_hash(d1)}')

# # -----------------------------------------------
# # unique_dicts
# print([d1, d1, d2])
# print(utils.unique_dicts([d1, d1, d2]))

# # -----------------------------------------------
# # subdict_list
# print(d_list)
# print(utils.subdict_list(d_list, ['brand', 'model']))

# # -----------------------------------------------
# # select_dict
# print('-----select_dict-----')
# print(d_list)
# print(utils.select_dict(d_list, {'brand': 'VW'}))

# # -----------------------------------------------
# # get_json_from_web(url, method='GET')
# # Example: Get geographic areas tree
# x = utils.get_json_from_web(
#     'https://unstats.un.org/SDGAPI/v1/sdg/GeoArea/Tree')
# for i in x:
#     print(i.keys())

# # -------------------------------------------------
# # traverse(tree, parentCode=None, parentName=None, itemCode='code', itemName='name', itemChildren='children')

# test_tree = {
#     'code': '1',
#     'name': 'root',
#     'extra': 3,
#     'children': [
#         {
#             'code': '1.1',
#             'name': 'child 1.1',
#             'children': [
#                 {
#                     'code': '1.1.1',
#                     'name': 'child 1.1.1',
#                     'children': None
#                 },
#                 {
#                     'code': '1.1.2',
#                     'name': 'child 1.1.2',
#                     'children': None
#                 }
#             ]
#         },
#         {
#             'code': '1.2',
#             'name': 'child 1.2',
#             'children': [
#                 {
#                     'code': '1.2.1',
#                     'name': 'child 1.2.1',
#                     'children': None
#                 },
#                 {
#                     'code': '1.2.2',
#                     'name': 'child 1.2.2',
#                     'children': None
#                 }
#             ]
#         }
#     ]
# }

# print(utils.traverse_tree(test_tree))

# dl1 = [
#     {'k1': 11, 'k2': 12, 'k3': 13},
#     {'k1': 21, 'k2': 22, 'k3': 23},
#     {'k1': 31, 'k2': 32, 'k3': 33},
#     {'k1': 41, 'k2': 42, 'k3': 43}
# ]

# dl2 = [
#     {'z1': 11, 'z2': 92, 'z3': 93},
#     {'z1': 11, 'z2': 82, 'z3': 83},
#     {'z1': 31, 'z2': 72, 'z3': 73},
#     {'z1': 51, 'z2': 62, 'z3': 63}
# ]


# left_on = ['k1']
# right_on = ['z1']

# print(utils.merge_dict_lists(dl1, dl2, left_on, right_on, how='inner'))
# print(utils.merge_dict_lists(dl1, dl2, left_on, right_on, how='left'))


# ---------------------------

# tags = utils.tsv2dictlist('data/external/tagsTemplate2019.Q3.G.01.txt')
# for i in tags:
#     tags_string = i['TAGS']
#     tags_string = re.sub('[\[\]\']', '', tags_string)
#     tags_list = tags_string.split(', ')
#     i['TAGS'] = tags_list

# print(tags[0:2])

# ----------------------------

x = utils.year_intervals(
    ['1995', '2000', '1996', '2001', '2002', '2003', '2004'])
print(x)
