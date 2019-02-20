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


def return_cylce_indeces(cycle, cycle_break):
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
