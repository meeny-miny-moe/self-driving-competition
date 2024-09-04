# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "image_transport;roscpp;rospy;std_msgs;std_srvs;sensor_msgs;camera_info_manager;dynamic_reconfigure".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lusb_cam".split(';') if "-lusb_cam" != "" else []
PROJECT_NAME = "usb_cam"
PROJECT_SPACE_DIR = "/home/pi/xycar_ws/install"
PROJECT_VERSION = "0.3.6"
