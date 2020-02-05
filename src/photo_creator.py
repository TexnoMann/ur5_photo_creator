#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import Empty

from libs.ur import *
from libs.cubicInterpolation import *

pub = rospy.Publisher("/photo", Empty, queue_size=10)
rospy.init_node('photo_creator', anonymous=False)


ip = "192.168.88.6"
port = 30004
config_filename = "config.xml"
time_delay = 0.002
init_pos = [0.0, -pi/2,0,-pi/2,0.0,0.0]

ur5 = UR(ip, port, config_filename, time_delay)
trj_planer = PoseTrjPlaner(2.0);
ur5.init(init_pos)

q1 = [  -51.89*pi/180,  -124.12*pi/180,    -94.16*pi/180,  -104.19*pi/180,  52.29*pi/180,   45.60*pi/180];
q2 = [  -84.97*pi/180,  -101.65*pi/180,  -114.82*pi/180,    -53.94*pi/180,  87.35*pi/180,   -6.86*pi/180];
q3 = [ -118.77*pi/180,  -127.41*pi/180,  -106.30*pi/180,    -74.04*pi/180,  147.19*pi/180,  24.74*pi/180];

currentPoint =ur5.getStatePoint()

ur5.goToPoint(currentPoint,q1,trj_planer, 2.0)
for i in range(0,5):
    ur5.goToPoint(q1,q2, trj_planer, 0.6)
    pub.publish(Empty())
    ur5.goToPoint(q2,q3, trj_planer, 0.6)
    pub.publish(Empty())
    ur5.goToPoint(q3,q2, trj_planer, 0.6)
    pub.publish(Empty())
    ur5.goToPoint(q2,q1, trj_planer, 0.6)
    pub.publish(Empty())
