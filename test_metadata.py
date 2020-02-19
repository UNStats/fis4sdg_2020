import metadata
import utils

m = metadata.all()
print(m[0].keys())
print('--------------------------')
print(m[0]['targets'][0].keys())
print('--------------------------')
print(m[0]['targets'][0]['indicators'][0].keys())
print('--------------------------')
print(m[0]['targets'][0]['indicators'][0]['series'][0].keys())
print('--------------------------')

# print(metadata.series())

# print(metadata.series()[0])
# print(metadata.indicators()[0])
# print(metadata.targets()[0])
# print(metadata.goals()[0])

print('--------------------------')
x = metadata.sdg_indicator_fmk('2019.Q4.G.01')


'data/external/tagsTemplate2019.Q3.G.01.txt', 'TAGS', 'seriesCode'
