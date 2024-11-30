// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dogniel_msgs:msg/ButtlerTurn.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__BUILDER_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dogniel_msgs/msg/detail/buttler_turn__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dogniel_msgs
{

namespace msg
{

namespace builder
{

class Init_ButtlerTurn_direction
{
public:
  Init_ButtlerTurn_direction()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dogniel_msgs::msg::ButtlerTurn direction(::dogniel_msgs::msg::ButtlerTurn::_direction_type arg)
  {
    msg_.direction = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dogniel_msgs::msg::ButtlerTurn msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dogniel_msgs::msg::ButtlerTurn>()
{
  return dogniel_msgs::msg::builder::Init_ButtlerTurn_direction();
}

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__BUTTLER_TURN__BUILDER_HPP_
