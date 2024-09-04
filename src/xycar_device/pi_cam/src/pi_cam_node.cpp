#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>

#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <sensor_msgs/CameraInfo.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "pi_cam_node");
    ros::NodeHandle n;
    ros::NodeHandle pn("~");

    ROS_INFO("pi_cam_node Open");

    int video_device = 0;
    int hz = 30;
    int resolution = 0;

    int width = 0;
    int height = 0;

    pn.param<int>("VideoDevice", video_device, 0);
    pn.param<int>("Hz", hz, 30);
    pn.param<int>("Resolution", resolution , 0);

    sensor_msgs::Image camera_image;
    cv_bridge::CvImage cv_bridge;
    ros::Publisher camera_image_publish = n.advertise<sensor_msgs::Image>("pi_cam", 1000);

    std_msgs::Header header;
    ros::Rate loop_rate(hz);

    cv::Mat image;

    cv::VideoCapture vc(video_device);

    if(vc.isOpened() != 1)
    {
        ROS_ERROR("Non-existent camera device number");
	return 0;
    }

    if(resolution == 1)
    {
        width = 640;
        height = 480;
    }
    else if(resolution == 2)
    {
        width = 320;
        height = 240;
    }
    else if(resolution == 3)
    {
        width = 160;
        height = 120;
    }
    else
    {
        width = vc.get(cv::CAP_PROP_FRAME_WIDTH);
        height = vc.get(cv::CAP_PROP_FRAME_HEIGHT);
    }

    vc.set(cv::CAP_PROP_FRAME_WIDTH, width);
    vc.set(cv::CAP_PROP_FRAME_HEIGHT, height);

    ros::Publisher camera_info_publish = n.advertise<sensor_msgs::CameraInfo>("pi_cam/camera_info", 1000);
    sensor_msgs::CameraInfo camera_info;

    camera_info.width = width;
    camera_info.height = height;

    ROS_INFO("OpenCV version : %s ", CV_VERSION);
    ROS_INFO("Camera Device Number : %d ", video_device);
    ROS_INFO("Camera Resolution : %dx%d ", width, height);

    while(ros::ok())
    {
        vc >> image;

        flip(image, image , 0);  // Image flip (upside down)

        cv_bridge = cv_bridge::CvImage(header,sensor_msgs::image_encodings::BGR8,image);
        cv_bridge.toImageMsg(camera_image);

        camera_image.header.stamp = ros::Time::now();
        camera_image.header.frame_id = "pi_cam";
        camera_image_publish.publish(camera_image);

        camera_info.header.stamp = ros::Time::now();
        camera_info.header.frame_id = "pi_cam";
        camera_info_publish.publish(camera_info);

        ros::spinOnce();
	loop_rate.sleep();
    }

    ROS_INFO("pi_cam_node Close");

    return 0;

}
