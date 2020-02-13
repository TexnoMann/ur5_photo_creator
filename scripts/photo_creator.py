#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import Empty

pub = rospy.Publisher("/photo", Empty, queue_size=10)
rospy.init_node('photo_creator', anonymous=True)

pub.publish(Empty())
