#include <iostream>
#include <GL/freeglut.h>
#include <GL/gl.h>
#include <cmath>
#include <array>
#include <string>
#include <unistd.h>

using namespace std;

struct point
{
  double x, y;
  point() = default;
  point(double x, double y): x(x), y(y) {};
};

const int width = 600, height = 600;
const int maxPoints = 100;
const int maxCount = 6;
const int axisWidth = 2;
const int funcWidth = 2;
const int arrowSize = 12;
const int markSize = 3;
const int graphDet = 300;
const int pointDet = 10;
const float pointRad = 3.0;
const float gridColorRatio = 0.4;
const float zoomDelta = 0.1;

const float graphWidth = 1.0 - 4.0 * (float) arrowSize / width;
const float graphHeight = 1.0 - 4.0 * (float) arrowSize / height;

int n;
array<point, maxPoints> points;

float x, y;
float power;

int displayMode = 0;
float graphSizeX = 1;
float graphSizeY = graphSizeX * (graphHeight / graphWidth);
float zoomScale = 1.0;

double graphToGlobalX(double x)
{
  return graphWidth * (x / graphSizeX);
}

double graphToGlobalY(double y)
{
  return graphHeight * (y / graphSizeY);
}

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

void glGraph()
{
  glLineWidth(axisWidth);
  glColor3f(1, 1, 1);

  glBegin(GL_LINES);

  glVertex2f(-1, 0);
  glVertex2f(1, 0);
  glVertex2f(0, 1);
  glVertex2f(0, -1);

  glVertex2f(1, 0);
  glVertex2f(1 - (float) arrowSize / width * 2.0, (float) arrowSize / height);
  glVertex2f(1, 0);
  glVertex2f(1 - (float) arrowSize / width * 2.0, (float) - arrowSize / height);

  glVertex2f(0, 1);
  glVertex2f((float) arrowSize / width, 1 - (float) arrowSize / height * 2.0);
  glVertex2f(0, 1);
  glVertex2f((float) - arrowSize / width, 1 - (float) arrowSize / height * 2.0);

  glEnd();

  glLineWidth(1);

  if (displayMode == 2)
    glColor3f(gridColorRatio, gridColorRatio, gridColorRatio);

  if (displayMode)
  {
    glBegin(GL_LINES);

    power = floor(log2(max(graphSizeX, graphSizeY) / maxCount));

    string scale = "Lab 3: " + to_string(pow(2, power));

    glutSetWindowTitle(&scale[0]);

    for (int mark = 1; mark < (float) graphSizeY / pow(2, power); mark++)
    {
      if (displayMode - 1)
      {
        glVertex2f(graphWidth, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(-graphWidth, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(graphWidth, graphToGlobalY(-mark * pow(2, power)));
        glVertex2f(-graphWidth, graphToGlobalY(-mark * pow(2, power)));
      }
      else
      {
        glVertex2f(2.0 * (float) markSize / width, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(-2.0 * (float) markSize / width, graphToGlobalY(mark * pow(2, power)));
        glVertex2f(2.0 * (float) markSize / width, graphToGlobalY(-mark * pow(2, power)));
        glVertex2f(-2.0 * (float) markSize / width, graphToGlobalY(-mark * pow(2, power)));
      }
    }

    for (int mark = 1; mark < (float) graphSizeX / pow(2, power); mark++)
    {
      if (displayMode - 1)
      {
        glVertex2f(graphToGlobalX(mark * pow(2, power)), graphHeight);
        glVertex2f(graphToGlobalX(mark * pow(2, power)), -graphHeight);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), graphHeight);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), -graphHeight);
      }
      else
      {
        glVertex2f(graphToGlobalX(mark * pow(2, power)), 2.0 * (float) markSize / height);
        glVertex2f(graphToGlobalX(mark * pow(2, power)), -2.0 * (float) markSize / height);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), 2.0 * (float) markSize / height);
        glVertex2f(graphToGlobalX(-mark * pow(2, power)), -2.0 * (float) markSize / height);
      }
    }

    glEnd();
  }

  glColor3f(1, 1, 1);
}

void glPoint(float x, float y)
{
  glBegin(GL_POLYGON);

  for (int step = 0; step < pointDet; step++)
  {
    glVertex2f(graphToGlobalX(x) - 2.0 * (float) pointRad / width *
               cos(2 * M_PI * ((float) step / pointDet)),
               graphToGlobalY(y) - 2.0 * (float) pointRad / height *
               sin(2 * M_PI * ((float) step / pointDet)));
  }

  glEnd();
}

void zoom(int key, int x, int y)
{
  if (key == GLUT_KEY_DOWN)
  {
    zoomScale *= (1 + zoomDelta);
  }
  if (key == GLUT_KEY_UP)
  {
    zoomScale /= (1 + zoomDelta);
  }
  if (key == GLUT_KEY_CTRL_R || key == GLUT_KEY_CTRL_L)
  {
    displayMode = (displayMode + 1) % 3;
  }
}

void display()
{
  glClearColor(0, 0, 0, 1);
  glClear(GL_COLOR_BUFFER_BIT);

  glGraph();

  for (int number = 0; number < n; number++)
  {
    glPoint(points[number].x, points[number].y);
  }

  glLineWidth(funcWidth);

  glBegin(GL_LINE_STRIP);

  for (int step = -graphDet; step <= graphDet; step++)
  {
    x = ((float) step / graphDet) * (graphSizeX / graphWidth);
    y = interpolation(x);
    glVertex2f(graphToGlobalX(x), graphToGlobalY(y));
  }

  glEnd();

  glutSwapBuffers();
}

void redraw()
{
  graphSizeX *= zoomScale;
  graphSizeY = graphSizeX * (graphHeight / graphWidth);

  zoomScale = 1.0;

  glutPostRedisplay();
}

int main(int argc, char** argv)
{
  cin >> n;

  for (int i = 0; i < n; i++)
  {
    cin >> points[i].x >> points[i].y;
    if (abs(points[i].x) > graphSizeX)
    {
      graphSizeX = abs(points[i].x);
    }
    if (abs(points[i].y) > graphSizeY)
    {
      graphSizeY = abs(points[i].y);
    }
  }

  if ((graphSizeY * graphHeight) > (graphSizeX * graphWidth))
  {
    graphSizeX = graphSizeY * (graphWidth / graphHeight);
  }
  else
  {
    graphSizeY = graphSizeX * (graphHeight / graphWidth);
  }

  array<float, maxPoints> polynomial;

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

  cout << "y = ";

  for (int i = n - 1; i >= 0; i--)
  {
    cout << to_string(polynomial[i]);
    if (i > 0)
      cout << " * x ^ " << to_string(i) << " + ";
  }

  cout << endl;

  string title = "Lab 3: " + to_string(1.0);

  glutInit(&argc, argv);

  glutSetOption(GLUT_MULTISAMPLE, 4);
  glEnable(GL_LINE_SMOOTH);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE);
  glutInitWindowSize(width, height);
  glutCreateWindow(&title[0]);
  glutPositionWindow(688 - width / 2, 384 - height / 2);
  glutDisplayFunc(display);
  glutSpecialFunc(zoom);
  glutIdleFunc(redraw);

  glutMainLoop();
}