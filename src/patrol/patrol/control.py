from turtlesim_msgs.msg import Pose


def command_for_pose(pose: 'Pose | None') -> tuple[float, float]:
    if pose is None:
        return 0.0, 0.0
    return 0.5, 0.3
