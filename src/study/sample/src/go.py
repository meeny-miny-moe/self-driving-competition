#!/usr/bin/env python
import rospy, time
from xycar_msgs.msg import xycar_motor

from std_msgs.msg import Float32


data = 0
motor = None

def callback(msg):
    global data
    data = msg.data


motor = None


def drive(data):
    motor_msg = xycar_motor()
    motor_msg.angle = data
    motor_msg.speed = 0
    motor.publish(motor_msg)


def start():
    global motor
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    print ("----- Xycar self driving -----")

def main():
    global motor
    rospy.init_node('student')
    rospy.Subscriber('memo', Float32, callback)
    start()
    
    
    
    
    time.sleep(0.1)

    while not rospy.is_shutdown():
        drive(data*4)
        time.sleep(0.1)
if __name__=='__main__':
    main()



    
