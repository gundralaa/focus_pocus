"""
Blink Pipeline

Uses data to implement simple treshold to count blinks
Makes a persistent running count of blink and calculates blink rate
Used to then classify under different circumstances
"""
import numpy as np
from brainflow.board_shim import BoardIds, BoardShim
from brainflow.data_filter import DataFilter 

def blink_pipe(board : BoardShim):
    # TODO: remove hyper parameters
    peak_threshold = 40
    peak_duration = 5
    gain = 1
    
    id = board.get_board_id()
    # sampling rate for frequency calculations
    sampling_rate = BoardShim.get_sampling_rate(id)
    # index of eeg channels
    eeg_channels = BoardShim.get_eeg_channels(id)
    # functional data pipe that is run by main program

    # TODO: determine peak_threshold and duration for each channel
    def threshold(frame):
        # models channel as normally distributed
        return max(frame) - np.std(frame) * gain
    
    def peaks(channel):
        peaks = []
        dur = 0
        for i, val in enumerate(channel):
            # label peak if val above threshold and enough time elapsed
            if val > peak_threshold and dur > peak_duration:
                peaks.append(i)
                dur = 0
            dur += 1
        return len(peaks)

    def pipe(data):
        blinks = [peaks(channel) for channel in data]
        blink_rate = np.mean(blinks) / (len(data[0]) * sampling_rate)
        return blink_rate
    return pipe