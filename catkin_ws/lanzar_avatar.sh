# Establecer proyector como monitor primario
#xrandr --output HDMI-0 --mode 854x480 --rate 60 --rotate right --primary

xrandr --output HDMI-0 --mode 1280x720 --primary
sleep 3

# Arrancar el blender
#blenderplayer "/home/disa/catkin_ws/src/modelo/modelo chica/rostro_au_jaime.blend"
#nohup blenderplayer -w 854 480 0 0 "/home/disa/catkin_ws/src/modelo/modelo chica/rostro_au_jaime_new.blend" &
#nohup blenderplayer -w 1280 720 0 0 "/home/disa/catkin_ws/src/modelo/490_ajustado_a_proyector.blend" &
nohup blenderplayer -w 1280 720 0 0 "/home/disa/catkin_ws/src/modelo/511.blend" &

sleep 3

# Establecer pantalla normal como monitor primario
xrandr --output DP-1-1 --primary

