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

class salidaKalman {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.identificador = null;
      this.pan = null;
      this.tilt = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('identificador')) {
        this.identificador = initObj.identificador
      }
      else {
        this.identificador = [];
      }
      if (initObj.hasOwnProperty('pan')) {
        this.pan = initObj.pan
      }
      else {
        this.pan = [];
      }
      if (initObj.hasOwnProperty('tilt')) {
        this.tilt = initObj.tilt
      }
      else {
        this.tilt = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type salidaKalman
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [identificador]
    bufferOffset = _arraySerializer.int32(obj.identificador, buffer, bufferOffset, null);
    // Serialize message field [pan]
    bufferOffset = _arraySerializer.float32(obj.pan, buffer, bufferOffset, null);
    // Serialize message field [tilt]
    bufferOffset = _arraySerializer.float32(obj.tilt, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type salidaKalman
    let len;
    let data = new salidaKalman(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [identificador]
    data.identificador = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [pan]
    data.pan = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [tilt]
    data.tilt = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 4 * object.identificador.length;
    length += 4 * object.pan.length;
    length += 4 * object.tilt.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'seguimiento/salidaKalman';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '258285ea72a30809b9246ee654073a66';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    int32[] identificador
    float32[] pan
    float32[] tilt
    
    
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
    const resolved = new salidaKalman(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.identificador !== undefined) {
      resolved.identificador = msg.identificador;
    }
    else {
      resolved.identificador = []
    }

    if (msg.pan !== undefined) {
      resolved.pan = msg.pan;
    }
    else {
      resolved.pan = []
    }

    if (msg.tilt !== undefined) {
      resolved.tilt = msg.tilt;
    }
    else {
      resolved.tilt = []
    }

    return resolved;
    }
};

module.exports = salidaKalman;
