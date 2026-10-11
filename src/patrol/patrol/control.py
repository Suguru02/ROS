import math

from turtlesim_msgs.msg import Pose

LINEAR_X_MIN = 0.0
LINEAR_X_MAX = 1.0
ANGULAR_Z_MIN = -1.0
ANGULAR_Z_MAX = 1.0
PUBLISH_HZ_MIN = 1.0
PUBLISH_HZ_MAX = 30.0


def validate_publish_hz(value: float) -> bool:
    """Проверяет, допустима ли частота публикации."""
    if not isinstance(value, (int, float)):
        return False
    if math.isnan(value) or math.isinf(value):
        return False
    return PUBLISH_HZ_MIN <= value <= PUBLISH_HZ_MAX


def validate_linear_speed(value: float) -> bool:
    """Проверяет, допустима ли линейная скорость."""
    if not isinstance(value, (int, float)):
        return False
    if math.isnan(value) or math.isinf(value):
        return False
    return LINEAR_X_MIN <= value <= LINEAR_X_MAX


def validate_turn_rate(value: float) -> bool:
    """Проверяет, допустима ли угловая скорость."""
    if not isinstance(value, (int, float)):
        return False
    if math.isnan(value) or math.isinf(value):
        return False
    return ANGULAR_Z_MIN <= value <= ANGULAR_Z_MAX


def command_for_pose(
    pose: 'Pose | None',
    linear_speed: float = 0.5,
    turn_rate: float = 0.3,
) -> tuple[float, float]:
    """Чистая функция: возвращает (linear_x, angular_z) на основе позы и параметров."""
    if pose is None:
        return 0.0, 0.0

    lx = max(LINEAR_X_MIN, min(linear_speed, LINEAR_X_MAX))
    az = max(ANGULAR_Z_MIN, min(turn_rate, ANGULAR_Z_MAX))
    return lx, az
