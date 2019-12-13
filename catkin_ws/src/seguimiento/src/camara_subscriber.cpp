#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>

using namespace std;
using namespace cv;

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
  try
  {
    //cv::imshow("Original", cv_bridge::toCvShare(msg, "bgr8")->image);
    
    //Espera 30 milisegundos antes de sobreescribir las imagenes
    cv::waitKey(30);

    //Muestra imagen recibida y su tamaño
    Mat colorFrame=cv_bridge::toCvShare(msg, "bgr8")->image;
    imshow("Color", colorFrame);
    //ROS_INFO_STREAM("Filas:"<< colorFrame.rows <<"Columnas:"<< colorFrame.cols);

    //Transforma a imagen de grises
    Mat grisFrame;
    cvtColor(colorFrame, grisFrame, COLOR_BGR2GRAY); 
    imshow("Gris", grisFrame);

    //Binariza
    Mat binFrame;
    threshold(grisFrame, binFrame, 0, 255, THRESH_BINARY_INV | CV_THRESH_OTSU);
    imshow("Bin", binFrame);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "image_listener");
  ros::NodeHandle nh;
  image_transport::ImageTransport it(nh);
  image_transport::Subscriber sub = it.subscribe("/webcam/image_raw/", 1, imageCallback);
  
  cv::namedWindow("Color", WINDOW_NORMAL);
  cv::namedWindow("Gris", WINDOW_NORMAL);
  cv::namedWindow("Bin", WINDOW_NORMAL);
  ros::spin();
  cv::destroyWindow("Color");
  cv::destroyWindow("Gris");
  cv::destroyWindow("Bin");
  ros::shutdown();
  return 0;

}
