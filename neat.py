#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions

#setup the window
window_width = 1366
window_height = 768
window = pyglet.window.Window(window_width,window_height)
window.set_caption("NEATLanding")
fps_display = pyglet.window.FPSDisplay(window=window)

#create drawoptions object
options = DrawOptions()

#setup space
space = pymunk.Space()
space.gravity = (0,-1000)

#Create rocket class
class Rocket:
    def __init__(self, mass = 1, height = 200, aspect_ratio = 0.12, friction = 0.3, elasticity = 0.2):
        # set rocket's pysical properties
        self.mass = mass
        self.aspect_ratio = aspect_ratio
        self.height = height
        self.diameter = int(self.height*self.aspect_ratio)
        self.moment = pymunk.moment_for_box(self.mass,(self.diameter,self.height))
        self.body = pymunk.Body(self.mass,self.moment)
        self.shape = pymunk.Poly.create_box(self.body,size=(self.diameter,self.height))
        self.friction = friction
        self.elasticity = elasticity

        # set rocket's  initial position
        self.body.position = window.width/2, window.height/2
        self.body.angle = 0.01
        self.body.velocity = 0.0,0.0
        self.body.angular_velocity = 0.0

        #add rocket to space
        space.add(self.body,self.shape)

    def remove(self,space):
        space.remove(self.body, self.shape)

#Create Base class
class Base:
    def __init__(self, height = 200, aspect_ratio = 0.12):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.height = height
        self.aspect_ratio = aspect_ratio
        self.diameter = int(self.height*self.aspect_ratio)
        self.shape = pymunk.Poly.create_box(self.body,size=(self.diameter,self.height))
        self.body.position = 600,100
        space.add(self.body,self.shape)
        self.shape.sensor = True

rocket = []
rocket.append(Rocket())

base = Base()

#on_draw window event
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    fps_display.draw()

@window.event
def on_mouse_press(x,y,button,modifier):
    pass

def update(dt):
    if rocket[0].body.position.y < -100:
        rocket[0].remove(space)
        del rocket[0] 
        rocket.append(Rocket())
            
    space.step(dt)

#Set pyglet update interval
pyglet.clock.schedule_interval(update,1.0/120)
pyglet.app.run()
