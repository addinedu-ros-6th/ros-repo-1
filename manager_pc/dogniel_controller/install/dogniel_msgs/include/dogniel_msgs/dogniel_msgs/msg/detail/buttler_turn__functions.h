// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__FUNCTIONS_H_
#define DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "dogniel_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "dogniel_msgs/msg/detail/buttler_turn__struct.h"

/// Initialize msg/ButtlerTurn message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dogniel_msgs__msg__ButtlerTurn
 * )) before or use
 * dogniel_msgs__msg__ButtlerTurn__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__init(dogniel_msgs__msg__ButtlerTurn * msg);

/// Finalize msg/ButtlerTurn message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
void
dogniel_msgs__msg__ButtlerTurn__fini(dogniel_msgs__msg__ButtlerTurn * msg);

/// Create msg/ButtlerTurn message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dogniel_msgs__msg__ButtlerTurn__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
dogniel_msgs__msg__ButtlerTurn *
dogniel_msgs__msg__ButtlerTurn__create();

/// Destroy msg/ButtlerTurn message.
/**
 * It calls
 * dogniel_msgs__msg__ButtlerTurn__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
void
dogniel_msgs__msg__ButtlerTurn__destroy(dogniel_msgs__msg__ButtlerTurn * msg);

/// Check for msg/ButtlerTurn message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__are_equal(const dogniel_msgs__msg__ButtlerTurn * lhs, const dogniel_msgs__msg__ButtlerTurn * rhs);

/// Copy a msg/ButtlerTurn message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__copy(
  const dogniel_msgs__msg__ButtlerTurn * input,
  dogniel_msgs__msg__ButtlerTurn * output);

/// Initialize array of msg/ButtlerTurn messages.
/**
 * It allocates the memory for the number of elements and calls
 * dogniel_msgs__msg__ButtlerTurn__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__Sequence__init(dogniel_msgs__msg__ButtlerTurn__Sequence * array, size_t size);

/// Finalize array of msg/ButtlerTurn messages.
/**
 * It calls
 * dogniel_msgs__msg__ButtlerTurn__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
void
dogniel_msgs__msg__ButtlerTurn__Sequence__fini(dogniel_msgs__msg__ButtlerTurn__Sequence * array);

/// Create array of msg/ButtlerTurn messages.
/**
 * It allocates the memory for the array and calls
 * dogniel_msgs__msg__ButtlerTurn__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
dogniel_msgs__msg__ButtlerTurn__Sequence *
dogniel_msgs__msg__ButtlerTurn__Sequence__create(size_t size);

/// Destroy array of msg/ButtlerTurn messages.
/**
 * It calls
 * dogniel_msgs__msg__ButtlerTurn__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
void
dogniel_msgs__msg__ButtlerTurn__Sequence__destroy(dogniel_msgs__msg__ButtlerTurn__Sequence * array);

/// Check for msg/ButtlerTurn message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__Sequence__are_equal(const dogniel_msgs__msg__ButtlerTurn__Sequence * lhs, const dogniel_msgs__msg__ButtlerTurn__Sequence * rhs);

/// Copy an array of msg/ButtlerTurn messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dogniel_msgs
bool
dogniel_msgs__msg__ButtlerTurn__Sequence__copy(
  const dogniel_msgs__msg__ButtlerTurn__Sequence * input,
  dogniel_msgs__msg__ButtlerTurn__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__FUNCTIONS_H_
