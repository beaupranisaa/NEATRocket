#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
import neat

from rocket import Rocket
from base import Base

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

#insert base
BASE_MARGIN = 100
NOT_BASE_MARGIN = 500
base = Base()
base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
        [BASE_MARGIN,window_height-BASE_MARGIN],
        [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
        [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])
base.insert(space)

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
    space.step(dt)

#Set pyglet update interval
pyglet.clock.schedule_interval(update,1.0/120)
pyglet.app.run()
