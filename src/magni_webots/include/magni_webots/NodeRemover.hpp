#ifndef MAGNI_WEBOTS_NODE_REMOVER_HPP
#define MAGNI_WEBOTS_NODE_REMOVER_HPP

#include "rclcpp/rclcpp.hpp"
#include "webots_ros2_driver/PluginInterface.hpp"
#include "webots_ros2_driver/WebotsNode.hpp"
#include <string>
#include <vector>

namespace magni_webots {
    class NodeRemover : public webots_ros2_driver::PluginInterface {
        public:
            NodeRemover();
            void step() override;
            void init(webots_ros2_driver::WebotsNode *node, std::unordered_map<std::string, std::string> &parameters) override;
        private:
            rclcpp::Logger logger_;
            std::string robot_name_;
            std::vector<std::string> nodes_to_remove_;
            WbNodeRef robot_;
            WbNodeRef get_robot_node(const std::string &robot_name);
            void remove_node(WbNodeRef node);

    };
}
#endif // MAGNI_WEBOTS_NODE_REMOVER_HPP // MAGNI_WEBOTS_NODE_REMOVER_HPP