// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dogniel_msgs:msg/DataMerge.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__BUILDER_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dogniel_msgs/msg/detail/data_merge__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dogniel_msgs
{

namespace msg
{

namespace builder
{

class Init_DataMerge_z
{
public:
  explicit Init_DataMerge_z(::dogniel_msgs::msg::DataMerge & msg)
  : msg_(msg)
  {}
  ::dogniel_msgs::msg::DataMerge z(::dogniel_msgs::msg::DataMerge::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dogniel_msgs::msg::DataMerge msg_;
};

class Init_DataMerge_theta
{
public:
  explicit Init_DataMerge_theta(::dogniel_msgs::msg::DataMerge & msg)
  : msg_(msg)
  {}
  Init_DataMerge_z theta(::dogniel_msgs::msg::DataMerge::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return Init_DataMerge_z(msg_);
  }

private:
  ::dogniel_msgs::msg::DataMerge msg_;
};

class Init_DataMerge_id
{
public:
  explicit Init_DataMerge_id(::dogniel_msgs::msg::DataMerge & msg)
  : msg_(msg)
  {}
  Init_DataMerge_theta id(::dogniel_msgs::msg::DataMerge::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_DataMerge_theta(msg_);
  }

private:
  ::dogniel_msgs::msg::DataMerge msg_;
};

class Init_DataMerge_left
{
public:
  explicit Init_DataMerge_left(::dogniel_msgs::msg::DataMerge & msg)
  : msg_(msg)
  {}
  Init_DataMerge_id left(::dogniel_msgs::msg::DataMerge::_left_type arg)
  {
    msg_.left = std::move(arg);
    return Init_DataMerge_id(msg_);
  }

private:
  ::dogniel_msgs::msg::DataMerge msg_;
};

class Init_DataMerge_right
{
public:
  Init_DataMerge_right()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DataMerge_left right(::dogniel_msgs::msg::DataMerge::_right_type arg)
  {
    msg_.right = std::move(arg);
    return Init_DataMerge_left(msg_);
  }

private:
  ::dogniel_msgs::msg::DataMerge msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dogniel_msgs::msg::DataMerge>()
{
  return dogniel_msgs::msg::builder::Init_DataMerge_right();
}

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DATA_MERGE__BUILDER_HPP_
