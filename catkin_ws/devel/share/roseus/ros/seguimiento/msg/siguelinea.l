;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::siguelinea)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'siguelinea (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::SIGUELINEA")
  (make-package "SEGUIMIENTO::SIGUELINEA"))

(in-package "ROS")
;;//! \htmlinclude siguelinea.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::siguelinea
  :super ros::object
  :slots (_header _distancia _angulo ))

(defmethod seguimiento::siguelinea
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:distancia __distancia) 0.0)
    ((:angulo __angulo) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _distancia (float __distancia))
   (setq _angulo (float __angulo))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:distancia
   (&optional __distancia)
   (if __distancia (setq _distancia __distancia)) _distancia)
  (:angulo
   (&optional __angulo)
   (if __angulo (setq _angulo __angulo)) _angulo)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float32 _distancia
    4
    ;; float32 _angulo
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float32 _distancia
       (sys::poke _distancia (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angulo
       (sys::poke _angulo (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float32 _distancia
     (setq _distancia (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angulo
     (setq _angulo (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::siguelinea :md5sum-) "8ba4eeb657900659451097c3c7c247d9")
(setf (get seguimiento::siguelinea :datatype-) "seguimiento/siguelinea")
(setf (get seguimiento::siguelinea :definition-)
      "Header header
float32 distancia
float32 angulo

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :seguimiento/siguelinea "8ba4eeb657900659451097c3c7c247d9")


