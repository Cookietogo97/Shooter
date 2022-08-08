import pygame


class Entity(object):

    def __init__(self, entity_type: str, health: int, speed_x: int, speed_y: int, pos_x: int, pos_y: int, shape: (),
                 surface: pygame.Surface, red: int, green: int, blue: int):
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

    def got_hit(self, damage: int):
        self.health -= damage

    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

    def draw(self):
        entity = []
        for point in self.shape:
            entity.append((point[0] + self.speed_x, point[1] + self.speed_y))
        pygame.draw.polygon(self.surface, (self.red, self.green, self.blue), entity)
