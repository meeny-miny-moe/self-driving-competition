#!/bin/bash

cython3 -3 --embed -o imu_3d_pygame.c imu_3d_pygame.py
gcc -Os -I /usr/include/python3.7 imu_3d_pygame.c -lpython3.7m -o imu_3d_pygame
