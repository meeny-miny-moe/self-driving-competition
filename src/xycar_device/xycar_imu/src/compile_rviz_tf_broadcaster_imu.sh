#!/bin/bash

cython3 -3 --embed -o tf_broadcaster_imu.c tf_broadcaster_imu.py
gcc -Os -I /usr/include/python3.7 tf_broadcaster_imu.c -lpython3.7m -o tf_broadcaster_imu
