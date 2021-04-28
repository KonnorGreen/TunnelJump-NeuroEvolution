import tensorflow as tf
from tensorflow.python.framework.ops import convert_to_tensor
import random


class NeuralNetwork:

    def __init__(self, a, b, c, d):
        if (isinstance(a, tf.keras.Sequential)):
            self.model = a
            self.input = b
            self.hidden = c
            self.output = d
        else:
            self.input = a
            self.hidden = b
            self.output = c
            self.model = self.create_model()

    def __repr__(self):
        return f'Input: {self.input}, Model: {self.model}'

    def create_model(self):  # brain
        model = tf.keras.Sequential()
        hidden = tf.keras.layers.Dense(
            units=self.hidden,
            input_shape=[self.input],
            activation='sigmoid'
        )
        model.add(hidden)
        output = tf.keras.layers.Dense(
            units=self.output,
            activation='sigmoid'
        )
        model.add(output)
        model.compile(loss='meanSquaredError',optimizer='adam')
        return model

    def copied(self):
        modelCopy = self.create_model()
        weights = self.model.get_weights()
        weightsCopies = []
        for i in range(len(weights)):
            weightsCopies.append(weights[i].copy())
        modelCopy.set_weights(weightsCopies)
        return NeuralNetwork(modelCopy, self.input, self.hidden, self.output)

    def mutate(self, rate):
        weights = self.model.get_weights()
        mutatedWeights = []
        for i in range(len(weights)):
            tensor = weights[i]
            shape = weights[i].shape
            values = tensor.copy() #We get a copy of the weights
            for j in range(len(values)):
                if(random.uniform(0,1) < rate): #We only mutate rate% of the time
                    w = values[j]
                    values[j] = w + random.gauss(1, 2) #Picking a new weight to adjust a small bit
            newTensor = tf.constant(values,dtype='float32', shape = shape)
            mutatedWeights.append(newTensor)
        self.model.set_weights(mutatedWeights)


    def dispose(self):
        tf.keras.backend.clear_session()

    
    def predict(self, inputs):
        inputs = convert_to_tensor(inputs)
        self.model.run_eagerly = False
        ys = self.model(inputs)
        #print(ys)
        tf.keras.backend.clear_session()
        outputs = ys[0]
        #print(outputs)
        return outputs