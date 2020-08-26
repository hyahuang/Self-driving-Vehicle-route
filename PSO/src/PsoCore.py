# uncompyle6 version 3.7.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: C:\Users\Sean\Desktop\GeneticCore.py
# Compiled at: 2020-05-11 23:19:57
# Size of source mod 2**32: 9843 bytes
__doc__ = '\nCreated on Sun May 10 03:07:51 2020\n\n@author: Sean\n'
import numpy as np

class PsoCore:

    def __init__(self, inputDimension, trainingDataSet, trainingData_ans):
        self.adaptivefunc = []
        self.errorList = []
        self.genomeCount = int(input('Input swarm number:'))
        self.neuralCount = int(input('Input neural number:'))
        self.parameter1 = float(input('Input parameter one(0~1):'))
        self.parameter2 = float(input('Input parameter two(0~1):'))
        self.inputDimension = inputDimension
        self.trainingDataSet = trainingDataSet
        self.trainingData_ans = trainingData_ans
        self.iteration = int(input('Input Iteration number(0~1):'))
        self.size = 0.08
        self.weightList = self.initWeight()
        self.MList = self.initMList()
        self.sigmaList = self.initSigma()
        self.BestWeightList = self.weightList
        self.BestMList = self.MList
        self.BestSigmaList = self.sigmaList
        self.velocityWeightList = self.initWeight()
        self.velocityMList = self.initMList()
        self.velocitySigmaList = self.initSigma() * 2 - 1
        self.best = 0
        self.vMax = 0.05
        self.vMin = -0.05

    def initWeight(self):
        initWeight = np.random.random((self.genomeCount, self.neuralCount + 1))
        initWeight = initWeight * 2 - 1
        return initWeight

    def initMList(self):
        MList = []
        for i in range(self.genomeCount):
            initM = np.random.random((self.neuralCount, self.inputDimension - 1))
            initM = initM * 2 - 1
            MList.append(initM)

        return np.array(MList)

    def initSigma(self):
        return np.random.random((self.genomeCount, self.neuralCount)) * 1

    def runRBF(self, sigma, oneM, weight):
        tmpArrayList = []
        for i in range(self.neuralCount):
            tmpArrayList.append(np.exp(-((self.trainingDataSet - oneM[i]) ** 2).sum(axis=1) / (2 * sigma[i] ** 2)))

        outputArray = np.dstack(tmpArrayList[:])[0]
        outputArray = np.column_stack((outputArray, np.ones(self.trainingDataSet.shape[0])))
        outputArray = outputArray.dot(weight.reshape(self.neuralCount + 1, 1))
        self.error = np.sqrt((self.trainingData_ans - outputArray) ** 2).sum(axis=0) / self.trainingDataSet.shape[0]
        return ((self.trainingData_ans - outputArray) ** 2).sum(axis=0) / 2

    def calAdaptiveFunc(self):
        for i in range(self.genomeCount):
            self.adaptivefunc.append(self.runRBF(self.sigmaList[i], self.MList[i], self.weightList[i]))
            self.errorList.append(self.error)

        self.adaptivefunc = np.array(self.adaptivefunc)

    def runPso(self):
        for i in range(self.genomeCount):
            if (self.runRBF(self.sigmaList[i], self.MList[i], self.weightList[i]) < self.runRBF(self.BestSigmaList[i], self.BestMList[i], self.BestWeightList[i])):
                self.BestWeightList[i] = self.weightList[i]
                self.BestMList[i] = self.MList[i]
                self.BestSigmaList[i] = self.sigmaList[i]
            g=i
            for j in range(self.genomeCount):
                 if (self.runRBF(self.BestSigmaList[j], self.BestMList[j], self.BestWeightList[j]) < self.runRBF(self.BestSigmaList[g], self.BestMList[g], self.BestWeightList[g])):
                     g=j
            
            for d in range(self.velocityMList[i].shape[0]):
                self.velocityWeightList[i][d] = self.velocityWeightList[i][d] + self.parameter1 * (self.BestWeightList[i][d]-self.weightList[i][d]) + self.parameter2 * (self.BestWeightList[g][d]-self.weightList[i][d])
                if (self.velocityWeightList[i][d] > self.vMax):
                    self.velocityWeightList[i][d] = self.vMax
                elif (self.velocityWeightList[i][d] < self.vMin):
                    self.velocityWeightList[i][d] = self.vMin
                
                self.weightList[i][d] = self.weightList[i][d] + self.velocityWeightList[i][d]
                if (self.weightList[i][d] > 1):
                    self.weightList[i][d] = 1
                elif (self.weightList[i][d] < -1):
                    self.weightList[i][d] = -1
                self.velocityMList[i][d] = self.velocityMList[i][d] + self.parameter1 * (self.BestMList[i][d]-self.MList[i][d]) + self.parameter2 * (self.BestMList[g][d]-self.MList[i][d])
                for k in range (self.velocityMList[i][d].shape[0]):
                    if (self.velocityMList[i][d][k] > self.vMax):
                        self.velocityMList[i][d][k] = self.vMax
                    elif (self.velocityMList[i][d][k] < self.vMin):
                        self.velocityMList[i][d][k] = self.vMin
                
                self.MList[i][d] = self.MList[i][d] + self.velocityMList[i][d]
                for k in range (self.velocityMList[i][d].shape[0]):
                    if (self.MList[i][d][k] > 1):
                        self.MList[i][d][k] = 1
                    elif (self.MList[i][d][k] < -1):
                        self.MList[i][d][k] = -1
                
                self.velocitySigmaList[i][d] = self.velocitySigmaList[i][d] + self.parameter1 * (self.BestSigmaList[i][d]-self.sigmaList[i][d]) +self.parameter2 * (self.BestSigmaList[g][d]-self.sigmaList[i][d])
                if (self.velocitySigmaList[i][d] > self.vMax):
                    self.velocitySigmaList[i][d] = self.vMax
                elif (self.velocitySigmaList[i][d] < self.vMin):
                    self.velocitySigmaList[i][d] = self.vMin
                    
                self.sigmaList[i][d] = self.sigmaList[i][d] + self.velocitySigmaList[i][d]
                if (self.sigmaList[i][d] > 1):
                    self.sigmaList[i][d] = 1
                elif (self.sigmaList[i][d] < 0):
                    self.sigmaList[i][d] = 1e-100
                    
            self.velocityWeightList[i][self.neuralCount] = self.velocityWeightList[i][self.neuralCount] + self.parameter1 * (self.BestWeightList[i][self.neuralCount]-self.weightList[i][self.neuralCount]) + self.parameter2 * (self.BestWeightList[g][self.neuralCount]-self.weightList[i][self.neuralCount])
            if (self.velocityWeightList[i][self.neuralCount] > self.vMax):
                self.velocityWeightList[i][self.neuralCount] = self.vMax
            elif (self.velocityWeightList[i][self.neuralCount] < self.vMin):
                self.velocityWeightList[i][self.neuralCount] = self.vMin
                
            self.weightList[i][self.neuralCount] = self.weightList[i][self.neuralCount] + self.velocityWeightList[i][self.neuralCount]
            if (self.weightList[i][self.neuralCount] > 1):
                self.weightList[i][self.neuralCount] = 1
            elif (self.weightList[i][self.neuralCount] < -1):
                self.weightList[i][self.neuralCount] = -1

    def runIteration(self):
        bestvalue = 10000
        for i in range(self.iteration):
            self.adaptivefunc = []
            self.errorList = []
            self.calAdaptiveFunc()
            self.runPso()
            for j in range(len(self.errorList)):
                if self.errorList[j] < bestvalue:
                    bestvalue = self.errorList[j]
                    bestWeight = self.weightList[j]
                    bestM = self.MList[j]
                    bestSigma = self.sigmaList[j]

            print('iteration: {iteration}, Error_rate: {error}'.format(iteration=i, error=bestvalue))

        f = open('./weight.txt', 'w')
        log = str(bestWeight[(-1)]) + '\n'
        for x in range(len(bestWeight) - 1):
            log = log + str(bestWeight[x]) + ' '
            for k in range(bestM[x].shape[0]):
                log = log + str(bestM[x][k]) + ' '

            log = log + str(bestSigma[x]) + '\n'

        f.write(log)