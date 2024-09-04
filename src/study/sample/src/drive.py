#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from xycar_msgs.msg import xycar_motor
from std_msgs.msg import Float32

bridge = CvBridge()
cv_image = np.empty(shape=[0])
motor = None

Width = 320
Height = 240
Offset = 170
Gap = 60


def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

def drive(angle, speed):
    global motor
    motor_msg = xycar_motor()
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor.publish(motor_msg)

def detect_edges(image):
    height, width = image.shape[:2]
    roi = image[Offset:Offset+Gap, 0:Width]
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([190, 50, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    blur = cv2.GaussianBlur(white_mask, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    return edges

def hough_lines(edges):
    return cv2.HoughLinesP(edges, 1, np.pi/180, 30, 30, 10)

def divide_left_right(lines):
    global Width
    low_slope_threshold = 0
    high_slope_threshold = 10

    left_lines = []
    right_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 == 0:
            continue
        slope = float(y2-y1) / float(x2-x1)
        if low_slope_threshold < abs(slope) < high_slope_threshold:
            if slope < 0:
                left_lines.append(line[0])
            else:
                right_lines.append(line[0])
    return left_lines, right_lines

def get_line_pos(lines, left=False, right=False):
    global Width, Gap
    x_sum = 0.0
    y_sum = 0.0
    size = len(lines)
    
    if size == 0:
        return 0
    
    for line in lines:
        x1, y1, x2, y2 = line
        x_sum += x1 + x2
        y_sum += y1 + y2

    x_avg = x_sum / (size * 2)
    y_avg = y_sum / (size * 2)
    
    if size == 0:
        return 0
    if left:
        x_pos = x_avg - 0.2 * (Gap / 2)
    elif right:
        x_pos = x_avg + 0.2 * (Gap / 2)
    else:
        x_pos = x_avg
    
    return x_pos

def process_image(frame):
    edges = detect_edges(frame)
    lines = hough_lines(edges)
    
    if lines is None:
        return (Width/2, Width/2, frame, 0)
    
    left_lines, right_lines = divide_left_right(lines)
    
    lpos = get_line_pos(left_lines, left=True)
    rpos = get_line_pos(right_lines, right=True)
    
    center = (lpos + rpos) / 2
    error = center - Width/2
    angle = error*0.8
    
    cv2.line(frame, (int(lpos), Offset+Gap), (int(lpos), Offset), (255,0,0), 3)
    cv2.line(frame, (int(rpos), Offset+Gap), (int(rpos), Offset), (0,0,255), 3)
    
    return lpos, rpos, frame, angle

def main():
    global motor
    rospy.init_node('lane_follower')
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    rospy.Subscriber("/usb_cam/image_raw/", Image, img_callback)
    pub_angle = rospy.Publisher('steering_angle', Float32, queue_size=10)
    
    print("----- Lane Follower Started -----")
    rate = rospy.Rate(30)
    
    while not rospy.is_shutdown():
        if cv_image.size != (Width*Height*3):
            continue
        
        lpos, rpos, processed_image, steering_angle = process_image(cv_image)
        
        drive(steering_angle, 15)
        pub_angle.publish(Float32(steering_angle))
        
        cv2.imshow("Lane Detection", processed_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        rate.sleep()
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass