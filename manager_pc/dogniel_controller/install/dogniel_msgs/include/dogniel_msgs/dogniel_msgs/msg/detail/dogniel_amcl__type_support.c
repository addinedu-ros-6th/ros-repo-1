// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dogniel_msgs/msg/detail/dogniel_amcl__rosidl_typesupport_introspection_c.h"
#include "dogniel_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dogniel_msgs/msg/detail/dogniel_amcl__functions.h"
#include "dogniel_msgs/msg/detail/dogniel_amcl__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dogniel_msgs__msg__DognielAmcl__init(message_memory);
}

void dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_fini_function(void * message_memory)
{
  dogniel_msgs__msg__DognielAmcl__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_member_array[4] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dogniel_msgs__msg__DognielAmcl, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dogniel_msgs__msg__DognielAmcl, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dogniel_msgs__msg__DognielAmcl, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "w",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dogniel_msgs__msg__DognielAmcl, w),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_members = {
  "dogniel_msgs__msg",  // message namespace
  "DognielAmcl",  // message name
  4,  // number of fields
  sizeof(dogniel_msgs__msg__DognielAmcl),
  dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_member_array,  // message members
  dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_init_function,  // function to initialize message memory (memory has to be allocated)
  dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_type_support_handle = {
  0,
  &dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dogniel_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dogniel_msgs, msg, DognielAmcl)() {
  if (!dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_type_support_handle.typesupport_identifier) {
    dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dogniel_msgs__msg__DognielAmcl__rosidl_typesupport_introspection_c__DognielAmcl_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
