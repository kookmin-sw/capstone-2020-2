# import
import os
import numpy as np
import pandas as pd
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import TensorDataset, DataLoader, Dataset

# 하이퍼 파라미터 설정 (일단 아무값이나 주고...)
num_epochs = 10
num_classes = 7
batch_size = 128
learning_rate = 0.001

# GPU 설정
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# GPU 설정 확인
print(torch.cuda.is_available())

################################### Model 설계 ###################################
# Conv2D:(3,3)x8 -> BatchNorm -> ReLU -> Conv2D:(3,3)x8 -> BatchNorm -> ReLU
# 두 갈래로 갈라짐
# 1) -> Sep-Conv2D:(3,3)x16-> BatchNorm -> ReLU -> Sep-Conv2D:(3x3)x16 -> BatchNorm -> MaxPooling
# 2) Conv2D -> BatchNorm
# 이 둘의 결과를 더함.
# -> Conv2D -> GlobalAveragePooling -> Softmax
    

############ 기존 코드에서 stride 안 줬을 때 디폴트 값 몇인지 찾아보기..
############ 케라스 Conv2D 랑 SeparableConv2D
class FaceEmotion(nn.Module):
    def __init__(self, block, num_classes=7):
        super(FaceEmotion, self).__init__()

        # base block
        self.base_block = nn.Sequencial(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, stride=1),
            nn.BatchNorm2d(8),
            nn.Conv2d(in_channels=8, out_channels=8, kernel_size=3, stride=1),
            nn.BatchNorm2d(8))

        # Residual black 1 - shortcut
        self.shortcut_1 = nn.BatchNorm2d(16)(nn.Conv2d(in_channels=8, out_channels=16, kernel_size=1, stride=2, biase=False))

        # Residual block 1
        self.residual_block_1 = nn.Sequencial(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=stride, padding=1,bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(out_channels=16, out_channels=16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 2 - shortcut
        self.shortcut_2 = nn.BatchNorm2d(32)(nn.Conv2d(in_channels=16, out_channels=32, kernel_size=1, stride=2, biase=False))

        # Residual block 2
        self.residual_block_2 = nn.Sequencial(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=stride, padding=1,bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(out_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 3 - shortcut
        self.shortcut_3 = nn.BatchNorm2d(64)(nn.Conv2d(in_channels=32, out_channels=64, kernel_size=1, stride=2, biase=False))

        # Residual block 3
        self.residual_block_3 = nn.Sequencial(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=stride, padding=1,bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(out_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 4 - shortcut
        self.shortcut_4 = nn.BatchNorm2d(128)(nn.Conv2d(in_channels=64, out_channels=128, kernel_size=1, stride=2, biase=False))

        # Residual block 4
        self.residual_block_4 = nn.Sequencial(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=stride, padding=1,bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(out_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(128),

            nn.MaxPool2d(kernel_size=3, stride=2))
        
        # 아웃 채널은 클래스의 수 7가지...
        self.last_conv = nn.Conv2d(in_channels=128, out_channels=7, kernel_size=3)
        ######### 여기 global average pooling 들어가야되는데 이거 값은 뭐로 준 거지..?
        ######### 기존 코드에서는 x = GlobalAveragePooling2D()(x) 라고만 되어 있음.. 찾아 보자...
        self.global_avg_pooling = ....
    

    def forward(self, x):
        x = self.base_block(x)
        x = self.residual_block_1(x) + shortcut_1(x)
        x = self.residual_block_2(x) + shortcut_2(x)
        x = self.residual_block_3(x) + shortcut_3(x)
        x = self.residual_block_4(x) + shortcut_4(x)

        x = self.last_conv(x)
        x = self.global_avg_pooling(x)

        # 벡터로 펴준다.
        x = x.view(x.size(0), -1)

        output = F.softmax(x, dim=0)

        return output