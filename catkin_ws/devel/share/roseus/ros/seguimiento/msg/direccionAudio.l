;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::direccionAudio)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'direccionAudio (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::DIRECCIONAUDIO")
  (make-package "SEGUIMIENTO::DIRECCIONAUDIO"))

(in-package "ROS")
;;//! \htmlinclude direccionAudio.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::direccionAudio
  :super ros::object
  :slots (_header _vad _doa ))

(defmethod seguimiento::direccionAudio
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:vad __vad) nil)
    ((:doa __doa) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _vad __vad)
   (setq _doa (round __doa))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:vad
   (&optional __vad)
   (if __vad (setq _vad __vad)) _vad)
  (:doa
   (&optional __doa)
   (if __doa (setq _doa __doa)) _doa)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; bool _vad
    1
    ;; int32 _doa
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; bool _vad
       (if _vad (write-byte -1 s) (write-byte 0 s))
     ;; int32 _doa
       (write-long _doa s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; bool _vad
     (setq _vad (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _doa
     (setq _doa (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::direccionAudio :md5sum-) "26d1631e5cd32777f7f0538fff298a47")
(setf (get seguimiento::direccionAudio :datatype-) "seguimiento/direccionAudio")
(setf (get seguimiento::direccionAudio :definition-)
      "Header header
bool vad
int32 doa


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



(provide :seguimiento/direccionAudio "26d1631e5cd32777f7f0538fff298a47")


