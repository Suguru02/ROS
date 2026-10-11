# ПР04 — Параметризуем движение patrol

## Окружение

- ROS 2: **Lyrical** (Python 3.14, `/usr/bin/python3`)
- Workspace: `/work`
- Пакет: `patrol` (`ament_python`, `rclpy`)
- Нода: `/patrol`
- Топик команды после remap: `/turtle1/cmd_vel` (`geometry_msgs/msg/Twist`)
- Запуск симулятора: `ros2 launch turtle_bringup sim.launch.py` (лог — `sim.log`)
- Запуск ноды: `ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel` (лог ноды — `patrol.log`)

## Параметры ноды

| Параметр | Default | Допустимый диапазон |
|---|---:|---:|
| `linear_speed` | 0.5 | [0.0, 1.0] |
| `turn_rate` | 0.3 | [-1.0, 1.0] |
| `publish_hz` | 10.0 | [1.0, 30.0] |

Список параметров ноды: `param-list.txt`. Значения по умолчанию: `param-get-defaults.txt`.

Валидация выполняется в `on_parameters_change` **до** изменения активного состояния: недопустимое значение возвращает `SetParametersResult(successful=False)`, и таймер не трогается. При допустимой смене `publish_hz` старый таймер останавливается через `cancel()` и создаётся новый с периодом `1 / publish_hz`; двух одновременных таймеров не остаётся (момент пересоздания виден в `patrol.log`).

## Стадия «Собрать»: рабочие параметры

Поток команд на частоте по умолчанию: `timeout 5 ros2 topic hz /turtle1/cmd_vel` даёт ≈ 10 Гц (`hz-10.txt`). Черепаха реально движется: позы с интервалом 3 с различаются (`pose-before.txt`, `pose-after.txt`).

Смена частоты 10 → 5 на живой ноде: `ros2 param set /patrol publish_hz 5.0` — `Set parameter successful`, поток перестроился на ≈ 5 Гц (`param-set-5.txt`, `hz-5.txt`).

Смена скорости и поворота на живой ноде: `ros2 param set /patrol linear_speed 0.8` и `ros2 param set /patrol turn_rate -0.5` приняты, новые значения видны в сообщении команды (`param-set-speed.txt`, `param-set-turn.txt`).

## Отклонение недопустимых значений (валидация включена)

- `ros2 param set /patrol publish_hz 0.0` — отклонено, значение и поток не изменились (`param-reject-0.txt`, `hz-after-reject.txt`).
- `ros2 param set /patrol publish_hz -2.0` — отклонено (`param-reject-neg.txt`).
- `ros2 param set /patrol publish_hz nan` — отклонено (`param-reject-nan.txt`).
- `ros2 param set /patrol linear_speed 2.0` — отклонено (`param-reject-speed.txt`).

Во всех случаях `ros2 param get` возвращает прежнее значение: проверка входа выполняется до изменения активного состояния.

## Стадия «Сломать»: воспроизводимый отказ без валидации

Проверка была временно отключена в рабочей копии: строка `if not validate_publish_hz(param.value):` заменена на `if False:`, пакет пересобран. После этого:

`ros2 param set /patrol publish_hz 0.0` — нода приняла ноль и погибла при пересоздании таймера: `ZeroDivisionError: division by zero` на строке `self.create_timer(1.0 / new_hz, ...)`, процесс завершился с кодом 1 (`defect-crash.txt`). Сам запрос установки параметра при этом завис: клиент не получил ответа, потому что нода умерла посередине обработки (`defect-param-set.txt`). После краша нода отсутствует в графе (`defect-node-list.txt`).

Отказ воспроизводим: отключённая валидация + `publish_hz 0.0` всегда дают `ZeroDivisionError` и гибель ноды.

## Стадия «Доказать»: ноль отклонён, старая частота сохранена

Валидация возвращена в исходное состояние, пакет пересобран, нода перезапущена.

- `ros2 param set /patrol publish_hz 5.0` — принято (`proof-set-5.txt`).
- `ros2 param set /patrol publish_hz 0.0` — отклонено: `Setting parameter failed`; `ros2 param get` возвращает 5.0 (`proof-reject-0-restored.txt`).
- Поток не изменился: ≈ 5 Гц, без «удвоения» от двух таймеров (`proof-hz-5-restored.txt`).

Вывод: ноль отклоняется до изменения таймера, активное состояние сохраняется, допустимое значение реально меняет поток. Дефект устранён.

## Тесты чистой функции

`python3 -m pytest src/patrol/test -q` — вывод в `tests.txt`. Покрыты: обычный переход 10→5 Гц, ноль, отрицательное значение, NaN, бесконечность и выход за диапазоны скорости/поворота.

## Готовый сервис /clear и готовый action /turtle1/rotate_absolute

- `ros2 service call /clear std_srvs/srv/Empty` — вывод в `clear.txt`; сервис очищает след черепахи.
- `ros2 action list -t` — вывод в `action-list.txt`; виден `/turtle1/rotate_absolute` с типом `turtlesim/action/RotateAbsolute`.

Отличие запроса и цели: сервис `/clear` работает по схеме «запрос—ответ»: клиент вызывает операцию и сразу получает один ответ об успехе. Action `/turtle1/rotate_absolute` — это цель долгосрочной задачи: сервер принимает goal, шлёт feedback во время выполнения, возвращает итоговый result и поддерживает отмену цели.
