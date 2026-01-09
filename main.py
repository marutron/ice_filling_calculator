from math import pi
from typing import Optional
import matplotlib.pyplot as plt


def calculate_channel_air_speed(
        piston_diameter: float,
        piston_stroke: float,
        channel_diameter: float,
        valves_count: int = 4,
        fixed: Optional[float] = None,
        chart: Optional[tuple] = (1000, 8000),
):
    """
    Рассчитывает скорость потока в канале (седле, без учёта ножки клапана)
    :param piston_diameter: диаметр поршня
    :param piston_stroke: ход поршня
    :param channel_diameter: диаметр канала, в котором измеряем скорость (например диаметр седла)
    :param valves_count: количество клапанов на цилиндр
    :param fixed: расчет для конкретных оборотов
    :param chart: диапазон оборотов для нанесения на график. Если None - график не рисуем
    :return:
    """

    def calc_speed(rp_m, cyl_vol, ch_sq, vlv_count) -> float:
        rp_s = rp_m / 60  # оборотов в секунду
        entrance_time = 1 / (2 * rp_s)  # сколько секунд занимает такт впуска [с]
        rate = cyl_vol / entrance_time  # расход воздуха в секунду [мм^3 / с]
        return rate / (1000 * ch_sq * (vlv_count / 2))  # скорость (м/сек)

    cylinder_volume = pi * piston_diameter ** 2 / 4 * piston_stroke  # мм^3
    channel_square = pi * channel_diameter ** 2 / 4  # мм^2

    match fixed:
        case None:
            x_axis = []
            y_axys = []
            for rpm in range(chart[0], chart[1] + 100, 100):
                x_axis.append(rpm)
                y_axys.append(
                    calc_speed(rpm, cylinder_volume, channel_square, valves_count)
                )

            plt.plot(x_axis, y_axys, label="Скорость воздуха в канале")
            plt.legend()
            plt.xlabel('обороты / мин.')
            plt.ylabel('м / с')
            plt.axhline(y=70, color="green", linestyle="--", label="Хорошая наполняемость")
            plt.axhline(y=90, color="green", linestyle="--", label="Хорошая наполняемость")
            plt.axhline(y=140, color="red", linestyle="--", label="Приемлемая наполняемость")
            plt.grid(visible=True)
            plt.show()
            return None
        case some:
            return calc_speed(some, cylinder_volume, channel_square, valves_count)


if __name__ == '__main__':
    # v2106 = calculate_channel_air_speed(79.8, 80, 33, valves_count=2)
    lvs = calculate_channel_air_speed(82.0, 84, 27.5, valves_count=4)
    pass
