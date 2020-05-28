import torch
import torchvision


# label preprocessing for DEAP dataset 
def process_label(val, numOfClass=2): 
    # 2 class
    if numOfClass == 2:
        if val > 5:
            return 1
        else:
            return 0
    # 3 class
    elif numOfClass == 3:
        if val > 6:
            return 2 # high
        elif val < 4:
            return 0 # low
        else:
            return 1 # neutral  

# Custom dataset class
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader

transform = transforms.Compose([transforms.ToTensor()])

class EEG_Dataset(Dataset):
    # load, split
    def __init__(self, data_list, dataset, target=-1, transform=None):
        self.data_list = data_list
        self.transform = transform
        self.dataset = dataset
        self.target = target
        
    def __len__(self):
        return len(self.data_list)
    
    def __getitem__(self, idx):
        if self.dataset == 'DEAP':
            spectro, label = self.data_list[idx][0], self.data_list[idx][1][self.target]
        elif self.dataset == 'SEED' or self.dataset == 'BCI':
            spectro, label = self.data_list[idx][0], self.data_list[idx][1]
        if self.transform:
            spectro = self.transform(spectro)
        return spectro, label

# Convert loaded dataset into a custom dataset instance
def get_train_test_set(train, test, bs, dataset):
    trainset = EEG_Dataset(train, dataset, target=-1, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=bs,
                                              shuffle=True, num_workers=2)
    testset = EEG_Dataset(test, dataset, target=-1, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=bs,
                                             shuffle=False, num_workers=2)
    return trainset, trainloader, testset, testloader

if __name__ == "__main__":
    print("환경설정 완료")