import pymunk
import random

class Rocket:
    def __init__(self, mass = 1, height = 200, aspect_ratio = 0.12, friction = 0.3, elasticity = 0.2, x_pos= 0, y_pos = 0):
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
        self.body.position = x_pos, y_pos
        self.body.angle = 0.01
        self.body.velocity = 0.0,0.0
        self.body.angular_velocity = random.uniform(-0.1,0.1)

    def insert(self,space):
        space.add(self.body, self.shape)

    def remove(self,space):
        space.remove(self.body, self.shape)

