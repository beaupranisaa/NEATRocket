#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
import neat
import os
import random
import pickle
import errno
import glob
import sys

from rocket import Rocket, RocketImage
from base import Base

if len(sys.argv) > 1:
    NETWORK_PATH = [str(path) for i,path in enumerate(sys.argv) if i > 0]
else:
    default_path = glob.glob('networksTest/Net_*')
    NETWORK_PATH = default_path

print("Networks:",NETWORK_PATH)

net_id = []
for net in NETWORK_PATH:
    net_str = net.split('_')[-1]
    net_str = net_str.split('.')[0]
    net_id.append(net_str)

#setup the window
window_width = 1366
window_height = 768
#window = pyglet.window.Window(window_width,window_height)
window = pyglet.window.Window(fullscreen=True)
window_width = window.width
window_height = window.height
window.set_caption("NEATLanding")
fps_display = pyglet.window.FPSDisplay(window=window)

batch = pyglet.graphics.Batch()

keyboard = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboard)

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

rocket_images = []

#state scale
CARTESIAN_SCALE = 200.0
ANGULAR_SCALE = 1.0/2.0

#on_draw window event
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    batch.draw()
    fps_display.draw()

@window.event
def on_mouse_press(x,y,button,modifier):
    base.move(x,y)

def get_states(rocket):
    #get rocket's current position and velocity
    x = float(rocket.body.position[0])/CARTESIAN_SCALE
    y = float(rocket.body.position[1])/CARTESIAN_SCALE
    a = float(rocket.body.angle)/ANGULAR_SCALE
    vx = float(rocket.body.velocity[0])/CARTESIAN_SCALE
    vy = float(rocket.body.velocity[1])/CARTESIAN_SCALE
    va = float(rocket.body.angular_velocity)

    #get base position
    bx = float(base.body.position[0])/CARTESIAN_SCALE
    by = float(base.body.position[1])/CARTESIAN_SCALE

    #calculate rocket state as mentioned in README
    ex = x-bx
    ey = y-by
    ea = a
    evx = vx
    evy = vy
    eva = va

    return [ex,ey,ea,evx,evy,eva]

step_count = 0

def update(dt):
    global nets
    global rockets
    global step_count

    dead_list = []

    step_count += 1

#    if(step_count % 600 == 0):
#        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
#                [BASE_MARGIN,window_height-BASE_MARGIN],
#                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
#                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])


    if(keyboard[pyglet.window.key.SPACE]):
        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                [BASE_MARGIN,window_height-BASE_MARGIN],
                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])

    for i, rocket in enumerate(rockets):
        rocket_images[i].attach(rocket)
        rocket.update()
        states = get_states(rocket)
        output = nets[i].activate(states)
        
        rocket.propel(output)

        if ((rocket.body.position.y < -400) or 
                (rocket.body.position.y > window_height+400) or
                (rocket.body.position.x < -400) or
                (rocket.body.position.x > window_width+400)):
            dead_list.append(i)

#    for i in dead_list:
#        print("removed:",i)
#        rockets[i].remove(space)
#        del nets[i]
#        del rockets[i]
    #    rockets[i] = (Rocket(x_pos = window.width//2, y_pos = window.height//2))
    #    rockets[i].shape.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
    #    rockets[i].shape.sensor = True
    #    rockets[i].insert(space)

    space.step(1.0/60.0)

nets = []
rockets = []
net_paths = []

def run():
    global nets
    global rockets

    for i,path in enumerate(NETWORK_PATH):
        if not os.path.exists(os.path.dirname(path)):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        if (len(path) == 0):
            raise FileNotFoundError("No Networks found")

        nets.append(pickle.load( open(path, "rb" )))

        rockets.append(Rocket(x_pos = window.width//2, y_pos = window.height//2,batch=batch,_id = f"            {net_id[i]}"))
        rocket_images.append(RocketImage(batch=batch))

        rockets[-1].insert(space)
        rockets[-1].visibility(False)
        rocket_images[-1].attach(rockets[-1])

    pyglet.app.run()

#Set pyglet update interval
pyglet.clock.schedule(update)
run()
