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

class siguelinea {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.distancia = null;
      this.angulo = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('distancia')) {
        this.distancia = initObj.distancia
      }
      else {
        this.distancia = 0.0;
      }
      if (initObj.hasOwnProperty('angulo')) {
        this.angulo = initObj.angulo
      }
      else {
        this.angulo = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type siguelinea
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [distancia]
    bufferOffset = _serializer.float32(obj.distancia, buffer, bufferOffset);
    // Serialize message field [angulo]
    bufferOffset = _serializer.float32(obj.angulo, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type siguelinea
    let len;
    let data = new siguelinea(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [distancia]
    data.distancia = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [angulo]
    data.angulo = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'seguimiento/siguelinea';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8ba4eeb657900659451097c3c7c247d9';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    float32 distancia
    float32 angulo
    
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
    const resolved = new siguelinea(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.distancia !== undefined) {
      resolved.distancia = msg.distancia;
    }
    else {
      resolved.distancia = 0.0
    }

    if (msg.angulo !== undefined) {
      resolved.angulo = msg.angulo;
    }
    else {
      resolved.angulo = 0.0
    }

    return resolved;
    }
};

module.exports = siguelinea;
