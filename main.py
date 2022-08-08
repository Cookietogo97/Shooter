import pygame

from Player import Player


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def draw_polygon(surface, drawable):
    pygame.draw.polygon(surface, drawable['Colour'], drawable['Shape'])


def calculate_collision(obj1, obj2):
    for point1 in range(len(obj1['Shape'])):
        if point1 != len(obj1['Shape']) - 1:
            line1 = (obj1['Shape'][point1], obj1['Shape'][point1 + 1])
        else:
            line1 = (obj1['Shape'][point1], obj1['Shape'][0])
        for point2 in range(len(obj2['Shape'])):
            if point2 != len(obj2['Shape']) - 1:
                line2 = (obj2['Shape'][point2], obj2['Shape'][point2 + 1])
            else:
                line2 = (obj2['Shape'][point2], obj2['Shape'][0])

            # From https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
            def ccw(a, b, c):
                return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

            if ccw(line1[0], line2[0], line2[1]) != ccw(line1[1], line2[0], line2[1]) and ccw(line1[0], line1[1], line2[0]) != ccw(line1[0], line1[1], line2[1]):
                return True


def create_bullet(position):
    return dict(Type='Bullet', Shape=([position[0], position[1]], [position[0], position[1] + 5], [position[0] + 5, position[1] + 2.5]), XSpeed=20, YSpeed=0, Colour=(0, 0, 0))


# def handle_bullet_collisions():
#     for entity1 in entities:
#         for entity2 in entities:
#             if entity1['Type'] == 'Bullet' and entity2['Type'] == 'Mob':
#                 if calculate_collision(entity1, entity2):
#                     entities.remove(entity2)


def main():
    pygame.init()
    pygame.display.set_caption('Shooter')

    screen = pygame.display.set_mode((720, 360))

    running = True

    clock = pygame.time.Clock()

    player = Player(10, 10, 10, 10, 10, ((0, 0), (0, 30), (30, 15)), screen, 100, 100, 100)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player.update()
        player.draw()
        pygame.display.update()
        screen.fill((255, 255, 255))


if __name__ == "__main__":
    main()
