"""
A set of functions that prepare data from a .xlsx file for plotting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def import_data(filename, sheet_count):
    """
    function to import and concatenate excel data
    requires that exported data contains columns:
        index, test_time, step_time, voltage, current, capacity, scapacity, energy, senergy, and state
    """
    names = ['index', 'test_time', 'step_time', 'voltage', 'current', 'capacity', 'scapacity', 'energy', 'senergy', 'state']
    df = pd.read_excel(filename, sheet_name='Sheet1', header=None, names=names)
    dfl = list([df])
    if sheet_count == 1:
        pass
    else:
        for i in range(1, sheet_count):
            sheet_name='Sheet1(Continued{})'.format(i)
            df0 = pd.read_excel(filename, sheet_name, header=None, names=names)
            dfl.append(df0)
    dataframe = pd.concat(dfl, ignore_index=True)
    return dataframe


def clean_prep_break(dataframe):
    """
    function that removes labels from in between cycles,
    adds a new column which contains the time in seconds,
    and outputs a list of cycle_breaks
    """
    times = dataframe['test_time']
    drop_labels = ['Mode', 'Rest', 'Charge CC', 'Charge C-Rate',
                   'Discharge CC', 'Discharge C-Rate', 'TestTime']
    drop_index = [i for i, time_0 in enumerate(times) if time_0 in drop_labels]
    index = [i for i, time_0 in enumerate(times) if time_0 not in drop_labels] 
    dataframe2 = dataframe.drop(drop_index)
    # add column with time converted to seconds
    t_sec = []
    times = dataframe2['test_time']
    for i in range(len(dataframe2['test_time'])):
        j = index[i]
        # convert overall time to seconds
        time_0 = str(times[j])
        if len(time_0) < 10:
            days = 0
            hours, minutes, seconds = time_0.split(':')
        else:
            days, time = time_0.split('-')
            hours, minutes, seconds = time.split(':')
        sec = int(days)*86400 + int(hours)*3600 + int(minutes)*60 + int(seconds)
        t_sec.append(sec)
    dataframe2['test_time_sec'] = t_sec
    # converts drop_index to a list of cycle_breaks
    cycle_break = []
    for i in range(len(dataframe.index)):
        if i - 1 in drop_index and i + 1 in drop_index:
            cycle_break.append(i)
        else:
            pass
    return dataframe2, cycle_break


def return_cycle_list(clean_dataframe, cycle_break, rest=True, reverse=True):
    # first break up the indexes for each cycle
    # empty list to collect lists of step_indeces
    index_list = []
    for i in range(0, len(cycle_break)-1):
        step_indeces = np.arange(cycle_break[i]+2, cycle_break[i+1]-1)
        index_list.append(step_indeces)
    # add all values after the last cycle_break as the final cycle
    step_indeces = np.arange(cycle_break[-1], clean_dataframe.index[-1]+1)
    index_list.append(step_indeces)
    index_list
    # drop rest data if True
    if rest is True:
        index_list.pop(0)
        print('Rest step removed')
    else:
        pass
    # if reverse is True the first cycle will only have a discharge while all
    # others will have a charge followed by a discharge
    cycle_list = []
    if reverse is True:
        cycle_list.append([index_list[0]])
        # remove first discharge from index_list
        index_list.pop(0)
        print('Reverse Mode: First cycle contains only initial discharge')
        print('{} complete cycles after intial discharge'.format(len(index_list)//2))
    else:
        print('{} complete cycles'.format(len(index_list)//2))
    for i in range(0, len(index_list)-1, 2):
        cycle = [index_list[i], index_list[i+1]]
        cycle_list.append(cycle)
    # if true there are an odd number of index lists indicating a partial cycle
    if len(index_list) % 2 == 1:
        cycle_list.append([index_list[-1]])
        print('Final cycle only contains charge data')
    else:
        pass
    return cycle_list


def plotprep(filename, sheet_count, rest=True, reverse=True):
    """
    docstring
    """
    dataframe = import_data(filename, sheet_count)
    clean_dataframe, cycle_break = clean_prep_break(dataframe)
    cycle_list = return_cycle_list(clean_dataframe, cycle_break, rest, reverse)
    return clean_dataframe, cycle_list
