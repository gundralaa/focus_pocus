"""
Sample Pipeline
This example uses the brainflow data_filter objects

Calculates alpha band power
"""
import argparse
import logging

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

# MATPLOTLIB (OLD)
def display_pipe(board, epoch_len):

    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot(121)
    ax.set_facecolor('#DEDEDE')

    def pipe(i):
        # returns avg band powers and std deviations
        data = board.get_current_board_data(epoch_len)[0]
        # DEBUG
        print("DEBUG: ", len(data))
        # -- FILTER --
        # -- NORMALIZE --
        mean, std = np.mean(data), np.std(data)
        norm_data = (data - mean) / std
        print("DEBUG: mean, std", mean, std)
        # -- PLOT --
        ax.cla()
        ax.plot(norm_data)
        ax.set_ylim(0, 1)
    
    ani = FuncAnimation(fig, pipe, interval=1000)
    plt.show()

# PYQT (NEW)
class Graph:
    def __init__(self, board_shim, pipe=None):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.pipe = pipe
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='Plot',size=(800, 600))

        self._init_timeseries()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()


    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        # --- CREATE PIPE DATA PLOT ---
        # ----------------------------
        # Channels
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i,col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            p.setTitle('Channel ' + str(i))
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)


    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        for count, channel in enumerate(self.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            # BAND PASS FILTERS -------
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # BAND STOP FILTERS ------
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 50.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 60.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # --- SET DATA ---
            self.curves[count].setData(data[channel].tolist())
        # --- UPDATE PIPE DATA PLOT
        # -------------------------

        self.app.processEvents()

