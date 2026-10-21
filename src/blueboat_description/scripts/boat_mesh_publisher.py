#!/usr/bin/env python3
"""Boat mesh marker that follows the boat.

Changes from the original:
  * The marker is attached to 'base_link' (it was fixed in 'map' at the
    origin with a constant orientation, so it never moved or turned).
  * The 90 deg rotation about X (STL Y-up -> ROS Z-up) is kept, and a yaw
    offset about Z is composed on top of it. The offset is a live parameter,
    so you can find the right value without restarting:

        ros2 param set /boat_mesh_publisher mesh_yaw_offset_deg 90.0

    Try 0, 90, 180, -90 until the bow of the mesh lines up with the
    /odometry/global arrow. Then make that value the default below.
  * Optional z offset (e.g. to sit the hull at the waterline).
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rcl_interfaces.msg import SetParametersResult
from visualization_msgs.msg import Marker


def mesh_orientation(yaw_offset_deg):
    """Quaternion = Rz(yaw_offset) * Rx(90 deg), returned as (x, y, z, w)."""
    half_yaw = math.radians(yaw_offset_deg) / 2.0
    cz, sz = math.cos(half_yaw), math.sin(half_yaw)
    cx = sx = math.sqrt(0.5)          # Rx(90 deg): sin(45), cos(45)
    return (cz * sx, sz * sx, sz * cx, cz * cx)


class BoatMeshPublisher(Node):

    def __init__(self):
        super().__init__('boat_mesh_publisher')

        self.declare_parameter('mesh_yaw_offset_deg', 90.0)
        self.declare_parameter('mesh_z_offset', 0.0)

        self.publisher = self.create_publisher(Marker, '/boat_mesh', 10)

        self.marker = Marker()

        # Attached to the boat, so it moves and turns with map->odom->base_link.
        self.marker.header.frame_id = 'base_link'

        self.marker.ns = 'blueboat'
        self.marker.id = 0
        self.marker.type = Marker.MESH_RESOURCE
        self.marker.action = Marker.ADD

        self.marker.mesh_resource = (
            'file:///root/blueboat_ws/src/'
            'blueboat_description/meshes/blueboat_small.stl'
        )

        self.marker.pose.position.x = 0.0
        self.marker.pose.position.y = 0.0
        self.marker.pose.position.z = float(self.get_parameter('mesh_z_offset').value)

        self.apply_yaw_offset(float(self.get_parameter('mesh_yaw_offset_deg').value))

        # Scale: reduce STL dimensions by 10 (as in the original)
        self.marker.scale.x = 0.1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1

        self.marker.color.r = 0.1
        self.marker.color.g = 0.4
        self.marker.color.b = 1.0
        self.marker.color.a = 1.0

        self.add_on_set_parameters_callback(self.on_params)

        self.timer = self.create_timer(0.5, self.publish_marker)

        self.get_logger().info('Blueboat mesh publisher started on /boat_mesh (frame base_link)')

    def apply_yaw_offset(self, yaw_deg):
        x, y, z, w = mesh_orientation(yaw_deg)
        self.marker.pose.orientation.x = x
        self.marker.pose.orientation.y = y
        self.marker.pose.orientation.z = z
        self.marker.pose.orientation.w = w

    def on_params(self, params):
        for p in params:
            if p.name == 'mesh_yaw_offset_deg':
                self.apply_yaw_offset(float(p.value))
                self.get_logger().info('mesh_yaw_offset_deg = {}'.format(p.value))
            elif p.name == 'mesh_z_offset':
                self.marker.pose.position.z = float(p.value)
        return SetParametersResult(successful=True)

    def publish_marker(self):
        # Zero stamp = "use the latest available transform".
        self.marker.header.stamp = Time().to_msg()
        self.publisher.publish(self.marker)


def main(args=None):
    rclpy.init(args=args)

    node = BoatMeshPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
