import random
import math


# static methods
def sigmoid(x: float) -> float:
    if x < 0:
        return 1 - 1 / (1 + math.exp(x))
    return 1 / (1 + math.exp(-x))


# return a random value between -1 and 1 rounded to one decimal place. Rounding makes it
# easier to read when debugging and printing
def gene():
    lower_bound = -10
    upper_bound = 10
    return random.randint(lower_bound, upper_bound) / 10


# simple weighted connection between two nodes
class Synapse:
    def __init__(self):
        self.weight = gene()


class Node:
    def __init__(self, index: int):
        self.bias = gene()  # bias
        self.synapses = []  # list of connections to nodes in next layer. 1 to many relationship
        self.activation = 0  # activation
        self.index = index  # index of node in layer, used later in activating

    def __str__(self):
        return "({}, {}, {}, {}) ".format(self.bias, self.activation, self.index, len(self.synapses))

    # used in firing of nodes
    def input(self, val):
        self.activation = val

    # activation function : sigmoid(bias + sum(previous nodes activation * previous nodes synapse connection))
    def activate(self, prev_layer):
        self.activation = self.bias
        for node in prev_layer.nodes:
            self.activation += node.activation * node.synapses[self.index]

        self.activation = sigmoid(self.activation)

    def add_connection(self):
        self.synapses.append(gene())


class Layer:
    def __init__(self, num_nodes: int):
        # list of nodes in layer
        self.nodes = [Node(index) for index in range(num_nodes)]

    def print_self(self):
        s = ""
        for node in self.nodes:
            s += node.__str__()

        return s


class Network:
    def __init__(self):
        self.layers = []

    def print_self(self):
        s = ""
        for layer in self.layers:
            s += layer.print_self() + "\n"

        return s

    # loops through nodes in second layer and activates them
    def feed_forward(self, first: Layer, second: Layer):
        for node in second.nodes:
            node.activate(first)

    def add_layer(self, num_nodes: int):
        layer = Layer(num_nodes)

        # connect all the nodes in the last layer to the nodes in the new layer
        if len(self.layers) > 0:
            for existing_node in self.layers[-1].nodes:  # last layer
                for node in layer.nodes:
                    existing_node.add_connection()

        self.layers.append(layer)

    # takes input through network and returns output activations
    def fire_network(self, inputs: list) -> list:
        if len(inputs) == len(self.layers[0].nodes):
            # load the input to the first layer of nodes
            for input, node in zip(inputs, self.layers[0].nodes):
                input = sigmoid(input)
                node.input(input)
            # feed one layer to the next
            for i in range(len(self.layers) - 1):
                self.feed_forward(self.layers[i], self.layers[i + 1])
            # return the activation of all the nodes in last layer
            return [node.activation for node in self.layers[-1].nodes]

        else:
            print("FIRE ERROR")



