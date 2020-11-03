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

from rocket import Rocket
from base import Base

NETWORK_DIR = 'networks/'

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

def get_states(rocket):
    #get rocket's current position and velocity
    x = float(rocket.body.position[0])/window_width
    y = float(rocket.body.position[1])/window_height
    a = float(rocket.body.angle)
    vx = float(rocket.body.velocity[0])/window_width
    vy = float(rocket.body.velocity[1])/window_height
    va = float(rocket.body.angular_velocity)

    #get base position
    bx = float(base.body.position[0])/window_width
    by = float(base.body.position[1])/window_height

    #calculate rocket state as mentioned in README
    ex = x-bx
    ey = y-by
    ea = a
    evx = vx
    evy = vy
    eva = va

    return [ex,ey,ea,evx,evy,eva]

def get_l2_norm(states):
    s = 0
    for i, state in enumerate(states):
        if(i == 3):
            break
        s += state**2
    return s

def propel_rocket(rocket, output):
    #output is a list of output states [longitudinal, upper lateral, lower lateral]
    #longitudinal thruster
    if output[0] > 0:
        rocket.body.apply_force_at_local_point((0,output[0]*2500),(0,-rocket.height//2))

    upper_lateral_force = 0.0
    lower_lateral_force = 0.0

    LATERAL_FORCE = 500.0

    #upper thruster
    if output[1] > 0:
        upper_lateral_force += output[1]*LATERAL_FORCE
        #lower_lateral_force += output[1]*LATERAL_FORCE
    elif output[1] < 0:
        upper_lateral_force -= -output[1]*LATERAL_FORCE
        #lower_lateral_force -= -output[1]*LATERAL_FORCE

    #lower thruster
#    if output[2] > 0:
#        upper_lateral_force += output[2]*LATERAL_FORCE
#        lower_lateral_force -= output[2]*LATERAL_FORCE
#    elif output[2] < 0:
#        upper_lateral_force -= -output[2]*LATERAL_FORCE
#        lower_lateral_force += -output[2]*LATERAL_FORCE

    rocket.body.apply_force_at_local_point((upper_lateral_force,0),(0,rocket.height//2))
    #rocket.body.apply_force_at_local_point((lower_lateral_force,0),(0,-rocket.height//2)) 

step_count = 0

def update(dt):
    global nets
    global rockets
    global step_count

    dead_list = []

    step_count += 1

    if(step_count % 300 == 0):
        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                [BASE_MARGIN,window_height-BASE_MARGIN],
                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])


    for i, rocket in enumerate(rockets):
        states = get_states(rocket)
        output = nets[i].activate(states)
        
        propel_rocket(rocket,output)

        if ((rocket.body.position.y < -100) or 
                (rocket.body.position.y > window_height+100) or
                (rocket.body.position.x < -100) or
                (rocket.body.position.x > window_width+100)):
            rocket.remove(space)
            dead_list.append(i)

    for i in dead_list:
        rockets[i] = (Rocket(x_pos = window.width//2, y_pos = window.height//2))
        rockets[i].shape.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
        rockets[i].shape.sensor = True
        rockets[i].insert(space)

    space.step(1.0/60.0)

nets = []
rockets = []

def run():
    global nets
    global rockets

    net_paths = glob.glob(f"{NETWORK_DIR}Net*")
    if (len(net_paths) == 0):
        raise FileNotFoundError("No Networks found")

    for net in net_paths:
        nets.append(pickle.load( open(net, "rb" )))

        rockets.append(Rocket(x_pos = window.width//2, y_pos = window.height//2))
        rockets[-1].shape.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
        rockets[-1].shape.sensor = True
        rockets[-1].insert(space)

    pyglet.app.run()

#Set pyglet update interval
pyglet.clock.schedule(update)

if not os.path.exists(os.path.dirname(NETWORK_DIR)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

run()
