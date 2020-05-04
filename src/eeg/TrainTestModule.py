# Test method
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    
    # Begin CHANGES
    fst_empty_cell = (columnwidth-3)//2 * " " + "t/p" + (columnwidth-3)//2 * " "
    
    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    # Print header
    print("    " + fst_empty_cell, end=" ")
    # End CHANGES
    
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
        
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()
        
def testModel(net, testloader, target_names, criterion, model_type,  detail=False):
    numOfClass = len(target_names)
    co = 0 # 맞은 개수
    to = 0 # 테스트셋 개수

    # [[0,0,0], [0,0,0], [0,0,0]] 
    conf_mat = [[0 for i in range(numOfClass)] for j in range(numOfClass)] 

    
    all_label = []
    all_out = []
    with torch.no_grad():
        running_loss = 0
        for data in testloader:
            images, labels = data
            outputs = net(images.float()) 
            loss = criterion(outputs, labels)
            running_loss += loss.item()

            # Update Confusion Matrix ==============================
            for i in range(len(outputs)):
                to += 1
                # ===============================print
                if detail:
                    if to <= 10:
                        print("Output : ", outputs[i])
                        print("Label : ", labels[i])
                    else: break
                # ===================================

                if model_type == "cla":
                    predicted = np.argmax(np.array(outputs[i])); 
                    label = labels[i].item()
                elif model_type == "reg":
                    predicted = 0 if outputs[i] < 5 else 1
                    label = 0 if labels[i].item() < 5 else 1
                
                all_label.append(label)
                all_out.append(predicted)
                
                conf_mat[predicted][label]+=1
                
                if predicted == label: 
                    co += 1
          # ===========================================================
        loss = running_loss/len(testloader.dataset)
        acc = 100 * (co / to)

        cm = confusion_matrix(all_label, all_out, labels = [i for i in range(0,numOfClass)])
        print_cm(cm, target_names)
        
        print("V_loss = %.06f  Acc = %.04f "%(loss, acc))
        return loss, acc, 1 #f1_score

    
# Train method
def train_model(net, model_type, trainloader, testloader, target_names, epoch=100, detail=True):
    t_loss_list = []
    v_loss_list = []
    f1_list = []
    acc_list = []
    criterion = None; optimizer = None

    # optimizer, loss function
    if model_type == "cla":
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(net.parameters(), lr=1e-4, weight_decay = 1e-5)
    elif model_type == "reg":
        criterion = nn.MSELoss() 
        criterion = nn.SmoothL1Loss() #
        optimizer = optim.Adam(net.parameters(), lr=1e-5, weight_decay = 1e-5)
        
    prev_acc = 0

    for epoch in range(epoch):
        running_loss = 0.0

        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            optimizer.zero_grad()
            outputs = net(inputs.float()) 
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        t_loss = running_loss/len(trainloader.dataset)
        if detail:
            print("\n[ Epoch %d ] T_Loss = %f \n"%(epoch+1, t_loss), end='' )
        
        try:
            val_loss, acc, f1 = testModel(net, testloader, target_names, criterion, model_type, False)
        except: continue

        if acc > prev_acc:
            #model_path = "torch_models/SEED_fftMap_ch8_10sec_5over/"+str(epoch)+"epoch.pth"
            #torch.save(net.state_dict(), model_path)
            prev_acc = acc

        t_loss_list.append(running_loss/len(trainloader.dataset))
        v_loss_list.append(val_loss)
        acc_list.append(acc)
        f1_list.append(f1)
    print('Finished Training')
    return net, t_loss_list, v_loss_list, f1_list, acc_list