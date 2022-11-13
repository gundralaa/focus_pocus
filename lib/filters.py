"""
Pipes for filtering time signals in a streaming setting
TODO: Optimize the ideas to use vector calculus
"""
from lib.pipe import Pipe
from brainflow.data_filter import DataFilter
from brainflow.board_shim import BoardShim

def low_pass_pipe(board: BoardShim) -> Pipe:
    def apply(data):
        return DataFilter.perform_lowpass(data, board.get_sampling_rate) 
