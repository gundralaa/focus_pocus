# Data Utils
import numpy as np
import mne
from brainflow.board_shim import BoardShim

def create_mne_info(board_id):
    eeg_ch_ind = BoardShim.get_eeg_channels(board_id)
    sf = BoardShim.get_sampling_rate(board_id)
    ch_name = ['time'] + ['marker'] + BoardShim.get_eeg_names(board_id)
    ch_type = ['misc'] * 2 + ['eeg'] * len(eeg_ch_ind)
    return mne.create_info(ch_name, sf, ch_type)

def data_to_mne_raw(board_id, data):
    info = create_mne_info(board_id)
    return mne.io.RawArray(data, info)
    

    

