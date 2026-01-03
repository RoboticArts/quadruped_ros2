# Copyright 2026, Robert Vasquez Zavaleta.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
import pytest
import subprocess

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, EmitEvent
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.events import Shutdown
import launch_testing
from launch_testing.actions import ReadyToTest
from launch.substitutions import PathJoinSubstitution 
from launch_ros.substitutions import FindPackageShare

@pytest.mark.launch_test
def generate_test_description():

    base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('quadruped_bringup'), 'launch/bringup_complete.launch.py'
            ])
        ),
        launch_arguments={
            'run_rviz': 'false',
            'headless_sim': 'true',
        }.items()
    )

    ready_to_test = ReadyToTest()

    shutdown_after_timer = TimerAction(
        period=30.0,
        actions=[EmitEvent(event=Shutdown(reason="Timeout reached"))]
    )

    ld = LaunchDescription([
        base,
        ready_to_test,
        shutdown_after_timer
    ])

    return ld, {}


import unittest
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class TestLaunchAlive(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = rclpy.create_node("test_node")
        cls.msg_received = False

        def callback(msg):
            cls.msg_received = True
            cls.last_msg = msg

        cls.sub = cls.node.create_subscription(
            Odometry,
            "/odom",
            callback,
            10
        )

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_odom_topic_active(self):
        timeout_sec = 20.0  # Wait until 20 seconds
        start = self.node.get_clock().now()

        while (self.node.get_clock().now() - start).nanoseconds < timeout_sec * 1e9:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if self.msg_received:
                break

        self.assertTrue(
            self.msg_received,
            "No messages for /odom"
        )


@launch_testing.post_shutdown_test()
class TestAfterShutdown(unittest.TestCase):

    # Kill gz sim because it always becomes a zombie
    def test_kill_leftover_gz(self, proc_info):
        subprocess.run(["pkill", "-9", "-f", "gz sim"], check=False)

    def test_no_unexpected_errors(self, proc_info):
        launch_testing.asserts.assertExitCodes(
            proc_info,
            allowable_exit_codes=[0, -15, -9, -2]
        )