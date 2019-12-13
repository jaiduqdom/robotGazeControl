// Generated by gencpp from file seguimiento/movimiento.msg
// DO NOT EDIT!


#ifndef SEGUIMIENTO_MESSAGE_MOVIMIENTO_H
#define SEGUIMIENTO_MESSAGE_MOVIMIENTO_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>

namespace seguimiento
{
template <class ContainerAllocator>
struct movimiento_
{
  typedef movimiento_<ContainerAllocator> Type;

  movimiento_()
    : header()
    , enMovimiento(false)
    , theta_robot(0.0)
    , psi_robot(0.0)  {
    }
  movimiento_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , enMovimiento(false)
    , theta_robot(0.0)
    , psi_robot(0.0)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint8_t _enMovimiento_type;
  _enMovimiento_type enMovimiento;

   typedef float _theta_robot_type;
  _theta_robot_type theta_robot;

   typedef float _psi_robot_type;
  _psi_robot_type psi_robot;





  typedef boost::shared_ptr< ::seguimiento::movimiento_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::seguimiento::movimiento_<ContainerAllocator> const> ConstPtr;

}; // struct movimiento_

typedef ::seguimiento::movimiento_<std::allocator<void> > movimiento;

typedef boost::shared_ptr< ::seguimiento::movimiento > movimientoPtr;
typedef boost::shared_ptr< ::seguimiento::movimiento const> movimientoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::seguimiento::movimiento_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::seguimiento::movimiento_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace seguimiento

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/kinetic/share/sensor_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'seguimiento': ['/home/disa/catkin_ws/src/seguimiento/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::seguimiento::movimiento_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::seguimiento::movimiento_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::seguimiento::movimiento_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::seguimiento::movimiento_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::seguimiento::movimiento_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::seguimiento::movimiento_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::seguimiento::movimiento_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0ea04302753729942b7a5e567e1e615e";
  }

  static const char* value(const ::seguimiento::movimiento_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0ea0430275372994ULL;
  static const uint64_t static_value2 = 0x2b7a5e567e1e615eULL;
};

template<class ContainerAllocator>
struct DataType< ::seguimiento::movimiento_<ContainerAllocator> >
{
  static const char* value()
  {
    return "seguimiento/movimiento";
  }

  static const char* value(const ::seguimiento::movimiento_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::seguimiento::movimiento_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Header header\n\
bool enMovimiento\n\
float32 theta_robot\n\
float32 psi_robot\n\
\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
";
  }

  static const char* value(const ::seguimiento::movimiento_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::seguimiento::movimiento_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.enMovimiento);
      stream.next(m.theta_robot);
      stream.next(m.psi_robot);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct movimiento_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::seguimiento::movimiento_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::seguimiento::movimiento_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "enMovimiento: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.enMovimiento);
    s << indent << "theta_robot: ";
    Printer<float>::stream(s, indent + "  ", v.theta_robot);
    s << indent << "psi_robot: ";
    Printer<float>::stream(s, indent + "  ", v.psi_robot);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SEGUIMIENTO_MESSAGE_MOVIMIENTO_H
