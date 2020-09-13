

def build_fact(text_type,
               conditions,
               da2_1,
               da2_2,
               da3_1,
               unit_1,
               unit_2,
               value_y_min,
               y_min,
               value_y_max,
               y_max,
               prog,
               prog_10,
               prog_12,
               prog_15,
               prog_mmr_max):

    fact_text = ''
    fact_values = []
    fact_units = []
    fact_years = []

    if text_type == '1':
        if conditions:
            fact_text = da3_1 + prog + " <span class='fact-value'>" + str(value_y_min) + "</span>  <span class='fact-unit'>" + unit_1 + "</span>  in  <span class='fact-year'>" + str(
                y_min) + "</span> to <span class='fact-value'>" + str(value_y_max) + unit_1 + "</span> in <span class='fact-year'>" + str(y_max) + "</span>."
            fact_values = [str(value_y_min), str(value_y_max)]
            fact_units = [unit_1, unit_1]
            fact_years = [str(y_min), str(y_max)]
        else:
            fact_text = da2_1 + " <span class='fact-value'>" + \
                str(value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + \
                "</span> in <span class='fact-year'>" + str(y_max) + "</span>."
            fact_values = [str(value_y_max)]
            fact_units = [unit_1]
            fact_years = [str(y_max)]

    elif text_type == '2':
        fact_text = "In <span class='fact-year'>" + str(y_max) + "</span>, <span class='fact-value'>" + str(
            value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span> " + da2_1
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '3':
        fact_text = "In <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(
            value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span> " + da2_2
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '4':
        fact_text = da2_1 + " <span class='fact-value'>" + str(value_y_max) + "</span> in <span class='fact-year'> " + str(
            y_max) + "</span> " + ", meaning " + str(float(value_y_max) * 100) + da2_2 + "."
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '7':
        fact_text = da2_1 + " <span class='fact-value'> " + \
            str(value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span> " + \
            " in " + " <span class='fact-year'> " + \
            str(y_max) + "</span> " + "."
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '8':
        fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, <span class='fact-value'> " + str(
            value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + "</span> " + da2_1 + "."
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '9':
        if conditions:
            fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + \
                "</span>, " + prog + " <span class='fact-value'> " + \
                str(value_y_min) + "</span> <span class='fact-unit'>" + unit_2 + \
                "</span> in <span class='fact-year'> " + \
                str(y_min) + "</span> "
            fact_values = [str(value_y_min), str(value_y_max)]
            fact_units = [unit_1, unit_1]
            fact_years = [str(y_min), str(y_max)]
        else:
            fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(
                value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + "</span>."
            fact_values = [str(value_y_max)]
            fact_units = [unit_1]
            fact_years = [str(y_max)]

    elif text_type == '10':
        fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(
            value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + "</span>. " + prog_10
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '11':
        fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(
            value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + "</span>. "
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '12':
        fact_text = "As of " + " <span class='fact-year'> " + \
            str(y_max) + "</span>, " + country_name + prog_12 + "."
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '13':
        fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span>, " + da2_1 + " <span class='fact-value'> " + str(
            value_y_max) + "</span> " + " <span class='fact-unit'>" + unit_1 + "</span> " + da2_2 + "."
        fact_values = [str(value_y_max)]
        fact_units = [unit_1]
        fact_years = [str(y_max)]

    elif text_type == '14':
        if conditions:
            fact_text = da3_1 + prog + " <span class='fact-value'>" + str(value_y_min) + "</span> <span class='fact-unit'>" + unit_1 + "</span> in <span class='fact-year'> " + str(
                y_min) + "</span> to <span class='fact-value'> " + str(value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span> in <span class='fact-year'> " + str(y_max) + "</span>."
            fact_values = [str(value_y_min), str(value_y_max)]
            fact_units = [unit_1, unit_1]
            fact_years = [str(y_min), str(y_max)]
        else:
            fact_text = da2_1 + " <span class='fact-value'> " + \
                str(value_y_max) + "</span> <span class='fact-unit'>" + prog_mmr_max + \
                unit_1 + "</span> in <span class='fact-year'> " + \
                str(y_max) + "</span>."
            fact_values = [str(value_y_max) + prog_mmr_max]
            fact_units = [unit_1]
            fact_years = [str(y_max)]

    elif text_type == '15':
        if conditions:
            fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span> , " + da2_1 + " <span class='fact-value'> " + str(
                value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span>," + prog + prog_15 + " in <span class='fact-year'> " + str(y_min) + "</span>."
            fact_values = [str(value_y_min), str(value_y_max)]
            fact_units = [unit_1, unit_1]
            fact_years = [str(y_min), str(y_max)]
        else:
            fact_text = "In " + " <span class='fact-year'> " + str(y_max) + "</span> , " + da2_1 + " <span class='fact-value'> " + str(
                value_y_max) + "</span> <span class='fact-unit'>" + unit_1 + "</span>."
            fact_values = [str(value_y_max)]
            fact_units = [unit_1]
            fact_years = [str(y_max)]

    return {'fact_text': fact_text,
            'fact_values': fact_values,
            'fact_units': fact_units,
            'fact_years': fact_years
            }

# Informatino about status of progress: decline/increase?


def prog_info(value_y_min_num,
              value_y_max_num,
              down,
              up,
              unit_1):

    prog = None
    prog_10 = None
    prog_12 = None
    prog_15 = None
    prog_mmr_min = None
    prog_mmr_max = None

    # -----------------------------------------
    if value_y_min_num and value_y_max_num:
        if (value_y_min_num > value_y_max_num):
            prog = down
            # Example: "declined from", "down from"
        elif (value_y_min_num < value_y_max_num):
            prog = up
            # Example: "increased from", "up from"
        else:
            prog = ""
    else:
        prog = ""

    # print(prog)

    # --------
    # prog.15
    # --------
    if value_y_min_num < 0.01:
        prog_15 = "nearly no coverage"
    else:
        prog_15 = str(value_y_min_num) + unit_1

    # --------
    # prog.10
    # --------
    if value_y_max_num:
        if value_y_max_num < 10:
            prog_10 = down
        else:
            prog_10 = up
    else:
        prog_10 = ''

    # --------
    # prog.12
    # --------

    if value_y_max_num is not None:
        if value_y_max_num > 0:
            prog_12 = up
        else:
            prog_12 = down
    else:
        prog_12 = ''

    # -------------
    # prog_mmr_min
    # -------------
    if value_y_min_num:
        if value_y_min_num > 1:
            prog_mmr_min = "deaths"
        else:
            prog_mmr_min = "death"
    else:
        prog_mmr_min = ""

    # -------------
    # prog_mmr_max
    # -------------

    if value_y_max_num:
        if value_y_max_num > 1:
            prog_mmr_max = "deaths"
        else:
            prog_mmr_max = "death"
    else:
        prog_mmr_max = ""

    #print("min = ",value_y_min_num)
    #print("max = ",value_y_max_num)
    #print("prog = ",prog)
    # print(prog_15)
    # print(prog_10)
    # display(print(prog_12))
    # print(prog_mmr_min)
    # print(prog_mmr_max)

    return {'prog': prog,
            'prog_10': prog_10,
            'prog_12': prog_12,
            'prog_15': prog_15,
            'prog_mmr_min': prog_mmr_min,
            'prog_mmr_max': prog_mmr_max
            }
