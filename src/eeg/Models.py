# Model class
import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self, n_channel, lin_len, out_len, n_electrodes, model_type):
        super(CNN, self).__init__()
        self.pool = nn.MaxPool2d(2) 
        
        self.conv1 = nn.Conv2d(n_channel, 8, 3)  # 8 => 4*
        self.batch1 = nn.BatchNorm2d(8) # 8=>4*

        self.conv2 = nn.Conv2d(8, 4, 3)
        self.batch2 = nn.BatchNorm2d(4)
        
        self.fc1 = nn.Linear(lin_len, 8) # 죽어라 이연지** 64=>8*
        self.fc2 = nn.Linear(8, out_len) 
        
        self.n_electrodes = n_electrodes
        self.model_type = model_type
        
        self.lin_len = lin_len

    def forward(self, x):
        # conv => batch => pool => relu
        if self.n_electrodes == 32:
            x = F.relu(self.pool(self.batch1(self.conv1(x))))
        elif self.n_electrodes == 8:
            x = F.relu(self.batch1(self.conv1(x))) # ch 8
        x = self.conv2(x)
        x = x.view(-1, self.lin_len)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        if self.model_type == "reg":
            return x
        else:
            return F.softmax(x, dim=1)