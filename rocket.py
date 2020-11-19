import pymunk
import random
import pyglet

class Rocket:
    def __init__(self, mass = 1, height = 200, aspect_ratio = 0.12, friction = 0.3, elasticity = 0.2, x_pos= 0, y_pos = 0, longitudinal_force = 2500, lateral_force = 200):
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

        self.LONGITUDINAL_FORCE = longitudinal_force
        self.LATERAL_FORCE = lateral_force

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


class RocketImage:
    def __init__(self):
        self.rocket_img = pyglet.image.load("img/rocket2.png")  # .convert_alpha()
        self.rocket_img.anchor_x =  380//2 #self.rocket_img.width//2
        self.rocket_img.anchor_y =  480//2 #®self.rocket_img.height//2
        self.rocket_height, self.rocket_width = 400,400
        self.texture = self.rocket_img.get_texture()
        self.texture.width = self.rocket_width
        self.texture.height = self.rocket_height

        self.rocket_sprite = pyglet.sprite.Sprite(self.rocket_img, x=0, y=0)

    def attach(self,rocket):
        self.rocket_sprite.update(rocket.body.position.x, rocket.body.position.y, -float(rocket.body.angle) * 180 / 3.1416)






