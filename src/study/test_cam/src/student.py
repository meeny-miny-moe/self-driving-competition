#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
data = 0
def callback(msg):
    global data
    data = msg.data
rospy.init_node('student')
sub = rospy.Subscriber('memo2', Int32, callback)
while not rospy.is_shutdown():
    rospy.wait_for_message('memo2', Int32)
    print(data)