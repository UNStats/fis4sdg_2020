import sdg_api
import metadata
import utils
import set_release
import os
import re

# ******************************************************************************
# GET DATA FOR EACH SERIES FROM THE API
# Save as tab-delimited files for each indicator-country dataset in the
# ..data/raw/<release>/ directory
# ******************************************************************************

release = set_release.set_release()

sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

series = metadata.series_catalog(sdg_meta)

# If some series have already bene processed, skip them:
files = os.listdir('data/raw/'+release)

series_done = []
for f in files:
    f_s = re.search(r'Series_(.*?)_RefArea_(.*?).txt', f).group(1)
    if f_s in series:
        series.remove(f_s)
        series_done.append(f_s)

print(f'{len(series_done)} have already been processed')
print(f'{len(series)} remain')

for s in series:
    # if s == 'EN_MAT_DOMCMPC':
    #    continue
    sdg_api.seriesData2tsv(s, release)
