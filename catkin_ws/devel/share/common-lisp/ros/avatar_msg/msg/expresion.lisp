; Auto-generated. Do not edit!


(cl:in-package avatar_msg-msg)


;//! \htmlinclude expresion.msg.html

(cl:defclass <expresion> (roslisp-msg-protocol:ros-message)
  ((exp
    :reader exp
    :initarg :exp
    :type cl:string
    :initform "")
   (au_ext
    :reader au_ext
    :initarg :au_ext
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (it
    :reader it
    :initarg :it
    :type cl:float
    :initform 0.0)
   (tt
    :reader tt
    :initarg :tt
    :type cl:float
    :initform 0.0))
)

(cl:defclass expresion (<expresion>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <expresion>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'expresion)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name avatar_msg-msg:<expresion> is deprecated: use avatar_msg-msg:expresion instead.")))

(cl:ensure-generic-function 'exp-val :lambda-list '(m))
(cl:defmethod exp-val ((m <expresion>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:exp-val is deprecated.  Use avatar_msg-msg:exp instead.")
  (exp m))

(cl:ensure-generic-function 'au_ext-val :lambda-list '(m))
(cl:defmethod au_ext-val ((m <expresion>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:au_ext-val is deprecated.  Use avatar_msg-msg:au_ext instead.")
  (au_ext m))

(cl:ensure-generic-function 'it-val :lambda-list '(m))
(cl:defmethod it-val ((m <expresion>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:it-val is deprecated.  Use avatar_msg-msg:it instead.")
  (it m))

(cl:ensure-generic-function 'tt-val :lambda-list '(m))
(cl:defmethod tt-val ((m <expresion>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader avatar_msg-msg:tt-val is deprecated.  Use avatar_msg-msg:tt instead.")
  (tt m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <expresion>) ostream)
  "Serializes a message object of type '<expresion>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'exp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'exp))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'au_ext))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'au_ext))
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
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <expresion>) istream)
  "Deserializes a message object of type '<expresion>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'exp) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'exp) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'au_ext) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'au_ext)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
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
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<expresion>)))
  "Returns string type for a message object of type '<expresion>"
  "avatar_msg/expresion")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'expresion)))
  "Returns string type for a message object of type 'expresion"
  "avatar_msg/expresion")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<expresion>)))
  "Returns md5sum for a message object of type '<expresion>"
  "e5171cc2831e9005bdc4c0ec061818bb")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'expresion)))
  "Returns md5sum for a message object of type 'expresion"
  "e5171cc2831e9005bdc4c0ec061818bb")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<expresion>)))
  "Returns full string definition for message of type '<expresion>"
  (cl:format cl:nil "string exp~%float32[] au_ext ~%float32 it~%float32 tt~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'expresion)))
  "Returns full string definition for message of type 'expresion"
  (cl:format cl:nil "string exp~%float32[] au_ext ~%float32 it~%float32 tt~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <expresion>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'exp))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'au_ext) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <expresion>))
  "Converts a ROS message object to a list"
  (cl:list 'expresion
    (cl:cons ':exp (exp msg))
    (cl:cons ':au_ext (au_ext msg))
    (cl:cons ':it (it msg))
    (cl:cons ':tt (tt msg))
))
