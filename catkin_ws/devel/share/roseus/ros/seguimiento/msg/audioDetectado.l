;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::audioDetectado)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'audioDetectado (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::AUDIODETECTADO")
  (make-package "SEGUIMIENTO::AUDIODETECTADO"))

(in-package "ROS")
;;//! \htmlinclude audioDetectado.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::audioDetectado
  :super ros::object
  :slots (_header _audioDetectado _inicio _final ))

(defmethod seguimiento::audioDetectado
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:audioDetectado __audioDetectado) nil)
    ((:inicio __inicio) 0)
    ((:final __final) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _audioDetectado __audioDetectado)
   (setq _inicio (round __inicio))
   (setq _final (round __final))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:audioDetectado
   (&optional __audioDetectado)
   (if __audioDetectado (setq _audioDetectado __audioDetectado)) _audioDetectado)
  (:inicio
   (&optional __inicio)
   (if __inicio (setq _inicio __inicio)) _inicio)
  (:final
   (&optional __final)
   (if __final (setq _final __final)) _final)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; bool _audioDetectado
    1
    ;; int32 _inicio
    4
    ;; int32 _final
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; bool _audioDetectado
       (if _audioDetectado (write-byte -1 s) (write-byte 0 s))
     ;; int32 _inicio
       (write-long _inicio s)
     ;; int32 _final
       (write-long _final s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; bool _audioDetectado
     (setq _audioDetectado (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _inicio
     (setq _inicio (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _final
     (setq _final (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get seguimiento::audioDetectado :md5sum-) "62c75742bc466861beb1235814383e65")
(setf (get seguimiento::audioDetectado :datatype-) "seguimiento/audioDetectado")
(setf (get seguimiento::audioDetectado :definition-)
      "Header header
bool audioDetectado
int32 inicio
int32 final


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



(provide :seguimiento/audioDetectado "62c75742bc466861beb1235814383e65")


