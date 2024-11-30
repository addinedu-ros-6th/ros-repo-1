// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_H_
#define DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/DognielAmcl in the package dogniel_msgs.
typedef struct dogniel_msgs__msg__DognielAmcl
{
  int32_t x;
  int32_t y;
  float z;
  float w;
} dogniel_msgs__msg__DognielAmcl;

// Struct for a sequence of dogniel_msgs__msg__DognielAmcl.
typedef struct dogniel_msgs__msg__DognielAmcl__Sequence
{
  dogniel_msgs__msg__DognielAmcl * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dogniel_msgs__msg__DognielAmcl__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_H_
