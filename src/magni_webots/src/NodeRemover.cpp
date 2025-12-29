/*
this code was created based on https://github.com/Ekumen-OS/andino_webots/blob/humble/node_remover_plugin/node_remover_plugin/node_remover_plugin.py
*/

#include "magni_webots/NodeRemover.hpp"
#include "rclcpp/rclcpp.hpp"
#include <cstdio>
#include <functional>
#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/supervisor.h>
#include <algorithm>

namespace magni_webots
{
  NodeRemover::NodeRemover()
      : logger_(rclcpp::get_logger("magni_webots::NodeRemover"))
  {
  }

  void NodeRemover::init(webots_ros2_driver::WebotsNode *node, std::unordered_map<std::string, std::string> &parameters)
  {
    (void)parameters; // unused for now
    logger_ = node->get_logger();
    RCLCPP_INFO(logger_, "starting node remover plugin");

    robot_name_ = "magni";
    nodes_to_remove_ = {
        "left_caster_wheel_joint",
        "left_caster_wheel_base_joint",
        "right_caster_wheel_joint",
        "right_caster_wheel_base_joint"};
  }

  void NodeRemover::step()
  {
    if (nodes_to_remove_.size() > 0)
    {
      if (!robot_)
      {
        robot_ = get_robot_node(robot_name_);
      }
      if (robot_)
      {
        remove_node(robot_);
      }
    }
  }

  WbNodeRef NodeRemover::get_robot_node(const std::string &robot_name)
  {
    RCLCPP_INFO(logger_, "looking for '%s' robot", robot_name.c_str());
    // Get the root node and its children field
    WbNodeRef root = wb_supervisor_node_get_root();
    if (!root)
    {
      RCLCPP_WARN(logger_, "unable to get supervisor root node");
      return nullptr;
    }

    WbFieldRef children_field = wb_supervisor_node_get_field(root, "children");
    if (!children_field)
    {
      RCLCPP_WARN(logger_, "unable to get children field from root");
      return nullptr;
    }

    const int child_count = wb_supervisor_field_get_count(children_field);
    RCLCPP_INFO(logger_, "root children count: %d", child_count);

    WbNodeRef magni_robot = nullptr;

    // iterate over root children and look for a Robot node with DEF name "magni"
    for (auto i = 0; i < child_count; ++i)
    {
      WbNodeRef child = wb_supervisor_field_get_mf_node(children_field, i);
      if (!child)
        continue;

      // Check node type: Robot
      // WB_NODE_ROBOT is defined in webots nodes header; compare using type name as a fallback
      const char *type_name = wb_supervisor_node_get_type_name(child);

      if (type_name && std::string(type_name) == "Robot")
      {
        WbFieldRef childName = wb_supervisor_node_get_field(child, "name");
        const char *name = wb_supervisor_field_get_sf_string(childName);
        if (name && std::string(name) == "magni")
        {
          magni_robot = child;
          RCLCPP_INFO(logger_, "found robot node '%s' at child index %d", robot_name.c_str(), i);
          break;
        }
      }
    }

    if (!magni_robot)
    {
      RCLCPP_WARN(logger_, "robot node '%s' not found among root children; skipping caster removal", robot_name.c_str());
    }
    return magni_robot;
  }

  void NodeRemover::remove_node(WbNodeRef node)
  {
    WbFieldRef nodeNameField = wb_supervisor_node_get_field(node, "name");
    const char *nodeName = nullptr;
    if (!nodeNameField) {
      // Many node types don't have a 'name' field; this is not an error.
      RCLCPP_DEBUG(logger_, "node has no name field; continuing traversal");
    } else {
      nodeName = wb_supervisor_field_get_sf_string(nodeNameField);
    }

    if(nodes_to_remove_.size() == 0){
      return;
    }

    // If node has a name, check whether it's listed for removal
    if (nodeName) {
      std::string nameStr(nodeName);
      // find matching entry in nodes_to_remove_
      auto it = std::find_if(nodes_to_remove_.begin(), nodes_to_remove_.end(),
                             [&](const std::string &target) {
                               // match either exact name or substring
                               return target == nameStr || nameStr.find(target) != std::string::npos;
                             });
      if (it != nodes_to_remove_.end()) {
        const char *logName = nodeName ? nodeName : "<unnamed>";
        RCLCPP_INFO(logger_, "removing node: %s", logName);
        wb_supervisor_node_remove(node);
        nodes_to_remove_.erase(it);
        return; // node removed, stop processing this subtree
      }
    }

    WbFieldRef devices = wb_supervisor_node_get_field(node, "device");
    if (devices) {
      int device_count = wb_supervisor_field_get_count(devices);
      for (int i = 0; i < device_count; i++) {
        WbNodeRef device_node = wb_supervisor_field_get_mf_node(devices, i);
        if (device_node){
          remove_node(device_node);
        }
      }
      WbFieldRef endpoint = wb_supervisor_node_get_field(node,"endPoint");
      WbNodeRef endpoint_node = wb_supervisor_field_get_sf_node(endpoint);
      if(endpoint_node){
        remove_node(endpoint_node);
      }
    }

    WbFieldRef children = wb_supervisor_node_get_field(node, "children");
    if (children) {
      int child_count = wb_supervisor_field_get_count(children);
      for (int i = 0; i < child_count; i++) {
        WbNodeRef child_node = wb_supervisor_field_get_mf_node(children, i);
        if (child_node){
          remove_node(child_node);
        }
      }
    }
 
  }
}
#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(magni_webots::NodeRemover, webots_ros2_driver::PluginInterface)
