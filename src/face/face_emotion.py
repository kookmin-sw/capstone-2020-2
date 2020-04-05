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

# GPU 설정
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# GPU 설정 확인
print(torch.cuda.is_available())



# 하이퍼 파라미터 설정 (일단 아무값이나 주고...)
num_epochs = 10
num_classes = 7
batch_size = 128
learning_rate = 0.001

'''
class MyDataset(Dataset):
    def __init__(self, df_data, data_dir="./", transform=None):
        super().__init__()
        self.df = df_data.values
        self.data_dir = data_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        img_name, label = self.df[index]
        img_path = os.path.join(self.data_dir, img_name + ".jpg")
        image = cv2.imread(img_path)
        
        if self.transform is not None:
            image = self.transform(image)

        return image, label
'''

trans1 = transforms.Compose([transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                            ])
trans2 = transforms.Compose([transforms.resize(64, 64),
                            transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                            ])
train_dataset_path = "dataset/Face_expression_recognition_dataset/images/train"
train_dataset = torchvision.datasets.ImageFolder(root=train_dataset_path, transform=trans1)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    

############ 기존 코드에서 stride 안 줬을 때 디폴트 값 몇인지 찾아보기..
############ 케라스 Conv2D 랑 SeparableConv2D
class FaceEmotion(nn.Module):
    def __init__(self, num_classes=7):
        super(FaceEmotion, self).__init__()

        # base block
        self.base_block = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=8, out_channels=8, kernel_size=3),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True))

        # Residual black 1 - shortcut
        self.shortcut_1 = nn.Sequential(
            nn.BatchNorm2d(16),
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=1, stride=2, bias=False))

        # Residual block 1
        self.residual_block_1 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1,bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(16),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 2 - shortcut
        self.shortcut_2 = nn.Sequential(
            nn.BatchNorm2d(32),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=1, stride=2, bias=False))

        # Residual block 2
        self.residual_block_2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1,bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 3 - shortcut
        self.shortcut_3 = nn.Sequential(
            nn.BatchNorm2d(64),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=1, stride=2, bias=False))

        # Residual block 3
        self.residual_block_3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1,bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),

            nn.MaxPool2d(kernel_size=3, stride=2))

        # Residual black 4 - shortcut
        self.shortcut_4 = nn.Sequential(
            nn.BatchNorm2d(128),
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=1, stride=2, bias=False))

        # Residual block 4
        self.residual_block_4 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1,bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),

            nn.MaxPool2d(kernel_size=3, stride=2))
        
        # 아웃 채널은 클래스의 수 7가지...
        self.last_block = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=7, kernel_size=3),
            nn.AdaptiveAvgPool2d((1, 1))        # 인자로 주는 값은 결과물의 H x W : 전역평균
        )

    def forward(self, x):
        x = self.base_block(x)
        x = self.residual_block_1(x) + shortcut_1(x)
        x = self.residual_block_2(x) + shortcut_2(x)
        x = self.residual_block_3(x) + shortcut_3(x)
        x = self.residual_block_4(x) + shortcut_4(x)

        x = self.last_block(x)

        # 벡터로 펴준다.
        x = x.view(x.size(0), -1)

        output = F.softmax(x, dim=0)

        return output