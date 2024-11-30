// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dogniel_msgs:msg/ArucoData.idl
// generated code does not contain a copyright notice
#include "dogniel_msgs/msg/detail/aruco_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
dogniel_msgs__msg__ArucoData__init(dogniel_msgs__msg__ArucoData * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // theta
  // z
  return true;
}

void
dogniel_msgs__msg__ArucoData__fini(dogniel_msgs__msg__ArucoData * msg)
{
  if (!msg) {
    return;
  }
  // id
  // theta
  // z
}

bool
dogniel_msgs__msg__ArucoData__are_equal(const dogniel_msgs__msg__ArucoData * lhs, const dogniel_msgs__msg__ArucoData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // theta
  if (lhs->theta != rhs->theta) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  return true;
}

bool
dogniel_msgs__msg__ArucoData__copy(
  const dogniel_msgs__msg__ArucoData * input,
  dogniel_msgs__msg__ArucoData * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // theta
  output->theta = input->theta;
  // z
  output->z = input->z;
  return true;
}

dogniel_msgs__msg__ArucoData *
dogniel_msgs__msg__ArucoData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ArucoData * msg = (dogniel_msgs__msg__ArucoData *)allocator.allocate(sizeof(dogniel_msgs__msg__ArucoData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dogniel_msgs__msg__ArucoData));
  bool success = dogniel_msgs__msg__ArucoData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dogniel_msgs__msg__ArucoData__destroy(dogniel_msgs__msg__ArucoData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dogniel_msgs__msg__ArucoData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dogniel_msgs__msg__ArucoData__Sequence__init(dogniel_msgs__msg__ArucoData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ArucoData * data = NULL;

  if (size) {
    data = (dogniel_msgs__msg__ArucoData *)allocator.zero_allocate(size, sizeof(dogniel_msgs__msg__ArucoData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dogniel_msgs__msg__ArucoData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dogniel_msgs__msg__ArucoData__fini(&data[i - 1]);
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
dogniel_msgs__msg__ArucoData__Sequence__fini(dogniel_msgs__msg__ArucoData__Sequence * array)
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
      dogniel_msgs__msg__ArucoData__fini(&array->data[i]);
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

dogniel_msgs__msg__ArucoData__Sequence *
dogniel_msgs__msg__ArucoData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__ArucoData__Sequence * array = (dogniel_msgs__msg__ArucoData__Sequence *)allocator.allocate(sizeof(dogniel_msgs__msg__ArucoData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dogniel_msgs__msg__ArucoData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dogniel_msgs__msg__ArucoData__Sequence__destroy(dogniel_msgs__msg__ArucoData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dogniel_msgs__msg__ArucoData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dogniel_msgs__msg__ArucoData__Sequence__are_equal(const dogniel_msgs__msg__ArucoData__Sequence * lhs, const dogniel_msgs__msg__ArucoData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dogniel_msgs__msg__ArucoData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dogniel_msgs__msg__ArucoData__Sequence__copy(
  const dogniel_msgs__msg__ArucoData__Sequence * input,
  dogniel_msgs__msg__ArucoData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dogniel_msgs__msg__ArucoData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dogniel_msgs__msg__ArucoData * data =
      (dogniel_msgs__msg__ArucoData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dogniel_msgs__msg__ArucoData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dogniel_msgs__msg__ArucoData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dogniel_msgs__msg__ArucoData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
