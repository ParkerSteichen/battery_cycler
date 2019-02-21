import pandas as pd
import numpy as np

def import_data(filename, sheet_count):
    """
    function to import and concatenate excel data
    requires that exported data contains columns:
        index, time, voltage, current, capacity, and state
    """
    names = ['index', 'time', 'voltage', 'current', 'capacity', 'state']
    df = pd.read_excel(filename, sheet_name='Sheet1', header=None, names=names)
    dfl = list([df])
    if sheet_count == 1:
        pass
    else:
        for i in range(1, sheet_count):
            sheet_name='Sheet1(Continued{})'.format(i)
            df0 = pd.read_excel(filename, sheet_name, header=None, names=names)
            dfl.append(df0)
    dff = pd.concat(dfl, ignore_index=True)
    return dff


def return_cycle_indeces(cycle, cycle_break):
    """docstring"""
    cycle_data = []
    start = cycle_break[cycle - 1] + 2
    end = cycle_break[cycle] - 1
    cycle_index = np.arange(start, end)
    return cycle_index


def clean_prep_break(dataframe):
    """
    function that removes labels from in between cycles,
    adds a new column which contains the time in seconds,
    and outputs a list of cycle_breaks
    """
    drop = ['Mode', 'Rest', 'Charge CC', 'Discharge CC', 'TestTime']
    times = dataframe['time']
    drop_index = []
    index = []
    for i in range(len(dataframe['time'])):
        time_0 = str(times[i])
        if time_0 in drop:
            drop_index.append(i)
        else:
            index.append(i)   
    dataframe2 = dataframe.drop(drop_index)
    # add column with time converted to seconds
    t_sec = []
    times = dataframe2['time']
    for i in range(len(dataframe2['time'])):
        j = index[i]
        time_0 = str(times[j])
        if len(time_0) < 10:
            days = 0
            hours, minutes, seconds = time_0.split(':')
        else:
            days, time = time_0.split('-')
            hours, minutes, seconds = time.split(':')
        sec = int(days)*86400 + int(hours)*3600 + int(minutes)*60 + int(seconds)
        t_sec.append(sec)
    dataframe2['time_sec'] = t_sec
    # converts drop_index to a list of cycle_breaks
    cycle_break = []
    for i in range(len(dataframe.index)):
        if i - 1 in drop_index and i + 1 in drop_index:
            cycle_break.append(i)
        else:
            pass
    return dataframe2, cycle_break


def reshape_cycle_indeces(df, df_break, rest=True):
    """
    function that reshapes the outputs of clean_prep_break
    Inputs:
    Returns:
        cylce_indeces, a reshaped dataframe where each cycle is callable
        by cycle number (example: for the 2nd cycle, the charge indeces
        for the cycle is at cycle_indeces[2][0], and the discharge data
        is at cycle_indeces[2][1])
    """
    cycle_indeces = []
    # saves rest data as index[0], if no rest saves None
    if rest == True:
        start = df_break[0] + 2
        end = df_break[1] - 1
        rest_index = np.arange(start, end)
        cycle_indeces.append(rest_index)
        num_cycles = len(df_break)//2
        if len(df_break) % 2 == 0:
            drop_partial = True
        elif len(df_break) % 2 != 0:
            drop_partial = False
        if drop_partial == True:
            for i in np.arange(1, len(df_break)-1, 2):
                charge_start = df_break[i]+2
                charge_end = df_break[i+1]-1
                charge_index = np.arange(charge_start, charge_end)
                discharge_start = df_break[i+1]+2
                discharge_end = df_break[i+2]-1
                discharge_index = np.arange(discharge_start, discharge_end)
                full_cycle_index = [charge_index, discharge_index]
                cycle_indeces.append(full_cycle_index)
        elif drop_partial == False:
            for i in np.arange(1, len(df_break)-3, 2):
                charge_start = df_break[i]+2
                charge_end = df_break[i+1]-1
                charge_index = np.arange(charge_start, charge_end)
                discharge_start = df_break[i+1]+2
                discharge_end = df_break[i+2]-1
                discharge_index = np.arange(discharge_start, discharge_end)
                full_cycle_index = [charge_index, discharge_index]
                cycle_indeces.append(full_cycle_index)
            i = len(df_break)-2
            charge_start = df_break[i]+2
            charge_end = df_break[i+1]-1
            charge_index = np.arange(charge_start, charge_end)
            discharge_start = df_break[i+1]+2
            discharge_end = df.index[-1]
            discharge_index = np.arange(discharge_start, discharge_end)
            full_cycle_index = [charge_index, discharge_index]
            cycle_indeces.append(full_cycle_index)
    elif rest == False:
        cycle_indeces.append('No Rest')
#         num_cycles = len(df_break)//2
#         if len(df_break) % 2 == 0:
#             drop_partial = False
#         elif len(df_break) % 2 != 0:
#             drop_partial = True
        print("""feature not currently supported,
              data must have rest period before first cycle""")
    return cycle_indeces
