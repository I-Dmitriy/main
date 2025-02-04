import sys

import pygame
import os

FPS = 50
pygame.init()
pygame.display.set_caption('MARIO')
pygame.key.set_repeat(200, 70)
size = width, height = WIDTH, HEIGHT = 1000, 400
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Вниз или вверх чтобы управлять"]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def mover(self, tx):
        self.rect = self.rect.move(tx, 0)

    def update(self, *args):
        if args:
            key = args[0].key
            rect = self.rect
            if key == pygame.K_UP:
                self.rect = self.rect.move(0, -tile_height)
            elif key == pygame.K_DOWN:
                self.rect = self.rect.move(0, tile_height)

            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect = rect


class Camera:

    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x > width:
            obj.rect.x -= width
        elif obj.rect.x < 0:
            obj.rect.x += width
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)

                new_player = Player(x, y)

    return new_player, x, y


if __name__ == '__main__':
    start_screen()
    player, level_x, level_y = generate_level(load_level('level_0.txt'))
    tx = 5
    v = 10

    clock = pygame.time.Clock()
    camera = Camera()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                tx += 10
                player_group.update(event)
        screen.fill('green')

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)
        player.mover(tx)
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()
