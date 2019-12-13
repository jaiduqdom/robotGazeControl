; Auto-generated. Do not edit!


(cl:in-package avatar_msg-msg)


;//! \htmlinclude AUlist.msg.html

(cl:defclass <AUlist> (roslisp-msg-protocol:ros-message)
  ((it
    :reader it
    :initarg :it
    :type cl:float
    :initform 0.0)
   (tt
    :reader tt
    :initarg :tt
    :type cl:float
    :initform 0.0)
   (au
    :reader au
    :initarg :au
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass AUlist (<AUlist>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <AUlist>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'AUlist)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name avatar_msg-msg:<AUlist> is deprecated: use avatar_msg-msg:AUlist instead.")))

(cl:ensure-generic-function 'it-val :lambda-list '(m))
(cl:defmethod it-val ((m <AUlist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:it-val is deprecated.  Use avatar_msg-msg:it instead.")
  (it m))

(cl:ensure-generic-function 'tt-val :lambda-list '(m))
(cl:defmethod tt-val ((m <AUlist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:tt-val is deprecated.  Use avatar_msg-msg:tt instead.")
  (tt m))

(cl:ensure-generic-function 'au-val :lambda-list '(m))
(cl:defmethod au-val ((m <AUlist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:au-val is deprecated.  Use avatar_msg-msg:au instead.")
  (au m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <AUlist>) ostream)
  "Serializes a message object of type '<AUlist>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'it))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'tt))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'au))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'au))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <AUlist>) istream)
  "Deserializes a message object of type '<AUlist>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'it) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'tt) (roslisp-utils:decode-single-float-bits bits)))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'au) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'au)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<AUlist>)))
  "Returns string type for a message object of type '<AUlist>"
  "avatar_msg/AUlist")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'AUlist)))
  "Returns string type for a message object of type 'AUlist"
  "avatar_msg/AUlist")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<AUlist>)))
  "Returns md5sum for a message object of type '<AUlist>"
  "48a51fcae9e2ae46610e83f259b0d91d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'AUlist)))
  "Returns md5sum for a message object of type 'AUlist"
  "48a51fcae9e2ae46610e83f259b0d91d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<AUlist>)))
  "Returns full string definition for message of type '<AUlist>"
  (cl:format cl:nil "float32 it~%float32 tt~%float32[] au~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'AUlist)))
  "Returns full string definition for message of type 'AUlist"
  (cl:format cl:nil "float32 it~%float32 tt~%float32[] au~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <AUlist>))
  (cl:+ 0
     4
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'au) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <AUlist>))
  "Converts a ROS message object to a list"
  (cl:list 'AUlist
    (cl:cons ':it (it msg))
    (cl:cons ':tt (tt msg))
    (cl:cons ':au (au msg))
))
