;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::salidaKalman)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'salidaKalman (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::SALIDAKALMAN")
  (make-package "SEGUIMIENTO::SALIDAKALMAN"))

(in-package "ROS")
;;//! \htmlinclude salidaKalman.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::salidaKalman
  :super ros::object
  :slots (_header _identificador _pan _tilt ))

(defmethod seguimiento::salidaKalman
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:identificador __identificador) (make-array 0 :initial-element 0 :element-type :integer))
    ((:pan __pan) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:tilt __tilt) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _identificador __identificador)
   (setq _pan __pan)
   (setq _tilt __tilt)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:identificador
   (&optional __identificador)
   (if __identificador (setq _identificador __identificador)) _identificador)
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
    ;; int32[] _identificador
    (* 4    (length _identificador)) 4
    ;; float32[] _pan
    (* 4    (length _pan)) 4
    ;; float32[] _tilt
    (* 4    (length _tilt)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32[] _identificador
     (write-long (length _identificador) s)
     (dotimes (i (length _identificador))
       (write-long (elt _identificador i) s)
       )
     ;; float32[] _pan
     (write-long (length _pan) s)
     (dotimes (i (length _pan))
       (sys::poke (elt _pan i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _tilt
     (write-long (length _tilt) s)
     (dotimes (i (length _tilt))
       (sys::poke (elt _tilt i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32[] _identificador
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _identificador (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _identificador i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; float32[] _pan
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _pan (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _pan i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _tilt
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tilt (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _tilt i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get seguimiento::salidaKalman :md5sum-) "258285ea72a30809b9246ee654073a66")
(setf (get seguimiento::salidaKalman :datatype-) "seguimiento/salidaKalman")
(setf (get seguimiento::salidaKalman :definition-)
      "Header header
int32[] identificador
float32[] pan
float32[] tilt


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



(provide :seguimiento/salidaKalman "258285ea72a30809b9246ee654073a66")


