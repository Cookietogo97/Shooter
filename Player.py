import pygame.key

from Entity import Entity


class Player(Entity):
    def __init__(self, health: int, speed_x: int, speed_y: int, pos_x: int, pos_y: int, shape: (),
                 surface: pygame.Surface, red: int, green: int, blue: int):
        super().__init__('Player', health, speed_x, speed_y, pos_x, pos_y, shape, surface, red, green, blue, 1)
        self.shot_delay = 100
        self.timer = pygame.time.get_ticks()
        self.size = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed_y = -10
        if keys[pygame.K_DOWN]:
            self.speed_y = 10
        if keys[pygame.K_LEFT]:
            self.speed_x = -10
        if keys[pygame.K_RIGHT]:
            self.speed_x = 10
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.timer > self.shot_delay:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, name='New Bullet'))
                self.timer = pygame.time.get_ticks()
        super().update()
        self.speed_x = 0
        self.speed_y = 0
