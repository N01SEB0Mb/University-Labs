#ifndef TRAJECTORY_CONFIG_HPP
#define TRAJECTORY_CONFIG_HPP

#include <cmath>

namespace config {
  // Розміри вікна
  const int WINDOW_WIDTH = 600;
  const int WINDOW_HEIGHT = 600;

  // Параметри трикутника
  const float TRG_SIDE = 300; // Довжина сторони трикутника
  const float TRG_HEIGHT = config::TRG_SIDE / sqrt(3); // Довжина висоти трикутника (a * 2 / (sqrt(3) / 2))
  const float TRG_OFFSET_ANGLE = (60.0) / 180.0 * M_PI; // Кут повороту трикутника (в дужках)

  // Параметри кола
  const float RADIUS_CIRCLE = 35; // Радіус кола
  const float RADIUS_DOT = 2; // Радіус точки

  // Деталізація руху (на скільки відрізків розбивається шлях)
  const float DETAILING_PATH = 1000; // Деталізація руху по лінії
  const float DETAILING_SPIN = DETAILING_PATH * (2.0 / 3.0 * M_PI * RADIUS_CIRCLE / TRG_SIDE); // Деталізація руху по кругу
  const float DETAILING_CIRCLE = 30; // Деталізація кола

  // Параметри виду
  bool IS_OUTSIDE = false; // Рух ззовні (true) / всередині (false)
  bool SHOW_CIRCLE = false; // Показувати коло з точкою (true) / траекторію точки (false)
}

#endif
