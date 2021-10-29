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

from pipes.alpha_power import alpha_pipe
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams

EPOCH_LEN = 1024

def connect_and_stream(args):
    # board parameters
    params = BrainFlowInputParams()
    params.serial_port = args.port
    # ganglion board object
    board = BoardShim(BoardIds.GANGLION_BOARD, params)
    board.prepare_session()
    board.start_stream(EPOCH_LEN * 4)
    return board

def poll_data(board, pipe):
    time.sleep(1)
    data = board.get_current_board_data(EPOCH_LEN)
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
    pipe = alpha_pipe(board)
    try: 
        while True:
            # replace the pipe below
            metric = poll_data(board, pipe)
            # poll_data(board, print)
            print('focus: ', metric)
    finally:
        kill_stream(board)
        print("Exited")
