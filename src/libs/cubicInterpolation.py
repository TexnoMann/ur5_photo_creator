import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CubicSpline():
    def __init__(self):
        self.poly = np.zeros((4,1))
        self.__wondermondMatrix = np.zeros((4,4))
        self.finalTime = 0

    def calcWondermondMatrix(self,ts, tf):
        self.__wondermondMatrix = np.matrix([[ts**3, ts**2, ts, 1],[3*ts**2, 2*ts, 1, 0],[tf**3, tf**2, tf, 1],[3*tf**2, 2*tf, 1, 0]])

    def getWondermondMatrix(self):
        return self.__wondermondMatrix

    def calcSpeed(self, time):
        if time >= self.finalTime:
            return np.matrix([[self.finalTime**3, self.finalTime**2, self.finalTime, 1]])* self.poly
        return (np.matrix([[time**3, time**2, time, 1]])* self.poly)


class PoseTrjPlaner:
    def __init__(self, maxSpeed):
        self.__maxSpeed = maxSpeed

    def poseCubicInterpolation(self,startPos, finishPos, finalTime):
        speed_p2p = abs(finishSpeed-startSpeed)/(finalTime)
        if speed_p2p>= self.__maxSpeed:
            print("[WARN] Trajectory planer give heigh speed, change final time")
            finalTime = abs(finishSpeed-startSpeed)/self.__maxSpeed;

        cubicSplines=[]
        for i in range(0,6):
            q = np.matrix([[startSpeed], [0], [finishSpeed], [0]])
            cubicSpline.calcWondermondMatrix(0, finalTime)
            cubicSpline.poly = np.linalg.inv(cubicSpline.getWondermondMatrix()) * q
            cubicSpline.finalTime = finalTime
            cubicSplines.append(cubicSpline)

        return cubicSplines


def testSplineGen(sSpeed, fSpeed, maxAccel):
    s =CubicSpline()
    planer = VelocityTrjPlaner(maxAccel, 200.0)
    planer.cubicInterpolation(s, sSpeed, fSpeed)
    time = np.arange(0,30,0.01)
    velsl =[]
    print(s.poly)
    for i in range(0,int(30/0.01)):
        print(s.calcSpeed(i*0.01)[0, 0])
        velsl.append(s.calcSpeed(i*0.01).item(0,0))
    vels = np.array(velsl)
    # print(velsl)
    plt.plot(time,velsl)
    plt.ylabel('speed')
    plt.xlabel('time')
    plt.show()


def main():
    testSplineGen(-200, 100.0, 15)

if __name__ == '__main__':
    main()
