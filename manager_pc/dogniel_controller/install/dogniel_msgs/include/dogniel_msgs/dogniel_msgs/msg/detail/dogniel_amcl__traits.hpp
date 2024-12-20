// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dogniel_msgs:msg/DognielAmcl.idl
// generated code does not contain a copyright notice

#ifndef DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__TRAITS_HPP_
#define DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dogniel_msgs/msg/detail/dogniel_amcl__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dogniel_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DognielAmcl & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: w
  {
    out << "w: ";
    rosidl_generator_traits::value_to_yaml(msg.w, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DognielAmcl & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: w
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w: ";
    rosidl_generator_traits::value_to_yaml(msg.w, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DognielAmcl & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace dogniel_msgs

namespace rosidl_generator_traits
{

[[deprecated("use dogniel_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dogniel_msgs::msg::DognielAmcl & msg,
  std::ostream & out, size_t indentation = 0)
{
  dogniel_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dogniel_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const dogniel_msgs::msg::DognielAmcl & msg)
{
  return dogniel_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<dogniel_msgs::msg::DognielAmcl>()
{
  return "dogniel_msgs::msg::DognielAmcl";
}

template<>
inline const char * name<dogniel_msgs::msg::DognielAmcl>()
{
  return "dogniel_msgs/msg/DognielAmcl";
}

template<>
struct has_fixed_size<dogniel_msgs::msg::DognielAmcl>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dogniel_msgs::msg::DognielAmcl>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dogniel_msgs::msg::DognielAmcl>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DOGNIEL_MSGS__MSG__DETAIL__DOGNIEL_AMCL__TRAITS_HPP_
