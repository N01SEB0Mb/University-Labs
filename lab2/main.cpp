#include <GL/gl.h>
#include <GL/freeglut.h>
#include <cmath>
#include <array>

using namespace std;

struct Point
{
  float x, y;
  Point() = default;
  Point(float x, float y): x(x), y(y) {};
};

const int width = 600, height = 600;
const float a = 400; // Сторона трикутника
const float trg_a = (60.0) / 180.0 * M_PI; // Кут повороту трикутника (в дужках)
const float r = 100; // Радіус кола
const float r_t = 1; // Радіус точки
const float a_det = 300; // Деталізація руху по лінії
const float r_det = a_det * (2.0 / 3.0 * M_PI * r / a); // Деталізація руху по кругу
const float c_det = 30; // Деталізація кола
bool outside = 1; // Рух ззовні (true) / всередині (false)
bool view = 0; // Показувати коло з точкою (true) / траекторію точки (false)

const float h = a / sqrt(3);

float convert_x(const float x)
{
  return 2.0 * (float) x / width;
}

float convert_y(const float y)
{
  return 2.0 * (float) y / height;
};

float point_ang = 0.0;
float x, y, ang = 150.0 + trg_a * 180.0 / M_PI;
float k, b, x_delta, a_delta;

array<Point, 3> trg = {{Point(h * cos(trg_a + 7.0 / 6.0 * M_PI),
                              h * sin(trg_a + 7.0 / 6.0 * M_PI)),
                        Point(h * cos(trg_a + 0.5 * M_PI),
                              h * sin(trg_a + 0.5 * M_PI)),
                        Point(h * cos(trg_a - M_PI / 6.0),
                              h * sin(trg_a - M_PI / 6.0))}};

array<array<Point, 2>, 3> trj1 = {{{Point(trg[0].x + r * cos(5.0 / 6.0 * M_PI + trg_a),
                                          trg[0].y + r * sin(5.0 / 6.0 * M_PI + trg_a)),
                                    Point(trg[1].x + r * cos(5.0 / 6.0 * M_PI + trg_a),
                                          trg[1].y + r * sin(5.0 / 6.0 * M_PI + trg_a))},

                                   {Point(trg[1].x + r * cos(M_PI / 6.0 + trg_a),
                                          trg[1].y + r * sin(M_PI / 6.0 + trg_a)),
                                    Point(trg[2].x + r * cos(M_PI / 6.0 + trg_a),
                                          trg[2].y + r * sin(M_PI / 6.0 + trg_a))},

                                   {Point(trg[2].x + r * cos(M_PI / -2.0 + trg_a),
                                          trg[2].y + r * sin(M_PI / -2.0 + trg_a)),
                                    Point(trg[0].x + r * cos(M_PI / -2.0 + trg_a),
                                          trg[0].y + r * sin(M_PI / -2.0 + trg_a))}}};

array<Point, 3> trj0 = {{Point(trg[0].x + 2 * r * cos(M_PI / 6.0 + trg_a),
                               trg[0].y + 2 * r * sin(M_PI / 6.0 + trg_a)),
                         Point(trg[1].x + 2 * r * cos(1.5 * M_PI + trg_a),
                               trg[1].y + 2 * r * sin(1.5 * M_PI + trg_a)),
                         Point(trg[2].x + 2 * r * cos(5.0 / 6.0 * M_PI + trg_a),
                               trg[2].y + 2 * r * sin(5.0 / 6.0 * M_PI + trg_a))}};

float length(const float delta_x, const float k_)
{
  float delta_y = delta_x * k_;
  return sqrt(pow(delta_x, 2) + pow(delta_y, 2));
}

void glTrg()
{
  glBegin(GL_LINE_LOOP);
  glColor3f(1, 1, 1);
  glVertex2f(convert_x(trg[0].x), convert_y(trg[0].y));
  glVertex2f(convert_x(trg[1].x), convert_y(trg[1].y));
  glVertex2f(convert_x(trg[2].x), convert_y(trg[2].y));
  glEnd();
}

void glCircle(const float x, const float y, const float r, const bool fill = false, const bool black = false)
{
  if (fill)
    glBegin(GL_POLYGON);
  else
    glBegin(GL_LINE_LOOP);

  float a_del = 2 * M_PI / c_det;
  if (black)
    glColor3f(0, 0, 0);
  else
    glColor3f(1, 1, 1);

  for (int point = 0; point < c_det; point++)
  {
    glVertex2f(convert_x(x + r * cos(a_del * point)), convert_y(y + r * sin(a_del * point)));
  }

  glEnd();
}

void display()
{
//  glClearColor( 0, 0, 0, 1 );
//  glClear(GL_COLOR_BUFFER_BIT);

  glTrg();

  for (int number = 0; number < 3; number++)
  {
    if (outside)
    {
      k = (trj1[number][0].y - trj1[number][1].y) / (trj1[number][0].x - trj1[number][1].x);
      b = trj1[number][0].y - trj1[number][0].x * k;
      x_delta = (trj1[number][1].x - trj1[number][0].x) / a_det;

      for (int step = 0; step <= a_det; step++)
      {
        if (view)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        x = trj1[number][0].x + step * x_delta;
        y = x * k + b;
        point_ang -= 180.0 * length(x_delta, k) / (M_PI * r);

        glTrg();

        if (view)
          glCircle(x, y, r, false);

        glCircle(x + r * cos(point_ang / 180.0 * M_PI),
                 y + r * sin(point_ang / 180.0 * M_PI), r_t, true, false);
        glutSwapBuffers();
      }

      a_delta = -120.0 / r_det;
      ang = ang - a_delta;

      for (int step = 0; step <= r_det; step++)
      {
        if (view)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        ang += a_delta;
        x = trg[(number + 1) % 3].x + r * cos(ang / 180.0 * M_PI);
        y = trg[(number + 1) % 3].y + r * sin(ang / 180.0 * M_PI);
        point_ang += a_delta;

        glTrg();

        if (view)
          glCircle(x, y, r, false);

        glCircle(x + r * cos(point_ang / 180.0 * M_PI),
                 y + r * sin(point_ang / 180.0 * M_PI), r_t, true, false);
        glutSwapBuffers();
      }
    }
    else
    {
      k = (trj0[number].y - trj0[(number + 1) % 3].y) / (trj0[number].x - trj0[(number + 1) % 3].x);
      b = trj0[number].y - trj0[number].x * k;
      x_delta = (trj0[(number + 1) % 3].x - trj0[number].x) / a_det;

      for (int step = 0; step <= a_det; step++)
      {
        x = trj0[number].x + step * x_delta;
        y = x * k + b;
        point_ang += 180 * length(x_delta, k) / (M_PI * r);

        if (view)
        {
          glClearColor(0, 0, 0, 1);
          glClear(GL_COLOR_BUFFER_BIT);
        }

        glTrg();

        if (view)
          glCircle(x, y, r, false);

        glCircle(x + r * cos(point_ang / 180.0 * M_PI), y + r * sin(point_ang / 180.0 * M_PI), r_t, true);
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
  glutInitWindowSize(width, height);
  glutCreateWindow("Lab 2");
  glutPositionWindow(688 - width / 2, 384 - height / 2);
  glutDisplayFunc(display);
  glutIdleFunc(display);

  glutMainLoop();
}