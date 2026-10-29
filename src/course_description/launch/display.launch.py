"""Launch robot_state_publisher for PR06."""

from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Start robot_state_publisher with expanded Xacro."""
    xacro_file = PathJoinSubstitution([
        FindPackageShare('course_description'),
        'urdf',
        'vehicle.urdf.xacro',
    ])

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher_node,
    ])
