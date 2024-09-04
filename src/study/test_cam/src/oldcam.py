#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32




bridge = CvBridge()
cv_image = np.empty(shape=[0])

def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
 



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



def hough_transform(edges, image):
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=35, maxLineGap=120)
    line_image = np.copy(image)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    steering_angle = calculate_steering_angle(image, lines)
    cv2.putText(line_image, f"Steering Angle: {steering_angle:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return line_image, steering_angle

def detect_edges(image):
    # 윗부분 삭제
    height, width = image.shape[:2]
    black_region_height = int(height * 0.7)  # 상위 50%를 검정색으로
    image[:black_region_height, :] = 0

    # BGR에서 HSV 색공간으로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 노란색 범위 정의 (HSV)
    lower_yellow = np.array([0, 80, 90])
    upper_yellow = np.array([80, 255, 255])

    # 흰색 범위 정의 (HSV)
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([190, 50, 255])

    # 마스크 생성
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    # 형태학적 연산을 위한 커널
    kernel = np.ones((3, 3), np.uint8)
    
    dilated_mask = cv2.dilate(combined_mask, kernel, iterations=1)

    eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)
    
    

    # 원본 이미지에 합쳐진 마스크 적용
    combined_result = cv2.bitwise_and(image, image, mask=eroded_mask)

    # 그레이스케일로 변환
    gray = cv2.cvtColor(combined_result, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny 엣지 검출 적용
    edges = cv2.Canny(blur, 50, 150)

    return yellow_mask, white_mask, combined_mask, combined_result, blur, edges

def main():
    
    
    rospy.init_node('my_cam', anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, img_callback)
    #222
    pub = rospy.Publisher('memo', Float32, queue_size=5)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        if cv_image.size != 0:
            yellow_mask, white_mask, combined_mask, combined_result, blur, edges = detect_edges(cv_image)
            line_image, steering_angle = hough_transform(edges, cv_image)
            #cv2.imshow("white_mask", white_mask)
            #cv2.imshow("yellow_mask", yellow_mask)
            #cv2.imshow("blur",blur)
            #cv2.imshow("Combined Result", combined_result)
            cv2.imshow("Steering Frame", line_image)
            cv2.imshow("original", cv_image)

            
            #print(f"Steering Angle: {steering_angle:.2f}")
            #3
            
            
            pub.publish(steering_angle)
       
         

            cv2.waitKey(1)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass



