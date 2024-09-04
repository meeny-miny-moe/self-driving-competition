#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import math
from matplotlib import pyplot as plt
from std_msgs.msg import Int32MultiArray

class UltraPlot:
    
    def __init__(self):
        self.sub_data = None
        self.ultra_data = None
        self.count = 0
        rospy.init_node('ultra_plot', anonymous=True)
        rospy.Subscriber('xycar_ultrasonic', Int32MultiArray, self.callback)
        self.plot_init()

    def plot_init(self):
        plt.title("Ultra plot")
        plt.xlabel("count")
        plt.ylabel("distance")
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.ion()

    def callback(self, data):
        self.sub_data = data.data

        callback_value = list(self.sub_data)

        # 8개 초음파 데이터 중에서 하나를 선택한다
        self.ultra_data = callback_value[2] 

    def loop(self):
        while not rospy.is_shutdown():
            if self.ultra_data != None:
                self.count += 1
                plt.plot(self.count, self.ultra_data, 'bo', markersize=3)
                plt.show()
                plt.pause(0.005)
                
                if self.count > 100:
                    self.count = 0
                    plt.clf()
                    self.plot_init()

if __name__ == '__main__':
    ultra_plot = UltraPlot()
    ultra_plot.loop()
    rospy.spin()
