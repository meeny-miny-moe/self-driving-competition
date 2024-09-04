#!/bin/bash

cython3 -3 --embed -o imu_node.c imu_node.py
gcc -Os -I /usr/include/python3.7 imu_node.c -lpython3.7m -o imu_node
