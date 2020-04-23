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
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report




dataset_path = "dataset/FER2013/fer2013/fer2013.csv"
image_size = (48,48)

# 하이퍼 파라미터 설정
batch_size = 32
# num_epochs = 110
num_epochs = 10
input_shape = (1, 48, 48)
validation_split = 0.2
verbose = 1
num_classes = 7
patience = 50
base_path = 'models/'
learning_rate = 0.001
l2_regularization = 0.01



class MyDataset(Dataset):
    def __init__(self, df_data, transform=None):
        super().__init__()
        pixels = df_data['pixels'].tolist()
        width, height = 48, 48
        faces = []
        for pixel_sequence in pixels:
            face = [int(pixel) for pixel in pixel_sequence.split(' ')]
            face = np.asarray(face).reshape(1, width, height)
            # face = cv2.resize(face.astype('uint8'), image_size)
            faces.append(face.astype('float32'))
        
        self.faces = np.asarray(faces)
        # self.faces = np.expand_dims(faces, -1)
        # self.emotions = pd.get_dummies(df_data['emotion']).values
        self.emotions = df_data['emotion'].values
        self.transform = transform
        print(self.faces[0].shape)

    def __len__(self):
        return self.emotions.shape[0]
    
    def __getitem__(self, index):
        return self.faces[index], self.emotions[index]




class FaceEmotion(nn.Module):
    def __init__(self, num_classes=num_classes):
        super(FaceEmotion, self).__init__()

        # base block
        self.base_block = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=8, out_channels=8, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True))

        # Residual black 1 - shortcut
        self.shortcut_1 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16))

        # Residual block 1
        self.residual_block_1 = nn.Sequential(
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(16),

            # nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
        )

        # Residual black 2 - shortcut
        self.shortcut_2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32))

        # Residual block 2
        self.residual_block_2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),

            # nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
        )

        # Residual black 3 - shortcut
        self.shortcut_3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64))

        # Residual block 3
        self.residual_block_3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),

            # nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
        )

        # Residual black 4 - shortcut
        self.shortcut_4 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(128))

        # Residual block 4
        self.residual_block_4 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),

            # nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
        )

        # 아웃 채널은 클래스의 수 7가지...
        self.last_block = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=num_classes, kernel_size=3),
            nn.AdaptiveAvgPool2d((1, 1))        # 인자로 주는 값은 결과물의 H x W : 전역평균
        )

    def forward(self, x):
        x = self.base_block(x)
        x = self.residual_block_1(x) + self.shortcut_1(x)
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
print("GPU : ", torch.cuda.is_available())

# Dataset 불러오기
print("Dataset Loading...")
trans_train = transforms.Compose([transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                            transforms.RandomRotation(10),
                            transforms.RandomHorizontalFlip(),
                            ])
trans_val = transforms.Compose([transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                            ])

data = pd.read_csv(dataset_path)
print(f"Dataset size : {len(data)}")
train, test = train_test_split(data, test_size=0.2, shuffle=True)
train, val = train_test_split(train, test_size=validation_split, shuffle=False)
print(f"train : {len(train)} + val {len(val)} / test : {len(test)}")

dataset_train = MyDataset(df_data=train, transform=trans_train)
dataset_val = MyDataset(df_data=val, transform=trans_val)

loader_train = DataLoader(dataset=dataset_train, batch_size=batch_size, shuffle=False, num_workers=0)
loader_val = DataLoader(dataset=dataset_val, batch_size=batch_size//2, shuffle=False,num_workers=0)



# model 객체 생성
model = FaceEmotion()
print("Network 생성")
# print(model)
model.cuda()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=l2_regularization)

total_step = len(loader_train)
for epoch in range(0, num_epochs):
    for i, (images, labels) in enumerate(loader_train):
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)

        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i%50) == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}], Loss : {loss.item()}")
            print(classification_report(labels, outputs, target_names=['class 1', 'class 2', 'class 3',
                                                'class 4', 'class 5', 'class 6', 'class 7']))


model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in loader_val:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f"Accuracy of the model for validation : {100 * correct / total}")


print("학습 끝. 모델 저장.")
torch.save(model, "FaceEmotionModel.pt")