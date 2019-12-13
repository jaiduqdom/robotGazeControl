;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::ganador)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'ganador (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::GANADOR")
  (make-package "SEGUIMIENTO::GANADOR"))

(in-package "ROS")
;;//! \htmlinclude ganador.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::ganador
  :super ros::object
  :slots (_header _ganador _pan _tilt ))

(defmethod seguimiento::ganador
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:ganador __ganador) 0)
    ((:pan __pan) 0.0)
    ((:tilt __tilt) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _ganador (round __ganador))
   (setq _pan (float __pan))
   (setq _tilt (float __tilt))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:ganador
   (&optional __ganador)
   (if __ganador (setq _ganador __ganador)) _ganador)
  (:pan
   (&optional __pan)
   (if __pan (setq _pan __pan)) _pan)
  (:tilt
   (&optional __tilt)
   (if __tilt (setq _tilt __tilt)) _tilt)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int32 _ganador
    4
    ;; float32 _pan
    4
    ;; float32 _tilt
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32 _ganador
       (write-long _ganador s)
     ;; float32 _pan
       (sys::poke _pan (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _tilt
       (sys::poke _tilt (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32 _ganador
     (setq _ganador (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _pan
     (setq _pan (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _tilt
     (setq _tilt (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::ganador :md5sum-) "acd34bbdf6fbc35f775b9daf437ae7b2")
(setf (get seguimiento::ganador :datatype-) "seguimiento/ganador")
(setf (get seguimiento::ganador :definition-)
      "Header header
int32 ganador
float32 pan
float32 tilt


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



(provide :seguimiento/ganador "acd34bbdf6fbc35f775b9daf437ae7b2")


