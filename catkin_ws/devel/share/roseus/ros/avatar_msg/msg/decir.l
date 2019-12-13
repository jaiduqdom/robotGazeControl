;; Auto-generated. Do not edit!


(when (boundp 'avatar_msg::decir)
  (if (not (find-package "AVATAR_MSG"))
    (make-package "AVATAR_MSG"))
  (shadow 'decir (find-package "AVATAR_MSG")))
(unless (find-package "AVATAR_MSG::DECIR")
  (make-package "AVATAR_MSG::DECIR"))

(in-package "ROS")
;;//! \htmlinclude decir.msg.html


(defclass avatar_msg::decir
  :super ros::object
  :slots (_palabras ))

(defmethod avatar_msg::decir
  (:init
   (&key
    ((:palabras __palabras) "")
    )
   (send-super :init)
   (setq _palabras (string __palabras))
   self)
  (:palabras
   (&optional __palabras)
   (if __palabras (setq _palabras __palabras)) _palabras)
  (:serialization-length
   ()
   (+
    ;; string _palabras
    4 (length _palabras)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _palabras
       (write-long (length _palabras) s) (princ _palabras s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _palabras
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _palabras (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get avatar_msg::decir :md5sum-) "f31a5a411200c463cdcdb46c34aa2c72")
(setf (get avatar_msg::decir :datatype-) "avatar_msg/decir")
(setf (get avatar_msg::decir :definition-)
      "string palabras

")



(provide :avatar_msg/decir "f31a5a411200c463cdcdb46c34aa2c72")


