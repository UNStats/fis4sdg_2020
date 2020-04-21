import set_release
import urllib3
import metadata
import utils
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
release = set_release.set_release()

# ******************************************************************************
# Set SDG Tags and Metadata
# ******************************************************************************

# ---------------------------------------------
# Read or update sdg metadata file
# ---------------------------------------------

tags_template = {'file': 'data/external/tagsTemplate2020.Q1.G.01.txt',
                 'seriesCodeCol': 'seriesCode',
                 'seriesTagsCol': 'seriesTags'}


sdg_meta = metadata.build_sdg_tree_metadata('data/external/GlobalIndicatorFramework2019_EN_ES_FR.xlsx',
                                            'Goals', 'Targets', 'Indicators', 'TierClassification',
                                            'data/external/sdgColors.json',
                                            tags_template['file'],
                                            tags_template['seriesCodeCol'],
                                            tags_template['seriesTagsCol'],
                                            release)

series_missing_tags = []
for g in sdg_meta:
    for t in g['targets']:
        for i in t['indicators']:
            for s in i['series']:
                if len(s['tags']) == 0:
                    series_missing_tags.append(s['code'])

series_missing_tags = list(set(series_missing_tags))

print(f'{len(series_missing_tags)} series are missing tags. \n {series_missing_tags}')

# Run the above to generate a new tags Template. After editing the tags tamplate, save it as a new txt file under data/external/
# and re-run the same command (changing the name of the tagsTemplate file if necessary).

edit_tags = utils.query_yes_no("Do you want to edit the tags template?")

if edit_tags:
    sys.exit('Run this script again after editing the tags template')
