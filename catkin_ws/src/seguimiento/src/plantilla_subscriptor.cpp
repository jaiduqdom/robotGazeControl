// Nodo subscriptor
// Autor: 
// Descripccion: Plantilla ejemplo nodo subscriptor
// Añadir al en CMakeLists.txt:
//	add_executable(subscriptor src/plantilla_subscriptor.cpp)
//	target_link_libraries(subscriptor ${catkin_LIBRARIES})

#include "ros/ros.h"
#include "std_msgs/Int32.h"


void topicCallback(const std_msgs::Int32::ConstPtr& msg)  //Funcion que se ejecuta cada vez que llega un mensaje
{
  //ROS_INFO("Mensaje Recibido: %d", msg->data);
  ROS_INFO_STREAM("Mensaje Recibido: " << msg->data);
}


int main(int argc, char **argv){

	ros::init(argc, argv, "subscriptor");

	ros::NodeHandle n;
				//se crea objeto subscriptor, "topic" debe coincidir con subscriptor
	ros::Subscriber sub = n.subscribe("topic", 1000, topicCallback);
	ros::spin();		//permite que se invoque sucesivamente el callback
				// Si la función main() hace algo mas en bucle poner ros::spinOnce()

	return 0;
}
