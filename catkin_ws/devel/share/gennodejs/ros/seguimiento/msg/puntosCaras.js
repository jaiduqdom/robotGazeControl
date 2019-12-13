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

class puntosCaras {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.numeroCaras = null;
      this.x1 = null;
      this.y1 = null;
      this.x2 = null;
      this.y2 = null;
      this.puntoX = null;
      this.puntoY = null;
      this.indiceCara = null;
      this.caraNueva = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('numeroCaras')) {
        this.numeroCaras = initObj.numeroCaras
      }
      else {
        this.numeroCaras = 0;
      }
      if (initObj.hasOwnProperty('x1')) {
        this.x1 = initObj.x1
      }
      else {
        this.x1 = [];
      }
      if (initObj.hasOwnProperty('y1')) {
        this.y1 = initObj.y1
      }
      else {
        this.y1 = [];
      }
      if (initObj.hasOwnProperty('x2')) {
        this.x2 = initObj.x2
      }
      else {
        this.x2 = [];
      }
      if (initObj.hasOwnProperty('y2')) {
        this.y2 = initObj.y2
      }
      else {
        this.y2 = [];
      }
      if (initObj.hasOwnProperty('puntoX')) {
        this.puntoX = initObj.puntoX
      }
      else {
        this.puntoX = [];
      }
      if (initObj.hasOwnProperty('puntoY')) {
        this.puntoY = initObj.puntoY
      }
      else {
        this.puntoY = [];
      }
      if (initObj.hasOwnProperty('indiceCara')) {
        this.indiceCara = initObj.indiceCara
      }
      else {
        this.indiceCara = [];
      }
      if (initObj.hasOwnProperty('caraNueva')) {
        this.caraNueva = initObj.caraNueva
      }
      else {
        this.caraNueva = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type puntosCaras
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [numeroCaras]
    bufferOffset = _serializer.int32(obj.numeroCaras, buffer, bufferOffset);
    // Serialize message field [x1]
    bufferOffset = _arraySerializer.int32(obj.x1, buffer, bufferOffset, null);
    // Serialize message field [y1]
    bufferOffset = _arraySerializer.int32(obj.y1, buffer, bufferOffset, null);
    // Serialize message field [x2]
    bufferOffset = _arraySerializer.int32(obj.x2, buffer, bufferOffset, null);
    // Serialize message field [y2]
    bufferOffset = _arraySerializer.int32(obj.y2, buffer, bufferOffset, null);
    // Serialize message field [puntoX]
    bufferOffset = _arraySerializer.int32(obj.puntoX, buffer, bufferOffset, null);
    // Serialize message field [puntoY]
    bufferOffset = _arraySerializer.int32(obj.puntoY, buffer, bufferOffset, null);
    // Serialize message field [indiceCara]
    bufferOffset = _arraySerializer.int32(obj.indiceCara, buffer, bufferOffset, null);
    // Serialize message field [caraNueva]
    bufferOffset = _arraySerializer.bool(obj.caraNueva, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type puntosCaras
    let len;
    let data = new puntosCaras(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [numeroCaras]
    data.numeroCaras = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [x1]
    data.x1 = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [y1]
    data.y1 = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [x2]
    data.x2 = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [y2]
    data.y2 = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [puntoX]
    data.puntoX = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [puntoY]
    data.puntoY = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [indiceCara]
    data.indiceCara = _arrayDeserializer.int32(buffer, bufferOffset, null)
    // Deserialize message field [caraNueva]
    data.caraNueva = _arrayDeserializer.bool(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 4 * object.x1.length;
    length += 4 * object.y1.length;
    length += 4 * object.x2.length;
    length += 4 * object.y2.length;
    length += 4 * object.puntoX.length;
    length += 4 * object.puntoY.length;
    length += 4 * object.indiceCara.length;
    length += object.caraNueva.length;
    return length + 36;
  }

  static datatype() {
    // Returns string type for a message object
    return 'seguimiento/puntosCaras';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b9577e30fd5aa6d52d9bd36c0e0026d1';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    int32 numeroCaras
    int32[] x1
    int32[] y1
    int32[] x2
    int32[] y2
    int32[] puntoX
    int32[] puntoY
    int32[] indiceCara
    bool[] caraNueva
    
    
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
    const resolved = new puntosCaras(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.numeroCaras !== undefined) {
      resolved.numeroCaras = msg.numeroCaras;
    }
    else {
      resolved.numeroCaras = 0
    }

    if (msg.x1 !== undefined) {
      resolved.x1 = msg.x1;
    }
    else {
      resolved.x1 = []
    }

    if (msg.y1 !== undefined) {
      resolved.y1 = msg.y1;
    }
    else {
      resolved.y1 = []
    }

    if (msg.x2 !== undefined) {
      resolved.x2 = msg.x2;
    }
    else {
      resolved.x2 = []
    }

    if (msg.y2 !== undefined) {
      resolved.y2 = msg.y2;
    }
    else {
      resolved.y2 = []
    }

    if (msg.puntoX !== undefined) {
      resolved.puntoX = msg.puntoX;
    }
    else {
      resolved.puntoX = []
    }

    if (msg.puntoY !== undefined) {
      resolved.puntoY = msg.puntoY;
    }
    else {
      resolved.puntoY = []
    }

    if (msg.indiceCara !== undefined) {
      resolved.indiceCara = msg.indiceCara;
    }
    else {
      resolved.indiceCara = []
    }

    if (msg.caraNueva !== undefined) {
      resolved.caraNueva = msg.caraNueva;
    }
    else {
      resolved.caraNueva = []
    }

    return resolved;
    }
};

module.exports = puntosCaras;
