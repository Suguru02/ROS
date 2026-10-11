import math

from patrol.control import (
    command_for_pose,
    validate_linear_speed,
    validate_publish_hz,
    validate_turn_rate,
)


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


def test_custom_parameters():
    class MockPose:
        pass

    linear, angular = command_for_pose(MockPose(), 0.8, -0.5)
    assert math.isclose(linear, 0.8, abs_tol=1e-9)
    assert math.isclose(angular, -0.5, abs_tol=1e-9)


def test_clamp_linear_speed():
    class MockPose:
        pass

    linear, _ = command_for_pose(MockPose(), 2.0, 0.3)
    assert linear == 1.0

    linear, _ = command_for_pose(MockPose(), -1.0, 0.3)
    assert linear == 0.0


def test_clamp_turn_rate():
    class MockPose:
        pass

    _, angular = command_for_pose(MockPose(), 0.5, 2.0)
    assert angular == 1.0

    _, angular = command_for_pose(MockPose(), 0.5, -2.0)
    assert angular == -1.0


def test_validate_publish_hz_valid():
    assert validate_publish_hz(10.0) is True
    assert validate_publish_hz(1.0) is True
    assert validate_publish_hz(30.0) is True
    assert validate_publish_hz(5.0) is True


def test_validate_publish_hz_zero():
    assert validate_publish_hz(0.0) is False


def test_validate_publish_hz_negative():
    assert validate_publish_hz(-5.0) is False


def test_validate_publish_hz_nan():
    assert validate_publish_hz(float('nan')) is False


def test_validate_publish_hz_inf():
    assert validate_publish_hz(float('inf')) is False


def test_validate_publish_hz_above_max():
    assert validate_publish_hz(31.0) is False


def test_validate_linear_speed_valid():
    assert validate_linear_speed(0.5) is True
    assert validate_linear_speed(0.0) is True
    assert validate_linear_speed(1.0) is True


def test_validate_linear_speed_invalid():
    assert validate_linear_speed(-0.1) is False
    assert validate_linear_speed(1.1) is False
    assert validate_linear_speed(float('nan')) is False


def test_validate_turn_rate_valid():
    assert validate_turn_rate(0.3) is True
    assert validate_turn_rate(-1.0) is True
    assert validate_turn_rate(1.0) is True


def test_validate_turn_rate_invalid():
    assert validate_turn_rate(-1.1) is False
    assert validate_turn_rate(1.1) is False
    assert validate_turn_rate(float('nan')) is False
