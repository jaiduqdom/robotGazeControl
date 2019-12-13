// Auto-generated. Do not edit!

// (in-package seguimiento.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class movimiento {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.enMovimiento = null;
      this.theta_robot = null;
      this.psi_robot = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('enMovimiento')) {
        this.enMovimiento = initObj.enMovimiento
      }
      else {
        this.enMovimiento = false;
      }
      if (initObj.hasOwnProperty('theta_robot')) {
        this.theta_robot = initObj.theta_robot
      }
      else {
        this.theta_robot = 0.0;
      }
      if (initObj.hasOwnProperty('psi_robot')) {
        this.psi_robot = initObj.psi_robot
      }
      else {
        this.psi_robot = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type movimiento
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [enMovimiento]
    bufferOffset = _serializer.bool(obj.enMovimiento, buffer, bufferOffset);
    // Serialize message field [theta_robot]
    bufferOffset = _serializer.float32(obj.theta_robot, buffer, bufferOffset);
    // Serialize message field [psi_robot]
    bufferOffset = _serializer.float32(obj.psi_robot, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type movimiento
    let len;
    let data = new movimiento(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [enMovimiento]
    data.enMovimiento = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [theta_robot]
    data.theta_robot = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [psi_robot]
    data.psi_robot = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 9;
  }

  static datatype() {
    // Returns string type for a message object
    return 'seguimiento/movimiento';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0ea04302753729942b7a5e567e1e615e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    bool enMovimiento
    float32 theta_robot
    float32 psi_robot
    
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new movimiento(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.enMovimiento !== undefined) {
      resolved.enMovimiento = msg.enMovimiento;
    }
    else {
      resolved.enMovimiento = false
    }

    if (msg.theta_robot !== undefined) {
      resolved.theta_robot = msg.theta_robot;
    }
    else {
      resolved.theta_robot = 0.0
    }

    if (msg.psi_robot !== undefined) {
      resolved.psi_robot = msg.psi_robot;
    }
    else {
      resolved.psi_robot = 0.0
    }

    return resolved;
    }
};

module.exports = movimiento;
