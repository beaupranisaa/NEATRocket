#!/usr/bin/python3

import numpy as np 
import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
import neat
import os
import random
import pickle

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

genomess = []
nets = []
rockets = []
step_count = 0
dead_rockets = []
generation = 0
best_fitness = -float('inf')


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
        rockets.append(Rocket(x_pos = window.width//2, y_pos = window.height//2))
        rockets[-1].shape.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
        rockets[-1].shape.sensor = True

        rockets[-1].insert(space)
        dead_rockets.append(0)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))

    base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
            [BASE_MARGIN,window_height-BASE_MARGIN],
            [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
            [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])

    pyglet.app.run()

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
        for i,genome in enumerate(genomess):
            genome.fitness -= (60*20-step_count)
            print(best_fitness,genome.fitness)
            if best_fitness < genome.fitness:
                best_fitness = genome.fitness
                best_fitness_idx = i
        
        if best_fitness_idx != -1:
            print("Saving Network")
            pickle.dump(nets[best_fitness_idx],open(f"{NETWORK_DIR}/Net{generation}.p","wb"))

        for rocket in rockets:
            rocket.remove(space)

        pyglet.app.exit()
        generation += 1
        nets = []
        step_count = 0
        genomess = []
        rockets = []

    # apply force to every rocket
    for i, net in enumerate(nets):
        states = get_states(rockets[i])
        output = net.activate(states)
        output_fitness = 0

        if((step_count % 300 == 0) and (i == 0)):
            base.random_position([BASE_MARGIN,window_width-BASE_MARGIN],
                    [BASE_MARGIN,window_height-BASE_MARGIN],
                    [window_width//2-NOT_BASE_MARGIN//2,window_width//2+NOT_BASE_MARGIN//2],
                    [window_height//2-NOT_BASE_MARGIN//2,window_height//2+NOT_BASE_MARGIN//2])
            #print(genomess[i].fitness)
            #print(output)
            pass
        
        for value in output:
            output_fitness += value**2
        genomess[i].fitness = genomess[i].fitness - get_l2_norm(states)
        propel_rocket(rockets[i],output)

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
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 3000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


#Set pyglet update interval
pyglet.clock.schedule(update)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')

if not os.path.exists(os.path.dirname(NETWORK_DIR)):
    os.makedirs(os.path.dirname(NETWORK_DIR))

run(config_path)





























