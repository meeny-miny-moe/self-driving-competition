#!/bin/bash

cython3 -3 --embed -o imu_3d_matplot.c imu_3d_matplot.py
gcc -Os -I /usr/include/python3.7 imu_3d_matplot.c -lpython3.7m -o imu_3d_matplot
