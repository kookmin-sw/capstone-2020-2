import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

# parameters 
eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_BOARD.value)
n_sec = 6
n_ch = 8
sf =  256 #board.get_sampling_rate(0)

# railed channels
is_railed = [{x:0} for x in range(0, 8)]
threshold_railed = int(pow(2,23)-1000) #fully railed should be +/- 2^23
threshold_railed_warn = int(pow(2,23) * 0.75)

def set_board():
    params = BrainFlowInputParams()
    params.serial_port = 'COM8'
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
    #print("Railed_channels : ", end = '')
    for ch in range(0, n_ch):
        val1,val2,val3 = temp_signal[ch][1:4]

        if val1 == val2 and val2 == val3:
            is_railed[ch] = True
            print(ch+1, ", ", end = '')
        else: is_railed[ch] = False;
    return is_railed