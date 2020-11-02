#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
from rocket import Rocket

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

#Create Base class
class Base:
    def __init__(self, height = 200, aspect_ratio = 0.12):
        # set base body and shape
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.height = height
        self.aspect_ratio = aspect_ratio
        self.diameter = int(self.height*self.aspect_ratio)
        self.shape = pymunk.Poly.create_box(self.body,size=(self.diameter,self.height))

        # set base's position
        self.body.position = 600,100
        space.add(self.body,self.shape)

        # set sensor = True to not handle collisions
        self.shape.sensor = True

rocket = []
rocket.append(Rocket(x_pos = window.width//2, y_pos = window.height//2))
rocket[-1].insert(space)

base = Base()

keyboard = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboard)

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
    if(keyboard[pyglet.window.key.W] or keyboard[pyglet.window.key.UP]):
        rocket[0].body.apply_force_at_local_point((0,1500),(0,-rocket[0].height//2))
    if(keyboard[pyglet.window.key.E] or keyboard[pyglet.window.key.RIGHT]):
        rocket[0].body.apply_force_at_local_point((100,0),(0,rocket[0].height//2))
    if(keyboard[pyglet.window.key.Q] or keyboard[pyglet.window.key.LEFT]):
        rocket[0].body.apply_force_at_local_point((-100,0),(0,rocket[0].height//2))
    if(keyboard[pyglet.window.key.A]):
        rocket[0].body.apply_force_at_local_point((-100,0),(0,-rocket[0].height//2))
    if(keyboard[pyglet.window.key.D]):
        rocket[0].body.apply_force_at_local_point((100,0),(0,-rocket[0].height//2))

    if rocket[0].body.position.y < -100:
        rocket[0].remove(space)
        del rocket[0] 
        rocket.append(Rocket(x_pos = window.width//2, y_pos = window.height//2))
        rocket[-1].insert(space)
            
    space.step(dt)

#Set pyglet update interval
pyglet.clock.schedule_interval(update,1.0/120)
pyglet.app.run()
