#!/usr/bin/env python
import urllib
import rospy
import os
from std_msgs.msg import Empty
from datetime import datetime


class PhotoNode:

    def __init__(self):
        rospy.init_node("photo_node", anonymous=False)
        rospy.Subscriber("/photo", Empty, self.callback)

        self.ip = rospy.get_param("~endpoint", "http://192.168.88.254:8089/")
	pwd = os.getcwd() + "/result"
	self.path = rospy.get_param("~newpath", pwd)
	try:
    	    os.mkdir(self.path)
	except OSError:
    	    print ("The directory %s already exists" % self.path)
	else:
            print ("Successfully created the directory %s " % self.path)

        #self.count = 0

    def callback(self, data):
	self.now = datetime.now()
	timestamp = self.now.strftime("%Y-%m-%d-%H-%M-%S")

        rospy.loginfo("Downloading image...")

        filename = "photo-" + "-"+ timestamp + ".jpg" # + str(self.count) + "--"+ timestamp + ".jpg"
	#directory_view_count = "result_view" + str(self.count % 3)

	full_filename = os.path.join(self.path, filename)
        urllib.urlretrieve(self.ip + "photoaf.jpg",  full_filename)
        #self.count += 1

        rospy.loginfo("Finished")

    def spin(self):
        rospy.spin()


if __name__ == "__main__":
    PhotoNode().spin()
