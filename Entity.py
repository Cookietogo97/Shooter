import pygame


class Entity(object):

    def __init__(self, entity_type: str, health: int, speed_x: int, speed_y: int, pos_x: int, pos_y: int, shape: (),
                 surface: pygame.Surface, red: int, green: int, blue: int, contact_damage):
        self.blue = blue
        self.green = green
        self.red = red
        self.entity_type = entity_type
        self.health = health
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shape = shape
        self.surface = surface
        self.contact_damage = contact_damage
        self.size = 0
        self.set_origin_center()

    def got_hit(self, damage: int):
        self.health -= damage

    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

    def draw(self):
        entity = []
        for point in self.shape:
            entity.append((point[0] + self.pos_x, point[1] + self.pos_y))
        pygame.draw.polygon(self.surface, (self.red, self.green, self.blue), entity)

    def set_origin_center(self):
        bottom = 0
        right = 0
        for point in self.shape:
            if point[0] > right:
                right = point[0]
            if point[1] > bottom:
                bottom = point[0]
        center = (right / 2, bottom / 2)
        new_shape = []
        for point in self.shape:
            new_shape.append((point[0] - center[0], point[1] - center[1]))
        self.shape = new_shape
        self.size = right
