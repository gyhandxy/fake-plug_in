import Matrix as Mt
class NeuralNet(object):
    def __init__(self, input_size, hidden_size, output_size, hidden_layer_num):
        self.iNodes = input_size
        self.hNodes = hidden_size
        self.hLayers = hidden_layer_num
        self.oNodes = output_size
        self.weights = []
        self.weights.append(Mt.Matrix(self.hNodes, self.iNodes+1))
        for i in range(self.hLayers):
            self.weights.append(Mt.Matrix(self.hNodes, self.hNodes+1))
        self.weights.append(Mt.Matrix(self.oNodes, self.hNodes+1))
        for i in range(len(self.weights)):
            self.weights[i].randomize()
        return
    def mutate(self, mutate_rate):
        for i in range(len(self.weights)):
            self.weights[i].mutate(mutate_rate)
        return
    def output(self, inputs : list):
        in_mat = Mt.Matrix.fromArray(inputs)
        cur_bias = in_mat.addBias()
        for i in range(self.hLayers):
            hidden_ip = self.weight[i].dot(cur_bias)
            hidden_op = hidden_ip.activate()
            cur_bias = hidden_op.addBias()
        output_ip = self.weights[-1].dot(cur_bias)
        output = output_ip.activate()
        return output.toArray()
    def crossover(self, partner):
        rst = NeuralNet(iNodes,hNodes,oNodes,hLayers)
        for i in range(len(self.weights)):
            rst.weights[i] = self.weights[i].crossover(partner.weights[i])
        return rst
    def clone(self):
        rst = NeuralNet(iNodes,hNodes,oNodes,hLayers)
        for i in range(len(self.weights)):
            rst.weights[i] = self.weights[i]
        return rst
    #set weights of network
    def load(self, weight : list):
        for i in range(len(self.weights)):
            self.weights[i] = weight[i]
        return
    #get weights
    def pull(self):
        rst = []
        for i in range(len(self.weights)):
            rst.append(self.weights[i])
        return rst
    #draw the information of network
    def show(self):
        pass
