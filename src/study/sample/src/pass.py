#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

rospy.init_node("pass")


value = 0

def callback(msg):
    global value
    value = msg.data
    value = value*100

sub = rospy.Subscriber('memo1', Int32, callback)
pub = rospy.Publisher('memo2', Int32, queue_size=10)

while not rospy.is_shutdown():
    rospy.wait_for_message('memo1', Int32)
    pub.publish(value)





	