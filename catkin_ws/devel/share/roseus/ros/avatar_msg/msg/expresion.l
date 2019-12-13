;; Auto-generated. Do not edit!


(when (boundp 'avatar_msg::expresion)
  (if (not (find-package "AVATAR_MSG"))
    (make-package "AVATAR_MSG"))
  (shadow 'expresion (find-package "AVATAR_MSG")))
(unless (find-package "AVATAR_MSG::EXPRESION")
  (make-package "AVATAR_MSG::EXPRESION"))

(in-package "ROS")
;;//! \htmlinclude expresion.msg.html


(defclass avatar_msg::expresion
  :super ros::object
  :slots (_exp _au_ext _it _tt ))

(defmethod avatar_msg::expresion
  (:init
   (&key
    ((:exp __exp) "")
    ((:au_ext __au_ext) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:it __it) 0.0)
    ((:tt __tt) 0.0)
    )
   (send-super :init)
   (setq _exp (string __exp))
   (setq _au_ext __au_ext)
   (setq _it (float __it))
   (setq _tt (float __tt))
   self)
  (:exp
   (&optional __exp)
   (if __exp (setq _exp __exp)) _exp)
  (:au_ext
   (&optional __au_ext)
   (if __au_ext (setq _au_ext __au_ext)) _au_ext)
  (:it
   (&optional __it)
   (if __it (setq _it __it)) _it)
  (:tt
   (&optional __tt)
   (if __tt (setq _tt __tt)) _tt)
  (:serialization-length
   ()
   (+
    ;; string _exp
    4 (length _exp)
    ;; float32[] _au_ext
    (* 4    (length _au_ext)) 4
    ;; float32 _it
    4
    ;; float32 _tt
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _exp
       (write-long (length _exp) s) (princ _exp s)
     ;; float32[] _au_ext
     (write-long (length _au_ext) s)
     (dotimes (i (length _au_ext))
       (sys::poke (elt _au_ext i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32 _it
       (sys::poke _it (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _tt
       (sys::poke _tt (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _exp
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _exp (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32[] _au_ext
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _au_ext (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _au_ext i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32 _it
     (setq _it (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _tt
     (setq _tt (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get avatar_msg::expresion :md5sum-) "e5171cc2831e9005bdc4c0ec061818bb")
(setf (get avatar_msg::expresion :datatype-) "avatar_msg/expresion")
(setf (get avatar_msg::expresion :definition-)
      "string exp
float32[] au_ext 
float32 it
float32 tt


")



(provide :avatar_msg/expresion "e5171cc2831e9005bdc4c0ec061818bb")


