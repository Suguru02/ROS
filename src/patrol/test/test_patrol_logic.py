import math

from patrol.control import command_for_pose


def test_missing_pose_returns_zero():
    linear, angular = command_for_pose(None)
    assert linear == 0.0
    assert angular == 0.0


def test_normal_pose_returns_command():
    class MockPose:
        pass

    linear, angular = command_for_pose(MockPose())
    assert math.isclose(linear, 0.5, abs_tol=1e-9)
    assert math.isclose(angular, 0.3, abs_tol=1e-9)


def test_command_within_limits():
    class MockPose:
        pass

    linear, angular = command_for_pose(MockPose())

    LINEAR_X_MIN = 0.0
    LINEAR_X_MAX = 0.5
    ANGULAR_Z_MIN = -1.0
    ANGULAR_Z_MAX = 1.0

    assert LINEAR_X_MIN <= linear <= LINEAR_X_MAX
    assert ANGULAR_Z_MIN <= angular <= ANGULAR_Z_MAX
