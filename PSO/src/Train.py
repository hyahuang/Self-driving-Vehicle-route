# uncompyle6 version 3.7.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: C:\Users\Sean\Desktop\Train.py
# Compiled at: 2020-05-12 10:54:19
# Size of source mod 2**32: 926 bytes
__doc__ = '\nCreated on Mon May 11 19:45:44 2020\n\n@author: Sean\n'
import numpy as np
from PsoCore import PsoCore

class Train:

    def __init__(self):
        self.filename = input('Input training data file name(train4dALL or train6dALL)(only accept txt file):')
        self.loadTrainingData()
        self.run = PsoCore(self.inputDimension, self.trainingDataSet, self.trainingData_ans)
        self.run.runIteration()

    def loadTrainingData(self):
        self.trainingDataSet = np.genfromtxt((self.filename + '.txt'), delimiter=' ')
        self.inputDimension = self.trainingDataSet.shape[1]
        self.trainingDataSet, self.trainingData_ans = np.hsplit(self.trainingDataSet, [self.inputDimension - 1])
        self.trainingDataSet = (self.trainingDataSet * 2 - 40) / 40
        self.trainingData_ans = self.trainingData_ans / 40


if __name__ == '__main__':
    Train()