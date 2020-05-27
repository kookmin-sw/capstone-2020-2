 #-*- coding: utf-8 -*- 
from preprocessModule import * # Signal Preprocessing Methods
from transformModule import * # Signal => Input form 
import numpy as np
import torch
import pickle

# setting
freqs = [freq for freq in range(4,46,1)]
chosen_channels = [i for i in range(0, 8)]
sf = 256
emo_map = {0 : "neutral", 1 : "sadness", 2 : "happiness", 
           3 : "disgust", 4 : "fear"}#, 5 : "anger", 6:"surprise"}

# load trained model 
from Models import * # CNN 

model = CNN(n_channel=1, lin_len=592, out_len=5,
            n_electrodes=8, model_type='cla')
model.load_state_dict(torch.load("eeg_classifier.pth"))
model.eval()


def rail_test(signal):
    n_railed = 0
    is_railed = [{x:0} for x in range(0, signal.shape[0])]
    # print("Railed_channels : ", end = '')
    for ch in range(0, signal.shape[0]):
        val1,val2,val3 = signal[ch][1:4]

        if val1 == val2 and val2 == val3:
            n_railed += 1
            is_railed[ch] = True
            print(ch+1, ", ", end = '')
        else: is_railed[ch] = False;
    return is_railed, n_railed


def predict_emotion_EEG(model, signal_path, chosen_channels, freqs, sf=256):
    # signal = read_signal_from_txt(signal_path)
    with open(signal_path, 'rb') as f:
        signal = pickle.load(f)
    
    is_railed, n_railed = rail_test(signal)
    
    # preprocessing
    copied_signal = copy.deepcopy(signal)
    copied_signal = down_sampling(copied_signal, chosen_channels)
    sf = sf // 2
    copied_signal = filtering(copied_signal, sf, chosen_channels)
    signal = copied_signal
    
    # transform into an input form
    fftMap = computefftMap(signal, chosen_channels, freqs, sf)
    fftMap = np.expand_dims(fftMap, axis=0)
    fftMap = np.expand_dims(fftMap, axis=0)
    fftMap_tensor = torch.from_numpy(fftMap)
    
    outputs = model(fftMap_tensor.float()) 
    #max_idx = np.argmax(outputs[0,:].detach().numpy())
    
    emo_dict = {}
    for idx, emo_class in emo_map.items():
        emo_dict[emo_class] = outputs[0][idx] 
        
    return emo_dict, n_railed, is_railed

if __name__ == "__main__":
    print("환경설정 완료")