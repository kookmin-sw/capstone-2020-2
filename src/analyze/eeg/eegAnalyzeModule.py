# Signal Preprocessing Methods
from preprocessModule import *
# Signal => Input form 
from transformModule import *
import numpy as np
import torch

emo_map = {0 : "neutral", 1 : "happiness", 2 : "sadness", 
           3:"disgust", 4 : "fear", 5 : "anger", 6:"surprise"}
def predict_emotion_EEG(model, signal, chosen_channels, freqs, sf):
    # preprocessing
    copied_signal = copy.deepcopy(signal)
    copied_signal = down_sampling(copied_signal, chosen_channels)
    copied_signal = filtering(copied_signal, sf, chosen_channels)
    signal = copied_signal
    
    # transform into an input form
    fftMap = computefftMap(signal, chosen_channels, freqs, sf)
    fftMap = np.expand_dims(fftMap, axis=0)
    fftMap = np.expand_dims(fftMap, axis=0)
    fftMap_tensor = torch.from_numpy(fftMap)
    
    outputs = model(fftMap_tensor.float()) 
    max_idx = np.argmax(outputs[0,:].detach().numpy())
    
    return emo_map[max_idx]