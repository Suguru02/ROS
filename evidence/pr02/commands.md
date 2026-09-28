# Команды и наблюдения ПР02

Опыт проведён в Docker-контейнере с ROS 2 Lyrical, `ROS_DOMAIN_ID=46`.
Старые процессы turtlesim и teleop были остановлены перед началом. Среда подключалась в каждом терминале.

## Терминал и workspace

Базовые команды Linux, использованные для подготовки и проверки:

| Команда | Назначение | Полученный результат |
|---|---|---|
| `pwd` | Показать текущий каталог | `/work`, корень репозитория и workspace |
| `ls -a` | Показать обычные и скрытые файлы | Видны `.git`, `src`, `evidence`, `build`, `install`, `log` |
| `mkdir -p evidence/pr02` | Создать вложенные каталоги | Успешное создание, повторный запуск не даёт ошибки |

Вывод этих команд и сведения о среде сохранены в [linux.txt](linux.txt).
`ros2 pkg prefix turtlesim` вернул `/opt/ros/lyrical`, а после сборки `ros2 pkg prefix turtle_bringup` вернул `/work/install/turtle_bringup` ([package-prefix.txt](package-prefix.txt)).

`>` заменяет содержимое файла стандартным выводом; `2>&1` направляет stderr туда же. `|` передаёт stdout следующей программе. В команде `colcon build 2>&1 | tee evidence/pr02/build.txt` программа `tee` одновременно показывает и сохраняет вывод. `set -o pipefail` сохраняет ненулевой статус `colcon` в конвейере. `source setup.bash` изменяет **текущую оболочку**, а не создаёт новый процесс.

## Пакет и launch

Пакет `turtle_bringup` был взят из шаблона курса. Сборка прошла успешно как в базовом виде ([build-empty.txt](build-empty.txt)), так и после добавления `launch/sim.launch.py` и настройки `data_files` в `setup.py` ([build.txt](build.txt)).

Установленный файл найден по пути `/work/install/turtle_bringup/share/turtle_bringup/launch/sim.launch.py`. Проверка синтаксиса `python3 -m py_compile src/turtle_bringup/launch/sim.launch.py` завершилась с кодом 0.

После `source install/setup.bash` команда `ros2 launch turtle_bringup sim.launch.py` запустила ноду `/turtlesim` ([nodes-running.txt](nodes-running.txt)). Нажатие `Ctrl+C` корректно завершило launch и ноду: [nodes-stopped.txt](nodes-stopped.txt) пуст. Для основного опыта launch был запущен вновь ([launch-experiment.txt](launch-experiment.txt)).

## Эксперимент с топиками: сбой и исправление

Teleop не запускался. `ros2 topic type /turtle1/pose` вернул `turtlesim_msgs/msg/Pose`.
Исходная поза: `x=5.544445, y=5.544445, theta=0.000000`.

Отправка одиночной правильной команды:

ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'

Ожидалось движение вперёд с поворотом. После одной публикации получено: `x=6.509309, y=5.796991, theta=0.504000`. Координаты и угол изменились. См. [pose-before.txt](pose-before.txt) и [pose-working.txt](pose-working.txt). Позднее скорость снова стала нулевой, так как единичная команда не задаёт постоянное движение.

После остановки черепахи исходная поза для сравнения была `x=6.509309, y=5.796991, theta=0.504000` ([pose-resting.txt](pose-resting.txt)). Был запущен непрерывный издатель в неверный топик:


ros2 topic pub --rate 1 --wait-matching-subscriptions 0 /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'

`ros2 topic info /cmd_vel --verbose` показал **1 издателя и 0 подписчиков** ([topic-broken.txt](topic-broken.txt)). На ожидаемом `/turtle1/cmd_vel` были **0 издателей и 1 подписчик** turtlesim ([topic-target-before-fix.txt](topic-target-before-fix.txt)). Оба топика имели тип `geometry_msgs/msg/Twist`, но полные имена различались. Повторный `ros2 topic echo /turtle1/pose --once` оставил все значения прежними ([pose-broken.txt](pose-broken.txt)).

Издатель был остановлен через `Ctrl+C`. В команде публикации изменено **только имя** на `/turtle1/cmd_vel`:
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'

Теперь `ros2 topic info /turtle1/cmd_vel --verbose` показал **1 издателя и 1 подписчика** ([topic-fixed.txt](topic-fixed.txt)). Новая поза стала `x=7.496103, y=7.944133, theta=1.768000` ([pose-fixed.txt](pose-fixed.txt)).

После остановки издателя и launch фоновых ROS-процессов не осталось ([nodes-final.txt](nodes-final.txt)).

**Вывод:** Причина дефекта — несовпадение **полного имени топика**, а не ошибка типа, сборки или домена. Наличие издателя в графе само по себе не доказывает доставку сообщений конкретному подписчику, если их имена не совпадают символ в символ.