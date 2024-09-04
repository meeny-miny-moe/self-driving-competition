; Auto-generated. Do not edit!


(cl:in-package xycar_msgs-msg)


;//! \htmlinclude xycar_motor.msg.html

(cl:defclass <xycar_motor> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0))
)

(cl:defclass xycar_motor (<xycar_motor>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <xycar_motor>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'xycar_motor)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name xycar_msgs-msg:<xycar_motor> is deprecated: use xycar_msgs-msg:xycar_motor instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <xycar_motor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader xycar_msgs-msg:header-val is deprecated.  Use xycar_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <xycar_motor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader xycar_msgs-msg:angle-val is deprecated.  Use xycar_msgs-msg:angle instead.")
  (angle m))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <xycar_motor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader xycar_msgs-msg:speed-val is deprecated.  Use xycar_msgs-msg:speed instead.")
  (speed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <xycar_motor>) ostream)
  "Serializes a message object of type '<xycar_motor>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <xycar_motor>) istream)
  "Deserializes a message object of type '<xycar_motor>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<xycar_motor>)))
  "Returns string type for a message object of type '<xycar_motor>"
  "xycar_msgs/xycar_motor")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'xycar_motor)))
  "Returns string type for a message object of type 'xycar_motor"
  "xycar_msgs/xycar_motor")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<xycar_motor>)))
  "Returns md5sum for a message object of type '<xycar_motor>"
  "86f102c3027ac5a649446e1f9f364baf")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'xycar_motor)))
  "Returns md5sum for a message object of type 'xycar_motor"
  "86f102c3027ac5a649446e1f9f364baf")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<xycar_motor>)))
  "Returns full string definition for message of type '<xycar_motor>"
  (cl:format cl:nil "Header header~%float32 angle~%float32 speed~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'xycar_motor)))
  "Returns full string definition for message of type 'xycar_motor"
  (cl:format cl:nil "Header header~%float32 angle~%float32 speed~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <xycar_motor>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <xycar_motor>))
  "Converts a ROS message object to a list"
  (cl:list 'xycar_motor
    (cl:cons ':header (header msg))
    (cl:cons ':angle (angle msg))
    (cl:cons ':speed (speed msg))
))
