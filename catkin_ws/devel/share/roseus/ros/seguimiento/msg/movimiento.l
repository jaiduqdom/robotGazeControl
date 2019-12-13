;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::movimiento)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'movimiento (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::MOVIMIENTO")
  (make-package "SEGUIMIENTO::MOVIMIENTO"))

(in-package "ROS")
;;//! \htmlinclude movimiento.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::movimiento
  :super ros::object
  :slots (_header _enMovimiento _theta_robot _psi_robot ))

(defmethod seguimiento::movimiento
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:enMovimiento __enMovimiento) nil)
    ((:theta_robot __theta_robot) 0.0)
    ((:psi_robot __psi_robot) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _enMovimiento __enMovimiento)
   (setq _theta_robot (float __theta_robot))
   (setq _psi_robot (float __psi_robot))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:enMovimiento
   (&optional __enMovimiento)
   (if __enMovimiento (setq _enMovimiento __enMovimiento)) _enMovimiento)
  (:theta_robot
   (&optional __theta_robot)
   (if __theta_robot (setq _theta_robot __theta_robot)) _theta_robot)
  (:psi_robot
   (&optional __psi_robot)
   (if __psi_robot (setq _psi_robot __psi_robot)) _psi_robot)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; bool _enMovimiento
    1
    ;; float32 _theta_robot
    4
    ;; float32 _psi_robot
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; bool _enMovimiento
       (if _enMovimiento (write-byte -1 s) (write-byte 0 s))
     ;; float32 _theta_robot
       (sys::poke _theta_robot (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _psi_robot
       (sys::poke _psi_robot (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; bool _enMovimiento
     (setq _enMovimiento (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _theta_robot
     (setq _theta_robot (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _psi_robot
     (setq _psi_robot (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::movimiento :md5sum-) "0ea04302753729942b7a5e567e1e615e")
(setf (get seguimiento::movimiento :datatype-) "seguimiento/movimiento")
(setf (get seguimiento::movimiento :definition-)
      "Header header
bool enMovimiento
float32 theta_robot
float32 psi_robot


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



(provide :seguimiento/movimiento "0ea04302753729942b7a5e567e1e615e")


