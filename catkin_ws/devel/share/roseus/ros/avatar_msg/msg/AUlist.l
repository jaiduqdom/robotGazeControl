;; Auto-generated. Do not edit!


(when (boundp 'avatar_msg::AUlist)
  (if (not (find-package "AVATAR_MSG"))
    (make-package "AVATAR_MSG"))
  (shadow 'AUlist (find-package "AVATAR_MSG")))
(unless (find-package "AVATAR_MSG::AULIST")
  (make-package "AVATAR_MSG::AULIST"))

(in-package "ROS")
;;//! \htmlinclude AUlist.msg.html


(defclass avatar_msg::AUlist
  :super ros::object
  :slots (_it _tt _au ))

(defmethod avatar_msg::AUlist
  (:init
   (&key
    ((:it __it) 0.0)
    ((:tt __tt) 0.0)
    ((:au __au) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _it (float __it))
   (setq _tt (float __tt))
   (setq _au __au)
   self)
  (:it
   (&optional __it)
   (if __it (setq _it __it)) _it)
  (:tt
   (&optional __tt)
   (if __tt (setq _tt __tt)) _tt)
  (:au
   (&optional __au)
   (if __au (setq _au __au)) _au)
  (:serialization-length
   ()
   (+
    ;; float32 _it
    4
    ;; float32 _tt
    4
    ;; float32[] _au
    (* 4    (length _au)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _it
       (sys::poke _it (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _tt
       (sys::poke _tt (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32[] _au
     (write-long (length _au) s)
     (dotimes (i (length _au))
       (sys::poke (elt _au i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _it
     (setq _it (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _tt
     (setq _tt (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32[] _au
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _au (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _au i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get avatar_msg::AUlist :md5sum-) "48a51fcae9e2ae46610e83f259b0d91d")
(setf (get avatar_msg::AUlist :datatype-) "avatar_msg/AUlist")
(setf (get avatar_msg::AUlist :definition-)
      "float32 it
float32 tt
float32[] au


")



(provide :avatar_msg/AUlist "48a51fcae9e2ae46610e83f259b0d91d")


