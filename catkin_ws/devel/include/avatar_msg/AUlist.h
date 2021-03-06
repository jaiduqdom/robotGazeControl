// Generated by gencpp from file avatar_msg/AUlist.msg
// DO NOT EDIT!


#ifndef AVATAR_MSG_MESSAGE_AULIST_H
#define AVATAR_MSG_MESSAGE_AULIST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace avatar_msg
{
template <class ContainerAllocator>
struct AUlist_
{
  typedef AUlist_<ContainerAllocator> Type;

  AUlist_()
    : it(0.0)
    , tt(0.0)
    , au()  {
    }
  AUlist_(const ContainerAllocator& _alloc)
    : it(0.0)
    , tt(0.0)
    , au(_alloc)  {
  (void)_alloc;
    }



   typedef float _it_type;
  _it_type it;

   typedef float _tt_type;
  _tt_type tt;

   typedef std::vector<float, typename ContainerAllocator::template rebind<float>::other >  _au_type;
  _au_type au;





  typedef boost::shared_ptr< ::avatar_msg::AUlist_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::avatar_msg::AUlist_<ContainerAllocator> const> ConstPtr;

}; // struct AUlist_

typedef ::avatar_msg::AUlist_<std::allocator<void> > AUlist;

typedef boost::shared_ptr< ::avatar_msg::AUlist > AUlistPtr;
typedef boost::shared_ptr< ::avatar_msg::AUlist const> AUlistConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::avatar_msg::AUlist_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::avatar_msg::AUlist_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace avatar_msg

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'avatar_msg': ['/home/disa/catkin_ws/src/avatar_msg/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::avatar_msg::AUlist_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::avatar_msg::AUlist_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::avatar_msg::AUlist_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::avatar_msg::AUlist_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::avatar_msg::AUlist_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::avatar_msg::AUlist_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::avatar_msg::AUlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "48a51fcae9e2ae46610e83f259b0d91d";
  }

  static const char* value(const ::avatar_msg::AUlist_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x48a51fcae9e2ae46ULL;
  static const uint64_t static_value2 = 0x610e83f259b0d91dULL;
};

template<class ContainerAllocator>
struct DataType< ::avatar_msg::AUlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "avatar_msg/AUlist";
  }

  static const char* value(const ::avatar_msg::AUlist_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::avatar_msg::AUlist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 it\n\
float32 tt\n\
float32[] au\n\
\n\
";
  }

  static const char* value(const ::avatar_msg::AUlist_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::avatar_msg::AUlist_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.it);
      stream.next(m.tt);
      stream.next(m.au);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct AUlist_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::avatar_msg::AUlist_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::avatar_msg::AUlist_<ContainerAllocator>& v)
  {
    s << indent << "it: ";
    Printer<float>::stream(s, indent + "  ", v.it);
    s << indent << "tt: ";
    Printer<float>::stream(s, indent + "  ", v.tt);
    s << indent << "au[]" << std::endl;
    for (size_t i = 0; i < v.au.size(); ++i)
    {
      s << indent << "  au[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.au[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // AVATAR_MSG_MESSAGE_AULIST_H
