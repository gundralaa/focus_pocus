"""
Focus Pocus Main Script

Configured for Open BCI Ganglion
board_id = 

Creates a live stream of data from a specified device
Applies different pipelines from the /pipes that calculate the focus metric
Runs callbacks on focus metric
Optionally plots focus

TODO (gundralaa): add pipe on seperate thread from data
"""
import argparse
import numpy as np
import time

from pprint import pprint

from lib.focus_pipe import focus_pipe
from lib.graph import Graph
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams

EPOCH_LEN = 1024

def connect_and_stream(args):
    # board parameters
    params = BrainFlowInputParams()
    params.serial_port = args.port
    # BOARD TYPE -------
    board = BoardShim(BoardIds.MUSE_S_BLED_BOARD, params)
    # board = BoardShim(BoardIds.GANGLION_BOARD, params)
    board.prepare_session()
    board.start_stream(EPOCH_LEN * 4)
    return board

# TODO: DELETE
def poll_data(data, pipe):
    time.sleep(1)
    print(len(data[0]))
    # run pipeline on data
    metric = pipe(data)
    return metric

def get_args():
    # arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, help='serial port', required=True, default='')
    args = parser.parse_args()
    return args

def kill_stream(board):
    board.stop_stream()
    board.release_session()

if __name__ == '__main__':
    BoardShim.enable_dev_board_logger()
    board = connect_and_stream(get_args())
    
    # --- PIPES ----
    # demo pipe
    focus_p = focus_pipe(board, 'alpha')
    focus2_p = focus_pipe(board, 'theta_ratio')
    focus3_p = focus_pipe(board, 'total_ratio')
    pipes = [focus_p, focus2_p]

    # BOARD INFO
    id = board.get_board_id()
    sampling_rate = BoardShim.get_sampling_rate(id)
    eeg_channels = BoardShim.get_eeg_channels(id)
    
    print('board_id:', id)
    print('number of channels', eeg_channels)
    print('sampling rate', sampling_rate)
    
    ## STREAM
    # display_pipe(board, EPOCH_LEN)
    try:
        print("------- START STREAM -------")
        print(BoardShim.get_board_descr(id))
        Graph(board, pipes)
    finally:
        print("------- END STREAM ------")
        kill_stream(board)
