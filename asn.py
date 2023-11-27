import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Constants
WIDTH, HEIGHT = 800, 600
SPHERE_RADIUS = 1.0
DAY_LENGTH = 360
VIEW_ANGLE = 30

# Initial variables
angle = 0
day_speed = 1
view_ecliptic = False

# Initialize Pygame and OpenGL
pygame.init()
display = (WIDTH, HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)


def draw_solar_system():
    global angle

    glPushMatrix()

    # Rotate based on the day
    glRotatef(angle, 0, 1, 0)

    #  sun
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), SPHERE_RADIUS, 100, 100)

    # planet rotation
    glRotatef(angle * DAY_LENGTH / 365, 0, 1, 0)
    glTranslatef(3, 0, 0)

    # Draw the planet
    glColor3f(3, 2, 1)
    gluSphere(gluNewQuadric(), SPHERE_RADIUS * 0.7, 100, 100)

    # Rotate the planet on its axis
    glRotatef(angle, 0, 1, 0)

    # Draw the moon
    glColor3f(0.5, 0.6, 0.7)
    glTranslatef(1.0, 0, 0)
    gluSphere(gluNewQuadric(), SPHERE_RADIUS * 0.3, 100, 100)

    glPopMatrix()


def change_view():
    global view_ecliptic
    if view_ecliptic:
        glTranslatef(0, 1, -5)
        glRotatef(-VIEW_ANGLE, 1, 0, 0)
    else:
        glTranslatef(0, -1, -5)
        glRotatef(VIEW_ANGLE, 1, 0, 0)
    view_ecliptic = not view_ecliptic


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                day_speed *= 2
            elif event.button == 3:  # Right mouse button
                day_speed /= 2
        if event.type == pygame.KEYDOWN:
            if event.key == ord('v') or event.key == ord('V'):
                change_view()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    angle += day_speed
    draw_solar_system()
    pygame.display.flip()
    pygame.time.wait(10)
