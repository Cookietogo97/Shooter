import pygame


entities = []


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def handle_input_for_object(obj):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        obj['YSpeed'] = -10
    if keys[pygame.K_DOWN]:
        obj['YSpeed'] = 10
    if keys[pygame.K_LEFT]:
        obj['XSpeed'] = -10
    if keys[pygame.K_RIGHT]:
        obj['XSpeed'] = 10
    if keys[pygame.K_SPACE]:
        entities.append(create_bullet((50, 180)))


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


def move_entities():
    for entity in entities:
        for point in entity['Shape']:
            point[0] += entity['XSpeed']
            point[1] += entity['YSpeed']


def handle_bullet_collisions():
    for entity1 in entities:
        for entity2 in entities:
            if entity1['Type'] == 'Bullet' and entity2['Type'] == 'Mob':
                if calculate_collision(entity1, entity2):
                    entities.remove(entity2)


def main():
    player = dict(Type='Player', Shape=([0, 0], [0, 50], [50, 25]), XSpeed=0, YSpeed=0, Colour=(0, 255, 0))
    bloc = dict(Type='Mob', Shape=([350, 180], [350, 220], [390, 220], [390, 180]), XSpeed=0, YSpeed=0, Colour=(255, 0, 0))
    entities.append(player)
    entities.append(bloc)
    print(player['Shape'])
    print(len(player['Shape']))
    pygame.init()
    pygame.display.set_caption('Shooter')

    screen = pygame.display.set_mode((720, 360))

    running = True

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        running = handle_events()
        handle_input_for_object(player)
        move_entities()
        player['XSpeed'] = 0
        player['YSpeed'] = 0
        handle_bullet_collisions()
        for entity in entities:
            draw_polygon(screen, entity)
        if calculate_collision(player, bloc):
            running = False
        pygame.display.update()
        screen.fill((255, 255, 255))


if __name__ == "__main__":
    main()
