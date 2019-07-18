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