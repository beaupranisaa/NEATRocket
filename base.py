import pymunk
import random

class Base:
    def __init__(self, height = 200, aspect_ratio = 0.12, x_pos = 0, y_pos = 0):
        # set base body and shape
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.height = height
        self.aspect_ratio = aspect_ratio
        self.diameter = int(self.height*self.aspect_ratio)
        self.shape = pymunk.Poly.create_box(self.body,size=(self.diameter,self.height))

        # set base's position
        self.body.position = x_pos, y_pos

        # set sensor = True to not handle collisions
        self.shape.sensor = True

    def insert(self,space):
        # add base to space
        space.add(self.body,self.shape)

    def random_position(self, x_range, y_range, not_x_range = [0,0], not_y_range=[0,0]):
        # randomly position the base

        # not x and not y should be a smaller window than x and y ranges
        if not ((x_range[0] < not_x_range[0]) or 
                (x_range[1] > not_x_range[1]) or
                (y_range[0] < not_y_range[0]) or
                (y_range[1] > not_y_range[1])):
            raise ValueError("Invalid position ranges")

        x_pos = random.randint(x_range[0],x_range[1])
        y_pos = random.randint(y_range[0],y_range[1])

        while((x_pos > not_x_range[0]) and 
                (x_pos < not_x_range[1]) and 
                (y_pos > not_y_range[0]) and 
                (y_pos < not_y_range[1])):
            x_pos = random.randint(x_range[0],x_range[1])
            y_pos = random.randint(y_range[0],y_range[1])

        #print(x_pos,y_pos)
        self.body.position = x_pos, y_pos




