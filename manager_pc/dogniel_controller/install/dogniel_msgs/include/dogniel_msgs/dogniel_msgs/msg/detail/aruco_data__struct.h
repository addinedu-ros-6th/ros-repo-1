// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dogniel_msgs:msg/ArucoData.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_H_
#define DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ArucoData in the package dogniel_msgs.
typedef struct dogniel_msgs__msg__ArucoData
{
  int32_t id;
  float theta;
  float z;
} dogniel_msgs__msg__ArucoData;

// Struct for a sequence of dogniel_msgs__msg__ArucoData.
typedef struct dogniel_msgs__msg__ArucoData__Sequence
{
  dogniel_msgs__msg__ArucoData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dogniel_msgs__msg__ArucoData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_H_
