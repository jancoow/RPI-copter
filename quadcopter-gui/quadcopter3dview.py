from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4.QtOpenGL import *
from PyQt4 import QtCore


class quadcopter3dview(QGLWidget):
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setGeometry(QtCore.QRect(700, 10, 441, 211))
        self.cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
        self.x_angle = 0
        self.y_angle = 0

    def paintGL(self):
        glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        #glScaled(1.1,1.1,1.1)
        glColor((1., 1., 1.))
        glLineWidth(1)
        glBegin(OpenGL.GL.GL_LINES)
        for x in range(-20, 22, 2):
            glVertex3f(x/10.,-1,-1)
            glVertex3f(x/10.,-1,1)

        for x in range(-20, 22, 2):
            glVertex3f(x/10.,-1, 1)
            glVertex3f(x/10., 1, 1)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z/10.)
            glVertex3f( 2, -1, z/10.)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z/10.)
            glVertex3f(-2,  1, z/10.)

        for z in range(-10, 12, 2):
            glVertex3f( 2, -1, z/10.)
            glVertex3f( 2,  1, z/10.)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y/10., 1)
            glVertex3f( 2, y/10., 1)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y/10., 1)
            glVertex3f(-2, y/10., -1)

        for y in range(-10, 12, 2):
            glVertex3f(2, y/10., 1)
            glVertex3f(2, y/10., -1)
        glEnd()
        glPushMatrix()

        glRotate(float(self.y_angle), 1, 0, 0)
        glRotate(-float(self.x_angle), 0, 0, 1)
        self.cube.render()
        glPopMatrix()


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(OpenGL.GL.GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w) / h, 0.001, 10.0)
        glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 1.0, -5.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)

    def initializeGL(self):
        glEnable(OpenGL.GL.GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(OpenGL.GL.GL_SMOOTH)
        glEnable(OpenGL.GL.GL_BLEND)
        glEnable(OpenGL.GL.GL_POLYGON_SMOOTH)
        glHint(OpenGL.GL.GL_POLYGON_SMOOTH_HINT, OpenGL.GL.GL_NICEST)
        glEnable(OpenGL.GL.GL_COLOR_MATERIAL)
        glEnable(OpenGL.GL.GL_LIGHTING)
        glEnable(OpenGL.GL.GL_LIGHT0)
        glLightfv(OpenGL.GL.GL_LIGHT0, OpenGL.GL.GL_AMBIENT, (0.3, 0.3, 0.3, 1.0));

    def setCordinats(self,x,y):
        self.x_angle = x
        self.y_angle = y
        self.repaint()

class Cube(object):
    num_faces = 6
    vertices = [(-1.0, -0.05, 0.5),
                 (1.0, -0.05, 0.5),
                 (1.0, 0.05, 0.5),
                 (-1.0, 0.05, 0.5),
                 (-1.0, -0.05, -0.5),
                 (1.0, -0.05, -0.5),
                 (1.0, 0.05, -0.5),
                 (-1.0, 0.05, -0.5)]
    normals = [(0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0)]  # bottom
    vertex_indices = [(0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4)]  # bottom

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def render(self):
        glColor(self.color)
        vertices = self.vertices

        # Draw all 6 faces of the cube
        glBegin(OpenGL.GL.GL_QUADS)
        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()
