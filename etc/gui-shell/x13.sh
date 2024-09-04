#!/bin/bash

export OPENBLAS_CORETYPE=ARMV8
export PYTHONDONTWRITEBYTECODE=1

source /opt/ros/noetic/setup.bash
source /home/pi/xycar_ws/devel/setup.bash
export ROS_MASTER_URI=http://10.42.0.1:11311
export ROS_HOSTNAME=10.42.0.1

tmp=`grep -r "export lidar_version" ~/.bashrc`
export lidar_version=`echo $tmp | awk -F'=' '{print $2}'`

tmp=`grep -r "export motor_version" ~/.bashrc`
export motor_version=`echo $tmp | awk -F'=' '{print $2}'`

tmp=`grep -r "export ROS_MASTER_URI" ~/.bashrc`
export ROS_MASTER_URI=`echo $tmp | awk -F'=' '{print $2}'`

tmp=`grep -r "export ROS_HOSTNAME" ~/.bashrc`
export ROS_HOSTNAME=`echo $tmp | awk -F'=' '{print $2}'`

roslaunch xycar_slam demo.launch
