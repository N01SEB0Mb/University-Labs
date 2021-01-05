#ifndef INTERPOLATION_CONFIG_HPP
#define INTERPOLATION_CONFIG_HPP

namespace config {
  // Розміри вікна
  const int WINDOW_WIDTH = 600;
  const int WINDOW_HEIGHT = 600;


  const int MAX_POINTS = 100;
  const int MAX_COUNT = 6;

  const int WIDTH_AXIS = 2;
  const int WIDTH_FUNCTION = 2;

  const int SIZE_ARROW = 12;
  const int MARK_SIZE = 3;

  const int graphDet = 300;
  const int pointDet = 10;

  const float pointRad = 3.0;
  const float gridColorRatio = 0.4;
  const float zoomDelta = 0.1;

  // Підрахування розмірів графіку
  const float graphWidth = 1.0 - 4.0 * (float) SIZE_ARROW / WINDOW_WIDTH;
  const float graphHeight = 1.0 - 4.0 * (float) SIZE_ARROW / WINDOW_HEIGHT;
}

#endif