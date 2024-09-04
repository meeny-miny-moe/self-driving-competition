#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import rospy
import os
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
cv_image = np.empty(shape=[0])

def img_callback(data):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

rospy.init_node('cam_tune', anonymous=True)
rospy.Subscriber("/usb_cam/image_raw", Image, img_callback)
rospy.wait_for_message("/usb_cam/image_raw", Image)
print("Camera Ready --------------")

count = 1

while not rospy.is_shutdown():
    if cv_image.size != 0:  # cv_image가 비어있지 않은 경우에만 처리
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edge_img = cv2.Canny(np.uint8(blur_gray), 60, 70)

        # 원본 이미지 저장
        
        
        filename = f"frame_{count}.jpg"
        path = "/home/pi/downloads/picture/"
        filepath = os.path.join(path, filename)
        cv2.imwrite(filepath, cv_image)
        count = count + 1
        print(f"Image saved to {filepath}")
            
        # 이미지 디스플레이
        cv2.imshow("original", cv_image)
        cv2.imshow("gray", gray)
        cv2.imshow("gaussian blur", blur_gray)
        cv2.imshow("edge", edge_img)
        cv2.waitKey(1)

out.release()
cv2.destroyAllWindows()
