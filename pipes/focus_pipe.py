"""
Sample Pipeline
This example uses the brainflow data_filter objects

Calculates alpha band power
"""
from pipes.pipe import Pipe
from brainflow.board_shim import BoardIds, BoardShim
from brainflow.data_filter import DataFilter 
import numpy as np

# NOTE
# bands = [delta, theta, alpha, beta, gamma]

class Bands:
    DELTA=0
    THETA=1
    ALPHA=2
    BETA=3
    GAMMA=4


def alpha(bands):
    # returns alpha wave avg
    return bands[Bands.ALPHA]

def ratio_theta(bands):
    # ratio alpha / theta
    return bands[Bands.ALPHA] / bands[Bands.THETA]

def total_ratio(bands):
    # ratio alpha / sum
    return bands[Bands.ALPHA] / sum(bands)

# IN: 2D EEG Data -> multichannel time domain
# OUT: Band Data -> see pipe_desc
def band_pipe(board : BoardShim) -> Pipe:
    id = board.get_board_id()
    sampling_rate = BoardShim.get_sampling_rate(id)
    eeg_channels = BoardShim.get_eeg_channels(id)
    def apply(data):
        bands_data = DataFilter.get_avg_band_powers(data, 
                eeg_channels, 
                sampling_rate,
                True)
        return bands_data
    return Pipe(apply)

# IN: 2D EEG Data -> multichannel time domain
# OUT: Focus Heuristic
def focus_pipe(board : BoardShim, heur='alpha') -> Pipe:
    # ADD INIT CODE HERE
    # ex samp_rate, channel_number
    bands_p = band_pipe(board)
    # ---- PIPE FUNCTION ----
    def apply(data):
        bands = bands_p.apply(data)[0]
        focus = 0
        if heur == 'alpha': focus = alpha(bands)
        elif heur == 'theta_ratio': focus = ratio_theta(bands)
        elif heur == 'total_ratio': focus = total_ratio(bands)
        return focus
    return Pipe(apply, name='focus')