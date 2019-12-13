; Auto-generated. Do not edit!


(cl:in-package avatar_msg-msg)


;//! \htmlinclude decir.msg.html

(cl:defclass <decir> (roslisp-msg-protocol:ros-message)
  ((palabras
    :reader palabras
    :initarg :palabras
    :type cl:string
    :initform ""))
)

(cl:defclass decir (<decir>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <decir>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'decir)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name avatar_msg-msg:<decir> is deprecated: use avatar_msg-msg:decir instead.")))

(cl:ensure-generic-function 'palabras-val :lambda-list '(m))
(cl:defmethod palabras-val ((m <decir>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:palabras-val is deprecated.  Use avatar_msg-msg:palabras instead.")
  (palabras m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <decir>) ostream)
  "Serializes a message object of type '<decir>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'palabras))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'palabras))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <decir>) istream)
  "Deserializes a message object of type '<decir>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'palabras) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'palabras) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<decir>)))
  "Returns string type for a message object of type '<decir>"
  "avatar_msg/decir")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'decir)))
  "Returns string type for a message object of type 'decir"
  "avatar_msg/decir")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<decir>)))
  "Returns md5sum for a message object of type '<decir>"
  "f31a5a411200c463cdcdb46c34aa2c72")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'decir)))
  "Returns md5sum for a message object of type 'decir"
  "f31a5a411200c463cdcdb46c34aa2c72")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<decir>)))
  "Returns full string definition for message of type '<decir>"
  (cl:format cl:nil "string palabras~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'decir)))
  "Returns full string definition for message of type 'decir"
  (cl:format cl:nil "string palabras~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <decir>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'palabras))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <decir>))
  "Converts a ROS message object to a list"
  (cl:list 'decir
    (cl:cons ':palabras (palabras msg))
))
