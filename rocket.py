import pymunk
import random
import pyglet
import cv2

class Rocket:
    def __init__(self,batch, mass = 1, height = 200, aspect_ratio = 0.115, friction = 0.3, elasticity = 0.2, x_pos= 0, y_pos = 0, longitudinal_force = 2500, lateral_force = 400, _id = None):
        # set rocket's pysical properties
        self.mass = mass
        self.aspect_ratio = aspect_ratio
        self.height = height
        self.diameter = int(self.height*self.aspect_ratio)
        self.moment = pymunk.moment_for_box(self.mass,(self.diameter,self.height))
        self.body = pymunk.Body(self.mass,self.moment)
        self.upper_lateral_force = 0.0
        self.lower_lateral_force = 0.0
        self.longitudinal_force = 0.0
        self.id = _id

        self.shape = pyglet.shapes.Rectangle(0,0,self.diameter,self.height, batch = batch)
        self.shape.anchor_position = (self.diameter//2,self.height//2)
        self.shape.color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.shape.opacity = 100

        self.label = pyglet.text.Label("",x=100,y=100,anchor_x='center',anchor_y = 'center',batch=batch)
        if (self.id):
            self.label.text = str(self.id)

        self.label.opacity = 100

        self.friction = friction
        self.elasticity = elasticity

        self.LONGITUDINAL_FORCE = longitudinal_force
        self.LATERAL_FORCE = lateral_force

        # set rocket's  initial position
        self.body.position = x_pos, y_pos
        self.body.angle = 0.01
        self.body.velocity = 0.0,0.0
        self.body.angular_velocity = random.uniform(-0.1,0.1)

    def update(self,text = None):
        self.shape.position = (self.body.position.x, self.body.position.y)
        self.shape.rotation = -float(self.body.angle)*180/3.1416

        self.label.x = self.body.position.x
        self.label.y = self.body.position.y 

        if text:
            self.label.text  = str(text)

    def visibility(self,visible = True):
        self.shape.visible = visible

    def insert(self,space):
        #space.add(self.body, self.shape)
        space.add(self.body)

    def remove(self,space):
        space.remove(self.body)
        self.label.delete()
        self.shape.delete()

    def propel(self, output):
        #output is a list of output states [longitudinal, upper lateral, lower lateral]
        self.upper_lateral_force = 0.0
        self.lower_lateral_force = 0.0
        self.longitudinal_force = 0.0

        self.longitudinal_force += max(0,output[0])*self.LONGITUDINAL_FORCE
        self.upper_lateral_force += output[1]*self.LATERAL_FORCE

        if len(output) == 3:
            self.lower_lateral_force -= output[2]*self.LATERAL_FORCE

        self.body.apply_force_at_local_point((0,self.longitudinal_force),(0,-self.height//2))
        self.body.apply_force_at_local_point((self.lower_lateral_force,0),(0,-self.height//2)) 
        self.body.apply_force_at_local_point((self.upper_lateral_force,0),(0,self.height//2))


class RocketImage:
    def __init__(self, batch = None):
        self.rocket_img = pyglet.image.load("img/falcon9_first_stage_resized.png")  # .convert_alpha()
        self.rocket_img.anchor_x =  self.rocket_img.width//2
        self.rocket_img.anchor_y =  self.rocket_img.height//2

        self.exhaust_img = pyglet.image.load("img/exhaust_flame_resized.png")
        self.exhaust_img.anchor_x =  self.exhaust_img.width//2
        self.exhaust_img.anchor_y =  self.exhaust_img.height + self.rocket_img.height//2

        self.booster_left_img = pyglet.image.load("img/exhaust_flame_resized_2.png")
        self.booster_left_img.anchor_x =  self.booster_left_img.width//2 + self.rocket_img.height//2 - 10
        self.booster_left_img.anchor_y =  self.booster_left_img.height//2 + 70

        self.booster_right_img = pyglet.image.load("img/exhaust_flame_resized_2.png")
        self.booster_right_img.anchor_x =  self.booster_right_img.width//2 - self.rocket_img.height//2 + 10
        self.booster_right_img.anchor_y =  self.booster_right_img.height//2 + 70

        self.booster2_left_img = pyglet.image.load("img/exhaust_flame_resized_2.png")
        self.booster2_left_img.anchor_x =  self.booster2_left_img.width//2 + self.rocket_img.height//2 - 10
        self.booster2_left_img.anchor_y =  self.booster2_left_img.height//2 + 70

        self.booster2_right_img = pyglet.image.load("img/exhaust_flame_resized_2.png")
        self.booster2_right_img.anchor_x =  self.booster2_right_img.width//2 - self.rocket_img.height//2 + 10
        self.booster2_right_img.anchor_y =  self.booster2_right_img.height//2 + 70
#        self.rocket_height, self.rocket_width = 5414,414
#        self.texture = self.rocket_img.get_texture()
#        self.texture.width = self.rocket_width
#        self.texture.height = self.rocket_height

        if batch:
            self.rocket_sprite = pyglet.sprite.Sprite(self.rocket_img, x=0, y=0, batch = batch)
            self.exhaust_sprite = pyglet.sprite.Sprite(self.exhaust_img, x=0, y=0, batch = batch)
            self.booster_left_sprite = pyglet.sprite.Sprite(self.booster_left_img, x=0, y=0, batch = batch)
            self.booster_right_sprite = pyglet.sprite.Sprite(self.booster_right_img, x=0, y=0, batch = batch)
            self.booster2_left_sprite = pyglet.sprite.Sprite(self.booster2_left_img, x=0, y=0, batch = batch)
            self.booster2_right_sprite = pyglet.sprite.Sprite(self.booster2_right_img, x=0, y=0, batch = batch)
        else:
            self.rocket_sprite = pyglet.sprite.Sprite(self.rocket_img, x=0, y=0)
            self.exhaust_sprite = pyglet.sprite.Sprite(self.exhaust_img, x=0, y=0)
            self.booster_left_sprite = pyglet.sprite.Sprite(self.booster_left_img, x=0, y=0)
            self.booster_right_sprite = pyglet.sprite.Sprite(self.booster_right_img, x=0, y=0)
            self.booster2_left_sprite = pyglet.sprite.Sprite(self.booster_left_img, x=0, y=0)
            self.booster2_right_sprite = pyglet.sprite.Sprite(self.booster_right_img, x=0, y=0)

    def attach(self,rocket):
        opacity = random.randint(100,255)

        self.rocket_sprite.update(rocket.body.position.x, rocket.body.position.y, -float(rocket.body.angle) * 180 / 3.1416)
        self.exhaust_sprite.update(rocket.body.position.x, rocket.body.position.y, -float(rocket.body.angle) * 180 / 3.1416)
        self.booster_left_sprite.update(rocket.body.position.x, rocket.body.position.y, 90-float(rocket.body.angle) * 180 / 3.1416)
        self.booster_right_sprite.update(rocket.body.position.x, rocket.body.position.y, -90-float(rocket.body.angle) * 180 / 3.1416)

        self.booster2_left_sprite.update(rocket.body.position.x, rocket.body.position.y, -90-float(rocket.body.angle) * 180 / 3.1416)
        self.booster2_right_sprite.update(rocket.body.position.x, rocket.body.position.y, 90-float(rocket.body.angle) * 180 / 3.1416)

        self.exhaust_sprite.opacity = opacity
        self.booster_left_sprite.opacity = opacity
        self.booster_right_sprite.opacity = opacity

        if(rocket.longitudinal_force > 10):
            self.exhaust_sprite.visible = True
        else:
            self.exhaust_sprite.visible = False

        if(rocket.upper_lateral_force > 50):
            self.booster_left_sprite.visible = True
            self.booster_right_sprite.visible = False
        elif(rocket.upper_lateral_force < -50):
            self.booster_right_sprite.visible = True
            self.booster_left_sprite.visible = False
        else:
            self.booster_right_sprite.visible = False
            self.booster_left_sprite.visible = False

        if(rocket.lower_lateral_force < -50):
            self.booster2_left_sprite.visible = True
            self.booster2_right_sprite.visible = False
        elif(rocket.lower_lateral_force > 50):
            self.booster2_right_sprite.visible = True
            self.booster2_left_sprite.visible = False
        else:
            self.booster2_right_sprite.visible = False
            self.booster2_left_sprite.visible = False





