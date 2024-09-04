#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################################
# 프로그램 명 : check_picam_device_port.py
# 작  성  자 : (주)자이트론
# 본 프로그램은 상업라이센스에 의해 제공되므로 무단배포 및 상업적 이용을 금합니다.
####################################################################

#=============================================
# 함께 사용되는 각종 파이썬 패키지들의 import 선언부
#=============================================
import subprocess, re

#=============================================
# Pi-Cam을 찾아내는데 사용되는 문자열
#=============================================
device_string = "bcm2835-v4l2-0"
#device_string = "bcm2835-isp"
#device_string = "HD USB"
 
#=============================================
# 변경할 런치파일 이름
#=============================================
filename = "/home/pi/xycar_ws/src/xycar_device/pi_cam/launch/pi_cam.launch"

#=============================================
# v4l2-ctl 명령을 실행한 후에 그 결과화면을 이용함
# "v4l2-ctl --list-devices" 결과화면은 다음과 같음
#
# bcm2835-codec-decode (platform:bcm2835-codec):
#   	/dev/video10
#   	/dev/video11
#
# bcm2835-isp (platform:bcm2835-isp):
#   	/dev/video13
#   	/dev/video14
#
# mmal service 16.1 (platform:bcm2835-v4l2-0):
#   	/dev/video2
#
# HD USB Camera: HD USB Camera (usb-0000:01:00.0-1.2):
#   	/dev/video0
#   	/dev/video1
#
# 위 결과에서 device_string ("bcm2835-v4l2-0")
# 부분을 찾고 바로 그 다음 라인을 읽어들여서 
# /video2 부분을 추출한 후에
# video 뒤쪽의 숫자를 스트링으로 반환한다.
#=============================================
def find_device_with_string(device_string):
    devices = subprocess.check_output(["v4l2-ctl", "--list-devices"]).decode("utf-8")
    devices_lines = devices.split('\n')
    for i, line in enumerate(devices_lines):
        if device_string in line and i + 1 < len(devices_lines):
            device_info = devices_lines[i + 1].strip().split(' ')[0].split('/')[-1]  
            device_num = re.search(r'video(\d+)', device_info).group(1)
            return device_num
    return 2

#=============================================
# video7 스트링에서 맨 뒤의 숫자 '7'을 확보했으므로
# 이걸 이용해서 pi-cma.launch 파일을 수정한다.
# 런치파일의 내용은 다음과 같다.
#
# <launch>
#  <node name="pi_cam_node" pkg="pi_cam" type="pi_cam_node" respawn="false" output="screen" >
#    <param name="VideoDevice" type="int" value="2"/>
#    <param name="Hz" type="int" value="30" />
#    <param name="Resolution" type="int" value="1" />
#  </node>  
# </launch>
#
# VideoDevice 파라미터의 value 부분을 바꾼다.
# 예를 들어 기존 value="2" 가 value="13"으로 바뀐다.
#=============================================

def replace_video_value(filename, new_video_value):
    # 파일을 읽기 모드로 엽니다.
    with open(filename, 'r') as file:
        filedata = file.read()

    # VideoDevice의 값을 변경합니다.    
    pattern = r'(\<param\s+name=\"VideoDevice\"\s+type=\"int\"\s+value=\")(\d+)(\"\/\>)'
    replaced_data = re.sub(pattern, rf'\g<1>{new_video_value}\g<3>', filedata)

    # 변경된 데이터를 파일에 씁니다.
    with open(filename, 'w') as file:
        file.write(replaced_data)

    #print(replaced_data)

#=============================================
# 메인 함수
#=============================================
def main():

    new_video_value = find_device_with_string(device_string)
    print("pi_cam # is:", new_video_value)

    if(new_video_value != None):
        print("OK, found pi_cam camera.")
        replace_video_value(filename, new_video_value)
    else:
        print("Please check pi_cam.launch.")

if __name__ == "__main__":
    main()
