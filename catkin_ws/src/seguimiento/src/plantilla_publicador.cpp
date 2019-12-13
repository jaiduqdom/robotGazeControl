// Nodo publicador
// Autor: 
// Descripccion: Plantilla ejemplo nodo publicador
// Añadir al en CMakeLists.txt:
//	add_executable(publicador src/plantilla_publicadorr.cpp)
//	target_link_libraries(publicador ${catkin_LIBRARIES})


#include "ros/ros.h"
#include "std_msgs/Int32.h" 		// Aqui se incluyen los includes de los mensajes 
//#include <geometry_msgs/Twist.h>  	// Para geometry_msgs::Twist


int main(int argc, char **argv){
	ros::init(argc, argv, "publicador"); //inicializa el sistema ROS
	ros::NodeHandle n;		//Declaramos manejador

	//Creamnos el objeto publicador
	ros::Publisher pub = n.advertise<std_msgs::Int32>("topic", 1000);

	ros::Rate loop_rate(10);  	//especifica la frecuencia de ejecución del bucle 10 veces/s
	int count = 0;
	while (ros::ok()) {		//bucle indefinido hasta que matemos el nodo Ctrl-C
					//Creamos el mensaje
		std_msgs::Int32 msg;	//Declaramos mensaje
		msg.data=count++;
		ROS_INFO("Mensaje publicado: %d", msg.data); //Sacamos por el terminal
		// ROS_INFO_STREAM("Mensaje publicado: " << msg.data); //Sacamos por el terminal c++

		pub.publish(msg); 	//publicamos mensaje

		ros::spinOnce();	
		loop_rate.sleep();	//Se duerme para ajustar el loop_rate
	}
}






		

