#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import time
import numpy as np
import statistics
from collections import deque
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32
from xycar_msgs.msg import xycar_motor


bridge = CvBridge()
cv_image = np.empty(shape=[0])
motor_pub = None



def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

## circle fun
def detect_circle(cv_img):
    # 이미지 불러오기
    image = cv_img
    
    
    # 이미지 크기를 절반으로 줄이기
    # image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

    height, width = image.shape[:2]
    cropped_image = image[0:height//2, width//2:width]
   
    # hsv image 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# =============================================================
# #color
    # lower_red = np.array([0, 100, 120])
    # upper_red= np.array([8, 255, 255])
# =============================================================

    ## rgb to hsb================================================
    # target_rgb = np.array([100, 40, 50])

    # target_hsv = cv2.cvtColor(np.uint8([[target_rgb]]), cv2.COLOR_BGR2HSV)[0][0]

    # tolerance = 20
    # s = 100
    # v = 100

    # lower_red = np.array([target_hsv[0] - tolerance , max(0, target_hsv[1] - s), max(0, target_hsv[2] - v)])
    # upper_red = np.array([target_hsv[0] + tolerance , min(255, target_hsv[1] + s), min(255, target_hsv[2] + v)])

    lower_red = np.array([0, 100, 120])
    upper_red= np.array([8, 255, 255])

    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((2, 2), np.uint8)
    
    #eroded_mask = cv2.erode(red_mask, kernel, iterations=1)
    kernel = np.ones((3, 3), np.uint8)
    dilated_mask = cv2.dilate(red_mask, kernel, iterations=3)

    #eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

    # crop_h, crop_w = cropped_image.shape[:2]
    # d_h, d_w = dilated_mask.shape[:2]

    # new_d = dilated_mask[d_h//2 - crop_h//2:d_h//2 + crop_h//2, d_w//2 - crop_w//2:d_w//2 + crop_w//2]

    # result = cv2.bitwise_or(new_d, cropped_image)

    return dilated_mask,cropped_image


def calculate_steering_angle(image, lines):
    height, width = image.shape[:2]

    if lines is None:
        return 0  # 차선이 감지되지 않으면 직진

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
    
    # 여기서 상단 부분을 검정색으로 만듭니다
    black_region_height = int(height * 0.7)  # 상위 70%를 검정색으로 (조정 가능)
    mask[:black_region_height, :] = 0
    
    masked_morphed = cv2.bitwise_and(morphed, mask)
    
    # 허프 변환을 이용한 직선 검출
    lines = cv2.HoughLinesP(masked_morphed, 1, np.pi/180, 40, minLineLength=35, maxLineGap=120)
    
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
    motor_msg.speed = 0
    motor_pub.publish(motor_msg)


def main():
    global motor_pub
    rospy.init_node('lane_follower', anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, img_callback, queue_size=1)
    
    motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    angle_pub = rospy.Publisher('steering_angle', Float32, queue_size=1)
    rate = rospy.Rate(30)
 
    LINE_THRESHOLD = 19  # 이 값 이상의 선이 감지되면 정지
    COOLDOWN_TIME =3
    lab = 0
    last_detection_time = rospy.Time(0)
    steering_angle = 0
  
    lab_time = rospy.Time.now()
    time_list = [13, 10]
    n = 0
    #Front
   

    

    while not rospy.is_shutdown():
        

        if cv_image.size != 0:


            #cv2.imshow("cv_image", cv_image)


            # before_angle = steering_angle
            gray, blur, sobel, binary, masked_morphed, result, lines = detect_edges(cv_image)
            steering_angle, line_count = hough_transform(cv_image, lines)

            ##test
            
            circle_img, crop_img = detect_circle(cv_image)
            
            h, w = circle_img.shape[:2]
            
            hh, ww = h*3, w*3
            
            resize_img = cv2.resize(crop_img, (hh, ww), interpolation = cv2.INTER_LINEAR)
            
            #cirle_img = circle_img.resize(circle_img, (circle_img[1]*3, circle_img[0]*3))
            #crop_img = crop_img.resize(crop_img, (crop_img[1]*3, crop_img[0]*3))

            cv2.imshow("circle_img", circle_img)
            cv2.imshow("img", crop_img)
            # cv2.imshow("resize", result_1)
            
            current_time = rospy.Time.now()
        
          



         

            if (rospy.Time.now() - lab_time).to_sec() > time_list[n]:
                n = 0

                if line_count >= LINE_THRESHOLD:
                    if lab == 2:
                        start_time = rospy.Time.now()
                        while (rospy.Time.now() - start_time).to_sec() < 0.5:
                            drive(10,10)
                        
                        print("if")
                        break
                        
                    else:

                        lab += 1
                        lab_time = rospy.Time.now()
                        
                        start_time = rospy.Time.now()
                        while (rospy.Time.now() - start_time).to_sec() < 0.5:
                            drive(5,25)

                        """
                        start_time = rospy.Time.now()
                        while (rospy.Time.now() - start_time).to_sec() < 0.8:
                            if cv_image.size != 0:
                                # before_angle = steering_angle
                                '''gray, blur, sobel, binary, masked_morphed, result,'''
                                lines = detect_edges(cv_image)
                                steering_angle, line_count = hough_transform(cv_image, lines)
                                drive(4,25)
                        """
                

                  
            
                    
            #cv2.imshow("Steering Frame", result)
            #print(f"Steering Angle: {steering_angle:.2f}, Lines: {line_count}, lab: {lab}")

            angle_pub.publish(Float32(steering_angle))
            drive(steering_angle*2.5,25) 

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        rate.sleep()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
        exit()
    except rospy.ROSInterruptException:
        pass