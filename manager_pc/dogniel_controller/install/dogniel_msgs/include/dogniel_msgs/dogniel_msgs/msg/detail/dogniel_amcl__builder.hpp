// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__BUILDER_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dogniel_msgs/msg/detail/dogniel_amcl__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dogniel_msgs
{

namespace msg
{

namespace builder
{

class Init_DognielAmcl_w
{
public:
  explicit Init_DognielAmcl_w(::dogniel_msgs::msg::DognielAmcl & msg)
  : msg_(msg)
  {}
  ::dogniel_msgs::msg::DognielAmcl w(::dogniel_msgs::msg::DognielAmcl::_w_type arg)
  {
    msg_.w = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dogniel_msgs::msg::DognielAmcl msg_;
};

class Init_DognielAmcl_z
{
public:
  explicit Init_DognielAmcl_z(::dogniel_msgs::msg::DognielAmcl & msg)
  : msg_(msg)
  {}
  Init_DognielAmcl_w z(::dogniel_msgs::msg::DognielAmcl::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_DognielAmcl_w(msg_);
  }

private:
  ::dogniel_msgs::msg::DognielAmcl msg_;
};

class Init_DognielAmcl_y
{
public:
  explicit Init_DognielAmcl_y(::dogniel_msgs::msg::DognielAmcl & msg)
  : msg_(msg)
  {}
  Init_DognielAmcl_z y(::dogniel_msgs::msg::DognielAmcl::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_DognielAmcl_z(msg_);
  }

private:
  ::dogniel_msgs::msg::DognielAmcl msg_;
};

class Init_DognielAmcl_x
{
public:
  Init_DognielAmcl_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DognielAmcl_y x(::dogniel_msgs::msg::DognielAmcl::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_DognielAmcl_y(msg_);
  }

private:
  ::dogniel_msgs::msg::DognielAmcl msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dogniel_msgs::msg::DognielAmcl>()
{
  return dogniel_msgs::msg::builder::Init_DognielAmcl_x();
}

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__BUILDER_HPP_
