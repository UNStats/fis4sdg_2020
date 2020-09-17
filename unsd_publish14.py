import set_release
import utils
import json
import country_profiles as cp
import statistics

import os.path
from os import path


verify = []

release = set_release.set_release()

# Read fact-builder rules:
fact_builder = utils.tsv2dictlist(
    'data/external/factBuilder_' + release + '.txt')


# for f in fact_builder:
#     f['DA2.1'] = re.sub("â€”", "\u2014", f['DA2.1'])
#     f['DA2.2'] = re.sub("â€”", "\u2014", f['DA2.2'])
#     f['DA3.1'] = re.sub("â€”", "\u2014", f['DA3.1'])

print(fact_builder[0])

# Create list of countries:
countryArray = utils.tsv2dictlist(
    'data/geography/refAreas.txt'
)

print(countryArray[1])

print("Total number or countries: ", len(countryArray))

# Get the list of goals, target, indicators and series:

sdg_meta = utils.open_json('data/external/metadata_' + release + '.json')

# Get catalog of UNSD itmes on SDG open data hug:

hub_catalogue = utils.tsv2dictlist(
    'data/external/hub_items_' + release + '.txt')

print(hub_catalogue[0])

# Create country profiles:

count_country = 0

for this_country in countryArray:

    # if this_country['M49'] not in ['8']:
    #     continue

    # if this_country['Country_Profile'] != '1':
    #     continue

    count_country += 1

    country_profile = {}
    country_profile['release'] = release

    country_code = str(this_country['M49'])
    country_name = this_country['areaName']

    country_profile['country_code'] = country_code
    country_profile['country_name'] = country_name
    country_profile['X'] = this_country['X']
    country_profile['Y'] = this_country['Y']
    country_profile['ISO3'] = this_country['ISO3']
    country_profile['UNMember'] = this_country['UN_Member']
    country_profile['CountryProfile'] = this_country['Country_Profile']

    print("Building country profile for ",
          country_name, " - (", count_country, ")")

    count_fact = 0
    goals = []

    for g in sdg_meta:

        # if g['code'] != '3':
        #     continue

        # print("- in goal " + g['code'])

        goal = {}

        goal['goalCode'] = g['code']

        targets = []

        for t in g['targets']:

            # if t['code'] != '2.2':
            #     continue

            # print("- - in target " + t['code'])

            target = {}

            target['targetCode'] = t['code']

            indicators = []

            for i in t['indicators']:

                # if i['reference'] != '2.2.2':
                #     continue

                # print("- - - in indicator " + i['reference'])

                indicator = {}
                indicator['indicatorCode'] = i['reference']
                indicator['facts'] = []

                facts = []

                if 'series' in i.keys():
                    for s in i['series']:

                        # print("- - - - in series " + s['code'])

                        if s['release'] == release:

                            # if s['code'] != 'SH_STA_WASTE':
                            #     continue

                            for this_fact in fact_builder:

                                # if this_fact['countryProfile'] != '1' or this_fact['seriesCode'] != s['code']:
                                #     continue

                                if this_fact['series'] != s['code'] or this_fact['goal'] != g['code']:
                                    continue

                                # print("- - - - - in fact " +
                                    #   this_fact['series'])

                                count_fact += 1

                                seriesCode = s['code']
                                seriesTitle = this_fact['TimeSeriesDescription'] + \
                                    ' (' + this_fact['unit'] + ')'
                                # print(seriesTitle)

                                for h in hub_catalogue:

                                    if h['goal'] != this_fact['goal']:
                                        continue
                                    if h['series'] != this_fact['series']:
                                        continue

                                    hub = h['id']

                                # print(hub)

                                dashboard = ''

                                # for d in dashboard_catalogue:
                                #     if d['series'] != this_fact['seriesCode']:
                                #         continue
                                #     dashboard = d['dashboard id']

                                # -----------------------------------------------------------
                                # Colect data for this fact
                                # -----------------------------------------------------------

                                cp_data_path = 'data/interim/' + release + \
                                    '/country_profiles/country_profile_data_' + \
                                    this_country['M49'] + '.json'

                                if path.exists(cp_data_path):
                                    data = utils.open_json(cp_data_path)
                                else:
                                    continue

                                data = utils.select_dict(
                                    data, {'seriesCode': this_fact['series']})

                                if len(data) > 0:
                                    data = data[0]
                                else:
                                    continue

                                # print(data)

                                # ----------------------------------------------------------------
                                # Main fact calculation
                                # ----------------------------------------------------------------

                                values = data['data_values']
                                years = data['data_years']
                                values_is_censored = data['data_is_censored']
                                values_numeric_part = data['data_numeric_part']
                                values_is_censored = data['data_is_censored']

                                # -----------------------------------------
                                # Manually change scale of large-number variables:

                                if s['code'] in ['VC_DSR_HOLN', 'IS_RDP_PORFVOL']:

                                    values[:] = [
                                        str(int(float(x)) / 1000000) for x in values]

                                    values_numeric_part[:] = [
                                        x / 1000000 for x in values_numeric_part]

                                    # print(
                                    #     f"Changed scale to millions: {values}")
                                    # print(
                                    #     f"Changed scale to millions: {values_numeric_part}")

                                    if max(values_numeric_part) < 0.1:
                                        verify.append({'series': s['code'],
                                                       'country': country_code})

                                if s['code'] in ['IS_RDP_FRGVOL', 'IS_RDP_PFVOL']:

                                    values[:] = [
                                        str(int(float(x)) / 1000000000) for x in values]

                                    values_numeric_part[:] = [
                                        x / 1000000000 for x in values_numeric_part]

                                    # print(
                                    #     f"Changed scale to billions: {values}")
                                    # print(
                                    #     f"Changed scale to billions: {max(values_numeric_part)}")

                                    if max(values_numeric_part) < 0.1:
                                        verify.append({'series': s['code'],
                                                       'country': country_code})

                                        # print(
                                        #     "--------------verify!!!-------------")
                                        # print(f"country: {s['code']}")
                                        # print(f"series: {country_code}")
                                        # print(
                                        # "------------------------------------")

                                # -----------------------------------------

                                for i in range(len(values)):

                                    decimal_pos = values[i].find('.')

                                    if decimal_pos == -1 and values_numeric_part[i] is not None:
                                        values_numeric_part[i] = int(
                                            values_numeric_part[i])

                                    if decimal_pos > -1:
                                        if len(values[i]) - decimal_pos > 1:
                                            values_numeric_part[i] = utils.round_KFM(
                                                values_numeric_part[i], 1)

                                # number of observations available
                                n = len(values_numeric_part)
                                y_min = min(years)    # first year available
                                # most recent year available
                                y_max = max(years)

                                # data value in the first year available
                                value_y_min = values[years.index(y_min)]
                                # data value in the most recent year available
                                value_y_max = values[years.index(y_max)]

                                # data value in the first year available
                                value_y_min_num = values_numeric_part[years.index(
                                    y_min)]

                                # data value in the most recent year available
                                value_y_max_num = values_numeric_part[years.index(
                                    y_max)]

                                value_y_min_is_censored = values_is_censored[years.index(
                                    min(years))]
                                value_y_max_is_censored = values_is_censored[years.index(
                                    max(years))]

                                # print(f'values = {values}')
                                # print(f'years = {years}')
                                # print(
                                #     f'values_numeric_part = {values_numeric_part}')
                                # print(f'n = {n}')
                                # print(f'y_min = {y_min}')
                                # print(f'y_max = {y_max}')
                                # print(f'value_y_min = {value_y_min}')
                                # print(f'value_y_max = {value_y_max}')
                                # print(f'value_y_min_num = {value_y_min_num}')
                                # print(f'value_y_max_num = {value_y_max_num}')
                                # print(values_numeric_part)

                                # print(f"----Series={this_fact['series']}")

                                value_median = statistics.median(
                                    values_numeric_part)

                                # print(f'value_median = {value_median}')

                                dif_first_last = abs(
                                    value_y_min_num - value_y_max_num)

                                # print(f'dif_first_last = {dif_first_last}')

                                # ------------------------------------------
                                fact_prog = cp.prog_info(value_y_min_num, value_y_max_num,
                                                         down=this_fact['Down'],
                                                         up=this_fact['Up'],
                                                         unit_1=this_fact['unit1'])

                                # print(fact_prog)

                                # --------------------------------------------------------------------

                                fact_text = ""

                                if value_y_max_num and value_median:
                                    condition1 = dif_first_last >= 0.05 * \
                                        abs(value_y_max_num)
                                    condition2 = not value_y_max_is_censored
                                    condition3 = value_y_max_num >= .25*value_median
                                    condition4 = int(y_min) < 2010
                                    condition5 = n > 1

                                    conditions = condition1 and condition2 and condition3 and condition4 and condition5
                                else:

                                    conditions = False

                                if value_y_min_is_censored:
                                    fact_value_y_min = value_y_min
                                else:
                                    fact_value_y_min = str(value_y_min_num)

                                if value_y_max_is_censored:
                                    fact_value_y_max = value_y_max
                                else:
                                    fact_value_y_max = str(value_y_max_num)

                                fact_elements = cp.build_fact(text_type=this_fact['Text.type'],
                                                              conditions=conditions,
                                                              da2_1=this_fact['DA2.1'],
                                                              da2_2=this_fact['DA2.2'],
                                                              da3_1=this_fact['DA3.1'],
                                                              unit_1=this_fact['unit1'],
                                                              unit_2=this_fact['unit2'],
                                                              value_y_min=fact_value_y_min,
                                                              y_min=y_min,
                                                              value_y_max=fact_value_y_max,
                                                              y_max=y_max,
                                                              prog=fact_prog['prog'],
                                                              prog_10=fact_prog['prog_10'],
                                                              prog_12=fact_prog['prog_12'],
                                                              prog_15=fact_prog['prog_15'],
                                                              prog_mmr_max=fact_prog['prog_mmr_max'],
                                                              country_name=country_name
                                                              )
                                fact = {}
                                fact['seriesCode'] = seriesCode
                                fact['seriesTitle'] = seriesTitle
                                fact['hub'] = hub
                                fact['dashboard'] = dashboard
                                fact['slice_dimensions'] = data['slice_dimensions']
                                fact['text_type'] = this_fact['Text.type']
                                fact['fact_text'] = fact_elements['fact_text']
                                fact['fact_values'] = fact_elements['fact_values']
                                fact['fact_units'] = fact_elements['fact_units']
                                fact['fact_years'] = fact_elements['fact_years']
                                fact['data_years'] = years
                                fact['data_values'] = values
                                fact['data_is_censored'] = values_is_censored
                                fact['data_numeric_part'] = values_numeric_part

                                if this_fact['Text.type'] == '10':
                                    fact['preferred_visualization'] = 'threshold'
                                    fact['threshold_value'] = float(
                                        this_fact['Threshold'])
                                    fact['threshold_units'] = this_fact['unit1']
                                elif this_fact['Text.type'] == '12':
                                    fact['preferred_visualization'] = 'boolean'
                                elif utils.is_quasiConstant(values_numeric_part, 0.0001):
                                    # display(values_numeric_part)
                                    fact['preferred_visualization'] = 'singleton'
                                    # display("Quasi constant! - series: " + seriesCode)
                                elif(len(values) > 2):
                                    fact['preferred_visualization'] = 'time_series'
                                else:
                                    fact['preferred_visualization'] = 'singleton'

                                # =======================
                                # print('***** apending fact ******')
                                # print(fact)
                                facts.append(fact)

                    if len(facts) > 0:
                        # print('**** facts ******\n')
                        # print(f'facts: {facts}')
                        indicator['facts'] = facts
                        indicators.append(indicator)

            target['indicators'] = indicators
            # display(target)

            if len(target['indicators']) > 0:
                # print('*** apending indicators **')
                # display(indicators)
                targets.append(target)

        goal['targets'] = targets
        # display(goal)

        if len(targets) > 0:
            # print('** apending targets ******')
            # display(targets)
            goals.append(goal)
            # display(goals)

    country_profile['goals'] = goals
    # display(goals)

    with open('data/interim/' + release + '/country_profiles/country_profile'+str(country_code).zfill(3) + ".json", 'w') as outfile:
        json.dump(country_profile, outfile, indent=4)

with open('data/interim/' + release + '/country_profiles/verify_units.json', 'w') as outfile:
    json.dump(verify, outfile, indent=4)
