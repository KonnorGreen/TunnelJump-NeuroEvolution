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
            activation='softmax'
        )
        model.add(output)
        model.compile(loss='mse',optimizer='adam')
        return model

    def copy(self):
        modelCopy = self.create_model()
        weights = self.model.get_weights()
        weightsCopies = []
        for i in range(len(weights)):
            weightsCopies[i] = weights[i].clone()
        modelCopy.set_weights(weightsCopies)
        return NeuralNetwork(modelCopy, self.input, self.hidden, self.output)


    def mutate(self, rate):
        weights = self.model.get_weights()
        mutatedWeights = []
        for i in range(len(weights)):
            tensor = weights[i]
            shape = weights[i].shape
            values = tensor.copy()
            for j in range(len(values)):
                if(random.uniform(0,1) < rate):
                    w = values[j]
                    values[j] = w + random.gauss(1, 2)
            newTensor = tf.constant(values,dtype='float32', shape = shape)
            mutatedWeights.append(newTensor)
        self.model.set_weights(mutatedWeights)


    def dispose(self):
        tf.keras.backend.clear_session()


    def predict(self, inputs):
        inputs = convert_to_tensor(inputs)
        ys = self.model.predict(inputs)
        tf.keras.backend.clear_session()
        outputs = ys[0]
        return outputs