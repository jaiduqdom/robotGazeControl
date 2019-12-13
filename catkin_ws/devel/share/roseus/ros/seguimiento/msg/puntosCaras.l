;; Auto-generated. Do not edit!


(when (boundp 'seguimiento::puntosCaras)
  (if (not (find-package "SEGUIMIENTO"))
    (make-package "SEGUIMIENTO"))
  (shadow 'puntosCaras (find-package "SEGUIMIENTO")))
(unless (find-package "SEGUIMIENTO::PUNTOSCARAS")
  (make-package "SEGUIMIENTO::PUNTOSCARAS"))

(in-package "ROS")
;;//! \htmlinclude puntosCaras.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass seguimiento::puntosCaras
  :super ros::object
  :slots (_header _numeroCaras _x1 _y1 _x2 _y2 _puntoX _puntoY _indiceCara _caraNueva ))

(defmethod seguimiento::puntosCaras
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:numeroCaras __numeroCaras) 0)
    ((:x1 __x1) (make-array 0 :initial-element 0 :element-type :integer))
    ((:y1 __y1) (make-array 0 :initial-element 0 :element-type :integer))
    ((:x2 __x2) (make-array 0 :initial-element 0 :element-type :integer))
    ((:y2 __y2) (make-array 0 :initial-element 0 :element-type :integer))
    ((:puntoX __puntoX) (make-array 0 :initial-element 0 :element-type :integer))
    ((:puntoY __puntoY) (make-array 0 :initial-element 0 :element-type :integer))
    ((:indiceCara __indiceCara) (make-array 0 :initial-element 0 :element-type :integer))
    ((:caraNueva __caraNueva) (let (r) (dotimes (i 0) (push nil r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _numeroCaras (round __numeroCaras))
   (setq _x1 __x1)
   (setq _y1 __y1)
   (setq _x2 __x2)
   (setq _y2 __y2)
   (setq _puntoX __puntoX)
   (setq _puntoY __puntoY)
   (setq _indiceCara __indiceCara)
   (setq _caraNueva __caraNueva)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:numeroCaras
   (&optional __numeroCaras)
   (if __numeroCaras (setq _numeroCaras __numeroCaras)) _numeroCaras)
  (:x1
   (&optional __x1)
   (if __x1 (setq _x1 __x1)) _x1)
  (:y1
   (&optional __y1)
   (if __y1 (setq _y1 __y1)) _y1)
  (:x2
   (&optional __x2)
   (if __x2 (setq _x2 __x2)) _x2)
  (:y2
   (&optional __y2)
   (if __y2 (setq _y2 __y2)) _y2)
  (:puntoX
   (&optional __puntoX)
   (if __puntoX (setq _puntoX __puntoX)) _puntoX)
  (:puntoY
   (&optional __puntoY)
   (if __puntoY (setq _puntoY __puntoY)) _puntoY)
  (:indiceCara
   (&optional __indiceCara)
   (if __indiceCara (setq _indiceCara __indiceCara)) _indiceCara)
  (:caraNueva
   (&optional __caraNueva)
   (if __caraNueva (setq _caraNueva __caraNueva)) _caraNueva)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int32 _numeroCaras
    4
    ;; int32[] _x1
    (* 4    (length _x1)) 4
    ;; int32[] _y1
    (* 4    (length _y1)) 4
    ;; int32[] _x2
    (* 4    (length _x2)) 4
    ;; int32[] _y2
    (* 4    (length _y2)) 4
    ;; int32[] _puntoX
    (* 4    (length _puntoX)) 4
    ;; int32[] _puntoY
    (* 4    (length _puntoY)) 4
    ;; int32[] _indiceCara
    (* 4    (length _indiceCara)) 4
    ;; bool[] _caraNueva
    (* 1    (length _caraNueva)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32 _numeroCaras
       (write-long _numeroCaras s)
     ;; int32[] _x1
     (write-long (length _x1) s)
     (dotimes (i (length _x1))
       (write-long (elt _x1 i) s)
       )
     ;; int32[] _y1
     (write-long (length _y1) s)
     (dotimes (i (length _y1))
       (write-long (elt _y1 i) s)
       )
     ;; int32[] _x2
     (write-long (length _x2) s)
     (dotimes (i (length _x2))
       (write-long (elt _x2 i) s)
       )
     ;; int32[] _y2
     (write-long (length _y2) s)
     (dotimes (i (length _y2))
       (write-long (elt _y2 i) s)
       )
     ;; int32[] _puntoX
     (write-long (length _puntoX) s)
     (dotimes (i (length _puntoX))
       (write-long (elt _puntoX i) s)
       )
     ;; int32[] _puntoY
     (write-long (length _puntoY) s)
     (dotimes (i (length _puntoY))
       (write-long (elt _puntoY i) s)
       )
     ;; int32[] _indiceCara
     (write-long (length _indiceCara) s)
     (dotimes (i (length _indiceCara))
       (write-long (elt _indiceCara i) s)
       )
     ;; bool[] _caraNueva
     (write-long (length _caraNueva) s)
     (dotimes (i (length _caraNueva))
       (if (elt _caraNueva i) (write-byte -1 s) (write-byte 0 s))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32 _numeroCaras
     (setq _numeroCaras (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32[] _x1
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _x1 (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _x1 i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _y1
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _y1 (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _y1 i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _x2
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _x2 (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _x2 i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _y2
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _y2 (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _y2 i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _puntoX
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _puntoX (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _puntoX i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _puntoY
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _puntoY (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _puntoY i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; int32[] _indiceCara
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _indiceCara (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _indiceCara i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; bool[] _caraNueva
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _caraNueva (make-list n))
     (dotimes (i n)
     (setf (elt _caraNueva i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;;
   self)
  )

(setf (get seguimiento::puntosCaras :md5sum-) "b9577e30fd5aa6d52d9bd36c0e0026d1")
(setf (get seguimiento::puntosCaras :datatype-) "seguimiento/puntosCaras")
(setf (get seguimiento::puntosCaras :definition-)
      "Header header
int32 numeroCaras
int32[] x1
int32[] y1
int32[] x2
int32[] y2
int32[] puntoX
int32[] puntoY
int32[] indiceCara
bool[] caraNueva


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



(provide :seguimiento/puntosCaras "b9577e30fd5aa6d52d9bd36c0e0026d1")


