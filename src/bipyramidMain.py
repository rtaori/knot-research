from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Tkinter import *
import sys
import math
import transform
import numpy as np
import bipyramid as bd
eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])

prevX = 0
prevY = 0
r = 0

edges = [
# top edges
[0,1],
[0,2],
[0,3],
#bottom edges
[4,5],
[4,6],
[4,7],
# line outs
[8,9],
[10,11],
[12,13],
#top edges to line outs
[1,11],
[3,10],
[1,13],
[2,12],
[2,9],
[3,8],
#bottom edges to line outs
[5,11],
[5,13],
[6,9],
[6,12],
[7,8],
[7,10],
]


geom = bd.Geometry()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0); # Set background color to black and opaque
    glClearDepth(1.0);                   # Set background depth to farthest
    glEnable(GL_DEPTH_TEST);   # Enable depth testing for z-culling
    glDepthFunc(GL_LEQUAL);    # Set the type of depth-test
    glShadeModel(GL_SMOOTH);   # Enable smooth shading
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

    #Draw Geometry
    global geom
    geom.buildGeometry()
    l_cost = geom.length_cost(1)
    print('length cost: ' + str(l_cost))
    a_cost = geom.angle_cost(1)
    print('angle cost: ' + str(a_cost))
    # p_cost = geom.planarity_cost(1)
    # print('planarity cost: ' + str(p_cost))
    # t_cost = l_cost + a_cost + p_cost
    # print('total cost: ' + t_cost)

    glBegin(GL_LINES)

    for i in range(len(edges)):
        if i == 0:
            glColor3f(1.0, 0.0, 0.0) 
        elif i == 6:
            glColor3f(0.0,1.0,0.0)
        elif i == 9:
            glColor3f(0.0,0.0,1.0)
        for v in edges[i]:
            glVertex3fv(geom.solid[v])
    glEnd()

    glutSwapBuffers()

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
    elif key == "=":
        geom.extraTranslation += 0.2
    elif key == "-":
        geom.extraTranslation -= 0.2
    
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
    glutCreateWindow("Solid")
    glutDisplayFunc(mainDisplay)
    glutReshapeFunc(mainReshape)
    glutMotionFunc(drag)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()
    return

if __name__ == '__main__': main()