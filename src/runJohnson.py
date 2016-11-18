from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
from johnson import Johnson

eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])

prevX, prevY = 0, 0

geom = Johnson()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glClearDepth(1.0);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);
    glShadeModel(GL_SMOOTH);
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);


def mainDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(eye[0],eye[1],eye[2],  0,0,0,  up[0],up[1],up[2])
    glBegin(GL_LINES)

    # x axis
    glColor3f(0.5, 1.0, 1.0) 
    glVertex3f(0.0,0.0,0.0)
    glVertex3f(15.0,0.0,0.0)

    # y axis
    glColor3f(1.0, 0.5, 1.0) 
    glVertex3f(0.0,0.0,0.0)
    glVertex3f(0.0,15.0,0.0)

    # z axis
    glColor3f(1.0, 1.0, 0.5) 
    glVertex3f(0.0,0.0,0.0)
    glVertex3f(0.0,0.0,15.0)

    glEnd()

    geom.update()

    glBegin(GL_LINES)

    # change color for easier viewing
    for i in range(len(geom.edges)):
        if i == 0:
            glColor3f(1.0, 0.0, 0.0) 
        elif i == 6:
            glColor3f(0.0,1.0,0.0)
        elif i == 9:
            glColor3f(0.0,0.0,1.0)
        for v in geom.edges[i]:
            glVertex3fv(geom.solid[v])

    glEnd()
    glutSwapBuffers()

    print(geom.stats())


def mainReshape(w,h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(45, float(w) / h, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def idle():
    glutPostRedisplay()


def drag(x,y):
    global prevX
    global prevY
    global eye
    global up
    diffX = x - prevX
    diffY = -y + prevY
    eye = transform.left(diffX,eye,up)
    eye, up = transform.up(diffY,eye,up)

    prevX = x
    prevY = y
    glutPostRedisplay()


def keyboard(key,x,y):
    global geom
    if key == 27:
        exit(0)
    elif key == '1':
        geom.top_height += geom.scale_factor
    elif key == '!':
        geom.top_height -= geom.scale_factor
    elif key == '2':
        geom.square_tip_out += geom.scale_factor
    elif key == '@':
        geom.square_tip_out -= geom.scale_factor
    elif key == '3':
        geom.square_tip_up += geom.scale_factor
    elif key == '#':
        geom.square_tip_up -= geom.scale_factor
    elif key == '4':
        geom.line_out += geom.scale_factor
    elif key == '$':
        geom.line_out -= geom.scale_factor
    elif key == 'a':
        geom.alpha *= geom.weight_factor
    elif key == 'A':
        geom.alpha /= geom.weight_factor
    elif key == 's':
        geom.beta *= geom.weight_factor
    elif key == 'S':
        geom.beta /= geom.weight_factor
    elif key == 'd':
        geom.gamma *= geom.weight_factor
    elif key == 'D':
        geom.gamma /= geom.weight_factor
    elif key == 'g':
        geom.take_step()

    glutPostRedisplay()


def mouse(button,state,x,y):
    global prevX
    global prevY
    if state == 1:
        prevX = 0
        prevY = 0


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Johnson")
    glutDisplayFunc(mainDisplay)
    glutReshapeFunc(mainReshape)
    glutMotionFunc(drag)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()
    return


if __name__ == '__main__': main()




























