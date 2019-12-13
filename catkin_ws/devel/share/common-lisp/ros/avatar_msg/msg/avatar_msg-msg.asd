
(cl:in-package :asdf)

(defsystem "avatar_msg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "AUlist" :depends-on ("_package_AUlist"))
    (:file "_package_AUlist" :depends-on ("_package"))
    (:file "center_face" :depends-on ("_package_center_face"))
    (:file "_package_center_face" :depends-on ("_package"))
    (:file "decir" :depends-on ("_package_decir"))
    (:file "_package_decir" :depends-on ("_package"))
    (:file "expresion" :depends-on ("_package_expresion"))
    (:file "_package_expresion" :depends-on ("_package"))
  ))