;; Auto-generated. Do not edit!


(when (boundp 'avatar_msg::center_face)
  (if (not (find-package "AVATAR_MSG"))
    (make-package "AVATAR_MSG"))
  (shadow 'center_face (find-package "AVATAR_MSG")))
(unless (find-package "AVATAR_MSG::CENTER_FACE")
  (make-package "AVATAR_MSG::CENTER_FACE"))

(in-package "ROS")
;;//! \htmlinclude center_face.msg.html


(defclass avatar_msg::center_face
  :super ros::object
  :slots (_center_x _center_y ))

(defmethod avatar_msg::center_face
  (:init
   (&key
    ((:center_x __center_x) 0.0)
    ((:center_y __center_y) 0.0)
    )
   (send-super :init)
   (setq _center_x (float __center_x))
   (setq _center_y (float __center_y))
   self)
  (:center_x
   (&optional __center_x)
   (if __center_x (setq _center_x __center_x)) _center_x)
  (:center_y
   (&optional __center_y)
   (if __center_y (setq _center_y __center_y)) _center_y)
  (:serialization-length
   ()
   (+
    ;; float32 _center_x
    4
    ;; float32 _center_y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _center_x
       (sys::poke _center_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _center_y
       (sys::poke _center_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _center_x
     (setq _center_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _center_y
     (setq _center_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get avatar_msg::center_face :md5sum-) "c51e51b1031fa051202f8de7f01927c6")
(setf (get avatar_msg::center_face :datatype-) "avatar_msg/center_face")
(setf (get avatar_msg::center_face :definition-)
      "float32 center_x
float32 center_y

")



(provide :avatar_msg/center_face "c51e51b1031fa051202f8de7f01927c6")


