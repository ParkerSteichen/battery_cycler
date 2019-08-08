"""
A set a functions for plotting battery cycle performance data.
"""

import matplotlib.pyplot as plt
import numpy as np

def cv_cycle_plot(ax, clean_dataframe, cycle_list, cycle_num, plot_color, plot_alpha, label=None):
    """
    docstring
    """
    # fetch indeces for specified cycle_num
    # check to see if complete cycle
    if len(cycle_list[cycle_num-1]) == 1:
        # check to see if initial discharge
        if cycle_num == 1:
            print('First cycle only contains discharge data')
            discharge_indeces = cycle_list[cycle_num-1][0]
            discharge_dataframe = clean_dataframe[clean_dataframe.index.isin(discharge_indeces)]
            ax.plot(discharge_dataframe['scapacity'],
                    discharge_dataframe['voltage'],
                    color=plot_color,
                    alpha=plot_alpha)
        else:
            print('Incomplete cycle, only contains charge data')
            charge_indeces = cycle_list[cycle_num-1][0]
            charge_dataframe = clean_dataframe[clean_dataframe.index.isin(charge_indeces)]
            ax.plot(charge_dataframe['scapacity'],
                    charge_dataframe['voltage'],
                    color=plot_color,
                    alpha=plot_alpha)
    else:
        # complete cycle so plot both
        charge_indeces = cycle_list[cycle_num-1][0]
        charge_dataframe = clean_dataframe[clean_dataframe.index.isin(charge_indeces)]
        discharge_indeces = cycle_list[cycle_num-1][1]
        discharge_dataframe = clean_dataframe[clean_dataframe.index.isin(discharge_indeces)]
        # now plot charge and discharge curves
        ax.plot(charge_dataframe['scapacity'],
                charge_dataframe['voltage'],
                color=plot_color,
                alpha=plot_alpha)
        ax.plot(discharge_dataframe['scapacity'],
                discharge_dataframe['voltage'],
                color=plot_color,
                alpha=plot_alpha)


def cv_plot(ax, clean_dataframe, cycle_list, input_list, plot_color):
    """
    docstring
    """
    # generate list of alpha values for fade effect
    if len(input_list) == 1:
        alpha_list = [1]
    elif len(input_list) == 2:
        alpha_list = [0.5, 1]
    else:
        alpha_list = np.linspace(0.25, 1, len(input_list))
    # iterate across input_list and plot each
    for i, cycle_num in enumerate(input_list):
        cv_cycle_plot(ax, clean_dataframe, cycle_list, cycle_num, plot_color,
                      alpha_list[i])


def dqdv_cycle_plot(ax, clean_dataframe, cycle_list, cycle_num, count, step, plot_color):
    """
    docstring
    """
    # extract cycle data
    charge_indeces = cycle_list[cycle_num-1][0]
    discharge_indeces = cycle_list[cycle_num-1][1]
    charge_df = clean_dataframe[clean_dataframe.index.isin(charge_indeces)]
    discharge_df = clean_dataframe[clean_dataframe.index.isin(discharge_indeces)]
    # extract Q and V values
    charge_q = list(charge_df['capacity'])
    charge_v = list(charge_df['voltage'])
    discharge_q = list(discharge_df['capacity'])
    discharge_v = list(discharge_df['voltage'])
    # interpolate q over charge curve
    v_points = np.linspace(min(charge_v), max(charge_v), count)
    q_points = np.interp(v_points, charge_v, charge_q)
    # interpolate q over discharge curve
    v_points2 = np.linspace(min(discharge_v), max(discharge_v), count)
    q_points2 = np.flip(np.interp(np.flip(v_points2), np.flip(discharge_v), np.flip(discharge_q)))
    # calculate charge dQ/dV
    dQ_dV = []
    voltages = []
    for i in range(0, len(q_points)-step):
        if i <= step/2:
            dQ_dV.append(0)
            voltages.append(v_points[i])
        else:
            dQ = q_points[i+int(step/2)] - q_points[i-int(step/2)]
            dV = v_points[i+int(step/2)] - v_points[i-int(step/2)]
            value = dQ/dV
            dQ_dV.append(value)
            voltages.append(v_points[i])
    for i in range(len(q_points)-step, len(q_points)):
            dQ_dV.append(0)
            voltages.append(v_points[i])
    # calculate discharge dQ/dV
    dQ_dV2 = []
    voltages2 = []
    for i in range(0, len(q_points2)-step):
        if i <= step/2:
            dQ_dV2.append(0)
            voltages2.append(v_points[i])
        else:
            dQ = q_points2[i+int(step/2)] - q_points2[i-int(step/2)]
            dV = v_points2[i+int(step/2)] - v_points2[i-int(step/2)]
            value = dQ/dV
            dQ_dV2.append(value)
            voltages2.append(v_points2[i])
    for i in range(len(q_points2)-step, len(q_points2)):
            dQ_dV2.append(0)
            voltages2.append(v_points2[i])
    # plot charge and discharge onto axis
    ax.plot(voltages, dQ_dV, color=plot_color, alpha=0.75)
    ax.plot(voltages2, dQ_dV2, color=plot_color, alpha=0.75)


def scap_plot(ax, clean_dataframe, cycle_list, plot_color, plot='all', cycle_range=None):
    """
    docstring
    """
    # first extract specific capacity data
    charge_caps = []
    discharge_caps = []
    for i, indeces in enumerate(cycle_list):
        if i == 0 and len(indeces) == 1:
            # first cycle only contains initial discharge
            discharge_indeces = cycle_list[i][0]
            discharge_df = clean_dataframe[clean_dataframe.index.isin(discharge_indeces)]
            charge_caps.append(None)
            discharge_caps.append(max(list(discharge_df['scapacity'])))
        elif i != 0 and len(indeces) == 1:
            # last cycle only contains charge
            charge_indeces = cycle_list[i][0]
            charge_df = clean_dataframe[clean_dataframe.index.isin(charge_indeces)]
            charge_caps.append(max(list(charge_df['scapacity'])))
            dischage_caps.append(None)
        else:
            # all normal cycles with both charge and discharge
            charge_indeces = cycle_list[i][0]
            discharge_indeces = cycle_list[i][1]
            charge_df = clean_dataframe[clean_dataframe.index.isin(charge_indeces)]
            discharge_df = clean_dataframe[clean_dataframe.index.isin(discharge_indeces)]
            charge_caps.append(max(list(charge_df['scapacity'])))
            discharge_caps.append(max(list(discharge_df['scapacity'])))
    # second establish plotting range
    if cycle_range == None:
        start = 0
        stop = len(cycle_list)
    else:
        start = cycle_range[0]-1
        stop = cycle_range[1]
    # last plot the data
    if plot in {'all', 'charge'}:
        plt.scatter(np.linspace(1, len(charge_caps), len(charge_caps))[start:stop],
            charge_caps[start:stop],
            color='white',
            edgecolors=plot_color)
    if plot in {'all', 'discharge'}:
        plt.scatter(np.linspace(1, len(discharge_caps), len(discharge_caps))[start:stop],
            discharge_caps[start:stop],
            color=plot_color)