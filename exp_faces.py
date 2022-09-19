'''
Data Collection Script
Used to collect N170 EEG signals based on
digitally presented stimuli of faces and other objects

Experiment
'''
import os
from random import choice
from glob import glob
import argparse
import numpy as np
import datetime

from pprint import pprint

from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from psychopy import visual, core, event

from stimuli import FACE_HOUSE

# LABEL
# 1 = face
# 2 = house

EPOCH_LEN = 1024
# Hyper Params
dur = 120
n_trials = 2000
inter_interval = 0.4
capture_len = 0.5

# BOARD CODE ----------------

def connect_and_stream(args):
    # board parameters
    params = BrainFlowInputParams()
    params.serial_port = args.port
    # BOARD TYPE -------
    board_id = BoardIds.MUSE_S_BLED_BOARD
    # board_id = BoardIds.GANGLION_BOARD
    board = BoardShim(board_id, params)
    pprint(BoardShim.get_board_descr(board_id))
    board.prepare_session()
    board.start_stream()
    return board

def record_buffer(board : BoardShim):
    n = board.get_board_data_count()
    b_id = board.get_board_id()
    print("DEBUG:n:", n)
    data = board.get_board_data()
    
    time_ind = BoardShim.get_timestamp_channel(b_id)
    mark_ind = BoardShim.get_marker_channel(b_id)
    eeg_ind = BoardShim.get_eeg_channels(b_id)
    inds = [time_ind, mark_ind] + eeg_ind
    
    arr = data[inds]
    f_name = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
    np.savetxt('./notebooks/data/' + f_name + '.txt', arr, fmt='%d')
    


def kill_stream(board):
    board.stop_stream()
    board.release_session()

# EXPERIMENT CODE ------------
def get_args():
    # arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, help='serial port', required=True, default='')
    args = parser.parse_args()
    return args

def load_imag(window):
    # faces
    # all front facing angles
    f_path = glob(os.path.join(FACE_HOUSE, "faces", "*_3.jpg"))
    h_path = glob(os.path.join(FACE_HOUSE, "houses", "*.3.jpg"))
    
    faces = [visual.ImageStim(window, image=path) for path in f_path]
    houses = [visual.ImageStim(window, image=path) for path in h_path]
    return [faces, houses]

def instructions():
    inst_text = """
    N170 Experiment
    Stay Still; Try not to blink;
    Focus on Images in the Center
    Spacebar to Continue
    """
    cur_win = visual.Window([800, 600], units='deg', monitor='testMonitor')
    stim = visual.TextBox2(cur_win, text=inst_text)
    stim.draw()
    
    cur_win.flip()
    event.waitKeys()
    cur_win.close()

def experiment(stimuli, window, mark_fn):
    for i in range(10):
        label = (i % 2) + 1
        image = choice(stimuli[label - 1])        
        # mark in stream start and end
        mark_fn(label)
        image.draw()
        core.wait(capture_len)
        
        # blank screen
        window.flip()
        
        # wait and turn off
        core.wait(inter_interval)
        window.flip()


def main():
    # streaming init
    board = connect_and_stream(get_args())
    time_ind = BoardShim.get_timestamp_channel(board.get_board_id())
    dbg_markers = []
    time_start = np.inf
    def mark(label):
        nonlocal time_start
        board.insert_marker(label)
        # debug
        time_stamp = board.get_current_board_data(1)[time_ind][0]
        time_start = min(time_stamp, time_start)
        dbg_markers.append([time_stamp - time_start, label])
    
    # main win
    main_win = visual.Window([800, 600], units='deg', monitor='testMonitor')
    instructions()
    stim = load_imag(main_win)
    experiment(stim, main_win, mark)
    
    # debug
    print(time_start, dbg_markers)

    # record and kill board
    record_buffer(board)
    kill_stream(board)

if __name__ == "__main__":
    main()

