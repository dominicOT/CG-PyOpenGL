import pygame
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


#....................................................................................................................................................
#pygame init
pygame.init()
display = (1400, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


#....................................................................................................................................................
#GL setup
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)



#....................................................................................................................................................
#init global vars
day_length = 1.0
planet_angle = 0.0
moon_angle = 0.0
view_angle = 0.0
view_toggle = False
planet_distance = 5.0
planet_radius = 0.6
moon_distance = 1.0
moon_radius = 0.2
planet_speed = 365.0 / 360.0
moon_speed = 30.0 / 360.0




#....................................................................................................................................................
#sketch earth, sun and moon
def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)
    gluSphere(quad, radius, slices, stacks)



#....................................................................................................................................................
#orbit path
def draw_orbit_path(radius, slices):
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()



#....................................................................................................................................................
#render func
def display():
    global planet_angle, moon_angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(view_angle, 1, 0, 0)
    glColor3f(1.0, 1.0, 0.0)
    draw_sphere(1.0, 50, 50)
    glColor3f(0.3, 0.3, 0.3)
    draw_orbit_path(planet_distance, 100)
    planet_x = planet_distance * math.cos(math.radians(planet_angle))
    planet_y = planet_distance * math.sin(math.radians(planet_angle))
    glPushMatrix()
    glTranslatef(planet_x, planet_y, 0.0)
    glColor3f(0.0, 1.0, 0.5)
    draw_sphere(planet_radius, 50, 50)
    glPopMatrix()
    moon_x = moon_distance * math.cos(math.radians(moon_angle))
    moon_y = moon_distance * math.sin(math.radians(moon_angle))
    glPushMatrix()
    glTranslatef(moon_x + planet_x, moon_y + planet_y, 0.0)
    glColor3f(0.5, 0.5, 0.5)
    draw_sphere(moon_radius, 50, 50)
    glPopMatrix()

    pygame.display.flip()




#....................................................................................................................................................
#handle mouse events
def mouse(button, state, x, y):
    global day_length

    if button == 1 and state == 1:
        day_length *= 2
    elif button == 3 and state == 1:
        day_length /= 2



#....................................................................................................................................................
#handle keyboard event
def keyboard():
    global view_toggle, view_angle

    keys = pygame.key.get_pressed()
    if keys[K_v]:
        view_toggle = not view_toggle
        if view_toggle:
            view_angle = 45.0
        else:
            view_angle = 0.0




#....................................................................................................................................................
clock = pygame.time.Clock()
print("Orbit Simulation Assignment")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse(event.button, event.type, *event.pos)
    
    keyboard()
    

    planet_angle += planet_speed * day_length
    moon_angle += moon_speed * day_length

    display()
    clock.tick(60)
  
