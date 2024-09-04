#!/usr/bin/env python

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
ROAD_WIDTH = 220

WALL_SIZE = 10
GOAL_WALL_SIZE = 100

SIDE_WALL_SIZE = 10 
COURSE_WALL_SIZE = WALL_SIZE 
STARTING_COORD1 = SCREEN_HEIGHT/3
STARTING_COORD2 = SCREEN_WIDTH - STARTING_COORD1
STARTING_COORD3 = SCREEN_HEIGHT*2/3

START_X = 0
START_Y = 0
START_WIDTH = WALL_SIZE
START_HEIGHT = STARTING_COORD1

GOAL_PICT = [230,10]
GOAL_ANGLE = 0

LOGO_POSI = [380,400]
LOGO_ANGLE = 0

INIT_POSITION = [3.5, 1.15]
INIT_ANGLE = 0.0

OBS = [
    [ 0, 0, WALL_SIZE, SCREEN_HEIGHT ],
    [ 0, 0, SCREEN_WIDTH, WALL_SIZE ],
    [ SCREEN_WIDTH-WALL_SIZE, WALL_SIZE, WALL_SIZE, SCREEN_HEIGHT-2*WALL_SIZE ],
    [ WALL_SIZE, SCREEN_HEIGHT-WALL_SIZE, SCREEN_WIDTH, WALL_SIZE ],
    [ WALL_SIZE+ROAD_WIDTH, WALL_SIZE+ROAD_WIDTH, SCREEN_WIDTH-2*(WALL_SIZE+ROAD_WIDTH), WALL_SIZE ],
    [ WALL_SIZE+ROAD_WIDTH, SCREEN_HEIGHT-(2*WALL_SIZE+ROAD_WIDTH), SCREEN_WIDTH-2*(WALL_SIZE+ROAD_WIDTH),
    WALL_SIZE ],
    [ WALL_SIZE+ROAD_WIDTH, 2*WALL_SIZE+ROAD_WIDTH, WALL_SIZE, SCREEN_HEIGHT-2*(2*WALL_SIZE+ROAD_WIDTH)],
    [ SCREEN_WIDTH-(2*WALL_SIZE+ROAD_WIDTH), 2*WALL_SIZE+ROAD_WIDTH, WALL_SIZE,
    SCREEN_HEIGHT-2*(2*WALL_SIZE+ROAD_WIDTH) ]
]

WARP_ANGLE = 0.0

WARP = [

]

GOAL = [ [230, 11, 22, 220] ]
