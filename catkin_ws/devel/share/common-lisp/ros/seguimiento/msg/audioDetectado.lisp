; Auto-generated. Do not edit!


(cl:in-package seguimiento-msg)


;//! \htmlinclude audioDetectado.msg.html

(cl:defclass <audioDetectado> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (audioDetectado
    :reader audioDetectado
    :initarg :audioDetectado
    :type cl:boolean
    :initform cl:nil)
   (inicio
    :reader inicio
    :initarg :inicio
    :type cl:integer
    :initform 0)
   (final
    :reader final
    :initarg :final
    :type cl:integer
    :initform 0))
)

(cl:defclass audioDetectado (<audioDetectado>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <audioDetectado>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'audioDetectado)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name seguimiento-msg:<audioDetectado> is deprecated: use seguimiento-msg:audioDetectado instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <audioDetectado>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:header-val is deprecated.  Use seguimiento-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'audioDetectado-val :lambda-list '(m))
(cl:defmethod audioDetectado-val ((m <audioDetectado>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:audioDetectado-val is deprecated.  Use seguimiento-msg:audioDetectado instead.")
  (audioDetectado m))

(cl:ensure-generic-function 'inicio-val :lambda-list '(m))
(cl:defmethod inicio-val ((m <audioDetectado>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:inicio-val is deprecated.  Use seguimiento-msg:inicio instead.")
  (inicio m))

(cl:ensure-generic-function 'final-val :lambda-list '(m))
(cl:defmethod final-val ((m <audioDetectado>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader seguimiento-msg:final-val is deprecated.  Use seguimiento-msg:final instead.")
  (final m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <audioDetectado>) ostream)
  "Serializes a message object of type '<audioDetectado>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'audioDetectado) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'inicio)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'final)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <audioDetectado>) istream)
  "Deserializes a message object of type '<audioDetectado>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:slot-value msg 'audioDetectado) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'inicio) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'final) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<audioDetectado>)))
  "Returns string type for a message object of type '<audioDetectado>"
  "seguimiento/audioDetectado")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'audioDetectado)))
  "Returns string type for a message object of type 'audioDetectado"
  "seguimiento/audioDetectado")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<audioDetectado>)))
  "Returns md5sum for a message object of type '<audioDetectado>"
  "62c75742bc466861beb1235814383e65")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'audioDetectado)))
  "Returns md5sum for a message object of type 'audioDetectado"
  "62c75742bc466861beb1235814383e65")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<audioDetectado>)))
  "Returns full string definition for message of type '<audioDetectado>"
  (cl:format cl:nil "Header header~%bool audioDetectado~%int32 inicio~%int32 final~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'audioDetectado)))
  "Returns full string definition for message of type 'audioDetectado"
  (cl:format cl:nil "Header header~%bool audioDetectado~%int32 inicio~%int32 final~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <audioDetectado>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <audioDetectado>))
  "Converts a ROS message object to a list"
  (cl:list 'audioDetectado
    (cl:cons ':header (header msg))
    (cl:cons ':audioDetectado (audioDetectado msg))
    (cl:cons ':inicio (inicio msg))
    (cl:cons ':final (final msg))
))
