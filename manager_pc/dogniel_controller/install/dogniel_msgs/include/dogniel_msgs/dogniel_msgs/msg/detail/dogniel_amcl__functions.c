// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice
#include "dogniel_msgs/msg/detail/dogniel_amcl__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
dogniel_msgs__msg__DognielAmcl__init(dogniel_msgs__msg__DognielAmcl * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  // w
  return true;
}

void
dogniel_msgs__msg__DognielAmcl__fini(dogniel_msgs__msg__DognielAmcl * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
  // w
}

bool
dogniel_msgs__msg__DognielAmcl__are_equal(const dogniel_msgs__msg__DognielAmcl * lhs, const dogniel_msgs__msg__DognielAmcl * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // w
  if (lhs->w != rhs->w) {
    return false;
  }
  return true;
}

bool
dogniel_msgs__msg__DognielAmcl__copy(
  const dogniel_msgs__msg__DognielAmcl * input,
  dogniel_msgs__msg__DognielAmcl * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // w
  output->w = input->w;
  return true;
}

dogniel_msgs__msg__DognielAmcl *
dogniel_msgs__msg__DognielAmcl__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DognielAmcl * msg = (dogniel_msgs__msg__DognielAmcl *)allocator.allocate(sizeof(dogniel_msgs__msg__DognielAmcl), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dogniel_msgs__msg__DognielAmcl));
  bool success = dogniel_msgs__msg__DognielAmcl__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dogniel_msgs__msg__DognielAmcl__destroy(dogniel_msgs__msg__DognielAmcl * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dogniel_msgs__msg__DognielAmcl__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dogniel_msgs__msg__DognielAmcl__Sequence__init(dogniel_msgs__msg__DognielAmcl__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DognielAmcl * data = NULL;

  if (size) {
    data = (dogniel_msgs__msg__DognielAmcl *)allocator.zero_allocate(size, sizeof(dogniel_msgs__msg__DognielAmcl), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dogniel_msgs__msg__DognielAmcl__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dogniel_msgs__msg__DognielAmcl__fini(&data[i - 1]);
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
dogniel_msgs__msg__DognielAmcl__Sequence__fini(dogniel_msgs__msg__DognielAmcl__Sequence * array)
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
      dogniel_msgs__msg__DognielAmcl__fini(&array->data[i]);
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

dogniel_msgs__msg__DognielAmcl__Sequence *
dogniel_msgs__msg__DognielAmcl__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DognielAmcl__Sequence * array = (dogniel_msgs__msg__DognielAmcl__Sequence *)allocator.allocate(sizeof(dogniel_msgs__msg__DognielAmcl__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dogniel_msgs__msg__DognielAmcl__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dogniel_msgs__msg__DognielAmcl__Sequence__destroy(dogniel_msgs__msg__DognielAmcl__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dogniel_msgs__msg__DognielAmcl__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dogniel_msgs__msg__DognielAmcl__Sequence__are_equal(const dogniel_msgs__msg__DognielAmcl__Sequence * lhs, const dogniel_msgs__msg__DognielAmcl__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dogniel_msgs__msg__DognielAmcl__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dogniel_msgs__msg__DognielAmcl__Sequence__copy(
  const dogniel_msgs__msg__DognielAmcl__Sequence * input,
  dogniel_msgs__msg__DognielAmcl__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dogniel_msgs__msg__DognielAmcl);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dogniel_msgs__msg__DognielAmcl * data =
      (dogniel_msgs__msg__DognielAmcl *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dogniel_msgs__msg__DognielAmcl__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dogniel_msgs__msg__DognielAmcl__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dogniel_msgs__msg__DognielAmcl__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
