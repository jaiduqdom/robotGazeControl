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

class AUlist {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.it = null;
      this.tt = null;
      this.au = null;
    }
    else {
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
      if (initObj.hasOwnProperty('au')) {
        this.au = initObj.au
      }
      else {
        this.au = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type AUlist
    // Serialize message field [it]
    bufferOffset = _serializer.float32(obj.it, buffer, bufferOffset);
    // Serialize message field [tt]
    bufferOffset = _serializer.float32(obj.tt, buffer, bufferOffset);
    // Serialize message field [au]
    bufferOffset = _arraySerializer.float32(obj.au, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type AUlist
    let len;
    let data = new AUlist(null);
    // Deserialize message field [it]
    data.it = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [tt]
    data.tt = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [au]
    data.au = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.au.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'avatar_msg/AUlist';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '48a51fcae9e2ae46610e83f259b0d91d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 it
    float32 tt
    float32[] au
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new AUlist(null);
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

    if (msg.au !== undefined) {
      resolved.au = msg.au;
    }
    else {
      resolved.au = []
    }

    return resolved;
    }
};

module.exports = AUlist;
