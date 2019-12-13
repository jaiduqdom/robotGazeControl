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

class audioDetectado {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.audioDetectado = null;
      this.inicio = null;
      this.final = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('audioDetectado')) {
        this.audioDetectado = initObj.audioDetectado
      }
      else {
        this.audioDetectado = false;
      }
      if (initObj.hasOwnProperty('inicio')) {
        this.inicio = initObj.inicio
      }
      else {
        this.inicio = 0;
      }
      if (initObj.hasOwnProperty('final')) {
        this.final = initObj.final
      }
      else {
        this.final = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type audioDetectado
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [audioDetectado]
    bufferOffset = _serializer.bool(obj.audioDetectado, buffer, bufferOffset);
    // Serialize message field [inicio]
    bufferOffset = _serializer.int32(obj.inicio, buffer, bufferOffset);
    // Serialize message field [final]
    bufferOffset = _serializer.int32(obj.final, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type audioDetectado
    let len;
    let data = new audioDetectado(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [audioDetectado]
    data.audioDetectado = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [inicio]
    data.inicio = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [final]
    data.final = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 9;
  }

  static datatype() {
    // Returns string type for a message object
    return 'seguimiento/audioDetectado';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '62c75742bc466861beb1235814383e65';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    bool audioDetectado
    int32 inicio
    int32 final
    
    
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
    const resolved = new audioDetectado(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.audioDetectado !== undefined) {
      resolved.audioDetectado = msg.audioDetectado;
    }
    else {
      resolved.audioDetectado = false
    }

    if (msg.inicio !== undefined) {
      resolved.inicio = msg.inicio;
    }
    else {
      resolved.inicio = 0
    }

    if (msg.final !== undefined) {
      resolved.final = msg.final;
    }
    else {
      resolved.final = 0
    }

    return resolved;
    }
};

module.exports = audioDetectado;
