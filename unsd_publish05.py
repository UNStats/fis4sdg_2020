import set_release
import availability
import utils
import re
import os

# *******************************************************************
# Obtain list of time series available for each SDG series
# *******************************************************************

release = set_release.set_release()

folder = 'data/raw/' + release
regex = r'Series_(.*?)_RefArea_(.*?).txt'
i_series = 1
i_geo = 2

series_list = availability.available_series(folder, regex, i_series, i_geo)

# If some series have already bene processed, skip them:
files = os.listdir('data/interim/'+release+'/time_series')

series_done = []
for f in files:
    f_s = re.search(r'TimeSeries_(.*?).txt', f).group(1)
    if f_s in series_list:
        series_list.remove(f_s)
        series_done.append(f_s)

print(f'{len(series_done)} have already been processed')
print(f'{len(series_list)} remain')

for s in series_list:

    # if s != 'VC_VOV_SEXL':
    #    continue

    # if s[0:2] != 'AG':
    #    continue

    ts = availability.available_time_series(s, release)

    file_out = 'data/interim/' + release + '/time_series/TimeSeries_' + s + '.txt'

    utils.dictList2tsv(ts, file_out)

    print(f'-- Finished series {s}')
