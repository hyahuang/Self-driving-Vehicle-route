# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:49:34 2020

@author: Sean
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QDialog,QVBoxLayout

class Main_window(QDialog):
    def __init__(self,figure):
        super().__init__()
        self.figure = figure
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class dotPair():#点对
    def __init__(self, sPoint=[0,0],ePoint = [1,1]):
        self.sPoint = sPoint
        self.ePoint = ePoint

class line():
    def __init__(self, sPoint, theta):
        self.sPoint=sPoint
        self.theta = np.append(np.cos(theta),np.sin(theta))
        self.a=self.theta[1]/self.theta[0]
        self.b=self.sPoint[1]-(self.a*self.sPoint[0])

def getDistance(l1, l2):
    sFlag = np.sum(np.array([l1.a,l1.b])*np.array([l2.sPoint[0],1]))
    sFlag= sFlag-l2.sPoint[1]
    eFlag = np.sum(np.array([l1.a,l1.b])*np.array([l2.ePoint[0],1]))
    eFlag= eFlag-l2.ePoint[1]
    num = 0
    num += int(sFlag)==0
    num += int(eFlag)==0
    num += int(sFlag)*int(eFlag) < 0
    if num==1:
        if l2.ePoint[0]-l2.sPoint[0]!=0:
            l2a=-((l2.ePoint[1]-l2.sPoint[1])/(l2.ePoint[0]-l2.sPoint[0]))
        else:
            l2a=1.633123935319537e+16 ##讓line2的x係數設為極大值表示鉛錘線
        l2b= (l2a*l2.sPoint[0])+l2.sPoint[1]
        a=np.array([[-(l1.a),1],[l2a,1]])
        b=np.array([l1.b,l2b])
        cross = np.linalg.solve(a,b)

        if (cross[0]-l1.sPoint[0])*l1.theta[0]>0 and (cross[1]-l1.sPoint[1])*l1.theta[1]>0:
            interceptx=(cross[0]-l1.sPoint[0])*(cross[0]-l1.sPoint[0])
            intercepty=(cross[1]-l1.sPoint[1])*(cross[1]-l1.sPoint[1])
            distance=(interceptx+intercepty)**0.5
            return float(distance)
        else:
            return False;
    else :
        return False;


def drawcar(circleX,circleY,carangle):
    carangle=(carangle/360)*2*np.pi
    theta = np.arange(0, 2*np.pi, 0.001)
    x = circleX+radius * np.cos(theta)
    y = circleY+radius * np.sin(theta)
    directionendX = circleX+(radius * np.cos(carangle))*2
    directionendY = circleY+(radius * np.sin(carangle))*2
    plt.plot([circleX,directionendX],[circleY,directionendY],color='r')
    plt.plot(x,y,color='r')
    
def changeplace(circleX,circleY,carangle,sida):
    carangle=(carangle/360)*2*np.pi
    sida=(sida/360)*2*np.pi
    circleX=circleX+np.cos(carangle+sida)+(np.sin(sida)*np.sin(carangle))
    circleY=circleY+np.sin(carangle+sida)-(np.sin(sida)*np.cos(carangle))
    carangle = carangle-np.arcsin((2*np.sin(sida))/6)
    carangle=(carangle/(2*np.pi))*360
    sida=(sida/(2*np.pi))*360
    if carangle<-90:
        carangle=carangle+360
    return circleX, circleY,carangle


if __name__ == '__main__':

    f= open("case01.txt","r")
    print("open")
    
    fig=plt.figure(figsize=(10,10))
    plt.xlim(-40, 100)
    plt.ylim(-100, 100)
    radius = 3.0
    strnum=''
    lines=[]
    sida=0
    
    ##讀起點+終點
    text=f.readline()
    counter=0
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
    plt.plot([leftendx,rightendx],[downendy,downendy],color='red')
    plt.plot([leftendx,rightendx],[upendy,upendy],color='red')
    plt.plot([leftendx,leftendx],[downendy,upendy],color='red')
    plt.plot([rightendx,rightendx],[downendy,upendy],color='red')
    
    ##讀線段
    dots=[]
    while True:
        text=f.readline()
        if text=="":
            break;
        counter=0;
        text=text+'\n'
        for x in text:
            if x != ',' and x!='\n':
                strnum=strnum+x
            else :
                if  counter==0:
                    coordinateX=int(strnum)
                    strnum=''
                    counter+=1
                elif counter==1:
                    coordinateY=int(strnum)
                    strnum=''
                    counter+=1
                    dots.append([coordinateX,coordinateY])               
    ##變成line
    lines=[]
    i=0
    leftdistance=1000
    rightdistance=1000
    middledistance=1000
    for i in range(len(dots)-1) :
        lines.append(dotPair(dots[i],dots[i+1]))
    
    for count in range(len(lines)):
        plt.plot([lines[count].sPoint[0],lines[count].ePoint[0]],[lines[count].sPoint[1],lines[count].ePoint[1]],color='blue')
    
    f.close()
    drawcar(circleX,circleY,carangle)
    weightL=0
    weightR=0
    weightM=0
    time=0
    fo4D = open("./text4D.txt",'w')
    fo6D = open("./text6D.txt",'w')
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window(fig)
    while True:
        leftdistance=1000
        rightdistance=1000
        middledistance=1000
        leftsensor = line([circleX,circleY],[((carangle+45)/360)*2*np.pi])
        rightsensor = line([circleX,circleY],[((carangle-45)/360)*2*np.pi])
        middlesensor = line([circleX,circleY],[(carangle/360)*2*np.pi])
        for count in range(len(lines)):
            tmp=getDistance(leftsensor,lines[count])
            if  tmp:
                if tmp<leftdistance:
                    leftdistance=tmp
        for count in range(len(lines)):
            tmp=getDistance(rightsensor,lines[count])
            if  tmp:
                if tmp<rightdistance:
                    rightdistance=tmp
        for count in range(len(lines)):
            tmp=getDistance(middlesensor,lines[count])
            if  tmp:
                if tmp<middledistance:
                    middledistance=tmp
        if leftdistance<10:
            weightL=1-((leftdistance-10)/10)
        else:
            weightL=0
        if rightdistance<10:
            weightR=1-((rightdistance-10)/10)
        else:
            weightR=0
        if middledistance<10:
            weightM=0.7;
            
        sida = (weightL*40+(-40*weightR))+2*weightM
        
        
    
    
        if sida>40: sida=40
        if sida<-40:sida =-40
        
        
        circleX,circleY,carangle=changeplace(circleX,circleY,carangle,sida)
        if time%1==0:   
            drawcar(circleX,circleY,carangle)
            main_window.show()
            string4D=str(middledistance)+' '+str(rightdistance)+' '+str(leftdistance)+' '+str(sida)+'\n'
            string6D=str(circleX)+' '+str(circleY)+' '+str(middledistance)+' '+str(rightdistance)+' '+str(leftdistance)+' '+str(sida)+'\n'
            fo4D.write(string4D)
            fo6D.write(string6D)
        time+=1
        if circleX>leftendx and circleX<rightendx and circleY<upendy and circleY>downendy:
            break;
    
    
    
    
    fo4D.close()
    fo6D.close()
    app.exec()

