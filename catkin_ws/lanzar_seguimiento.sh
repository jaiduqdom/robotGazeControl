echo Lanzamiento de sistema de seguimiento y avatar de la cabeza robótica
# Establecer proyector como monitor primario
# xrandr --output HDMI-0 --mode 854x480 --rate 60 --rotate right --primary
xrandr --output HDMI-0 --mode 1280x720 --primary
sleep 3

# Arrancar el blender
echo Arrancamos el avatar...
#blenderplayer "/home/disa/catkin_ws/src/modelo/modelo chica/rostro_au_jaime.blend"
#nohup blenderplayer -w 854 480 0 0 "/home/disa/catkin_ws/src/modelo/modelo chica/rostro_au_jaime_new.blend" &
#blenderplayer -w 1280 720 0 0 "/home/disa/catkin_ws/src/modelo/490_ajustado_a_proyector.blend" &
#blenderplayer -w 1280 720 0 0 "/home/disa/catkin_ws/src/modelo/510_ajustado_a_proyector.blend" &
blenderplayer -w 1280 720 0 0 "/home/disa/catkin_ws/src/modelo/511.blend" &

sleep 3

# Establecer de nuevo la pantalla normal como monitor primario
xrandr --output DP-1-1 --primary
sleep 3

# Arrancamos el bridge del avatar
# echo Arrancamos el bridge del avatar...
# cd /home/disa/catkin_ws
# rosrun blender_control ros_blender_bridge.py &

# Arrancamos el control de gestos del avatar
# echo Arrancamos el control de gestos del avatar...
# cd /home/disa/catkin_ws/src/blender_control/src
# rosrun blender_control gestion_gestos.py &

# Lanzamos la gráfica de rqt_plot para visualizar red competitiva
rqt_plot /entradaRedCompetitiva/data[0] /entradaRedCompetitiva/data[1] &
rqt_plot /salidaRedCompetitiva/data[0] /salidaRedCompetitiva/data[1] &

#rqt_plot &
#sleep 1
#topicnames=(/entradaRedCompetitiva/data[0], /entradaRedCompetitiva/data[1], /salidaRedCompetitiva/data[0], /salidaRedCompetitiva/data[1])
#for topic in ${topicnames[@]}
#do
#  rqt --command-start-plugin rqt_plot --args "${topic}" &
#done


# Lanzamos el sistema de seguimiento
echo Lanzamos el sistema de seguimiento...
# cd /home/disa/catkin_ws
roslaunch seguimiento seguimientoRobot.launch &

# Lanzamos los gestos (Los gestos se integran en el módulo de seguimiento)
# echo Lanzamos los gestos...
# rosrun blender_control comportamiento.py demo_cabeza_nueva.yaml &


