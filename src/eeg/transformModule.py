# 필요한 라이브러리들
from collections import defaultdict
import numpy as np

# Signal Processing Library
from scipy import signal
import pyeeg as pe
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

base_num_DEAP = 1280

channels = {
    "FP1" : {"Tw" : 0, "Ge" : 0},
    "AF3" : {"Tw" : 1, "Ge" : 1},
    "F3" : {"Tw" : 3, "Ge" : 2}, 
    "F7" : {"Tw" : 2, "Ge" : 3}, 
    "FC5" : {"Tw" : 5, "Ge" : 4}, 
    "FC1" : {"Tw" : 4, "Ge" : 5}, 
    "C3" : {"Tw" : 7, "Ge" : 6}, 
    "T7" : {"Tw" : 6, "Ge" : 7}, 
    "CP5" : {"Tw" : 9, "Ge" : 8}, 
    "CP1" : {"Tw" : 8, "Ge" : 9}, 
    "P3" : {"Tw" : 11, "Ge" : 10}, 
    "P7" : {"Tw" : 10, "Ge" : 11}, 
    "PO3" : {"Tw" : 13, "Ge" : 12}, 
    "O1" : {"Tw" : 14, "Ge" : 13}, 
    "OZ" : {"Tw" : 15, "Ge" : 14},
    "PZ" : {"Tw" : 12, "Ge" : 15}, 
    "FP2" : {"Tw" : 29, "Ge" : 16}, 
    "AF4" : {"Tw" : 28, "Ge" : 17}, 
    "FZ" : {"Tw" : 30, "Ge" : 18}, 
    "F4" : {"Tw" : 26, "Ge" : 19}, 
    "F8" : {"Tw" : 27, "Ge" : 20}, 
    "FC6" : {"Tw" : 24, "Ge" : 21}, 
    "FC2" : {"Tw" : 25, "Ge" : 22},
    "CZ" : {"Tw" : 31, "Ge" : 23}, 
    "C4" : {"Tw" : 22, "Ge" : 24}, 
    "T8" : {"Tw" : 23, "Ge" : 25}, 
    "CP6" : {"Tw" : 20, "Ge" : 26}, 
    "CP2" : {"Tw" : 21, "Ge" : 27}, 
    "P4" : {"Tw" : 18, "Ge" : 28}, 
    "P8" : {"Tw" : 19, "Ge" : 29}, 
    "PO4" : {"Tw" : 17, "Ge" : 30},
    "O2" : {"Tw" : 16, "Ge" : 31} 
}

# (1 ~ 22) : Twente, (23 ~ 32) : Geneva
# hw = "Tw" if participant_id <= 22 else "Ge" # 이거 아니래
hw = "Ge" 

all_channels = list(channels.keys())
# =======================================================

# eeg signal을 변환하는 다양한 함수들을 정의
def computeFD(total_signal, chosen_channels):
    fd_values = []
    
    for ch, idx in channels.items():
        if ch not in chosen_channels: continue     
        input_signal = total_signal[channels[ch][hw]]
    
        fd = pe.hfd(input_signal, 5)
        fd_values.append(fd)
    return fd_values

def computefftMap(total_signal, chosen_channels, freqs, sf=128):
    # Init
    fftMap = False
        
    for ch, idx in channels.items():
        if ch not in chosen_channels: continue     
        input_signal = total_signal[channels[ch][hw]]
        
        # Fast Fourier Transform ========================
        ffts = pe.bin_power(input_signal, freqs, sf)
        fft = ffts[1]
        # ===============================================
        
        # FFT Map
        if type(fftMap) == bool: 
            fftMap = fft
        else:
            fftMap = np.vstack((fftMap, fft)) 
    return fftMap