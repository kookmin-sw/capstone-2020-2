import numpy as np

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