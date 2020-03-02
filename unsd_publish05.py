import set_release
import availability
import utils

# *******************************************************************
# Obtain list of time series available for each SDG series
# *******************************************************************

release = set_release.set_release()

folder = 'data/raw/' + release
regex = r'Series_(.*?)_RefArea_(.*?).txt'
i_series = 1
i_geo = 2

series_list = availability.available_series(folder, regex, i_series, i_geo)

for s in series_list:

    # if s != 'VC_VOV_SEXL':
    #    continue

    ts = availability.available_time_series(s, release)

    file_out = 'data/interim/' + release + '/time_series/Series_' + s + '.txt'

    utils.dictList2tsv(ts, file_out)

    print(f'-- Finished series {s}')
