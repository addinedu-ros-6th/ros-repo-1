// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dogniel_msgs__msg__ButtlerTurn __attribute__((deprecated))
#else
# define DEPRECATED__dogniel_msgs__msg__ButtlerTurn __declspec(deprecated)
#endif

namespace dogniel_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ButtlerTurn_
{
  using Type = ButtlerTurn_<ContainerAllocator>;

  explicit ButtlerTurn_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->direction = "";
    }
  }

  explicit ButtlerTurn_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : direction(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->direction = "";
    }
  }

  // field types and members
  using _direction_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _direction_type direction;

  // setters for named parameter idiom
  Type & set__direction(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->direction = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> *;
  using ConstRawPtr =
    const dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dogniel_msgs__msg__ButtlerTurn
    std::shared_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dogniel_msgs__msg__ButtlerTurn
    std::shared_ptr<dogniel_msgs::msg::ButtlerTurn_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ButtlerTurn_ & other) const
  {
    if (this->direction != other.direction) {
      return false;
    }
    return true;
  }
  bool operator!=(const ButtlerTurn_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ButtlerTurn_

// alias to use template instance with default allocator
using ButtlerTurn =
  dogniel_msgs::msg::ButtlerTurn_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__STRUCT_HPP_
