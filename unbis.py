from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
import utils
import metadata



# Read UN BIS terms

URL = 'http://metadata.un.org/thesaurus/alphabetical?lang=en'
content = requests.get(URL)

soup = BeautifulSoup(content.text, 'html.parser')

terms = soup.find_all("a", {"class": "bc-link"})

terms_list = []
for a in terms:
    d = dict()
    d['term'] = a.text.lower()
    d['url'] = a['href']
    terms_list.append(d)


# Read tags template:

tags_template = utils.tsv2dictlist('data/external/tagsTemplate2021.Q1.G.01.txt')
print(tags_template[0].keys())



tags = metadata.read_tags('data/external/tagsTemplate2021.Q1.G.01.txt', 'seriesCode', 'seriesTags')

# print(tags)

unique_tags = []
for s in tags:
    unique_tags.extend(s['tags'])

unique_tags = sorted(list(set(unique_tags)))


print(unique_tags)

tags_unbis = []
for t in unique_tags:
    if t == 'women\s health':
        t = 'women\'s health'
    if t == 'workers\ rights':
        t = 'workers\' rights'
    dd = dict()
    dd['tag'] = t
    dd['unbis_url'] = ''
    print(t)
    for i in terms_list:
        if i['term'] != t:
            continue
        print(i)
        dd['unbis_url'] = i['url']
    
    tags_unbis.append(dd)

utils.dictList2tsv(tags_unbis, 'data/external/tags_unbis.txt')
