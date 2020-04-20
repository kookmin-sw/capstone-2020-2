# import
import os
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import TensorDataset, DataLoader, Dataset




class FaceEmotion(nn.Module):
    def __init__(self, input_channel=3, num_classes=7):
        super(FaceEmotion, self).__init__()

        # base block
        self.base_block = nn.Sequential(
            nn.Conv2d(in_channels=input_channel, out_channels=8, kernel_size=3, stride=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=8, out_channels=8, kernel_size=3, stride=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True))

        # Residual black 1 - shortcut
        self.shortcut_1 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=1, stride=2, bias=False),
            nn.BatchNorm2d(16))

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
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=1, stride=2, bias=False),
            nn.BatchNorm2d(32))

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
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=1, stride=2, bias=False),
            nn.BatchNorm2d(64))

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
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=1, stride=2, bias=False),
            nn.BatchNorm2d(128))

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
        print(x.shape)
        x = self.base_block(x)
        print("base_block shape", x.shape)
        res_x_1 = self.residual_block_1(x)
        print("res_x_1 shape", res_x_1.shape)
        short_x_1 = self.shortcut_1(x)
        print("short_x_1 shape", short_x_1.shape)
        x = res_x_1 + short_x_1
        print(x.shape)
        x = self.residual_block_2(x) + self.shortcut_2(x)
        x = self.residual_block_3(x) + self.shortcut_3(x)
        x = self.residual_block_4(x) + self.shortcut_4(x)

        x = self.last_block(x)

        # 벡터로 펴준다.
        x = x.view(x.size(0), -1)

        output = F.softmax(x, dim=0)

        return output



# GPU 설정
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# GPU 설정 확인
print(torch.cuda.is_available())

# 하이퍼 파라미터 설정
num_epochs = 10
num_classes = 7
batch_size = 128
learning_rate = 0.001


trans1 = transforms.Compose([transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                            ])
'''
trans2 = transforms.Compose([transforms.resize(64, 64),
                            transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                            ])
'''
train_dataset_path = "dataset/Face_expression_recognition_dataset/images/train"
train_dataset = torchvision.datasets.ImageFolder(root=train_dataset_path, transform=trans1)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    

# model 객체 생성
model = FaceEmotion()
print("Network 생성")
print(model)
model.cuda()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

total_step = len(train_loader)
for epoch in range(0, num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backword()
        optimizer.step()
        
        if (i%10) == 0:
            print(f"Epoch [{i}/{num_epochs}], Step [{i+1}/{total_step}, Loss : {loss.item}")

print("학습 끝. 모델 저장.")
torch.save(model, "FaceEmotionModel.pt")