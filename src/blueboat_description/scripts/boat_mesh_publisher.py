#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker


class BoatMeshPublisher(Node):

    def __init__(self):
        super().__init__('boat_mesh_publisher')

        self.publisher = self.create_publisher(
            Marker,
            '/boat_mesh',
            10
        )

        self.marker = Marker()

        # Reference frame
        self.marker.header.frame_id = 'map'

        # Marker identification
        self.marker.ns = 'blueboat'
        self.marker.id = 0
        self.marker.type = Marker.MESH_RESOURCE
        self.marker.action = Marker.ADD

        # STL file path
        self.marker.mesh_resource = (
            'file:///root/blueboat_ws/src/'
            'blueboat_description/meshes/blueboat_small.stl'
        )

        # Position
        self.marker.pose.position.x = 0.0
        self.marker.pose.position.y = 0.0
        self.marker.pose.position.z = 0.0

        # Rotate 90 degrees around X axis
        self.marker.pose.orientation.x = math.sin(math.pi / 4.0)
        self.marker.pose.orientation.y = 0.0
        self.marker.pose.orientation.z = 0.0
        self.marker.pose.orientation.w = math.cos(math.pi / 4.0)

        # Scale: reduce STL dimensions by 1000
        self.marker.scale.x = 0.1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1

        # Boat color: blue
        self.marker.color.r = 0.1
        self.marker.color.g = 0.4
        self.marker.color.b = 1.0
        self.marker.color.a = 1.0

        # Publish repeatedly so RViz receives the marker
        self.timer = self.create_timer(
            0.5,
            self.publish_marker
        )

        self.get_logger().info(
            'Blueboat mesh publisher started on /boat_mesh'
        )

    def publish_marker(self):
        self.marker.header.stamp = self.get_clock().now().to_msg()
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
