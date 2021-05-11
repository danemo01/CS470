import keras
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np
import math

# Functions generating random inputs (2D coordinates) for each class
# We are simply assuming normally distributed samples for each class

# def get_class_0_example():
#     return [np.random.normal(0.2, 0.6), np.random.normal(0.8, 0.6)]

# def get_class_1_example():
#     return [np.random.normal(0.7, 0.6), np.random.normal(-0.1, 0.6)]

# def get_class_2_example():
#     return [np.random.normal(-0.4, 0.6), np.random.normal(-0.2, 0.6)]

def get_class_0_example():
    center = (-0.1, 0.4)
    radius = 0.5
    angle = np.random.uniform(0.5, 4.6)
    stdev = 0.04
    # stdev = 0.30
    return [np.random.normal(center[0] + radius * math.cos(angle), stdev), np.random.normal(center[1] + radius * math.sin(angle), stdev)]

def get_class_1_example():
    center = (-0.1, -0.05)
    radius = 0.4
    angle = np.random.uniform(4.5, 8.2)
    stdev = 0.03
    # stdev = 0.30
    return [np.random.normal(center[0] + radius * math.cos(angle), stdev), np.random.normal(center[1] + radius * math.sin(angle), stdev)]

def get_class_2_example():
    center = (0.0, 0.0)
    radius = 0.85
    angle = np.random.uniform(3.8, 5.9)
    stdev = 0.035
    # stdev = 0.30
    return [np.random.normal(center[0] + radius * math.cos(angle), stdev), np.random.normal(center[1] + radius * math.sin(angle), stdev)]

num_classes = 3

num_train_exemplars_class_0 = 1000
num_train_exemplars_class_1 = 1000
num_train_exemplars_class_2 = 1000

num_test_exemplars_class_0 = 100
num_test_exemplars_class_1 = 100
num_test_exemplars_class_2 = 100

# Build matrices for inputs (x) and desired outputs (y) (here: class labels 0, 1, or 2)
x_train = []
y_train_labels = []

np.random.seed(0)

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
num_outputs = num_classes
batch_size = 20
num_epochs = 50

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# build the neural network model
model = Sequential()
model.add(Dense(50, activation='relu', name='hidden'))
model.add(Dense(num_outputs, activation='softmax', name='output'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=batch_size, epochs=num_epochs, verbose=2, validation_data=(x_test, y_test))

model.summary()

# Check the classification performance of the trained network on the test data 
final_train_loss, final_train_accuracy = model.evaluate(x_train, y_train, verbose=0)
final_test_loss, final_test_accuracy = model.evaluate(x_test, y_test, verbose=0)
 
print('Final training loss:', final_train_loss)
print('Final training accuracy:', final_train_accuracy)
print('Final test loss:', final_test_loss)
print('Final test accuracy:', final_test_accuracy)

# Get the network outputs for a grid of test inputs (each row is one output vector)

x_test_grid = []
for x1 in range(100):
    for x2 in range(100):
        x_test_grid.append([(x1 - 50)/50, (x2 - 50)/50])

x_test_grid = np.array(x_test_grid)

y_test_predicted = model.predict(x_test)
y_test_grid_predicted = model.predict(x_test_grid)

# The output neuron with the greatest activation indicates the class of the input
# as predicted by the network. 
y_test_labels_predicted = np.argmax(y_test_predicted, axis=-1)
y_test_grid_labels_predicted = np.argmax(y_test_grid_predicted, axis=-1)

plt.subplots()
plt.subplot(231)

class_colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
region_colors = [(1.0, 0.7, 0.7), (0.7, 1.0, 0.7), (0.7, 0.7, 1.0)]
for c in range(num_classes):
    plt.plot(x_train[y_train_labels == c, 0], x_train[y_train_labels == c, 1], '.', markerfacecolor=class_colors[c], 
             markeredgecolor=class_colors[c], label='Class ' + str(c))

plt.axis('square')
plt.title('Training Data')
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.legend(loc=(1.05, 0))

plt.subplot(232)

for c in range(num_classes):
    plt.plot(x_test_grid[y_test_grid_labels_predicted == c, 0], x_test_grid[y_test_grid_labels_predicted == c, 1], '.', markerfacecolor=region_colors[c], 
             markeredgecolor=region_colors[c], label='Region ' + str(c))

for c in range(num_classes):
    plt.plot(x_train[y_train_labels == c, 0], x_train[y_train_labels == c, 1], '.', markerfacecolor=class_colors[c], 
             markeredgecolor=class_colors[c], label='Class ' + str(c))

plt.axis('square')
plt.title('Resulting Classification Function')
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.legend(loc=(1.05, 0))

ax = plt.subplot(233)

train_label = 'Training Set (Final: %.2f)'%(100 * final_train_accuracy)
test_label = 'Training Set (Final: %.2f)'%(100 * final_test_accuracy)

plt.plot(100 * np.array(history.history['accuracy']), label=train_label)
plt.plot(100 * np.array(history.history['val_accuracy']), label=test_label)
plt.title('Classification Accuracy during Training')
plt.xlabel('Epochs Completed')
plt.ylabel('Accuracy (Percent)')
plt.ylim([0, 100])
plt.yticks(list(range(0, 100, 5)))
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.legend(loc='lower right')

plt.subplot(234)

for c in range(num_classes):
    plt.plot(x_test[y_test_labels == c, 0], x_test[y_test_labels == c, 1], '.', markerfacecolor=class_colors[c], 
             markeredgecolor=class_colors[c], label='Class ' + str(c))

plt.axis('square')
plt.title('Test Data')
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.legend(loc=(1.05, 0))

plt.subplot(235)

for c in range(num_classes):
    plt.plot(x_test[y_test_labels_predicted == c, 0], x_test[y_test_labels_predicted == c, 1], '.', markerfacecolor=class_colors[c], 
             markeredgecolor=class_colors[c], label='Class ' + str(c))

plt.plot(x_test[y_test_labels_predicted != y_test_labels, 0], x_test[y_test_labels_predicted != y_test_labels, 1], 'o', 
         markerfacecolor='none', markeredgecolor='black', label='Misclassified')

plt.axis('square')
plt.title('Network Output for Test Input')
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.legend(loc=(1.05, 0))

ax = plt.subplot(236)

train_label = 'Training Set (Final: %.2f)'%(final_train_loss)
test_label = 'Training Set (Final: %.2f)'%(final_test_loss)

plt.plot(100 * np.array(history.history['loss']), label=train_label)
plt.plot(100 * np.array(history.history['val_loss']), label=test_label)
plt.title('Network Loss (Error) during Training')
plt.xlabel('Epochs Completed')
plt.ylabel('Loss')
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.legend(loc='upper right')

plt.show()
