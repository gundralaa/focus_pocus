# Correlation Pipes

from lib.pipe import Pipe
from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter
import numpy as np

def corr_pipe(board : BoardShim) -> Pipe:
    id = board.get_board_id()
    eeg_chan = BoardShim.get_eeg_channels(id)
    def apply(data):
        eeg_raw = data[eeg_chan]
        return np.correlate(eeg_raw[0], eeg_raw[-1])[0]
    return Pipe(apply, name="cross-correlation")
