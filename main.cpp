#include <iostream>
#include <cmath>
#include <optional>
#include <vector>
#include <matplot/matplot.h>

/**
 * Рассчитывает скорость воздуха в канале (от числа оборотов)
 * @param rp_m количество оборотов в минуту
 * @param cyl_vol объем цилиндра
 * @param ch_sq площадь седла канала
 * @param vlv_count количество клапанов на цилиндр: 2 или 4
 * @return скорость воздуха в канале
 */
double calc_speed(const int rp_m, const double cyl_vol, const double ch_sq, int vlv_count) {
    const double valve_count = vlv_count;
    const double rpm = rp_m;
    const double rp_s = rpm / 60; // оборотов в секунду
    const double entrance_time = 1 / (2 * rp_s); // сколько секунд занимает такт впуска [с]
    const double rate = cyl_vol / entrance_time; // расход воздуха в секунду [мм^3 / с]
    return rate / (1000 * ch_sq * (valve_count / 2)); // скорость (м/сек)
}

double calculate_channel_air_speed(
    float piston_diameter,
    float piston_stroke,
    float channel_diameter,
    int valves_count,
    const std::optional<int> fixed = std::nullopt,
    const int *chart = nullptr
) {
    const double cylinder_volume = std::numbers::pi * pow(piston_diameter, 2) / 4 * piston_stroke; // мм^3
    const double channel_square = std::numbers::pi * pow(channel_diameter, 2) / 4; // мм^2

    if (chart == nullptr) {
        constexpr int default_chart[2] = {1000, 8000};
        chart = default_chart;
    }

    if (!fixed.has_value()) {
        std::vector<int> x_axis;
        std::vector<double> y_axis;
        for (int rpm = chart[0]; rpm <= chart[1]; rpm += 100) {
            x_axis.push_back(rpm);
            y_axis.push_back(calc_speed(rpm, cylinder_volume, channel_square, valves_count));
        }
        return 0.0;
    } else {
        return calc_speed(fixed.value(), cylinder_volume, channel_square, valves_count);
    }
}

int main() {
    auto fixed_lvs = calculate_channel_air_speed(82.0, 84, 27.5, 4, 4000);
    std::cout << fixed_lvs << std::endl;


    return 0;
}
