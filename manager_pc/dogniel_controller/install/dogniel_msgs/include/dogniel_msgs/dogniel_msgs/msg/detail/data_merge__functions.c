// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dogniel_msgs:msg/DataMerge.idl
// generated code does not contain a copyright notice
#include "dogniel_msgs/msg/detail/data_merge__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
dogniel_msgs__msg__DataMerge__init(dogniel_msgs__msg__DataMerge * msg)
{
  if (!msg) {
    return false;
  }
  // right
  // left
  // id
  // theta
  // z
  return true;
}

void
dogniel_msgs__msg__DataMerge__fini(dogniel_msgs__msg__DataMerge * msg)
{
  if (!msg) {
    return;
  }
  // right
  // left
  // id
  // theta
  // z
}

bool
dogniel_msgs__msg__DataMerge__are_equal(const dogniel_msgs__msg__DataMerge * lhs, const dogniel_msgs__msg__DataMerge * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // right
  if (lhs->right != rhs->right) {
    return false;
  }
  // left
  if (lhs->left != rhs->left) {
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
dogniel_msgs__msg__DataMerge__copy(
  const dogniel_msgs__msg__DataMerge * input,
  dogniel_msgs__msg__DataMerge * output)
{
  if (!input || !output) {
    return false;
  }
  // right
  output->right = input->right;
  // left
  output->left = input->left;
  // id
  output->id = input->id;
  // theta
  output->theta = input->theta;
  // z
  output->z = input->z;
  return true;
}

dogniel_msgs__msg__DataMerge *
dogniel_msgs__msg__DataMerge__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DataMerge * msg = (dogniel_msgs__msg__DataMerge *)allocator.allocate(sizeof(dogniel_msgs__msg__DataMerge), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dogniel_msgs__msg__DataMerge));
  bool success = dogniel_msgs__msg__DataMerge__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dogniel_msgs__msg__DataMerge__destroy(dogniel_msgs__msg__DataMerge * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dogniel_msgs__msg__DataMerge__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dogniel_msgs__msg__DataMerge__Sequence__init(dogniel_msgs__msg__DataMerge__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DataMerge * data = NULL;

  if (size) {
    data = (dogniel_msgs__msg__DataMerge *)allocator.zero_allocate(size, sizeof(dogniel_msgs__msg__DataMerge), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dogniel_msgs__msg__DataMerge__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dogniel_msgs__msg__DataMerge__fini(&data[i - 1]);
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
dogniel_msgs__msg__DataMerge__Sequence__fini(dogniel_msgs__msg__DataMerge__Sequence * array)
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
      dogniel_msgs__msg__DataMerge__fini(&array->data[i]);
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

dogniel_msgs__msg__DataMerge__Sequence *
dogniel_msgs__msg__DataMerge__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dogniel_msgs__msg__DataMerge__Sequence * array = (dogniel_msgs__msg__DataMerge__Sequence *)allocator.allocate(sizeof(dogniel_msgs__msg__DataMerge__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dogniel_msgs__msg__DataMerge__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dogniel_msgs__msg__DataMerge__Sequence__destroy(dogniel_msgs__msg__DataMerge__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dogniel_msgs__msg__DataMerge__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dogniel_msgs__msg__DataMerge__Sequence__are_equal(const dogniel_msgs__msg__DataMerge__Sequence * lhs, const dogniel_msgs__msg__DataMerge__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dogniel_msgs__msg__DataMerge__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dogniel_msgs__msg__DataMerge__Sequence__copy(
  const dogniel_msgs__msg__DataMerge__Sequence * input,
  dogniel_msgs__msg__DataMerge__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dogniel_msgs__msg__DataMerge);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dogniel_msgs__msg__DataMerge * data =
      (dogniel_msgs__msg__DataMerge *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dogniel_msgs__msg__DataMerge__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dogniel_msgs__msg__DataMerge__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dogniel_msgs__msg__DataMerge__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
