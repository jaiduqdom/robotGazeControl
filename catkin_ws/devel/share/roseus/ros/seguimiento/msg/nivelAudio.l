;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::nivelAudio)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'nivelAudio (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::NIVELAUDIO")
  (make-package "SEGUIMIENTO::NIVELAUDIO"))

(in-package "ROS")
;;//! \htmlinclude nivelAudio.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::nivelAudio
  :super ros::object
  :slots (_header _rms ))

(defmethod seguimiento::nivelAudio
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:rms __rms) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _rms (float __rms))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:rms
   (&optional __rms)
   (if __rms (setq _rms __rms)) _rms)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float32 _rms
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float32 _rms
       (sys::poke _rms (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float32 _rms
     (setq _rms (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::nivelAudio :md5sum-) "b7f88596f71fe2965f91f0e52ac92c01")
(setf (get seguimiento::nivelAudio :datatype-) "seguimiento/nivelAudio")
(setf (get seguimiento::nivelAudio :definition-)
      "Header header
float32 rms


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



(provide :seguimiento/nivelAudio "b7f88596f71fe2965f91f0e52ac92c01")


