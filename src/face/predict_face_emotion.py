import cv2
import torch
from torch.autograd import Variable
# import torch.nn.functional as F
import torchvision.transforms as transforms

from face_emotion import FaceEmotion

model = FaceEmotion()
model.load_state_dict(torch.load("FaceEmotionModel.pt"))


image = cv2.imread('10.jpg',cv2.IMREAD_GRAYSCALE)
transformation = transforms.Compose([transforms.ToTensor()]) 
image_tensor = transformation(image).float()
inp = Variable(image_tensor)

output = model.predict(inp.unsqueeze_(0))
print(output.data)

emotion = torch.max(output.data, 1)
print(emotion)