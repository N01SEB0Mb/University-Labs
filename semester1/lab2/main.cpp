#include <GL/gl.h>
#include <GL/freeglut.h>
#include <cmath>
#include <array>
#include "config.hpp"

// Point structure (store X and Y coordinate)
struct Point
{
  float x, y;
  Point() = default;
  Point(float x, float y): x(x), y(y) {};
};

float convertX(const float x)
{
  return 2.0 * (float) x / config::WINDOW_WIDTH;
}

float convertY(const float y)
{
  return 2.0 * (float) y / config::WINDOW_HEIGHT;
};

float pointAngle = 0.0;
float x, y, angle = 150.0 + config::TRG_OFFSET_ANGLE * 180.0 / M_PI;
float k, b, xDelta, aDelta;

// Triangle (array of 3 points)
std::array<Point, 3> trg = {
        {
          Point(config::TRG_HEIGHT * cos(config::TRG_OFFSET_ANGLE + 7.0 / 6.0 * M_PI), // 1-st point X
                config::TRG_HEIGHT * sin(config::TRG_OFFSET_ANGLE + 7.0 / 6.0 * M_PI)), // 1-st point Y
          Point(config::TRG_HEIGHT * cos(config::TRG_OFFSET_ANGLE + 0.5 * M_PI), // 2-nd point X
                config::TRG_HEIGHT * sin(config::TRG_OFFSET_ANGLE + 0.5 * M_PI)), // 2-nd point Y
          Point(config::TRG_HEIGHT * cos(config::TRG_OFFSET_ANGLE - M_PI / 6.0), // 3-rd point X
                config::TRG_HEIGHT * sin(config::TRG_OFFSET_ANGLE - M_PI / 6.0)) // 3-rd point Y
        }
};

std::array<std::array<Point, 2>, 3> trajectory1 = {
        {
          {
            Point(trg[0].x + config::RADIUS_CIRCLE * cos(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE),
                  trg[0].y + config::RADIUS_CIRCLE * sin(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE)),
            Point(trg[1].x + config::RADIUS_CIRCLE * cos(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE),
                  trg[1].y + config::RADIUS_CIRCLE * sin(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE))
          },
          {
            Point(trg[1].x + config::RADIUS_CIRCLE * cos(M_PI / 6.0 + config::TRG_OFFSET_ANGLE),
                  trg[1].y + config::RADIUS_CIRCLE * sin(M_PI / 6.0 + config::TRG_OFFSET_ANGLE)),
            Point(trg[2].x + config::RADIUS_CIRCLE * cos(M_PI / 6.0 + config::TRG_OFFSET_ANGLE),
                  trg[2].y + config::RADIUS_CIRCLE * sin(M_PI / 6.0 + config::TRG_OFFSET_ANGLE))
          },
          {
            Point(trg[2].x + config::RADIUS_CIRCLE * cos(M_PI / -2.0 + config::TRG_OFFSET_ANGLE),
                  trg[2].y + config::RADIUS_CIRCLE * sin(M_PI / -2.0 + config::TRG_OFFSET_ANGLE)),
            Point(trg[0].x + config::RADIUS_CIRCLE * cos(M_PI / -2.0 + config::TRG_OFFSET_ANGLE),
                  trg[0].y + config::RADIUS_CIRCLE * sin(M_PI / -2.0 + config::TRG_OFFSET_ANGLE))
          }
        }
};

std::array<Point, 3> trajectory0 = {
        {
          Point(trg[0].x + 2 * config::RADIUS_CIRCLE * cos(M_PI / 6.0 + config::TRG_OFFSET_ANGLE),
                trg[0].y + 2 * config::RADIUS_CIRCLE * sin(M_PI / 6.0 + config::TRG_OFFSET_ANGLE)),
          Point(trg[1].x + 2 * config::RADIUS_CIRCLE * cos(1.5 * M_PI + config::TRG_OFFSET_ANGLE),
                trg[1].y + 2 * config::RADIUS_CIRCLE * sin(1.5 * M_PI + config::TRG_OFFSET_ANGLE)),
          Point(trg[2].x + 2 * config::RADIUS_CIRCLE * cos(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE),
                trg[2].y + 2 * config::RADIUS_CIRCLE * sin(5.0 / 6.0 * M_PI + config::TRG_OFFSET_ANGLE))
        }
};

// Get length using X delta and K ratio
float length(const float deltaX, const float ratioK)
{
  float deltaY = deltaX * ratioK;
  return (float) sqrt(pow(deltaX, 2) + pow(deltaY, 2));
}

// Draws triangle
void glTrg()
{
  glBegin(GL_LINE_LOOP);
  glColor3f(1, 1, 1);

  glVertex2f(convertX(trg[0].x), convertY(trg[0].y));
  glVertex2f(convertX(trg[1].x), convertY(trg[1].y));
  glVertex2f(convertX(trg[2].x), convertY(trg[2].y));

  glEnd();
}

// Draw circle
void glCircle(const float x, const float y, const float r, const bool fill = false, const bool black = false)
{
  if (fill)
    glBegin(GL_POLYGON);
  else
    glBegin(GL_LINE_LOOP);

  float a_del = 2 * M_PI / config::DETAILING_CIRCLE;

  if (black)
    glColor3f(0, 0, 0);
  else
    glColor3f(1, 1, 1);

  for (int point = 0; point < config::DETAILING_CIRCLE; point++)
  {
    glVertex2f(convertX(x + r * cos(a_del * point)), convertY(y + r * sin(a_del * point)));
  }

  glEnd();
}

void display()
{
  glTrg();

  for (int number = 0; number < 3; number++)
  {
    if (config::IS_OUTSIDE)
    {
      k = (trajectory1[number][0].y - trajectory1[number][1].y) / (trajectory1[number][0].x - trajectory1[number][1].x);
      b = trajectory1[number][0].y - trajectory1[number][0].x * k;
      xDelta = (trajectory1[number][1].x - trajectory1[number][0].x) / config::DETAILING_PATH;

      for (int step = 0; step <= config::DETAILING_PATH; step++)
      {
        if (config::SHOW_CIRCLE)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        x = trajectory1[number][0].x + step * xDelta;
        y = x * k + b;
        pointAngle -= 180.0 * length(xDelta, k) / (M_PI * config::RADIUS_CIRCLE);

        glTrg();

        if (config::SHOW_CIRCLE)
          glCircle(x, y, config::RADIUS_CIRCLE, false);

        glCircle(x + config::RADIUS_CIRCLE * cos(pointAngle / 180.0 * M_PI),
                 y + config::RADIUS_CIRCLE * sin(pointAngle / 180.0 * M_PI), config::RADIUS_DOT, true, false);
        glutSwapBuffers();
      }

      aDelta = -120.0 / config::DETAILING_SPIN;
      angle = angle - aDelta;

      for (int step = 0; step <= config::DETAILING_SPIN; step++)
      {
        if (config::SHOW_CIRCLE)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        angle += aDelta;
        x = trg[(number + 1) % 3].x + config::RADIUS_CIRCLE * cos(angle / 180.0 * M_PI);
        y = trg[(number + 1) % 3].y + config::RADIUS_CIRCLE * sin(angle / 180.0 * M_PI);
        pointAngle += aDelta;

        glTrg();

        if (config::SHOW_CIRCLE)
          glCircle(x, y, config::RADIUS_CIRCLE, false);

        glCircle(x + config::RADIUS_CIRCLE * cos(pointAngle / 180.0 * M_PI),
                 y + config::RADIUS_CIRCLE * sin(pointAngle / 180.0 * M_PI), config::RADIUS_DOT, true, false);
        glutSwapBuffers();
      }
    }
    else
    {
      k = (trajectory0[number].y - trajectory0[(number + 1) % 3].y) / (trajectory0[number].x - trajectory0[(number + 1) % 3].x);
      b = trajectory0[number].y - trajectory0[number].x * k;
      xDelta = (trajectory0[(number + 1) % 3].x - trajectory0[number].x) / config::DETAILING_PATH;

      for (int step = 0; step <= config::DETAILING_PATH; step++)
      {
        x = trajectory0[number].x + step * xDelta;
        y = x * k + b;
        pointAngle += 180 * length(xDelta, k) / (M_PI * config::RADIUS_CIRCLE);

        if (config::SHOW_CIRCLE)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        glTrg();

        if (config::SHOW_CIRCLE)
          glCircle(x, y, config::RADIUS_CIRCLE, false);

        glCircle(x + config::RADIUS_CIRCLE * cos(pointAngle / 180.0 * M_PI), y + config::RADIUS_CIRCLE * sin(pointAngle / 180.0 * M_PI), config::RADIUS_DOT, true);
        glutSwapBuffers();
      }
    }
  }
}

int main(int argc, char** argv)
{

  glutInit(&argc, argv);
  glutSetOption(GLUT_MULTISAMPLE, 4);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE);
  glutInitWindowSize(config::WINDOW_WIDTH, config::WINDOW_HEIGHT);
  glutCreateWindow("Lab 2");
  glutPositionWindow(688 - config::WINDOW_WIDTH / 2, 384 - config::WINDOW_HEIGHT / 2);
  glutDisplayFunc(display);
  glutIdleFunc(display);

  glutMainLoop();
}