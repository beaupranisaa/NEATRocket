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

        self.LONGITUDINAL_FORCE = 2500
        self.LATERAL_FORCE = 200.0

        # set rocket's  initial position
        self.body.position = x_pos, y_pos
        self.body.angle = 0.01
        self.body.velocity = 0.0,0.0
        self.body.angular_velocity = random.uniform(-0.1,0.1)

    def insert(self,space):
        space.add(self.body, self.shape)

    def remove(self,space):
        space.remove(self.body, self.shape)

    def propel(self, output):
        #output is a list of output states [longitudinal, upper lateral, lower lateral]
        upper_lateral_force = 0.0
        lower_lateral_force = 0.0
        longitudinal_force = 0.0

        longitudinal_force += max(0,output[0])*self.LONGITUDINAL_FORCE
        upper_lateral_force += output[1]*self.LATERAL_FORCE

        if len(output) == 3:
            lower_lateral_force -= output[2]*self.LATERAL_FORCE

        self.body.apply_force_at_local_point((0,longitudinal_force),(0,-self.height//2))
        self.body.apply_force_at_local_point((lower_lateral_force,0),(0,-self.height//2)) 
        self.body.apply_force_at_local_point((upper_lateral_force,0),(0,self.height//2))
