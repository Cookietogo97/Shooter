import math
import random

import pygame

from Entity import Entity
from Player import Player


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def draw_polygon(surface, drawable):
    pygame.draw.polygon(surface, drawable['Colour'], drawable['Shape'])


def calculate_lines_for_entity(entity):
    lines = []
    for point in range(len(entity.shape)):
        lines.append(((entity.shape[point][0] + entity.pos_x, entity.shape[point][1] + entity.pos_y),
                      (entity.shape[point + 1 if point != len(entity.shape) - 1 else 0][0] + entity.pos_x,
                       entity.shape[point + 1 if point != len(entity.shape) - 1 else 0][1] + entity.pos_y)))
    return lines


def calculate_collision(entity1: Entity, entity2: Entity):
    for line1 in calculate_lines_for_entity(entity1):
        for line2 in calculate_lines_for_entity(entity2):
            # From https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
            def ccw(a, b, c):
                return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

            if ccw(line1[0], line2[0], line2[1]) != ccw(line1[1], line2[0], line2[1]) \
                    and ccw(line1[0], line1[1], line2[0]) != ccw(line1[0], line1[1], line2[1]):
                return True
    if math.sqrt(
            (entity2.pos_x - entity1.pos_x) ** 2 + (entity2.pos_y - entity1.pos_y) ** 2) < entity1.size + entity2.size:
        return True


def main():
    screen_width = 1280
    screen_height = 720
    score = 0
    pygame.init()
    pygame.display.set_caption('Shooter')

    font = pygame.font.Font(None, 32)

    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True

    clock = pygame.time.Clock()

    player = Player(10, 0, 0, 0, 0, ((0, 0), (0, 30), (30, 15)), screen, 100, 100, 100)
    entities = [player]

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                entities.append(Entity('Bullet', 1, 10, 0, player.pos_x, player.pos_y, ((0, 0), (0, 5), (5, 3)),
                                       screen, 255, 0, 0, 1))

        if random.random() > 0.95:
            entities.append(Entity('Mob', 1, -2, 0, screen_width + 20, random.randint(10, screen_height - 10), ((0, 0), (0, 20), (20, 20), (20, 0)),
                                   screen, 0, 0, 255, 1))

        for entity1 in entities:
            for entity2 in entities:
                if (entity1.entity_type == 'Player' and entity2.entity_type == 'Mob'
                    or entity1.entity_type == 'Bullet' and entity2.entity_type == 'Mob') \
                        and calculate_collision(entity1, entity2):
                    entity1.health -= entity2.contact_damage
                    entity2.health -= entity1.contact_damage
        for entity in entities:
            if entity.health <= 0 and entity.entity_type == 'Mob':
                score += 1
                entities.remove(entity)
            elif entity.health <= 0:
                entities.remove(entity)
                continue
            if entity.entity_type == 'Bullet' and entity.pos_x > screen_width + 20 \
                    or entity.entity_type == 'Mob' and entity.pos_x < -20:
                entities.remove(entity)
                continue
            entity.update()
        for entity in entities:
            entity.draw()
        health_text = font.render(f'Health: {player.health}', False, (0, 0, 0))
        score_text = font.render(f'Score: {score}', False, (0, 0, 0))
        screen.blit(health_text, health_text.get_rect())
        score_rect = score_text.get_rect()
        score_rect.move_ip(screen_width - score_rect.right, 0)
        screen.blit(score_text, score_rect)
        if player.health <= 0:
            game_over_text = font.render('Game Over', False, (204, 34, 0))
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.move_ip(screen_width / 2 - game_over_text_rect.right / 2,
                                        screen_height / 2 - game_over_text_rect.bottom / 2)
            screen.blit(game_over_text, game_over_text_rect)
        pygame.display.update()
        screen.fill((255, 255, 255))


if __name__ == "__main__":
    main()
