#!/home/rom/Desktop/AIT/ML/bin/python3

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

#Create a rocket
rocket_mass = 1
rocket_aspect_ratio = 0.12
rocket_height = 200
rocket_diameter = int(rocket_height*rocket_aspect_ratio)
rocket_moment = pymunk.moment_for_box(rocket_mass,(rocket_diameter,rocket_height))
rocket_body = pymunk.Body(rocket_mass,rocket_moment)
rocket_shape = pymunk.Poly.create_box(rocket_body,size=(rocket_diameter,rocket_height))
rocket_body.position = window.width/2, window.height/2
rocket_body.angle = 0.01
rocket_body.velocity = 0.0,0.0
rocket_body.angular_velocity = 0.0
rocket_shape.friction = 0.3
rocket_shape.elasticity = 0.2
space.add(rocket_body,rocket_shape)

#TODO: Create a base
base_body = pymunk.Body(body_type=pymunk.Body.STATIC)
base_shape = pymunk.Segment(base_body,(0,0),(100,0),2)
base_body.position = 600,100
base_shape.elasticity = 1.0
base_shape.friction = 1.0
space.add(base_body,base_shape)


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
    if(keyboard[pyglet.window.key.UP]):
        rocket_body.apply_force_at_local_point((0,1500),(0,-rocket_height//2))
    if(keyboard[pyglet.window.key.RIGHT]):
        rocket_body.apply_force_at_local_point((100,0),(0,rocket_height//2))
    if(keyboard[pyglet.window.key.LEFT]):
        rocket_body.apply_force_at_local_point((-100,0),(0,rocket_height//2))
    if(keyboard[pyglet.window.key.DOWN]):
        rocket_body.apply_force_at_local_point((0,3000),(0,-rocket_height//2))

    for shape in space.shapes:
        if shape.body.position.y < -100:
            rocket_body.position = window.width/2, window.height/2
            rocket_body.angle = 0.01
            rocket_body.velocity = 0.0,0.0
            rocket_body.angular_velocity = 0.0
            #space.remove(shape.body,shape)
            #print("removed:",shape)
            
    space.step(dt)

#Set pyglet update interval
pyglet.clock.schedule_interval(update,1.0/120)
pyglet.app.run()
