// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dogniel_msgs:msg/DataMerge.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__STRUCT_H_
#define DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/DataMerge in the package dogniel_msgs.
typedef struct dogniel_msgs__msg__DataMerge
{
  float right;
  float left;
  int32_t id;
  float theta;
  float z;
} dogniel_msgs__msg__DataMerge;

// Struct for a sequence of dogniel_msgs__msg__DataMerge.
typedef struct dogniel_msgs__msg__DataMerge__Sequence
{
  dogniel_msgs__msg__DataMerge * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dogniel_msgs__msg__DataMerge__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__STRUCT_H_
