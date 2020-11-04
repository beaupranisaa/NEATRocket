#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
import neat
import os
import random
import pickle
import glob
import sys

from rocket import Rocket
from base import Base

if len(sys.argv) == 2:
    NETWORK_DIR = sys.argv[1]
elif len(sys.argv) > 2:
    raise "Too many directories to write to"
else:
    NETWORK_DIR = 'networksTest/'

#setup the window
window_width = 1366
window_height = 768
window = pyglet.window.Window(window_width,window_height)
#window = pyglet.window.Window(fullscreen = True)
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
base = Base(x_pos = window_width//2,y_pos = window_height//2)
base.insert(space)

#state scale
CARTESIAN_SCALE = 200.0
ANGULAR_SCALE = 1.0/2.0

#global variables for simulation and training
genomess = []
nets = []
rockets = []
step_count = 0
dead_rockets = []
generation = 0
best_fitness = -float('inf')

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

def get_fitness(states):
    state_weights = [1,1,1,0,0,0]
    s = 0
    for i, (state,state_weights) in enumerate(zip(states,state_weights)):
        s += state_weights*(state**2)
    return s

def get_fitness2(states):
    state_weights = [1,1,1,0,0,0]
    s = 0
    for i, (state,state_weights) in enumerate(zip(states,state_weights)):
        s += state_weights*(abs(state))
    return s

def eval_genomes(genomes, config):
    #this function runs once a generation
    global genomess
    global rockets
    global nets
    global dead_rockets

    dead_rockets = []
    rockets = []
    nets = []

    for i, (genome_id, genome) in enumerate(genomes):
        genomess.append(genome)
        genomess[-1].fitness = 0
        rockets.append(Rocket(x_pos = window.width//2, y_pos = window.height//2, lateral_force = 1000))
        rockets[-1].shape.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255), 100.0)
        rockets[-1].shape.sensor = True

        rockets[-1].insert(space)

        dead_rockets.append(0)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))

    pyglet.app.run()

    base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
            [BASE_MARGIN,window_height-BASE_MARGIN],
            [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
            [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])

def update(dt):
    global nets
    global step_count
    global genomess
    global rockets
    global dead_rockets
    global generation
    global best_fitness

    step_count += 1

    if(((step_count) >= 60*20) or (sum(dead_rockets) == 100)):
        best_fitness_idx = -1
        best_fitness = -float('inf')
        for i,genome in enumerate(genomess):
            genome.fitness -= (60*20-step_count)*5
            if best_fitness < genome.fitness:
                best_fitness = genome.fitness
                best_fitness_idx = i
        
        if best_fitness_idx != -1:
            print("Saving Network")
            pickle.dump(nets[best_fitness_idx],open(f"{NETWORK_DIR}/Net_{generation}.p","wb"))

        for rocket in rockets:
            rocket.remove(space)

        pyglet.app.exit()
        generation += 1
        nets = []
        step_count = 0
        genomess = []
        rockets = []

    if((step_count % 300 == 0)):
        base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                [BASE_MARGIN,window_height-BASE_MARGIN],
                [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])

    # apply force to every rocket
    for i, net in enumerate(nets):
        states = get_states(rockets[i])
        output = net.activate(states)

       # output_fitness = 0
       # 
       # for value in output:
       #     output_fitness += value**2

        genomess[i].fitness = genomess[i].fitness - get_fitness2(states)
        rockets[i].propel(output)

        if ((rockets[i].body.position.y < -100) or 
                (rockets[i].body.position.y > window_height+100) or
                (rockets[i].body.position.x < -100) or
                (rockets[i].body.position.x > window_width+100)):
            dead_rockets[i] = 1
            #rockets[i].remove(space)
            #genomess[i].fitness = genomess[i].fitness - 10

    space.step(1.0/60.0)


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 3000 generations.
    winner = p.run(eval_genomes, 3000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

#Set pyglet update interval
pyglet.clock.schedule(update)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')

if not os.path.exists(os.path.dirname(NETWORK_DIR)):
    os.makedirs(os.path.dirname(NETWORK_DIR))
else:
    net_paths = glob.glob(f"{NETWORK_DIR}Net*")
    for paths in net_paths:
        os.remove(paths)

run(config_path)
