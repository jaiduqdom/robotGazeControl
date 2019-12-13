; Auto-generated. Do not edit!


(cl:in-package seguimiento-msg)


;//! \htmlinclude movimiento.msg.html

(cl:defclass <movimiento> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (enMovimiento
    :reader enMovimiento
    :initarg :enMovimiento
    :type cl:boolean
    :initform cl:nil)
   (theta_robot
    :reader theta_robot
    :initarg :theta_robot
    :type cl:float
    :initform 0.0)
   (psi_robot
    :reader psi_robot
    :initarg :psi_robot
    :type cl:float
    :initform 0.0))
)

(cl:defclass movimiento (<movimiento>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <movimiento>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'movimiento)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name seguimiento-msg:<movimiento> is deprecated: use seguimiento-msg:movimiento instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <movimiento>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:header-val is deprecated.  Use seguimiento-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'enMovimiento-val :lambda-list '(m))
(cl:defmethod enMovimiento-val ((m <movimiento>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:enMovimiento-val is deprecated.  Use seguimiento-msg:enMovimiento instead.")
  (enMovimiento m))

(cl:ensure-generic-function 'theta_robot-val :lambda-list '(m))
(cl:defmethod theta_robot-val ((m <movimiento>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:theta_robot-val is deprecated.  Use seguimiento-msg:theta_robot instead.")
  (theta_robot m))

(cl:ensure-generic-function 'psi_robot-val :lambda-list '(m))
(cl:defmethod psi_robot-val ((m <movimiento>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:psi_robot-val is deprecated.  Use seguimiento-msg:psi_robot instead.")
  (psi_robot m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <movimiento>) ostream)
  "Serializes a message object of type '<movimiento>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'enMovimiento) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'theta_robot))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'psi_robot))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <movimiento>) istream)
  "Deserializes a message object of type '<movimiento>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:slot-value msg 'enMovimiento) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta_robot) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'psi_robot) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<movimiento>)))
  "Returns string type for a message object of type '<movimiento>"
  "seguimiento/movimiento")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'movimiento)))
  "Returns string type for a message object of type 'movimiento"
  "seguimiento/movimiento")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<movimiento>)))
  "Returns md5sum for a message object of type '<movimiento>"
  "0ea04302753729942b7a5e567e1e615e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'movimiento)))
  "Returns md5sum for a message object of type 'movimiento"
  "0ea04302753729942b7a5e567e1e615e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<movimiento>)))
  "Returns full string definition for message of type '<movimiento>"
  (cl:format cl:nil "Header header~%bool enMovimiento~%float32 theta_robot~%float32 psi_robot~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'movimiento)))
  "Returns full string definition for message of type 'movimiento"
  (cl:format cl:nil "Header header~%bool enMovimiento~%float32 theta_robot~%float32 psi_robot~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <movimiento>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <movimiento>))
  "Converts a ROS message object to a list"
  (cl:list 'movimiento
    (cl:cons ':header (header msg))
    (cl:cons ':enMovimiento (enMovimiento msg))
    (cl:cons ':theta_robot (theta_robot msg))
    (cl:cons ':psi_robot (psi_robot msg))
))
