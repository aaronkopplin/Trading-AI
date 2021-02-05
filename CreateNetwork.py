import NeuralNet as nn


network = nn.Network()
network.add_layer(3)  # input
network.add_layer(2)  # hidden
network.add_layer(1)  # output

out = network.fire_network([.5, .5, .5])

print(out)
