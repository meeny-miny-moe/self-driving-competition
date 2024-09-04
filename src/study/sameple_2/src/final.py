#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
import statistics
from collections import deque
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32
from xycar_msgs.msg import xycar_motor
from std_msgs.msg import Int32MultiArray
from functools import wraps
import os

bridge = CvBridge()
cv_image = np.empty(shape=[0])
motor_pub = None



def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    

# 조향 각도 조절
def calculate_steering_angle(image, lines):
    height, width = image.shape[:2]

    # 차선이 감지되지 않으면 직진
    if lines is None:
        return 0 
    
    # 차선이 감지된 경우
    left_lines = []
    right_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue  # 수직선 무시
        slope = (y2 - y1) / (x2 - x1)
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)

    # 왼쪽과 오른쪽 차선의 평균 위치 계산
    left_x = 0
    right_x = width
    if len(left_lines) > 0:
        left_x = np.mean([line[0][0] for line in left_lines])
    if len(right_lines) > 0:
        right_x = np.mean([line[0][0] for line in right_lines])

    # 차선 중심 계산
    center = (left_x + right_x) / 2

    # 차량의 현재 위치 (화면 하단 중앙)
    car_position = width / 2

    # 편차 계산
    deviation = center - car_position

    # 조향 각도 계산 (단순화된 예시)
    steering_angle = deviation / (width / 2) * 45  # 최대 ±45도 조향 가정

    return steering_angle

def hough_transform(image, lines):
    line_image = np.copy(image)
    line_count = 0

    if lines is not None:
        line_count = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    steering_angle = calculate_steering_angle(image, lines)
    cv2.putText(line_image, f"Steering Angle: {steering_angle:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(line_image, f"Lines: {line_count}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #cv2.imshow("Steering Frame", line_image)
    return steering_angle, line_count

    

def detect_edges(image):
    height, width = image.shape[:2]
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가우시안 블러 적용
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 소벨 엣지 검출
    sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobelx**2 + sobely**2)
    sobel = np.uint8(sobel / np.max(sobel) * 255)
    
    # 이진화
    _, binary = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)
    
    # 모폴로지 연산
    kernel = np.ones((5,5), np.uint8)
    morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 관심 영역 설정 (ROI)
    mask = np.zeros_like(morphed)
    roi_corners = np.array([[(0, height), (width//2 - 50, height//2 + 50), 
                             (width//2 + 50, height//2 + 50), (width, height)]], dtype=np.int32)
    cv2.fillPoly(mask, roi_corners, 255)
    
    # 상단 부분을 검정색
    black_region_height = int(height * 0.7)  # 상위 70%를 검정색으로 (조정 가능)
    mask[:black_region_height, :] = 0
    
    masked_morphed = cv2.bitwise_and(morphed, mask)
    
    # 허프 변환을 이용한 직선 검출
    lines = cv2.HoughLinesP(masked_morphed, 1, np.pi/180, 50, minLineLength=50, maxLineGap=120)
    # lines = cv2.HoughLinesP(masked_morphed, 1, np.pi/180, 40, minLineLength=35, maxLineGap=120)

    # 검출된 라인 그리기
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # 원본 이미지와 라인 이미지 합치기
    result = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    
    return gray, blur, sobel, binary, masked_morphed, result, lines



def drive(angle,speed):
    motor_msg = xycar_motor()
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor_pub.publish(motor_msg)
    


def main():
    global motor_pub
    global angle_pub
    
    rospy.init_node('lane_follower', anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, img_callback)
    rospy.wait_for_message("/usb_cam/image_raw/", Image)
    
    
    motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    angle_pub = rospy.Publisher('steering_angle', Float32, queue_size=1)
    
    
    LINE_THRESHOLD = 22
    lab = 0
    steering_angle = 0



    while not rospy.is_shutdown():

        if cv_image.size != 0:

            lines = detect_edges(cv_image)
            steering_angle, line_count = hough_transform(cv_image, lines)

            #print(f"Steering Angle: {steering_angle:.2f}, Lines: {line_count}, lab: {lab}")
        
            # 전제조건이 line_count가 LINE_THRESHOLD보다 커야지 lab을 조사함
            if line_count >= LINE_THRESHOLD:
                # 한바퀴 돌고 두바퀴 째 멈춤
                if lab >= 1:
                    start_time = rospy.Time.now()
                    while (rospy.Time.now() - start_time).to_sec() < 1:
                        drive(5,5)
                    
                    print("stop car")
                    print()
                    break

                # 출발선 무시하고 주행
                else:
                    print("lab count + 1")
                    print()
                    lab += 1
                    
                    start_time = rospy.Time.now()
                    while (rospy.Time.now() - start_time).to_sec() < 1:
                        drive(-5, 25)
                    continue
                    
            if steering_angle*3.2 >= 100:
                drive(100,25)
            elif steering_angle*3.2 <= -100:
                drive(-100,25)
            else:
                drive(steering_angle*3.2,25) 

      

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
        
    except rospy.ROSInterruptException:
        pass
    
