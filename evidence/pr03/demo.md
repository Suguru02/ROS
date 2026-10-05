# ПР03: воспроизведение и исправление разрыва связи

Окружение: ROS 2 Lyrical, пакет `turtle_bringup` из ПР02, `ROS_DOMAIN_ID=47`.
Перед командами: `source /opt/ros/lyrical/setup.bash`, после сборки — `source install/setup.bash`.

## Порядок опыта

1. Команда `ros2 pkg create --build-type ament_python --node-name patrol patrol --dependencies rclpy geometry_msgs` создала каркас. После реализации `colcon build --symlink-install --packages-select patrol` и `ros2 run patrol patrol` показали `/patrol` в графе (`minimal-nodes.txt`, `minimal-node.log`).

2. Добавлены подписка `/turtle1/pose`, таймер 0,1 с, издатель относительного `cmd_vel` и чистая функция `command_for_pose`. Без запущенного turtlesim `/patrol` публиковал нулевой Twist: `nodes-without-sim.txt`, `command-before-pose.txt`. Это проверка поведения до первой pose.

3. Запущен симулятор `ros2 launch turtle_bringup sim.launch.py`. Команда `ros2 topic type /turtle1/pose` дала `turtlesim_msgs/msg/Pose` в Lyrical (`pose-type.txt`). Нода получила pose и публиковала ненулевой Twist, но без remap связь с turtlesim отсутствовала.

4. После `Ctrl+C` нода запущена с `--ros-args -r cmd_vel:=/turtle1/cmd_vel`. Поза и поток команд проверены повторно; затем нода остановлена. Через 2 с скорость turtlesim стала нулевой (`pose-after-stop.txt`). Исчезновение ноды не является мгновенной командой торможения: симулятор останавливается после прекращения поступления команд.

## Таблица наблюдений

| Проверка | Наблюдение | Файл |
| --- | --- | --- |
| `ros2 node info /patrol` без remap | Подписка `/turtle1/pose`, издатель `/cmd_vel` | `patrol-info-broken.txt` |
| `ros2 topic info /cmd_vel --verbose` | 1 издатель, 0 подписчиков | `topic-broken.txt`, `command-broken.txt` |
| `ros2 topic info /turtle1/cmd_vel --verbose` | 0 издателей, 1 подписчик | `topic-target-broken.txt` |
| Поза до и после ошибочного запуска | `x=5.5444445610`, `y=5.5444445610` без изменения | `pose-broken-before.txt`, `pose-broken-after.txt` |
| `ros2 node info /patrol` после remap | Издатель `/turtle1/cmd_vel` | `patrol-info-fixed.txt` |
| `ros2 topic info /turtle1/cmd_vel --verbose` | 1 издатель, 1 подписчик | `topic-fixed.txt` (в `command-fixed.txt` — содержимое сообщения) |
| Поза после исправления | `x=6.7707562447`, `y=8.3354368210`, движение подтверждено | `pose-fixed.txt` |
| `ros2 topic hz /turtle1/cmd_vel` | ~10,000 Гц на окне 109 интервалов | `command-hz.txt`, `hz-start.txt`, `hz-end.txt`, `command-hz-exit.txt` |
| Список нод после остановки patrol | Только `/turtlesim` | `nodes-after-patrol-stop.txt` |
| Команда перед выходом | Нулевой Twist | `command-before-pose-exit.txt` |
| Инфо о ноде без симулятора | Нода не найдена | `patrol-info-no-sim.txt` |
| Результаты pytest | 6 passed, 1 skipped | `tests.txt` |
| Лог сборки | `Summary: 1 package finished` | `build.txt` |

Частота измерялась в течение 12 с, чтобы накопить более 10 с наблюдений.
Команда `timeout --signal=INT 12s ros2 topic hz /turtle1/cmd_vel` завершилась
кодом 124 по истечении заданного окна (`command-hz-exit.txt`); это ожидаемое
завершение измерения. `tests.txt` содержит результат тестов: 6 passed,
1 skipped. Пропущен созданный генератором шаблонный copyright-тест.

## Быстрое повторение на сдаче

После сборки в терминале A запустить `ros2 launch turtle_bringup sim.launch.py`,
в B запустить `ros2 run patrol patrol`, в C выполнить:

```bash
ros2 node info /patrol
ros2 topic info /cmd_vel --verbose
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic echo /turtle1/pose --once