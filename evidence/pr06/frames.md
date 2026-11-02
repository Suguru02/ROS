# PR06 frames

Все преобразования в обязательной части — фиксированные, публикует их одна нода:
`robot_state_publisher` (топик `/tf_static`, RELIABLE + TRANSIENT_LOCAL).
Меняющихся преобразований нет, поэтому дублирующих владельцев нет.
Размеры и позиции взяты из SDF `models/course_ackermann/model.sdf`.

| Joint | Parent | Child | Type | Expected transform (xyz, rpy) | Publisher owner |
|---|---|---|---|---|---|
| base_to_front_left_knuckle | base_link | front_left_knuckle | fixed | 0.40, 0.31, 0.0 / 0,0,0 | robot_state_publisher |
| base_to_front_right_knuckle | base_link | front_right_knuckle | fixed | 0.40, -0.31, 0.0 / 0,0,0 | robot_state_publisher |
| front_left_knuckle_to_front_left_wheel | front_left_knuckle | front_left_wheel | fixed | 0.0, 0.0, 0.0 / 0,0,0 | robot_state_publisher |
| front_right_knuckle_to_front_right_wheel | front_right_knuckle | front_right_wheel | fixed | 0.0, 0.0, 0.0 / 0,0,0 | robot_state_publisher |
| base_link_to_rear_left_wheel | base_link | rear_left_wheel | fixed | -0.40, 0.31, 0.0 / 0,0,0 | robot_state_publisher |
| base_link_to_rear_right_wheel | base_link | rear_right_wheel | fixed | -0.40, -0.31, 0.0 / 0,0,0 | robot_state_publisher |
| base_to_lidar | base_link | lidar_link | fixed | 0.28, 0.0, 0.38 / 0,0,0 | robot_state_publisher |
| base_to_camera | base_link | camera_link | fixed | 0.28, 0.0, 0.38 / 0,0,0 | robot_state_publisher |
| base_to_imu | base_link | imu_link | fixed | 0.28, 0.0, 0.38 / 0,0,0 | robot_state_publisher |
