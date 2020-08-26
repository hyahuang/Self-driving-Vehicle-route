# uncompyle6 version 3.7.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: C:\Users\Sean\Desktop\runRBF.py
# Compiled at: 2020-05-12 10:58:47
# Size of source mod 2**32: 9448 bytes
__doc__ = '\nCreated on Sat May  9 23:12:44 2020\n\n@author: Sean\n'
import numpy as np, tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class dotPair:

    def __init__(self, sPoint=[
 0, 0], ePoint=[1, 1]):
        self.sPoint = sPoint
        self.ePoint = ePoint


class line:

    def __init__(self, sPoint, theta):
        self.sPoint = sPoint
        self.theta = np.append(np.cos(theta), np.sin(theta))
        self.a = self.theta[1] / self.theta[0]
        self.b = self.sPoint[1] - self.a * self.sPoint[0]


def getDistance(l1, l2):
    sFlag = np.sum(np.array([l1.a, l1.b]) * np.array([l2.sPoint[0], 1]))
    sFlag = sFlag - l2.sPoint[1]
    eFlag = np.sum(np.array([l1.a, l1.b]) * np.array([l2.ePoint[0], 1]))
    eFlag = eFlag - l2.ePoint[1]
    num = 0
    num += int(sFlag) == 0
    num += int(eFlag) == 0
    num += int(sFlag) * int(eFlag) < 0
    if num == 1:
        if l2.ePoint[0] - l2.sPoint[0] != 0:
            l2a = -((l2.ePoint[1] - l2.sPoint[1]) / (l2.ePoint[0] - l2.sPoint[0]))
        else:
            l2a = 1.633123935319537e+16
        l2b = l2a * l2.sPoint[0] + l2.sPoint[1]
        a = np.array([[-l1.a, 1], [l2a, 1]])
        b = np.array([l1.b, l2b])
        cross = np.linalg.solve(a, b)
        if (cross[0] - l1.sPoint[0]) * l1.theta[0] > 0:
            if (cross[1] - l1.sPoint[1]) * l1.theta[1] > 0:
                interceptx = (cross[0] - l1.sPoint[0]) * (cross[0] - l1.sPoint[0])
                intercepty = (cross[1] - l1.sPoint[1]) * (cross[1] - l1.sPoint[1])
                distance = (interceptx + intercepty) ** 0.5
                return float(distance)
        return False
    else:
        return False


def drawcar(circleX, circleY, carangle, ax):
    carangle = carangle / 360 * 2 * np.pi
    theta = np.arange(0, 2 * np.pi, 0.001)
    x = circleX + radius * np.cos(theta)
    y = circleY + radius * np.sin(theta)
    directionendX = circleX + radius * np.cos(carangle) * 2
    directionendY = circleY + radius * np.sin(carangle) * 2
    ax.plot([circleX, directionendX], [circleY, directionendY], color='r')
    ax.plot(x, y, color='r')


def changeplace(circleX, circleY, carangle, sida):
    carangle = carangle / 360 * 2 * np.pi
    sida = sida / 360 * 2 * np.pi
    circleX = circleX + np.cos(carangle + sida) + np.sin(sida) * np.sin(carangle)
    circleY = circleY + np.sin(carangle + sida) - np.sin(sida) * np.cos(carangle)
    carangle = carangle - np.arcsin(2 * np.sin(sida) / 6)
    carangle = carangle / (2 * np.pi) * 360
    sida = sida / (2 * np.pi) * 360
    if carangle < -90:
        carangle = carangle + 360
    return (
     circleX, circleY, carangle)


def output(inputSet, sigma, oneM, weight, neuralCount):
    tmpArrayList = []
    for i in range(neuralCount):
        tmpArrayList.append(np.exp(-((inputSet - oneM[i]) ** 2).sum(axis=0) / (2 * sigma[i] ** 2)))

    outputArray = np.dstack(tmpArrayList[:])[0]
    outputArray = np.column_stack((outputArray, np.ones(1)))
    outputArray = outputArray.dot(weight.reshape(neuralCount + 1, 1))
    outputArray = outputArray.sum(axis=0)
    return outputArray


if __name__ == '__main__':
    window = tk.Tk()
    text = []
    f = open('./case01.txt', 'r')
    fweight = open('./weight.txt', 'r')
    bias = fweight.readline()
    text.append(fweight.read())
    aa = text[0].split()
    text = []
    for x in aa:
        text.append(float(x))

    fweight.close()
    dcount = open('./weight.txt', 'r')
    print(dcount.readline())
    a = dcount.readline()
    a = a.split()
    dcount.close()
    a = np.array(a)
    array = np.array(text)
    print(a.shape[0])
    if a.shape[0] == 5:
        dimension = 3
        neuralCount = int(array.shape[0] / 5)
        array = array.reshape(int(array.shape[0] / 5), 5)
        weight, array = np.hsplit(array, [1])
        Mlist, sigma = np.hsplit(array, [3])
    else:
        dimension = 5
        neuralCount = int(array.shape[0] / 7)
        array = array.reshape(int(array.shape[0] / 7), 7)
        weight, array = np.hsplit(array, [1])
        Mlist, sigma = np.hsplit(array, [5])
    weight = np.insert(weight, (weight.shape[0]), bias, axis=0)
    weight = weight.reshape(1, neuralCount + 1)[0]
    sigma = sigma.reshape(1, neuralCount)[0]
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    bar1 = FigureCanvasTkAgg(fig, window)
    bar1.get_tk_widget().pack(side=(tk.LEFT), fill=(tk.BOTH))
    ax.set_xlim(-40, 100)
    ax.set_ylim(-100, 100)
    radius = 3.0
    strnum = ''
    lines = []
    sida = 0
    text = f.readline()
    counter = 0
    for x in text:
        if x != ',' and x!= '\n' :
            strnum=strnum+x
        else :
            if  counter==0:
                circleX=int(strnum)
                strnum=''
                counter+=1
            elif counter==1:
                circleY=int(strnum)
                strnum=''
                counter+=1
            elif counter==2:
                carangle=int(strnum)
                strnum=''
                counter+=1
    text=f.readline()
    counter=0
    for x in text:
        if x != ',' and x!='\n':
            strnum=strnum+x
        else :
           if  counter==0:
                leftendx=int(strnum)
                strnum=''
                counter+=1
           elif counter==1:
                upendy=int(strnum)
                strnum=''
                counter+=1
    text=f.readline()
    counter=0
    for x in text:
        if x != ',' and x!='\n' :
            strnum=strnum+x
        else :
            if  counter==0:
                rightendx=int(strnum)
                strnum=''
                counter+=1
            elif counter==1:
                downendy=int(strnum)
                strnum=''
                counter+=1

    ax.plot([leftendx, rightendx], [downendy, downendy], color='red')
    ax.plot([leftendx, rightendx], [upendy, upendy], color='red')
    ax.plot([leftendx, leftendx], [downendy, upendy], color='red')
    ax.plot([rightendx, rightendx], [downendy, upendy], color='red')
    dots = []
    while 1:
        text = f.readline()
        if text == '':
            break
        counter = 0
        text = text + '\n'
        for x in text:
            if x != ',' and x != '\n':
                strnum = strnum + x
            elif counter == 0:
                coordinateX = int(strnum)
                strnum = ''
                counter += 1
            elif counter == 1:
                coordinateY = int(strnum)
                strnum = ''
                counter += 1
                dots.append([coordinateX, coordinateY])

    lines = []
    i = 0
    leftdistance = 1000
    rightdistance = 1000
    middledistance = 1000
    for i in range(len(dots) - 1):
        lines.append(dotPair(dots[i], dots[(i + 1)]))

    for count in range(len(lines)):
        ax.plot([lines[count].sPoint[0], lines[count].ePoint[0]], [lines[count].sPoint[1], lines[count].ePoint[1]], color='blue')

    f.close()
    drawcar(circleX, circleY, carangle, ax)
    weightL = 0
    weightR = 0
    weightM = 0
    time1 = 0
    fo4D = open('./text4D.txt', 'w')
    fo6D = open('./text6D.txt', 'w')
    while 1:
        leftdistance = 1000
        rightdistance = 1000
        middledistance = 1000
        leftsensor = line([circleX, circleY], [(carangle + 45) / 360 * 2 * np.pi])
        rightsensor = line([circleX, circleY], [(carangle - 45) / 360 * 2 * np.pi])
        middlesensor = line([circleX, circleY], [carangle / 360 * 2 * np.pi])
        for count in range(len(lines)):
            tmp = getDistance(leftsensor, lines[count])
            if tmp and tmp < leftdistance:
                leftdistance = tmp

        for count in range(len(lines)):
            tmp = getDistance(rightsensor, lines[count])
            if tmp and tmp < rightdistance:
                rightdistance = tmp

        for count in range(len(lines)):
            tmp = getDistance(middlesensor, lines[count])
            if tmp and tmp < middledistance:
                middledistance = tmp

        if dimension == 3:
            inputset = np.array([middledistance, rightdistance, leftdistance])
            inputset = (inputset * 2 - 40) / 40
        else:
            inputset = np.array([circleX, circleY, middledistance, rightdistance, leftdistance])
            inputset = (inputset * 2 - 40) / 40
        sida = output(inputset, sigma, Mlist, weight, neuralCount)
        sida = sida[0] * 40
        if sida > 40:
            sida = 40
        if sida < -40:
            sida = -40
        circleX, circleY, carangle = changeplace(circleX, circleY, carangle, int(sida))
        if time1 % 1 == 0:
            drawcar(circleX, circleY, carangle, ax)
            bar1.draw()
            window.update()
            string4D = str(middledistance) + ' ' + str(rightdistance) + ' ' + str(leftdistance) + ' ' + str(sida) + '\n'
            string6D = str(circleX) + ' ' + str(circleY) + ' ' + str(middledistance) + ' ' + str(rightdistance) + ' ' + str(leftdistance) + ' ' + str(sida) + '\n'
            fo4D.write(string4D)
            fo6D.write(string6D)
        time1 += 1
        if circleX > leftendx and circleX < rightendx and circleY < upendy and circleY > downendy:
            break

    fo4D.close()
    fo6D.close()
    window.mainloop()