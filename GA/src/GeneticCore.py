# uncompyle6 version 3.7.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: C:\Users\Sean\Desktop\GeneticCore.py
# Compiled at: 2020-05-11 23:19:57
# Size of source mod 2**32: 9843 bytes
__doc__ = '\nCreated on Sun May 10 03:07:51 2020\n\n@author: Sean\n'
import numpy as np

class GeneticCore:

    def __init__(self, inputDimension, trainingDataSet, trainingData_ans):
        self.adaptivefunc = []
        self.errorList = []
        self.genomeCount = int(input('Input genome number:'))
        self.neuralCount = int(input('Input neural number:'))
        self.inputDimension = inputDimension
        self.trainingDataSet = trainingDataSet
        self.trainingData_ans = trainingData_ans
        self.crossProb = float(input('Input crossover Probability number(0~1):'))
        self.mutateProb = float(input('Input mutate Probability number(0~1):'))
        self.iteration = int(input('Input Iteration number(0~1):'))
        self.size = 0.08
        self.weightList = self.initWeight()
        self.MList = self.initMList()
        self.sigmaList = self.initSigma()
        self.best = 0

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

    def replicate(self):
        percentOfGenome = []
        newMList = []
        newSigma = []
        newWeight = []
        for i in range(self.genomeCount):
            percentOfGenome.append(self.adaptivefunc[i] / self.adaptivefunc.sum(axis=0))

        while len(newWeight) < self.genomeCount:
            threshold = np.random.random() / self.genomeCount
            for i in range(len(percentOfGenome)):
                if percentOfGenome[i] < threshold and len(newWeight) < self.genomeCount:
                    newMList.append(self.MList[i])
                    newSigma.append(self.sigmaList[i])
                    newWeight.append(self.weightList[i])

        self.MList = np.array(newMList)
        self.sigmaList = np.array(newSigma)
        self.weightList = np.array(newWeight)

    def crossover(self):
        newMList = []
        newSigma = []
        newWeight = []
        tmp1 = []
        tmp2 = []
        for i in range(self.genomeCount):
            threshold = np.random.random()
            if threshold > 1 - self.crossProb and len(tmp1) == 0:
                tmp1.append(self.MList[i])
                tmp1.append(self.sigmaList[i])
                tmp1.append(self.weightList[i])
                tmp1 = np.array(tmp1)
            elif threshold > 1 - self.crossProb and len(tmp1) != 0:
                tmp2.append(self.MList[i])
                tmp2.append(self.sigmaList[i])
                tmp2.append(self.weightList[i])
                tmp2 = np.array(tmp2)
                distance = (tmp1 - tmp2) * 0.02
                if np.random.random() > 0:
                    tmp1 = tmp1 - distance
                    tmp2 = tmp2 - distance
                else:
                    tmp1 = tmp1 + distance
                    tmp2 = tmp2 + distance
                for x in range(tmp1[0].shape[0]):
                    for j in range(tmp1[0][x].shape[0]):
                        if tmp1[0][x][j] < -1:
                            tmp1[0][x][j] = -1

                newMList.append(tmp1[0])
                for j in range(tmp1[1].shape[0]):
                    if tmp1[1][j] < 0:
                        tmp1[1][j] = 1e-100

                newSigma.append(tmp1[1])
                for j in range(tmp1[2].shape[0]):
                    if tmp1[2][j] < -1:
                        tmp1[2][j] = -1

                newWeight.append(tmp1[2])
                for x in range(tmp2[0].shape[0]):
                    for j in range(tmp2[0][x].shape[0]):
                        if tmp2[0][x][j] < -1:
                            tmp2[0][x][j] = -1

                newMList.append(tmp2[0])
                for j in range(tmp2[1].shape[0]):
                    if tmp2[1][j] < 0:
                        tmp2[1][j] = 1e-100

                newSigma.append(tmp2[1])
                for j in range(tmp2[2].shape[0]):
                    if tmp2[2][j] < -1:
                        tmp2[2][j] = -1

                newWeight.append(tmp2[2])
                tmp1 = []
                tmp2 = []
            else:
                newMList.append(self.MList[i])
                newSigma.append(self.sigmaList[i])
                newWeight.append(self.weightList[i])

        if len(tmp1) != 0:
            newMList.append(tmp1[0])
            newSigma.append(tmp1[1])
            newWeight.append(tmp1[2])
            tmp1 = []
        self.MList = np.array(newMList)
        self.sigmaList = np.array(newSigma)
        self.weightList = np.array(newWeight)

    def mutate(self):
        for i in range(self.genomeCount):
            threshold = np.random.random()
            if threshold > 1 - self.mutateProb:
                self.MList[i] = self.MList[i] + self.size * (np.random.random() * 2 - 1)
                self.sigmaList[i] = self.sigmaList[i] + self.size * (np.random.random() * 2 - 1)
                self.weightList[i] = self.weightList[i] + self.size * (np.random.random() * 2 - 1)
                for x in range(self.MList[i].shape[0]):
                    for j in range(self.MList[i][x].shape[0]):
                        if self.MList[i][x][j] < -1:
                            self.MList[i][x][j] = -1

                for j in range(self.sigmaList[i].shape[0]):
                    if self.sigmaList[i][j] < 0:
                        self.sigmaList[i][j] = 1e-100

                for j in range(self.weightList[i].shape[0]):
                    if self.weightList[i][j] < -1:
                        self.weightList[i][j] = -1

    def runIteration(self):
        bestvalue = 10000
        for i in range(self.iteration):
            self.adaptivefunc = []
            self.errorList = []
            self.calAdaptiveFunc()
            self.replicate()
            self.crossover()
            self.mutate()
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