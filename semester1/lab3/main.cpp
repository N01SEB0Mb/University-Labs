#include <iostream>
#include <GL/freeglut.h>
#include <GL/gl.h>
#include <cmath>
#include <array>
#include <string>

#include "config.hpp"

// Point structure (store X and Y coordinate)
struct point
{
  double x, y;
  point() = default;
  point(double x, double y): x(x), y(y) {};
};

// Used variables
int n;
std::array<point, config::MAX_POINTS> points;

float x, y;
float power;

int displayMode = 0;
float graphSizeX = 1;
float graphSizeY = graphSizeX * (config::graphHeight / config::graphWidth);
float zoomScale = 1.0;


// Convert graph X to global X
double graphToGlobalX(double x)
{
  return config::graphWidth * (x / graphSizeX);
}

// Convert graph Y to global Y
double graphToGlobalY(double y)
{
  return config::graphHeight * (y / graphSizeY);
}

// Interpolate points
double interpolation(const double x)
{
  double result = 0.0;

  for (int i = 0; i < n; i++)
  {
    double polynomial = points[i].y;

    for (int j = 0; j < n; j++)
    {
      if (i != j)
      {
        polynomial *= (x - points[j].x) / (points[i].x - points[j].x);
      }
    }

    result += polynomial;
  }

  return result;
}

// Draw graph
void glGraph()
{
  glLineWidth(config::WIDTH_AXIS);
  glColor3f(1, 1, 1);

  glBegin(GL_LINES);

  glVertex2f(-1, 0);
  glVertex2f(1, 0);
  glVertex2f(0, 1);
  glVertex2f(0, -1);

  glVertex2f(1, 0);
  glVertex2f(1 - (float) config::SIZE_ARROW / config::WINDOW_WIDTH * 2.0, (float) config::SIZE_ARROW / config::WINDOW_HEIGHT);
  glVertex2f(1, 0);
  glVertex2f(1 - (float) config::SIZE_ARROW / config::WINDOW_WIDTH * 2.0, (float) - config::SIZE_ARROW / config::WINDOW_HEIGHT);

  glVertex2f(0, 1);
  glVertex2f((float) config::SIZE_ARROW / config::WINDOW_WIDTH, 1 - (float) config::SIZE_ARROW / config::WINDOW_HEIGHT * 2.0);
  glVertex2f(0, 1);
  glVertex2f((float) - config::SIZE_ARROW / config::WINDOW_WIDTH, 1 - (float) config::SIZE_ARROW / config::WINDOW_HEIGHT * 2.0);

  glEnd();

  glLineWidth(1);

  if (displayMode == 2)
    glColor3f(config::gridColorRatio, config::gridColorRatio, config::gridColorRatio);

  if (displayMode)
  {
    glBegin(GL_LINES);

    power = floor(log2(std::max(graphSizeX, graphSizeY) / config::MAX_COUNT));

    std::string scale = "Lab 3: " + std::to_string(pow(2, power));

    glutSetWindowTitle(&scale[0]);

    for (int mark = 1; mark < (float) graphSizeY / pow(2, power); mark++)
    {
      if (displayMode - 1)
      {
        glVertex2f(config::graphWidth, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(-config::graphWidth, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(config::graphWidth, graphToGlobalY(-mark * pow(2, power)));
        glVertex2f(-config::graphWidth, graphToGlobalY(-mark * pow(2, power)));
      }
      else
      {
        glVertex2f(2.0 * (float) config::MARK_SIZE / config::WINDOW_WIDTH, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(-2.0 * (float) config::MARK_SIZE / config::WINDOW_WIDTH, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(2.0 * (float) config::MARK_SIZE / config::WINDOW_WIDTH, graphToGlobalY(-mark * pow(2, power)));
        glVertex2f(-2.0 * (float) config::MARK_SIZE / config::WINDOW_WIDTH, graphToGlobalY(-mark * pow(2, power)));
      }
    }

    for (int mark = 1; mark < (float) graphSizeX / pow(2, power); mark++)
    {
      if (displayMode - 1)
      {
        glVertex2f(graphToGlobalX(mark * pow(2, power)), config::graphHeight);
        glVertex2f(graphToGlobalX(mark * pow(2, power)), -config::graphHeight);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), config::graphHeight);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), -config::graphHeight);
      }
      else
      {
        glVertex2f(graphToGlobalX(mark * pow(2, power)), 2.0 * (float) config::MARK_SIZE / config::WINDOW_HEIGHT);
        glVertex2f(graphToGlobalX(mark * pow(2, power)), -2.0 * (float) config::MARK_SIZE / config::WINDOW_HEIGHT);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), 2.0 * (float) config::MARK_SIZE / config::WINDOW_HEIGHT);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), -2.0 * (float) config::MARK_SIZE / config::WINDOW_HEIGHT);
      }
    }

    glEnd();
  }

  glColor3f(1, 1, 1);
}


// Draw graph point
void glPoint(float x, float y)
{
  glBegin(GL_POLYGON);

  for (int step = 0; step < config::pointDet; step++)
  {
    glVertex2f(graphToGlobalX(x) - 2.0 * (float) config::pointRad / config::WINDOW_WIDTH *
                                   cos(2 * M_PI * ((float) step / config::pointDet)),
               graphToGlobalY(y) - 2.0 * (float) config::pointRad / config::WINDOW_HEIGHT *
                                   sin(2 * M_PI * ((float) step / config::pointDet)));
  }

  glEnd();
}

// Zoom key bindings
void zoom(int key, int x, int y)
{
  if (key == GLUT_KEY_DOWN)
  {
    zoomScale *= (1 + config::zoomDelta);
  }
  if (key == GLUT_KEY_UP)
  {
    zoomScale /= (1 + config::zoomDelta);
  }
  if (key == GLUT_KEY_CTRL_R || key == GLUT_KEY_CTRL_L)
  {
    displayMode = (displayMode + 1) % 3;
  }
}

// Glut display func
void display()
{
  glClearColor(0, 0, 0, 1);
  glClear(GL_COLOR_BUFFER_BIT);

  glGraph();

  for (int number = 0; number < n; number++)
  {
    glPoint(points[number].x, points[number].y);
  }

  glLineWidth(config::WIDTH_FUNCTION);

  glBegin(GL_LINE_STRIP);

  for (int step = -config::graphDet; step <= config::graphDet; step++)
  {
    x = ((float) step / config::graphDet) * (graphSizeX / config::graphWidth);
    y = interpolation(x);
    glVertex2f(graphToGlobalX(x), graphToGlobalY(y));
  }

  glEnd();

  glutSwapBuffers();
}

// Glut redraw screen
void redraw()
{
  graphSizeX *= zoomScale;
  graphSizeY = graphSizeX * (config::graphHeight / config::graphWidth);

  zoomScale = 1.0;

  glutPostRedisplay();
}

int main(int argc, char** argv)
{
  std::cout << "Type number of points: ";
  std::cin >> n;

  std::cout << "Type points:" << std::endl;

  for (int i = 0; i < n; i++)
  {
    std::cin >> points[i].x >> points[i].y;
    if (abs(points[i].x) > graphSizeX)
    {
      graphSizeX = abs(points[i].x);
    }
    if (abs(points[i].y) > graphSizeY)
    {
      graphSizeY = abs(points[i].y);
    }
  }

  if ((graphSizeY * config::graphHeight) > (graphSizeX * config::graphWidth))
  {
    graphSizeX = graphSizeY * (config::graphWidth / config::graphHeight);
  }
  else
  {
    graphSizeY = graphSizeX * (config::graphHeight / config::graphWidth);
  }

  std::array<float, config::MAX_POINTS> polynomial;

  for (int j = 0; j < n; j++)
  {
    float multiplier = points[j].y;

    for (int i = 0; i < n; i++)
    {
      if (i != j)
        multiplier /= (points[j].x - points[i].x);
    }

    for (int i = 0; i < pow(2, n); i++)
    {
      float temp_mul = 1.0;
      float order = 0;
      for (int k = 1; k <= n; k++)
      {
        if ((i % (int) pow(2, k)) >= pow(2, k - 1))
        {
          if (k - 1 != j)
          {
            temp_mul *= -points[k - 1].x;
          }
        }
        else
        {
          order += 1;
        }
      }
      polynomial[order] += temp_mul * multiplier;
    }
  }

  std::cout << "Lagrange polynomial:" << std::endl;
  std::cout << "f(x) = ";

  for (int i = n - 1; i >= 0; i--)
  {
    std::cout << std::to_string(polynomial[i]);
    if (i > 0)
      std::cout << " * x ^ " << std::to_string(i) << " + ";
  }

  std::cout << std::endl;

  std::string title = "Lab 3: " + std::to_string(1.0);

  glutInit(&argc, argv);

  glutSetOption(GLUT_MULTISAMPLE, 4);
  glEnable(GL_LINE_SMOOTH);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE);
  glutInitWindowSize(config::WINDOW_WIDTH, config::WINDOW_HEIGHT);
  glutCreateWindow(&title[0]);
  glutPositionWindow(688 - config::WINDOW_WIDTH / 2, 384 - config::WINDOW_HEIGHT / 2);
  glutDisplayFunc(display);
  glutSpecialFunc(zoom);
  glutIdleFunc(redraw);

  glutMainLoop();
}
