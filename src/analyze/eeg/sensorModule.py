import argparse
import time
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def set_board():
    params = BrainFlowInputParams()
    params.serial_port = '/dev/ttyUSB0'
    BoardShim.enable_dev_board_logger()
    return BoardShim(0, params)

def start_record(board):
    board.prepare_session()
    # while not board.is_prepared():
    board.start_stream()
    
def stop_record(board):
    board.stop_stream()
    board.release_session()

def rail_test(signal):
    n_railed = 0
    is_railed = [{x:0} for x in range(0, signal.shape[0])]
    # print("Railed_channels : ", end = '')
    for ch in range(0, signal.shape[0]):
        val1,val2,val3 = signal[ch][1:4]

        if val1 == val2 and val2 == val3:
            n_railed += 1
            is_railed[ch] = True
            # print(ch+1, ", ", end = '')
        else: is_railed[ch] = False;
    return is_railed, n_railed

if __name__ == "__main__":
    print("Complete setting")
    