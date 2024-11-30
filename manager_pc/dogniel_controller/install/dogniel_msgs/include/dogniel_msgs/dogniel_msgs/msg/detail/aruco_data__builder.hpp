// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dogniel_msgs:msg/ArucoData.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__BUILDER_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dogniel_msgs/msg/detail/aruco_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dogniel_msgs
{

namespace msg
{

namespace builder
{

class Init_ArucoData_z
{
public:
  explicit Init_ArucoData_z(::dogniel_msgs::msg::ArucoData & msg)
  : msg_(msg)
  {}
  ::dogniel_msgs::msg::ArucoData z(::dogniel_msgs::msg::ArucoData::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dogniel_msgs::msg::ArucoData msg_;
};

class Init_ArucoData_theta
{
public:
  explicit Init_ArucoData_theta(::dogniel_msgs::msg::ArucoData & msg)
  : msg_(msg)
  {}
  Init_ArucoData_z theta(::dogniel_msgs::msg::ArucoData::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return Init_ArucoData_z(msg_);
  }

private:
  ::dogniel_msgs::msg::ArucoData msg_;
};

class Init_ArucoData_id
{
public:
  Init_ArucoData_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArucoData_theta id(::dogniel_msgs::msg::ArucoData::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ArucoData_theta(msg_);
  }

private:
  ::dogniel_msgs::msg::ArucoData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dogniel_msgs::msg::ArucoData>()
{
  return dogniel_msgs::msg::builder::Init_ArucoData_id();
}

}  // namespace dogniel_msgs

#endif  // DOGNIEL_MSGS__MSG__DETAIL__ARUCO_DATA__BUILDER_HPP_
