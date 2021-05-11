import keras
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np

# Functions generating random inputs (2D coordinates) for each class
# We are simply assuming normally distributed samples for each class

def get_class_0_example():
    return [np.random.normal(0.2, 0.1), np.random.normal(0.8, 0.1)]

def get_class_1_example():
    return [np.random.normal(0.5, 0.1), np.random.normal(0.3, 0.1)]

def get_class_2_example():
    return [np.random.normal(-0.4, 0.1), np.random.normal(-0.2, 0.1)]

num_classes = 3

num_train_exemplars_class_0 = 30
num_train_exemplars_class_1 = 30
num_train_exemplars_class_2 = 30

num_test_exemplars_class_0 = 10
num_test_exemplars_class_1 = 10
num_test_exemplars_class_2 = 10

# Build matrices for inputs (x) and desired outputs (y) (here: class labels 0, 1, or 2)
x_train = []
y_train_labels = []

for i in range(num_train_exemplars_class_0):
    x_train.append(get_class_0_example())
    y_train_labels.append(0)
for i in range(num_train_exemplars_class_1):
    x_train.append(get_class_1_example())
    y_train_labels.append(1)
for i in range(num_train_exemplars_class_2):
    x_train.append(get_class_2_example())
    y_train_labels.append(2)

x_train = np.array(x_train)
y_train_labels = np.array(y_train_labels)

x_test = []
y_test_labels = []

for i in range(num_test_exemplars_class_0):
    x_test.append(get_class_0_example())
    y_test_labels.append(0)
for i in range(num_test_exemplars_class_1):
    x_test.append(get_class_1_example())
    y_test_labels.append(1)
for i in range(num_test_exemplars_class_2):
    x_test.append(get_class_2_example())
    y_test_labels.append(2)

x_test = np.array(x_test)
y_test_labels = np.array(y_test_labels)

# convert class labels (indices) to desired output vectors. For example, for an input from class 1, 
# we would like the network output to be [0, 1, 0]
y_train = keras.utils.to_categorical(y_train_labels)
y_test = keras.utils.to_categorical(y_test_labels)

input_shape = (2,)
num_outputs = 3
batch_size = 2
num_epochs = 10

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')


# build the neural network model
model = Sequential()

model.add(Dense(num_outputs, activation='softmax', name='output'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=num_epochs,
          verbose=1,
          validation_data=(x_test, y_test))

model.summary()

# Check the classification performance of the trained network on the test data 
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Get the network outputs for the test inputs (each row is one output vector)
y_test_predicted = model.predict(x_test)

# The output neuron with the greatest activation indicates the class of the input
# as predicted by the network. 
y_test_labels_predicted = np.argmax(y_test_predicted, axis=-1)

plt.subplots()
plt.subplot(131)

for c in range(num_classes):
    plt.plot(x_train[y_train_labels == c, 0], x_train[y_train_labels == c, 1], '.', label='Class ' + str(c))

plt.axis('square')
plt.title('Training Data')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()

plt.subplot(132)

for c in range(num_classes):
    plt.plot(x_test[y_test_labels == c, 0], x_test[y_test_labels == c, 1], '.', label='Class ' + str(c))

plt.axis('square')
plt.title('Test Data')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()

plt.subplot(133)

for c in range(num_classes):
    plt.plot(x_test[y_test_labels_predicted == c, 0], x_test[y_test_labels_predicted == c, 1], '.', label='Class ' + str(c))

plt.axis('square')
plt.title('Network Output for Test Inputs')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()

plt.show()
