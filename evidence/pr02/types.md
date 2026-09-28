cd /work

cat > evidence/pr02/types.md << 'EOF'
# Типы сообщений ПР02

| Топик | Тип | Назначение |
|---|---|---|
| `/turtle1/cmd_vel` | `geometry_msgs/msg/Twist` | Команда скорости для `/turtlesim` |
| `/turtle1/pose` | `turtlesim_msgs/msg/Pose` | Положение и текущие скорости черепахи |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Намеренно ошибочное полное имя в опыте |

Источники: `ros2 topic type /turtle1/pose` ([pose-type.txt](pose-type.txt)),
`ros2 topic info ... --verbose` ([topic-fixed.txt](topic-fixed.txt)),
`ros2 interface show geometry_msgs/msg/Twist` ([twist-interface.txt](twist-interface.txt)).
В Jazzy интерфейс позы называется `turtlesim/msg/Pose`.

`Twist` содержит два вектора `linear` и `angular`, каждый с полями `x`, `y`, `z` типа `float64`.
Для плоского turtlesim используем `linear.x=1.0` (движение вперёд) и `angular.z=0.5` (поворот против часовой стрелки). Остальные компоненты нулевые.
`Twist` не содержит `timestamp`/`frame_id` и не задаёт целевую позицию.

`Pose` включает `x`/`y` — координаты на плоскости, `theta` — угол в радианах,
`linear_velocity`/`angular_velocity` — текущие скорости.
Изменение x/y/theta доказывает движение; нулевые скорости после прекращения
публикаций подтверждают остановку. Одной видимости топика для этого недостаточно.
EOF