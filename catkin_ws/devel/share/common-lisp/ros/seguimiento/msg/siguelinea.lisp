; Auto-generated. Do not edit!


(cl:in-package seguimiento-msg)


;//! \htmlinclude siguelinea.msg.html

(cl:defclass <siguelinea> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (distancia
    :reader distancia
    :initarg :distancia
    :type cl:float
    :initform 0.0)
   (angulo
    :reader angulo
    :initarg :angulo
    :type cl:float
    :initform 0.0))
)

(cl:defclass siguelinea (<siguelinea>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <siguelinea>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'siguelinea)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name seguimiento-msg:<siguelinea> is deprecated: use seguimiento-msg:siguelinea instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <siguelinea>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:header-val is deprecated.  Use seguimiento-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'distancia-val :lambda-list '(m))
(cl:defmethod distancia-val ((m <siguelinea>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:distancia-val is deprecated.  Use seguimiento-msg:distancia instead.")
  (distancia m))

(cl:ensure-generic-function 'angulo-val :lambda-list '(m))
(cl:defmethod angulo-val ((m <siguelinea>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:angulo-val is deprecated.  Use seguimiento-msg:angulo instead.")
  (angulo m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <siguelinea>) ostream)
  "Serializes a message object of type '<siguelinea>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'distancia))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angulo))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <siguelinea>) istream)
  "Deserializes a message object of type '<siguelinea>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'distancia) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angulo) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<siguelinea>)))
  "Returns string type for a message object of type '<siguelinea>"
  "seguimiento/siguelinea")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'siguelinea)))
  "Returns string type for a message object of type 'siguelinea"
  "seguimiento/siguelinea")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<siguelinea>)))
  "Returns md5sum for a message object of type '<siguelinea>"
  "8ba4eeb657900659451097c3c7c247d9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'siguelinea)))
  "Returns md5sum for a message object of type 'siguelinea"
  "8ba4eeb657900659451097c3c7c247d9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<siguelinea>)))
  "Returns full string definition for message of type '<siguelinea>"
  (cl:format cl:nil "Header header~%float32 distancia~%float32 angulo~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'siguelinea)))
  "Returns full string definition for message of type 'siguelinea"
  (cl:format cl:nil "Header header~%float32 distancia~%float32 angulo~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <siguelinea>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <siguelinea>))
  "Converts a ROS message object to a list"
  (cl:list 'siguelinea
    (cl:cons ':header (header msg))
    (cl:cons ':distancia (distancia msg))
    (cl:cons ':angulo (angulo msg))
))
