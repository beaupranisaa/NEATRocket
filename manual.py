#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions

from rocket import Rocket, RocketImage
from base import Base

#setup the window
window_width = 1366
window_height = 768
#window = pyglet.window.Window(window_width,window_height)
window = pyglet.window.Window(fullscreen=True)
window_width = window.width
window_height = window.height
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

batch = pyglet.graphics.Batch()

#insert rocket
rocket = []
rocket.append(Rocket(x_pos = window.width//2, y_pos = window.height//2,lateral_force=300,batch=batch))
rocket[-1].insert(space)

rocket_image = RocketImage(batch = batch)
rocket_image.attach(rocket[-1])

keyboard = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboard)


#on_draw window event
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    batch.draw()
    fps_display.draw()

def update(dt):
    output = [0,0,0]

    if(keyboard[pyglet.window.key.W] or keyboard[pyglet.window.key.UP]):
        output[0] += 1
    if(keyboard[pyglet.window.key.E] or keyboard[pyglet.window.key.RIGHT]):
        output[1] += 1
    if(keyboard[pyglet.window.key.Q] or keyboard[pyglet.window.key.LEFT]):
        output[1] -= 1
    if(keyboard[pyglet.window.key.A]):
        output[2] -= 1
    if(keyboard[pyglet.window.key.D]):
        output[2] += 1
    if(keyboard[pyglet.window.key.SPACE]):
        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                [BASE_MARGIN,window_height-BASE_MARGIN],
                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])

    rocket[0].propel(output)

    if ((rocket[0].body.position.y < -100) or 
            (rocket[0].body.position.y > window_height+100) or
            (rocket[0].body.position.x < -100) or
            (rocket[0].body.position.x > window_width+100)):
        rocket[0].remove(space)
        del rocket[0] 
        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                [BASE_MARGIN,window_height-BASE_MARGIN],
                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])
        rocket.append(Rocket(x_pos = window.width//2, y_pos = window.height//2,lateral_force = 300,batch=batch))
        rocket[-1].insert(space)
        rocket_image.attach(rocket[-1])
            
#    rocket_image.rocket_sprite.update(rocket[0].body.position.x, rocket[0].body.position.y, -float(rocket[0].body.angle) * 180 / 3.1416)
#    rocket_image.exhaust_sprite.update(rocket[0].body.position.x, rocket[0].body.position.y, -float(rocket[0].body.angle) * 180 / 3.1416)
    rocket_image.attach(rocket[0])
    rocket[0].update()
    rocket[0].visibility(False)

    space.step(1/60)

#Set pyglet update interval
pyglet.clock.schedule(update)
pyglet.app.run()
