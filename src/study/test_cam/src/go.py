#!/usr/bin/env python
import rospy, time
from xycar_msgs.msg import xycar_motor

from std_msgs.msg import Float32


data = 0

motor = None

def callback(msg):
    global data
    data = msg.data
    data = data * 3 +5



motor = None

## 13, 20, 30
def drive(data):
    if data>20 or data < -20:
        motor_msg = xycar_motor()
        motor_msg.angle = data-10
        motor_msg.speed = 20
        motor.publish(motor_msg)

    elif data>10 or data < -10:
        motor_msg = xycar_motor()
        motor_msg.angle = data-10
        motor_msg.speed = 20
        motor.publish(motor_msg)

    else:
        motor_msg = xycar_motor()
        motor_msg.angle = data-10
        motor_msg.speed = 20
        motor.publish(motor_msg)


def start():
    global motor
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    

def main():
    global motor
    rospy.init_node('student')
    rospy.Subscriber('memo', Float32, callback)
    start()
    
    
    
    
    time.sleep(1)

    while not rospy.is_shutdown():
        drive(data)
        time.sleep(0.1)
        
if __name__=='__main__':
    main()



    
