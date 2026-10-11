import math

from geometry_msgs.msg import Twist
from patrol.control import (
    command_for_pose,
    validate_linear_speed,
    validate_publish_hz,
    validate_turn_rate,
)
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.parameter import Parameter
from turtlesim_msgs.msg import Pose


class Patrol(Node):
    """Нода с параметрами: linear_speed, turn_rate, publish_hz."""

    def __init__(self) -> None:
        super().__init__('patrol')

        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)

        self.latest_pose: Pose | None = None
        self.pose_subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.on_pose, 10)
        self.command_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        hz = self.get_parameter('publish_hz').value
        self.timer = self.create_timer(1.0 / hz, self.on_timer)

        self.add_on_set_parameters_callback(self.on_parameters_change)

    def on_pose(self, message: Pose) -> None:
        self.latest_pose = message

    def on_timer(self) -> None:
        linear_speed = self.get_parameter('linear_speed').value
        turn_rate = self.get_parameter('turn_rate').value
        lx, az = command_for_pose(self.latest_pose, linear_speed, turn_rate)
        command = Twist()
        command.linear.x = lx
        command.angular.z = az
        self.command_publisher.publish(command)

    def on_parameters_change(
        self, params: list[Parameter],
    ) -> 'rclpy.parameter.SetParametersResult':
        from rcl_interfaces.msg import SetParametersResult
        result = SetParametersResult(successful=True)

        for param in params:
            if param.name == 'publish_hz':
                if not validate_publish_hz(param.value):
                    result.successful = False
                    result.reason = (
                        f'publish_hz={param.value} вне диапазона '
                        f'[{1.0}, {30.0}] или не является конечным числом'
                    )
                    self.get_logger().error(result.reason)
                    return result

            elif param.name == 'linear_speed':
                if not validate_linear_speed(param.value):
                    result.successful = False
                    result.reason = (
                        f'linear_speed={param.value} вне диапазона '
                        f'[{0.0}, {1.0}] или не является конечным числом'
                    )
                    self.get_logger().error(result.reason)
                    return result

            elif param.name == 'turn_rate':
                if not validate_turn_rate(param.value):
                    result.successful = False
                    result.reason = (
                        f'turn_rate={param.value} вне диапазона '
                        f'[{-1.0}, {1.0}] или не является конечным числом'
                    )
                    self.get_logger().error(result.reason)
                    return result

        for param in params:
            if param.name == 'publish_hz' and result.successful:
                old_hz = self.get_parameter('publish_hz').value
                new_hz = param.value
                if not math.isclose(old_hz, new_hz):
                    self.timer.cancel()
                    self.timer = self.create_timer(1.0 / new_hz, self.on_timer)
                    self.get_logger().info(
                        f'Таймер пересоздан: {old_hz} Гц -> {new_hz} Гц')

        return result


def main(args=None):
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
