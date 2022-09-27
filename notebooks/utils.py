# Data Utils
import numpy as np
import mne
from brainflow.board_shim import BoardShim

def create_mne_info(board_id):
    eeg_ch_ind = BoardShim.get_eeg_channels(board_id)
    sf = BoardShim.get_sampling_rate(board_id)
    ch_name =  ['marker'] + BoardShim.get_eeg_names(board_id)
    ch_type = ['stim'] + ['eeg'] * len(eeg_ch_ind)
    return mne.create_info(ch_name, sf, ch_type)

def data_to_mne_raw(board_id, data):
    info = create_mne_info(board_id)
    # convert data values
    data[1:] *= 1e-6
    return mne.io.RawArray(data, info)
    

    

