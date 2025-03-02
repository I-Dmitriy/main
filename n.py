import sys
import random
import pygame
import os

retry = 1
level = 0
while retry >= 1:
    FPS = 50
    pygame.init()
    pygame.display.set_caption('Игра "Яндекс доставка"')
    pygame.key.set_repeat(200, 70)
    size = width, height = WIDTH, HEIGHT = 500, 1000
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    left_right = 1


    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        size = width, height = WIDTH, HEIGHT = 1000, 1000
        button_retry = pygame.Rect(300, 700, 400, 100)
        button_quit = pygame.Rect(300, 810, 400, 100)
        screen = pygame.display.set_mode(size)
        with open("score.txt", "r") as f:
            scores = f.readlines()
            best_score1 = int(scores[0])
            best_score2 = int(scores[1])
            best_score3 = int(scores[2])
            best_score4 = int(scores[3])
            best_score5 = int(scores[4])
            best_score6 = int(scores[5])
            best_score7 = int(scores[6])
            best_score8 = int(scores[7])
            best_score9 = int(scores[8])
            best_score10 = int(scores[9])

        intro_text = ["Вправо или влево чтобы управлять",
                      f"Рекорд 1 уровня: {best_score1}, Рекорд 2 уровня: {best_score2}",
                      f"Рекорд 3 уровня: {best_score3}, Рекорд 4 уровня: {best_score4}",
                      f"Рекорд 5 уровня: {best_score5}, Рекорд 6 уровня: {best_score6}",
                      f"Рекорд 7 уровня: {best_score7}, Рекорд 8 уровня: {best_score8}",
                      f"Рекорд 9 уровня: {best_score9}, Рекорд 10 уровня: {best_score10}"
                      ]
        clock = pygame.time.Clock()
        fon = pygame.transform.scale(load_image('Fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 60)
        text_coord = 10
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_retry.collidepoint(event.pos):
                            return True
                        if button_quit.collidepoint(event.pos):
                            return False
            if button_retry.collidepoint(pygame.mouse.get_pos()):  
                pygame.draw.rect(screen, 'red', button_retry)
            elif button_quit.collidepoint(pygame.mouse.get_pos()): 
                pygame.draw.rect(screen, 'red', button_quit)
            else:
                pygame.draw.rect(screen, 'yellow', button_retry)
                pygame.draw.rect(screen, 'yellow', button_quit)

                # Обычный цвет кнопки

                # Отрисовка текста на кнопке
            font = pygame.font.Font(None, 36)
            text = font.render("начать", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_retry.center)
            screen.blit(text, text_rect)

            font = pygame.font.Font(None, 36)
            text = font.render("выйти", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_quit.center)
            screen.blit(text, text_rect)
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
        'wall': load_image('barrier.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('player.png')

    tile_width = tile_height = 50


    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            self.pos_x = pos_x
            self.pos_y = pos_y
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
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
                tile_width * pos_x, tile_height * pos_y + 5)
            self.start_coords = [tile_width * pos_x, tile_height * pos_y + 5]

        def mover(self, tx):

            rect = self.rect
            self.rect = self.rect.move(0, tx)

            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect = rect
                return False
            return True

        def update(self, *args):
            global left_right
            if args:
                key = args[0].key
                rect = self.rect
                if key == pygame.K_RIGHT or key == pygame.K_d:
                    self.rect = self.rect.move(tile_width, 0)
                    if left_right == 1:
                        pass
                    else:
                        self.image = pygame.transform.flip(self.image, True, False)
                        screen.blit(self.image, ((500 - 50) // 2, (1000 - 50) // 2))
                        pygame.display.flip()
                        left_right = 1
                elif key == pygame.K_LEFT or key == pygame.K_a:
                    self.rect = self.rect.move(-tile_width, 0)
                    if left_right == 0:
                        pass
                    else:
                        self.image = pygame.transform.flip(self.image, True, False)
                        screen.blit(self.image, ((500 - 50) // 2, (1000 - 50) // 2))
                        pygame.display.flip()
                        left_right = 0

                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect = rect


    class Camera:

        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            obj.rect.x += self.dx
            if obj.rect.y > height:
                obj.rect.y -= height
            elif obj.rect.y < 0:
                obj.rect.y += height
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


    def end_screen(score):
        button_retry = pygame.Rect(300, 700, 400, 100)
        button_quit = pygame.Rect(300, 810, 400, 100)
        size = width, height = WIDTH, HEIGHT = 1010, 1000
        screen = pygame.display.set_mode(size)
        with open("score.txt", "r") as f:
            scores = f.readlines()
            best_score = int(scores[level])
        if score > best_score:
            if level < 9:
                scores[level] = str(score) + '\n'
            else:
                scores[level] = str(score)
            best_score = score

            with open("score.txt", 'w') as file:
                file.writelines(scores)


        intro_text = [f"Ваш счёт: {score}", f"Рекорд {level + 1} уровня: {best_score}"]
        clock = pygame.time.Clock()
        fon = pygame.transform.scale(load_image('Fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 65)
        text_coord = 10
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()

            intro_rect.top = text_coord
            intro_rect.x += 305
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_retry.collidepoint(event.pos):
                            return True
                        if button_quit.collidepoint(event.pos):
                            return False
            if button_retry.collidepoint(pygame.mouse.get_pos()):  
                pygame.draw.rect(screen, 'red', button_retry)
            elif button_quit.collidepoint(pygame.mouse.get_pos()):  
                pygame.draw.rect(screen, 'red', button_quit)
            else:
                pygame.draw.rect(screen, 'yellow', button_retry)
                pygame.draw.rect(screen, 'yellow', button_quit)

                # Обычный цвет кнопки

                # Отрисовка текста на кнопке
            font = pygame.font.Font(None, 36)
            text = font.render("заново", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_retry.center)
            screen.blit(text, text_rect)

            font = pygame.font.Font(None, 36)
            text = font.render("выйти", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_quit.center)
            screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(FPS)


    if __name__ == '__main__':
        levels = random.choice(
            ['level_1.txt', 'level_2.txt', 'level_3.txt', 'level_4.txt', 'level_5.txt', 'level_6.txt',
             'level_7.txt', 'level_8.txt', 'level_9.txt', 'level_10.txt'])
        if levels == "level_2.txt":
            level = 1
        elif levels == "level_3.txt":
            level = 2
        elif levels == "level_4.txt":
            level = 3
        elif levels == "level_5.txt":
            level = 4
        elif levels == "level_6.txt":
            level = 5
        elif levels == "level_7.txt":
            level = 6
        elif levels == "level_8.txt":
            level = 7
        elif levels == "level_9.txt":
            level = 8
        elif levels == "level_10.txt":
            level = 9
        if retry == 1:
            if start_screen():

                pygame.key.set_repeat(200, 70)
                size = width, height = WIDTH, HEIGHT = 500, 1000
                screen = pygame.display.set_mode(size)

                player, level_x, level_y = generate_level(load_level(levels))
                pygame.mixer.music.load("data/backtrack.mp3")
                pygame.mixer.music.play(-1)
                tx = 5
                v = 10
                score = 0
                clock = pygame.time.Clock()
                camera = Camera()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            retry = 0
                        if event.type == pygame.KEYDOWN:
                            tx += 0.1
                            player_group.update(event)

                    screen.fill('black')
                    score += 1

                    camera.update(player)

                    for sprite in all_sprites:
                        camera.apply(sprite)
                    if not player.mover(tx):
                        running = False

                        pygame.mixer.music.stop()
                        if end_screen(score):
                            retry += 1
                        else:
                            retry = 0

                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()

                    clock.tick(FPS)
                pygame.quit()
            else:
                retry = -1
                pygame.quit()
        else:



            pygame.key.set_repeat(200, 70)
            size = width, height = WIDTH, HEIGHT = 500, 1000
            screen = pygame.display.set_mode(size)

            player, level_x, level_y = generate_level(load_level(levels))
            pygame.mixer.music.load("data/backtrack.mp3")
            pygame.mixer.music.play(-1)
            tx = 5
            v = 10
            score = 0
            clock = pygame.time.Clock()
            camera = Camera()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        retry = 0
                    if event.type == pygame.KEYDOWN:
                        tx += 0.03
                        player_group.update(event)

                screen.fill('black')
                score += 1

                camera.update(player)

                for sprite in all_sprites:
                    camera.apply(sprite)
                if not player.mover(tx):
                    running = False

                    pygame.mixer.music.stop()
                    if end_screen(score):
                        retry += 1
                    else:
                        retry = 0

                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()

                clock.tick(FPS)
            pygame.quit()
