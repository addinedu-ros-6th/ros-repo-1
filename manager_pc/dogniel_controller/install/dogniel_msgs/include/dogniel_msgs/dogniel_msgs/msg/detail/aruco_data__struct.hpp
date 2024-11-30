// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dogniel_msgs:msg/ArucoData.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dogniel_msgs__msg__ArucoData __attribute__((deprecated))
#else
# define DEPRECATED__dogniel_msgs__msg__ArucoData __declspec(deprecated)
#endif

namespace dogniel_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ArucoData_
{
  using Type = ArucoData_<ContainerAllocator>;

  explicit ArucoData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->theta = 0.0f;
      this->z = 0.0f;
    }
  }

  explicit ArucoData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->theta = 0.0f;
      this->z = 0.0f;
    }
  }

  // field types and members
  using _id_type =
    int32_t;
  _id_type id;
  using _theta_type =
    float;
  _theta_type theta;
  using _z_type =
    float;
  _z_type z;

  // setters for named parameter idiom
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__theta(
    const float & _arg)
  {
    this->theta = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dogniel_msgs::msg::ArucoData_<ContainerAllocator> *;
  using ConstRawPtr =
    const dogniel_msgs::msg::ArucoData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::ArucoData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::ArucoData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dogniel_msgs__msg__ArucoData
    std::shared_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dogniel_msgs__msg__ArucoData
    std::shared_ptr<dogniel_msgs::msg::ArucoData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArucoData_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->theta != other.theta) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArucoData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArucoData_

// alias to use template instance with default allocator
using ArucoData =
  dogniel_msgs::msg::ArucoData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__STRUCT_HPP_
