from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import numpy as np
import copy

def down_sampling(signal, chosen_channels):
    down_signal = []
    for ch in chosen_channels:
        copy_signal = copy.deepcopy(signal[ch]) # ch 단위로 카피해야함.. (이상함..아무튼 그럼..)
        down_signal.append(DataFilter.perform_downsampling(copy_signal, 2, AggOperations.MEAN.value))
    down_signal = np.array(down_signal)
    return down_signal

def filtering(signal, sf, chosen_channels):
    for ch in chosen_channels:
        copy_signal = copy.deepcopy(signal[ch])

        DataFilter.perform_lowpass(copy_signal, sf, 50.0, 5, FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
        DataFilter.perform_highpass (copy_signal, sf, 3.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        
        signal[ch] = copy_signal
    return signal


# 0과 1 사이로 scailing
def scale(signal):
    minVal = np.min(signal)
    maxVal = np.max(signal)
    
    signal = (signal - minVal) / (maxVal - minVal)     
    return signal

# 정규화
def normalize(signal):    
    n = np.linalg.norm(signal);
    signal = signal/n
        
    return signal

# 표준화 (평균이 0, 분산이 1 이 되도록.)
def standardize(signal):
    M = np.mean(signal);
    S = np.std(signal);
    signal = (signal - M) / S
    
    return signal