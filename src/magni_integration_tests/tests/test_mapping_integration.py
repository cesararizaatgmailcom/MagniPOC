import os
import time
import unittest

import launch
import launch.actions
import launch_ros.actions
import launch_testing
import launch_testing.actions
import rclpy
import rclpy.node
from ament_index_python.packages import get_package_share_directory

from nav_msgs.msg import OccupancyGrid
from cartographer_ros_msgs.srv import WriteState


def generate_test_description():
    pkg_webots = get_package_share_directory('magni_webots')
    pkg_mapping = get_package_share_directory('magni_mapping')
    pkg_tests = get_package_share_directory('magni_integration_tests')

    # Resource bag (should be provided in resources/drive.bag)
    bagfile = os.path.join(pkg_tests, 'resources', 'drive.bag')

    webots_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(pkg_webots, 'launch', 'magni_spawn.launch.py')
        )
    )

    mapping_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(pkg_mapping, 'launch', 'mapping.launch.py')
        ), launch_arguments={'use_sim_time': 'true'}.items()
    )

    bag_play = launch.actions.ExecuteProcess(
        cmd=['ros2', 'bag', 'play', bagfile, '--clock'],
        output='screen',
    )

    # wait a bit and then signal ReadyToTest
    ready_timer = launch.actions.TimerAction(period=5.0, actions=[launch_testing.actions.ReadyToTest()])

    ld = launch.LaunchDescription([
        webots_launch,
        mapping_launch,
        bag_play,
        ready_timer,
    ])

    return ld, {'bagfile': bagfile}


class TestMappingIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('test_mapping_integration')

    def tearDown(self):
        self.node.destroy_node()

    def test_map_topic_published(self):
        # Skip test if bagfile not provided
        bagfile = os.environ.get('BAGFILE')
        if bagfile is None:
            # The launch description passes bagfile via the test context binding; retrieve via environment fallback
            bagfile = os.path.join(get_package_share_directory('magni_integration_tests'), 'resources', 'drive.bag')

        if not os.path.exists(bagfile):
            raise unittest.SkipTest('No bagfile present in resources — place a rosbag at tests/resources/drive.bag to run this test')

        msgs = []

        sub = self.node.create_subscription(OccupancyGrid, '/map', lambda msg: msgs.append(msg), 10)
        try:
            # Wait up to 30s for a /map message
            deadline = time.time() + 30.0
            while time.time() < deadline and not msgs:
                rclpy.spin_once(self.node, timeout_sec=1.0)
            assert len(msgs) > 0, 'No /map message received within timeout'
        finally:
            self.node.destroy_subscription(sub)

    def test_write_state_service(self):
        # Skip if service unavailable or bag not present
        bagfile = os.path.join(get_package_share_directory('magni_integration_tests'), 'resources', 'drive.bag')
        if not os.path.exists(bagfile):
            raise unittest.SkipTest('No bagfile present in resources — skipping write_state test')

        client = self.node.create_client(WriteState, '/write_state')
        if not client.wait_for_service(timeout_sec=20.0):
            self.skipTest('WriteState service not available')

        filename = os.path.join(os.getcwd(), 'integration_map.pbstream')
        req = WriteState.Request()
        req.filename = filename

        fut = client.call_async(req)
        # Wait for service result (up to 10s)
        deadline = time.time() + 10.0
        while time.time() < deadline and not fut.done():
            rclpy.spin_once(self.node, timeout_sec=0.5)

        if not fut.done():
            self.fail('write_state service call did not finish')

        # Give a brief moment for file to be created
        time.sleep(1.0)
        assert os.path.exists(filename) and os.path.getsize(filename) > 0, 'pbstream file missing or empty'


@launch_testing.post_shutdown_test()
class TestMappingPostShutdown(unittest.TestCase):
    def test_exit_codes(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
