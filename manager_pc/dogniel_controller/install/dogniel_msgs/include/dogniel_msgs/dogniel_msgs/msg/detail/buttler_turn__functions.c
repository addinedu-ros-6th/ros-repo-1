// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice
#include "dogniel_msgs/msg/detail/buttler_turn__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `direction`
#include "rosidl_runtime_c/string_functions.h"

bool
dogniel_msgs__msg__ButtlerTurn__init(dogniel_msgs__msg__ButtlerTurn * msg)
{
  if (!msg) {
    return false;
  }
  // direction
  if (!rosidl_runtime_c__String__init(&msg->direction)) {
    dogniel_msgs__msg__ButtlerTurn__fini(msg);
    return false;
  }
  return true;
}

void
dogniel_msgs__msg__ButtlerTurn__fini(dogniel_msgs__msg__ButtlerTurn * msg)
{
  if (!msg) {
    return;
  }
  // direction
  rosidl_runtime_c__String__fini(&msg->direction);
}

bool
dogniel_msgs__msg__ButtlerTurn__are_equal(const dogniel_msgs__msg__ButtlerTurn * lhs, const dogniel_msgs__msg__ButtlerTurn * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // direction
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->direction), &(rhs->direction)))
  {
    return false;
  }
  return true;
}

bool
dogniel_msgs__msg__ButtlerTurn__copy(
  const dogniel_msgs__msg__ButtlerTurn * input,
  dogniel_msgs__msg__ButtlerTurn * output)
{
  if (!input || !output) {
    return false;
  }
  // direction
  if (!rosidl_runtime_c__String__copy(
      &(input->direction), &(output->direction)))
  {
    return false;
  }
  return true;
}

dogniel_msgs__msg__ButtlerTurn *
dogniel_msgs__msg__ButtlerTurn__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ButtlerTurn * msg = (dogniel_msgs__msg__ButtlerTurn *)allocator.allocate(sizeof(dogniel_msgs__msg__ButtlerTurn), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dogniel_msgs__msg__ButtlerTurn));
  bool success = dogniel_msgs__msg__ButtlerTurn__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dogniel_msgs__msg__ButtlerTurn__destroy(dogniel_msgs__msg__ButtlerTurn * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dogniel_msgs__msg__ButtlerTurn__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dogniel_msgs__msg__ButtlerTurn__Sequence__init(dogniel_msgs__msg__ButtlerTurn__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ButtlerTurn * data = NULL;

  if (size) {
    data = (dogniel_msgs__msg__ButtlerTurn *)allocator.zero_allocate(size, sizeof(dogniel_msgs__msg__ButtlerTurn), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dogniel_msgs__msg__ButtlerTurn__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dogniel_msgs__msg__ButtlerTurn__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
dogniel_msgs__msg__ButtlerTurn__Sequence__fini(dogniel_msgs__msg__ButtlerTurn__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      dogniel_msgs__msg__ButtlerTurn__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

dogniel_msgs__msg__ButtlerTurn__Sequence *
dogniel_msgs__msg__ButtlerTurn__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ButtlerTurn__Sequence * array = (dogniel_msgs__msg__ButtlerTurn__Sequence *)allocator.allocate(sizeof(dogniel_msgs__msg__ButtlerTurn__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dogniel_msgs__msg__ButtlerTurn__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dogniel_msgs__msg__ButtlerTurn__Sequence__destroy(dogniel_msgs__msg__ButtlerTurn__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dogniel_msgs__msg__ButtlerTurn__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dogniel_msgs__msg__ButtlerTurn__Sequence__are_equal(const dogniel_msgs__msg__ButtlerTurn__Sequence * lhs, const dogniel_msgs__msg__ButtlerTurn__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dogniel_msgs__msg__ButtlerTurn__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dogniel_msgs__msg__ButtlerTurn__Sequence__copy(
  const dogniel_msgs__msg__ButtlerTurn__Sequence * input,
  dogniel_msgs__msg__ButtlerTurn__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dogniel_msgs__msg__ButtlerTurn);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dogniel_msgs__msg__ButtlerTurn * data =
      (dogniel_msgs__msg__ButtlerTurn *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dogniel_msgs__msg__ButtlerTurn__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dogniel_msgs__msg__ButtlerTurn__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dogniel_msgs__msg__ButtlerTurn__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
