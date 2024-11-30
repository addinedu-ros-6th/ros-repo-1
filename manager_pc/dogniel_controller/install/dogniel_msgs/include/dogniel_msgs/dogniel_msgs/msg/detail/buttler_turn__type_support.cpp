// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dogniel_msgs/msg/detail/buttler_turn__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace dogniel_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ButtlerTurn_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dogniel_msgs::msg::ButtlerTurn(_init);
}

void ButtlerTurn_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dogniel_msgs::msg::ButtlerTurn *>(message_memory);
  typed_message->~ButtlerTurn();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ButtlerTurn_message_member_array[1] = {
  {
    "direction",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dogniel_msgs::msg::ButtlerTurn, direction),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ButtlerTurn_message_members = {
  "dogniel_msgs::msg",  // message namespace
  "ButtlerTurn",  // message name
  1,  // number of fields
  sizeof(dogniel_msgs::msg::ButtlerTurn),
  ButtlerTurn_message_member_array,  // message members
  ButtlerTurn_init_function,  // function to initialize message memory (memory has to be allocated)
  ButtlerTurn_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ButtlerTurn_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ButtlerTurn_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace dogniel_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dogniel_msgs::msg::ButtlerTurn>()
{
  return &::dogniel_msgs::msg::rosidl_typesupport_introspection_cpp::ButtlerTurn_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dogniel_msgs, msg, ButtlerTurn)() {
  return &::dogniel_msgs::msg::rosidl_typesupport_introspection_cpp::ButtlerTurn_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
