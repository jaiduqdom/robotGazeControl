; Auto-generated. Do not edit!


(cl:in-package seguimiento-msg)


;//! \htmlinclude nivelAudio.msg.html

(cl:defclass <nivelAudio> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (rms
    :reader rms
    :initarg :rms
    :type cl:float
    :initform 0.0))
)

(cl:defclass nivelAudio (<nivelAudio>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <nivelAudio>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'nivelAudio)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name seguimiento-msg:<nivelAudio> is deprecated: use seguimiento-msg:nivelAudio instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <nivelAudio>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:header-val is deprecated.  Use seguimiento-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'rms-val :lambda-list '(m))
(cl:defmethod rms-val ((m <nivelAudio>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:rms-val is deprecated.  Use seguimiento-msg:rms instead.")
  (rms m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <nivelAudio>) ostream)
  "Serializes a message object of type '<nivelAudio>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rms))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <nivelAudio>) istream)
  "Deserializes a message object of type '<nivelAudio>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rms) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<nivelAudio>)))
  "Returns string type for a message object of type '<nivelAudio>"
  "seguimiento/nivelAudio")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'nivelAudio)))
  "Returns string type for a message object of type 'nivelAudio"
  "seguimiento/nivelAudio")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<nivelAudio>)))
  "Returns md5sum for a message object of type '<nivelAudio>"
  "b7f88596f71fe2965f91f0e52ac92c01")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'nivelAudio)))
  "Returns md5sum for a message object of type 'nivelAudio"
  "b7f88596f71fe2965f91f0e52ac92c01")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<nivelAudio>)))
  "Returns full string definition for message of type '<nivelAudio>"
  (cl:format cl:nil "Header header~%float32 rms~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'nivelAudio)))
  "Returns full string definition for message of type 'nivelAudio"
  (cl:format cl:nil "Header header~%float32 rms~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <nivelAudio>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <nivelAudio>))
  "Converts a ROS message object to a list"
  (cl:list 'nivelAudio
    (cl:cons ':header (header msg))
    (cl:cons ':rms (rms msg))
))
