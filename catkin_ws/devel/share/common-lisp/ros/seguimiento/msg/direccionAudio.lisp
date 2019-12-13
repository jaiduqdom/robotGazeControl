; Auto-generated. Do not edit!


(cl:in-package seguimiento-msg)


;//! \htmlinclude direccionAudio.msg.html

(cl:defclass <direccionAudio> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (vad
    :reader vad
    :initarg :vad
    :type cl:boolean
    :initform cl:nil)
   (doa
    :reader doa
    :initarg :doa
    :type cl:integer
    :initform 0))
)

(cl:defclass direccionAudio (<direccionAudio>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <direccionAudio>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'direccionAudio)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name seguimiento-msg:<direccionAudio> is deprecated: use seguimiento-msg:direccionAudio instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <direccionAudio>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:header-val is deprecated.  Use seguimiento-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'vad-val :lambda-list '(m))
(cl:defmethod vad-val ((m <direccionAudio>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:vad-val is deprecated.  Use seguimiento-msg:vad instead.")
  (vad m))

(cl:ensure-generic-function 'doa-val :lambda-list '(m))
(cl:defmethod doa-val ((m <direccionAudio>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:doa-val is deprecated.  Use seguimiento-msg:doa instead.")
  (doa m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <direccionAudio>) ostream)
  "Serializes a message object of type '<direccionAudio>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'vad) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'doa)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <direccionAudio>) istream)
  "Deserializes a message object of type '<direccionAudio>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:slot-value msg 'vad) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'doa) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<direccionAudio>)))
  "Returns string type for a message object of type '<direccionAudio>"
  "seguimiento/direccionAudio")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'direccionAudio)))
  "Returns string type for a message object of type 'direccionAudio"
  "seguimiento/direccionAudio")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<direccionAudio>)))
  "Returns md5sum for a message object of type '<direccionAudio>"
  "26d1631e5cd32777f7f0538fff298a47")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'direccionAudio)))
  "Returns md5sum for a message object of type 'direccionAudio"
  "26d1631e5cd32777f7f0538fff298a47")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<direccionAudio>)))
  "Returns full string definition for message of type '<direccionAudio>"
  (cl:format cl:nil "Header header~%bool vad~%int32 doa~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'direccionAudio)))
  "Returns full string definition for message of type 'direccionAudio"
  (cl:format cl:nil "Header header~%bool vad~%int32 doa~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <direccionAudio>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <direccionAudio>))
  "Converts a ROS message object to a list"
  (cl:list 'direccionAudio
    (cl:cons ':header (header msg))
    (cl:cons ':vad (vad msg))
    (cl:cons ':doa (doa msg))
))
