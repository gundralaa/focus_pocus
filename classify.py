'''
Periodically check user p300 state. 
Setup streamer and poll streamer to connect to cnn model
Display p300 peaks and time stamps
'''

import numpy as np
import argparse
import time

from lib.graph import Graph
from lib.model import CNN2D

import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes
import torch

if __name__ == '__main__':
    # params
    params = BrainFlowInputParams()

    ## CONFIGURE HERE
    params.serial_port = "COM5"
    board_id = BoardIds.MUSE_2_BLED_BOARD
    board = BoardShim(board_id, params)
    eeg_chan = BoardShim.get_exg_channels(board_id)
    sampling_rate = BoardShim.get_sampling_rate(board_id)

    # start stream
    board.prepare_session()
    buffer_size = 1024 * 4
    board.start_stream(buffer_size)
    data_size = 232
    
    # load model
    state_dict = torch.load('notebooks/trained_model.pt')
    # model = CNN2D(input_size=(1, 4, data_size), kernel_size=[7, 7, 5, 5, 3, 3], conv_channels=[1, 32, 16, 8])
    model = CNN2D(input_size=(1, 4, data_size),
            kernel_size=[1, 8],
            conv_channels=[1, 8])
    model.load_state_dict(state_dict)
    
    # start display
    try:
        print("-- START STREAM --")
        # start nlp
        while True:
            # wait for input mode
            data = board.get_current_board_data(data_size)
            
            if (data.shape[1] < data_size): continue

            for i in eeg_chan:
                DataFilter.perform_bandpass(data[i], sampling_rate, 51.0, 100.0, 2, FilterTypes.BUTTERWORTH.value, 0)

            data = torch.reshape(torch.FloatTensor(data[eeg_chan]), (1, 1, 4, data_size))


            pred = model(data)
            pred_class = pred.data.max(1)[1]
            
            print(pred_class)
            time.sleep(0.1)
            # update display array confidence
            # if array confidence > threshold
            # retrieve option
            # send to nlp
            # send new options to display
    finally:
        print("-- END STREAM --")
    
    # stop stream
    board.stop_stream()
    board.release_session()

    