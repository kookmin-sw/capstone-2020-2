from sklearn.metrics import classification_report, confusion_matrix, cohen_kappa_score
from keras.models import load_model


class_total = [0, 0, 0, 0, 0, 0, 0]
class_correct = [0, 0, 0, 0, 0, 0, 0]


# x_test 와 y_test 로 data generator 객체 생성
test_generator = data_generator.flow(x_test, y_test, batch_size=batch_size, shuffle=False)
test_generator.reset()


model = load_model('_mini_XCEPTION.48-0.63.hdf5', compile=False)

# test 데이터 셋을 모델에 넣어 예측값을 얻음.
pred = model.predict_generator(test_generator, steps=len(test_generator), verbose=2)
y_pred = np.argmax(pred, axis=1)
label = np.argmax(y_test.values, axis=1)

for idx in range(0, len(y_pred)):
  if y_pred[idx] == label[idx]:
    class_correct[y_pred[idx]] += 1
  class_total[label[idx]] += 1




import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline


class_names = ['Angry', 'Disgust','Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
for emotion in range(0, 7):
    print(f"Accuracy of {class_names[emotion]} : {100 * class_correct[emotion] / class_total[emotion]}")

conf_matrix = pd.DataFrame(confusion_matrix(label, y_pred), index=class_names, columns=class_names)
plt.figure(figsize=(20,15))
sns.heatmap(conf_matrix, annot=True)