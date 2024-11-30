// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dogniel_msgs__msg__DognielAmcl __attribute__((deprecated))
#else
# define DEPRECATED__dogniel_msgs__msg__DognielAmcl __declspec(deprecated)
#endif

namespace dogniel_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DognielAmcl_
{
  using Type = DognielAmcl_<ContainerAllocator>;

  explicit DognielAmcl_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0l;
      this->y = 0l;
      this->z = 0.0f;
      this->w = 0.0f;
    }
  }

  explicit DognielAmcl_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0l;
      this->y = 0l;
      this->z = 0.0f;
      this->w = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    int32_t;
  _x_type x;
  using _y_type =
    int32_t;
  _y_type y;
  using _z_type =
    float;
  _z_type z;
  using _w_type =
    float;
  _w_type w;

  // setters for named parameter idiom
  Type & set__x(
    const int32_t & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const int32_t & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__w(
    const float & _arg)
  {
    this->w = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> *;
  using ConstRawPtr =
    const dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dogniel_msgs__msg__DognielAmcl
    std::shared_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dogniel_msgs__msg__DognielAmcl
    std::shared_ptr<dogniel_msgs::msg::DognielAmcl_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DognielAmcl_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->w != other.w) {
      return false;
    }
    return true;
  }
  bool operator!=(const DognielAmcl_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DognielAmcl_

// alias to use template instance with default allocator
using DognielAmcl =
  dogniel_msgs::msg::DognielAmcl_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__STRUCT_HPP_
