# 필요한 라이브러리들
from collections import defaultdict
import numpy as np

# Signal Processing Library
from scipy import signal
import pyeeg as pe
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
# =======================================================

# eeg signal을 변환하는 다양한 함수들을 정의
def computeFD(total_signal, chosen_channels): # 채널 인덱스 리스트
    fd_values = []
    
    for ch in chosen_channels:
        input_signal = total_signal[ch]
    
        fd = pe.hfd(input_signal, 5)
        fd_values.append(fd)
    return fd_values

def computefftMap(total_signal, chosen_channels, freqs, sf=128):
    # Init
    fftMap = False
        
    for ch in chosen_channels:  
        input_signal = total_signal[ch]
        
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