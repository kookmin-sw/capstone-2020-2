from scipy import io # load .mat file
from openpyxl import load_workbook

# Channel 
SEED_channels = {'FP1': 0, 'FPZ': 1, 'FP2': 2, 'AF3': 3, 
                 'AF4': 4, 'F7': 5, 'F5': 6, 'F3': 7, 
                 'F1': 8, 'FZ': 9, 'F2': 10, 'F4': 11,
                 'F6': 12, 'F8': 13, 'FT7': 14, 'FC5': 15,
                 'FC3': 16, 'FC1': 17, 'FCZ': 18, 'FC2': 19,
                 'FC4': 20, 'FC6': 21, 'FT8': 22, 'T7': 23,
                 'C5': 24, 'C3': 25, 'C1': 26, 'CZ': 27,
                 'C2': 28, 'C4': 29, 'C6': 30, 'T8': 31,
                 'TP7': 32, 'CP5': 33, 'CP3': 34, 'CP1': 35,
                 'CPZ': 36, 'CP2': 37, 'CP4': 38, 'CP6': 39,
                 'TP8': 40, 'P7': 41, 'P5': 42, 'P3': 43,
                 'P1': 44, 'PZ': 45, 'P2': 46, 'P4': 47,
                 'P6': 48, 'P8': 49, 'PO7': 50, 'PO5': 51,
                 'PO3': 52, 'POZ': 53, 'PO4': 54, 'PO6': 55,
                 'PO8': 56, 'CB1': 57, 'O1': 58, 'OZ': 59,
                 'O2': 60, 'CB2': 61}

SEED_all_channel_names = list(SEED_channels.keys())
SEED_all_channel_values = list(SEED_channels.values())

DEAP_channels = {"FP1":0, "AF3":1, "F3":2, "F7":3,
                 "FC5":4, "FC1":5, "C3":6, "T7":7,
                 "CP5":8, "CP1":9, "P3":10,
                 "P7":11, "PO3":12, "O1":13, 
                 "OZ":14, "PZ":15, "FP2":16, 
                 "AF4":17, "FZ":18, "F4":19,
                 "F8":20, "FC6":21, "FC2":22,
                 "CZ":23, "C4":24, "T8":25,
                 "CP6":26, "CP2":27, "P4":28,
                 "P8":29, "PO4":30, "O2":31}

DEAP_all_channel_names = list(DEAP_channels.keys())
DEAP_all_channel_values = list(DEAP_channels.values())