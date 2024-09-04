#!/bin/bash

source /opt/ros/noetic/setup.bash
source /home/pi/xycar_ws/devel/setup.bash
export ROS_MASTER_URI=http://10.42.0.1:11311
export ROS_HOSTNAME=10.42.0.1

export PYTHONDONTWRITEBYTECODE=1 

alias cm='cd /home/pi/xycar_ws && catkin_make'

export PYTHONPATH=/home/pi/xycar_ws/devel/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages

python /home/pi/xycar_ws/src/xycar_device/pi_cam/src/check_picam_device_port.py
roslaunch pi_cam pi_cam_viewer.launch