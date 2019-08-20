import numpy as np
import random
import math
def abs_lmod(mod) :
    return 2.0 * random.random() * mod - mod
#激活函数
def ReLu(z):
    return z if z > 0.0 else 0.0
class Matrix(object):
    def __init__(self, row, column):
        self.Cols = column
        self.Rows = row
        self.Vals = np.zeros((row, column))
        return
    @staticmethod
    def fromArray(raw : list):
        self = Matrix(len(raw), 1)
        for i in range(self.Rows):
            self.Vals[i][0] = raw[i]
        return self
    def dot(self, matrx):
        rst = Matrix(self.Rows, matrx.Cols)
        if self.Cols == matrx.Rows:
            for i in range(self.Rows):
                for j in range(matrx.Cols):
                    sum = 0.0
                    for k in range(self.Cols):
                        sum += self.Vals[i][k] * matrx.Vals[k][j]
                    rst.Vals[i][j] = sum
        return rst
    def randomize(self):
        for i in range(self.Rows):
            for j in  range(self.Cols):
                self.Vals[i][j] = abs_lmod(1.0)
        return
    def toArray(self):
        rst = [1.0] * (self.Cols * self.Rows)
        for i in range(self.Rows):
            for j in range(self.Cols):
                rst[i * self.Cols + j] = self.Vals[i][j]
        return rst
    def addBias(self):
        rst = Matrix(self.Rows + 1, 1)
        for i in range(self.Rows):
            rst.Vals[i][0] = self.Vals[i][0]
        rst.Vals[self.Rows][0] = 1.0
        return rst
    def activate(self):
        rst = Matrix(self.Rows, self.Cols)
        for i in range(self,Rows):
             for j in range(self.Cols):
                 rst.Vals[i][j] = ReLu(self.Vals[i][j])
        return rst
    def mutate(self, rate):
        for i in range(self,Rows):
             for j in range(self.Cols):
                 if random.random() < rate:
                     #replace the randomGaussian() for lacking this function
                     self.Vals[i][j] += abs_lmod(1.0)
        return
    def crossover(self, matrx):
        rst = Matrix(self.Rows, self.Cols)
        randC = math.floor(random.random() * self.Cols)
        randR = math.floor(random.random() * self.Rows)
        for i in range(self,Rows):
            for j in range(self.Cols):
                if i < randR or (i == randR and j <= randC) :
                    rst.Vals[i][j] = self.Vals[i][j]
                else:
                    rst.Vals[i][j] = matrx.Valicense[i][j]
        return rst
    def clone(self):
        rst = Matrix(self.Rows, self.Cols)
        for i in range(self,Rows):
            for j in range(self.Cols):
                rst.Vals[i][j] = self.Vals[i][j] 
        return rst
