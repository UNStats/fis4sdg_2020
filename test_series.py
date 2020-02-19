import sdg_api
import utils

x = sdg_api.sdg_tree()

print(x[0].keys())
print(x[0]['targets'][0].keys())
print(x[0]['targets'][0]['indicators'][0].keys())
print(x[0]['targets'][0]['indicators'][0]['series'][0].keys())
