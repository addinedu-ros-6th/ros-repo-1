// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_H_
#define DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'direction'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ButtlerTurn in the package dogniel_msgs.
typedef struct dogniel_msgs__msg__ButtlerTurn
{
  rosidl_runtime_c__String direction;
} dogniel_msgs__msg__ButtlerTurn;

// Struct for a sequence of dogniel_msgs__msg__ButtlerTurn.
typedef struct dogniel_msgs__msg__ButtlerTurn__Sequence
{
  dogniel_msgs__msg__ButtlerTurn * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dogniel_msgs__msg__ButtlerTurn__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_H_
