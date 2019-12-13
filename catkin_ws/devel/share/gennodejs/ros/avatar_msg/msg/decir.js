// Auto-generated. Do not edit!

// (in-package avatar_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class decir {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.palabras = null;
    }
    else {
      if (initObj.hasOwnProperty('palabras')) {
        this.palabras = initObj.palabras
      }
      else {
        this.palabras = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type decir
    // Serialize message field [palabras]
    bufferOffset = _serializer.string(obj.palabras, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type decir
    let len;
    let data = new decir(null);
    // Deserialize message field [palabras]
    data.palabras = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.palabras.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'avatar_msg/decir';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f31a5a411200c463cdcdb46c34aa2c72';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string palabras
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new decir(null);
    if (msg.palabras !== undefined) {
      resolved.palabras = msg.palabras;
    }
    else {
      resolved.palabras = ''
    }

    return resolved;
    }
};

module.exports = decir;
