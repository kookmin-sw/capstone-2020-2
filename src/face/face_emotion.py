# import
import os
import copy
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
from sklearn.metrics import plot_confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame




dataset_path = "dataset/FER2013/fer2013/fer2013.csv"
image_size = (48,48)

# 하이퍼 파라미터 설정
batch_size = 64
num_epochs = 100
# num_epochs = 10
input_shape = (1, 48, 48)
validation_split = 0.2
verbose = 1
num_classes = 7
patience = 50

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

        # output = F.softmax(x, dim=0)

        return x

    def predict(self, x):
        x = self.forward(x)
        output = F.softmax(x, dim=1)

        return output



def loading_dataset():
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
    dataset_test = MyDataset(df_data=test,transform=None)

    loader_train = DataLoader(dataset=dataset_train, batch_size=batch_size, shuffle=True, num_workers=0)
    loader_val = DataLoader(dataset=dataset_val, batch_size=batch_size, shuffle=True, num_workers=0)
    loader_test = DataLoader(dataset=dataset_test, batch_size=batch_size, shuffle=True, num_workers=0)

    return loader_train, loader_val, loader_test



def training_model():
    # GPU 설정
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # GPU 설정 확인
    print("GPU : ", torch.cuda.is_available())

    # model 객체 생성
    model = FaceEmotion()
    print("Network 생성")
    model.cuda()

    criterion = nn.CrossEntropyLoss()
    # optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

    best_acc = 0
    best_model = model

    for epoch in range(0, num_epochs):    
        # Training
        model.train(True)
        running_loss = 0.0
        running_corrects = 0
        running_total = 0
        total_step = len(loader_train)
        for i, (images, labels) in enumerate(loader_train):
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)

            y_true = labels.cpu().numpy()
            _, predicted = torch.max(outputs.data, 1)
            # predicted = predicted.cpu().numpy()

            optimizer.zero_grad()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            # running_corrects += torch.sum(predicted == labels.data)
            # running_corrects += (predicted == labels).sum().item()
            running_corrects += sum(1 for a, b in zip(predicted, labels) if a == b)
            running_total += len(y_true)

        # Traing Epoch 한 번 끝.
        epoch_loss = running_loss / len(loader_train)
        epoch_acc = 100 * running_corrects / running_total

            # if (i%100) == 0:
                # print(outputs[0])
                # print(f"labels shape : {labels.shape}, outputs shape : {outputs.shape}")
        
        print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}], Train Accuracy : {epoch_acc}, Train Loss : {loss.item()}")

        # validation
        model.train(False)
        running_loss = 0.0
        running_corrects = 0
        running_total = 0
        total_step = len(loader_val)
        for i, (images, labels) in enumerate(loader_val):
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)

            y_true = labels.cpu().numpy()
            _, predicted = torch.max(outputs.data, 1)
            predicted = predicted.cpu().numpy()
            
            
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            # running_corrects += torch.sum(predicted == labels.data)
            # running_corrects += (predicted == labels).sum().item()
            running_corrects += sum(1 for a, b in zip(predicted, labels) if a == b)
            running_total += len(y_true)
        
        # Validation Epoch 한 번 끝
        # 평균 loss, accuracy 구하기
        epoch_loss = running_loss / len(loader_val)
        epoch_acc = 100 * running_corrects / running_total

        print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}], Val accuracy : {epoch_acc}")
        # 가장 성능이 좋았던 epoch 에서의 모델을 저장.
        if epoch_acc > best_acc:
            print("Best Model is saved...")
            best_acc = epoch_acc
            best_model = copy.deepcopy(model)
            # class_names = ['Angry', 'Fear','Disgust', 'Happy', 'Sad', 'Surprised', 'Neutral']
            # print(classification_report(y_true, predicted, zero_division=0))

    print("학습 끝. 모델 저장.")
    torch.save(best_model.state_dict(), "FaceEmotionModel.pt") 



def confusion_matrix(preds, labels, conf_matrix):
    preds = torch.argmax(preds, 1)
    for p, t in zip(preds, labels):
        conf_matrix[p, t] += 1
    return conf_matrix



def test_model():
    # GPU 설정
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # GPU 설정 확인
    print("GPU : ", torch.cuda.is_available())

    model = FaceEmotion()
    model.load_state_dict(torch.load("FaceEmotionModel.pt"))
    model.cuda()
    model.train(False)

    conf_matrix = np.zeros((7, 7))

    class_total = [0, 0, 0, 0, 0, 0, 0]
    class_correct = [0, 0, 0, 0, 0, 0, 0]
   
    running_loss = 0.0
    running_corrects = 0
    running_total = 0

    total_step = len(loader_test)
    for i, (images, labels) in enumerate(loader_test):
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)

        conf_matrix = confusion_matrix(outputs, labels, conf_matrix)

        y_true = labels.cpu().numpy()
        _, predicted = torch.max(outputs.data, 1)

        c = (predicted == labels).squeeze()
        for idx in range(len(labels)):
            label = labels[idx]
            pred = predicted[idx]
            if label == pred:
                class_correct[label] += 1
            class_total[label] += 1
        
        if (i % 10 == 0):
            print (f"Step : {i+1} / {total_step}")
        

    class_names = ['Angry', 'Fear','Disgust', 'Happy', 'Sad', 'Surprised', 'Neutral']
    for emotion in range(0, 7):
        print(f"Accuracy of {class_names[emotion]} : {100 * class_correct[emotion] / class_total[emotion]}")

    df = DataFrame(conf_matrix, index=class_names, columns=class_names)
    print(df)
    plt.figure(figsize=(15, 15))
    sns.heatmap(df, annot=True)


if __name__ == "__main__":
    loading_dataset()
    training_model()