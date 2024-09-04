#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
cv_image = np.empty(shape=[0])

def detect_line_segments(edges):
    rho = 1  # 거리 해상도 (픽셀 단위)
    angle = np.pi / 180  # 각도 해상도 (라디안 단위)
    min_threshold = 10  # 최소 투표(교차점) 개수
    min_line_length = 8  # 선의 최소 길이
    max_line_gap = 4  # 선 간격의 최대 길이

    line_segments = cv2.HoughLinesP(edges, rho, angle, min_threshold, 
                                    minLineLength=min_line_length, 
                                    maxLineGap=max_line_gap)

    return line_segments

def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

def bird_eye_view(image):
    height, width = image.shape[:2]
    
    # 원근 변환 적용을 위한 네 개의 점 설정 (원본 이미지에서의 좌표)
    src_points = np.float32([
        [width * 0.45, height * 0.65],
        [width * 0.55, height * 0.65],
        [width * 0.1, height],
        [width * 0.9, height]
    ])
    
    # 변환 후의 네 개의 점 설정 (변환된 이미지에서의 좌표)
    dst_points = np.float32([
        [width * 0.2, 0],
        [width * 0.8, 0],
        [width * 0.2, height],
        [width * 0.8, height]
    ])
    
    # 변환 행렬 계산
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # 원근 변환 적용
    bird_eye_image = cv2.warpPerspective(image, matrix, (width, height))
    
    return bird_eye_image

def detect_edges(image):
    height, width = image.shape[:2]
    black_region_height = int(height * 0.4)  # 상위 40%를 검정색으로
    image[:black_region_height, :] = 0
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
    
    kernel = np.ones((5,5), np.uint8)
    eroded_mask = cv2.erode(combined_mask, kernel, iterations=1)
    dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=1)
    
    combined_result = cv2.bitwise_and(image, image, mask=dilated_mask)
    
    gray = cv2.cvtColor(combined_result, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edges = cv2.Canny(blur, 50, 150)
    
    bird_eye_edges = bird_eye_view(edges)
    
    line_segments = detect_line_segments(bird_eye_edges)
    
    line_image = np.zeros_like(image)
    
    if line_segments is not None:
        for line in line_segments:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                

    bird_eye_image = bird_eye_view(image)
    result = cv2.addWeighted(bird_eye_image, 0.8, line_image, 1, 0)

    return yellow_mask, white_mask, combined_mask, combined_result, blur, edges, result, angle

def main():
    rospy.init_node('lane_detection_node', anonymous=True)
    rospy.Subscriber("/camera/rgb/image_raw", Image, img_callback)
    
    while not rospy.is_shutdown():
        if cv_image.size != 0:
            yellow_mask, white_mask, combined_mask, combined_result, blur, edges, result, angle = detect_edges(cv_image)
            
            print("Detected angles:", angle)

            cv2.imshow("Yellow Mask", yellow_mask)
            cv2.imshow("White Mask", white_mask)
            cv2.imshow("Combined Mask", combined_mask)
            cv2.imshow("Combined Result", combined_result)
            cv2.imshow("Blur", blur)
            cv2.imshow("Edges", edges)
            cv2.imshow("Result", result)
            cv2.waitKey(1)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
