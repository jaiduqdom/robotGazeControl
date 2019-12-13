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

class expresion {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.exp = null;
      this.au_ext = null;
      this.it = null;
      this.tt = null;
    }
    else {
      if (initObj.hasOwnProperty('exp')) {
        this.exp = initObj.exp
      }
      else {
        this.exp = '';
      }
      if (initObj.hasOwnProperty('au_ext')) {
        this.au_ext = initObj.au_ext
      }
      else {
        this.au_ext = [];
      }
      if (initObj.hasOwnProperty('it')) {
        this.it = initObj.it
      }
      else {
        this.it = 0.0;
      }
      if (initObj.hasOwnProperty('tt')) {
        this.tt = initObj.tt
      }
      else {
        this.tt = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type expresion
    // Serialize message field [exp]
    bufferOffset = _serializer.string(obj.exp, buffer, bufferOffset);
    // Serialize message field [au_ext]
    bufferOffset = _arraySerializer.float32(obj.au_ext, buffer, bufferOffset, null);
    // Serialize message field [it]
    bufferOffset = _serializer.float32(obj.it, buffer, bufferOffset);
    // Serialize message field [tt]
    bufferOffset = _serializer.float32(obj.tt, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type expresion
    let len;
    let data = new expresion(null);
    // Deserialize message field [exp]
    data.exp = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [au_ext]
    data.au_ext = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [it]
    data.it = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [tt]
    data.tt = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.exp.length;
    length += 4 * object.au_ext.length;
    return length + 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'avatar_msg/expresion';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e5171cc2831e9005bdc4c0ec061818bb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string exp
    float32[] au_ext 
    float32 it
    float32 tt
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new expresion(null);
    if (msg.exp !== undefined) {
      resolved.exp = msg.exp;
    }
    else {
      resolved.exp = ''
    }

    if (msg.au_ext !== undefined) {
      resolved.au_ext = msg.au_ext;
    }
    else {
      resolved.au_ext = []
    }

    if (msg.it !== undefined) {
      resolved.it = msg.it;
    }
    else {
      resolved.it = 0.0
    }

    if (msg.tt !== undefined) {
      resolved.tt = msg.tt;
    }
    else {
      resolved.tt = 0.0
    }

    return resolved;
    }
};

module.exports = expresion;
