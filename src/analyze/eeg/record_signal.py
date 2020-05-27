from sensorModule import *
import pickle
import numpy as np
import keyboard
import sys

n_sec = 6
n_ch = 8
sf =  256 #board.get_sampling_rate(0)
eeg_channels = [i for i in range(0,8)]
splitted_signal = []


# =======================================
if __name__ == '__main__':
    has_sensor = True if sys.argv[1] == 'y' else False
    
    if has_sensor:
        try:
            board = set_board() 
            start_record(board)
        except:
            print("Can't connect to an EEG sensor")
            sys.exit(1)
        
    while True:
        if keyboard.is_pressed('q') :
            break
        time.sleep(1) # save recent n_seconds signal for every 1 second.
        if has_sensor:
            temp_signal = board.get_current_board_data(n_sec * sf) # latest data from a board **
        else:
            temp_signal = np.random.rand(8, n_sec * sf)
        
        temp_signal = temp_signal[eeg_channels, :]
        print(temp_signal.shape)

        railed_channels, n_railed  = rail_test(temp_signal)
        if n_railed != 0:
            print("Railed Channels = ", railed_channels)
            continue # do not saved railed signals?
        splitted_signal.append(temp_signal)

        # save 
        with open("test_signal.txt", 'wb') as f:
            pickle.dump(temp_signal, f)
            
    # whole signal (Warn : could contain railed signals)
    if has_sensor:
        total_signal = board.get_board_data() # get all data and remove it from internal buffer
        total_signal = total_signal[eeg_channels, :]
        print("Total signal length = ", total_signal.shape[1] // sf)

        stop_record(board)
    print("Connection closed")
    sys.exit(0)