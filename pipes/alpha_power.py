"""
Sample Pipeline
This example uses the brainflow data_filter objects

Calculates alpha band power
"""
from brainflow.board_shim import BoardIds, BoardShim
from brainflow.data_filter import DataFilter 

def alpha_pipe(board : BoardShim):
    id = board.get_board_id()
    # sampling rate for frequency calculations
    sampling_rate = BoardShim.get_sampling_rate(id)
    # index of eeg channels
    eeg_channels = BoardShim.get_eeg_channels(id)
    # functional data pipe that is run by main program
    def pipe(data):
        # returns avg band powers and std deviations
        bands = DataFilter.get_avg_band_powers(data, 
                eeg_channels, 
                sampling_rate,
                True)
        return bands[0][0]
    return pipe
