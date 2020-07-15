import pygame
import random
import Snakes as sn
import Food as fd


class Game:
    white = (255, 255, 255)
    black = (0, 0, 0)

    red = (200, 0, 0)
    light_red = (255, 0, 0)

    yellow = (200, 200, 0)
    light_yellow = (255, 255, 0)

    green = (34, 170, 60)
    light_green = (0, 255, 0)

    blue = (0, 0, 255)
    light_blue = (0, 128, 255)

    def __init__(self, screen_width, screen_height, speed, difficulty):
        pygame.init()

        self.game_over = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.block_size = 20

        # set default font
        self.game_font_mini = pygame.font.SysFont("comicsansms", 20)
        self.game_font_s = pygame.font.SysFont("comicsansms", 30)
        self.game_font_m = pygame.font.SysFont("inkfree", 50)
        self.game_font_l = pygame.font.SysFont("comicsansms", 100)

        self.running = True

        # create display
        self.game_display = pygame.display.set_mode((self.screen_width, self.screen_height))

        # set clock for fps control
        self.clock = pygame.time.Clock()

        # instantiate snake
        self.snake = sn.Snake(self.game_display, self.block_size, 640, 360)

        # instantiate fruit
        self.fruit = fd.Fruit(self.screen_width, self.screen_height, self.block_size)

        self.head = pygame.image.load('../graphics/head.png')
        self.part = pygame.image.load('../graphics/part.png')
        self.apple = pygame.image.load('../graphics/apple.png')

        # set window name
        pygame.display.set_caption("Snake")

        # method for input general messages
        self.choice = 0
        self.difficulty = difficulty
        self.speed = speed
        self.run = 1
        self.intro = False
        self.paused = False
        self.gcont = False
        self.descrpt = False
        self.while_scores = False

    def game_intro(self):
        pygame.mixer.music.load("../music/intro.mp3")
        pygame.mixer.music.play(-1)
        self.intro = True

        while self.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.intro = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            self.game_display.blit(pygame.image.load('../graphics/background.png'), (0, 0))
            self.button("Gra", 320-200, 620, 200, 80, self.green, self.light_green, action="play")
            self.button("Kontrola", 400, 620, 200, 80, self.yellow, self.light_yellow, action="controls")
            self.button("Wyniki",  self.screen_width/2+40, 620, 200, 80, self.blue, self.light_blue, action="scores")
            self.button("Wyjscie", self.screen_width/4 * 3, 620, 200, 80, self.red, self.light_red, action="quit")

            pygame.display.update()
            self.clock.tick(15)
        return self.difficulty, self.speed

    def main_loop(self):
        pygame.mixer.music.load("../music/game_1.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            self.run = 1
            # Handle game over situation
            if self.game_over:
                self.explosion(self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, self.snake)
                self.game_over_dialog()

            for event in pygame.event.get():
                # Handle exit through x corner button
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle KeyDown events. Note that it will works with arrows and WSAD
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.turn_left()
                        break
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.turn_right()
                        break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.turn_up()
                        break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.turn_down()
                        break

                    # handle pause game
                    if event.key == pygame.K_SPACE:
                        self.pause_game()

            # execute snake logic
            self.snake.move()
            # Check collision with boundaries
            if self.difficulty == 0:
                self.game_display.blit(pygame.image.load('../graphics/background3.png'), (0, 0))
                if self.check_collision(self.snake):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
            elif self.difficulty == 2:
                self.game_display.blit(pygame.image.load('../graphics/background5.png'), (0, 0))
                if self.check_collision(self.snake):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collisions_special(self.snake):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
            else:
                self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
                if self.check_collision_without_walls(self.snake):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()

            # check if eaten fruit
            if self.check_fruit_collision(self.snake):
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.run = 0
                pygame.mixer.Sound.play(pygame.mixer.Sound("../music/eat.wav"))

            self.draw_score()
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            self.button("Pauza", 0, 30, 60, 24, self.red, self.light_red, action="pause", size="mini")
            pygame.display.update()
            # set fps
            self.clock.tick(self.speed)

    # this method checks collisions that result in game over
    def check_collision(self, collide):
        if collide.moving:
            if collide.segments[0].pos_x < collide.block_size or \
                    collide.segments[0].pos_x >= self.screen_width - collide.block_size:
                return True
            if collide.segments[0].pos_y < collide.block_size or \
                    collide.segments[0].pos_y >= self.screen_height - collide.block_size:
                return True

            # check collision of the snake with itself
            head_pos_x = collide.segments[0].pos_x
            head_pos_y = collide.segments[0].pos_y
            for s in collide.segments[1:]:
                if head_pos_x == s.pos_x and head_pos_y == s.pos_y:
                    return True
            return False
        else:
            return True

    def check_collision_without_walls(self, collide):
        if collide.moving:
            if collide.segments[0].pos_x < 0:
                collide.segments[0].pos_x = self.screen_width - collide.block_size
            elif collide.segments[0].pos_x > self.screen_width - collide.block_size:
                collide.segments[0].pos_x = 0
            if collide.segments[0].pos_y < 0:
                collide.segments[0].pos_y = self.screen_height-collide.block_size
            elif collide.segments[0].pos_y > self.screen_height - collide.block_size:
                collide.segments[0].pos_y = 0

            # check collision of the snake with itself
            head_pos_x = collide.segments[0].pos_x
            head_pos_y = collide.segments[0].pos_y
            for s in collide.segments[1:]:
                if head_pos_x == s.pos_x and head_pos_y == s.pos_y:
                    return True
            return False
        else:
            return True

    @staticmethod
    def check_collision_between(object1, object2):
        # check collision of the snake with another
        for s in object1.segments:
            for r in object2.segments:
                if r.pos_x - 10 <= s.pos_x <= r.pos_x + 10 and r.pos_y - 10 <= s.pos_y <= r.pos_y + 10:
                    return True
        return False

    @staticmethod
    def check_collisions_special(collide):
        if collide.moving:
            if (200 <= collide.segments[0].pos_x <= 460 or 800 <= collide.segments[0].pos_x <= 1060) and \
                    (200 <= collide.segments[0].pos_y <= 220 or 450 < collide.segments[0].pos_y <= 470):
                return True
            if (200 <= collide.segments[0].pos_x <= 220 or 1040 <= collide.segments[0].pos_x <= 1060) and \
                    200 <= collide.segments[0].pos_y <= 480:
                return True
            return False
        else:
            return True

    # Check if snake eats fruit
    def check_fruit_collision(self, object):
        if object.segments[0].pos_y - 15 <= self.fruit.pos_y <= object.segments[0].pos_y+15 and \
                object.segments[0].pos_x - 15 <= self.fruit.pos_x <= object.segments[0].pos_x+15:
            return True
        return False

    def put_message(self, message, y_displace=0, font="large", colour=black):
        text = self.game_font_l.render(message, True, colour)
        middle = text.get_rect()
        if font == "large":
            text = self.game_font_l.render(message, True, colour)
            middle = text.get_rect()
        elif font == "mid":
            text = self.game_font_m.render(message, True, colour)
            middle = text.get_rect()
        elif font == "small":
            text = self.game_font_s.render(message, True, colour)
            middle = text.get_rect()
        middle.center = self.screen_width / 2, self.screen_height / 2 + y_displace
        self.game_display.blit(text, middle)

    # handle pause situation
    def pause_game(self):
        self.paused = True

        self.put_message("Zatrzymane", -150)
        pygame.display.update()
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = False

            self.button("Gra", self.screen_width / 3 - 100 + 25, 500, 200, 80, self.green, self.light_green,
                        action="continue")
            self.button("Menu", self.screen_width / 3 * 2 - 100 - 25, 500, 200, 80, self.red, self.light_red,
                        action="menu")
            self.clock.tick(30)
            pygame.display.update()
        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))

    # Handle game over situation
    def game_over_dialog(self):
        while self.game_over:
            self.put_message("Koniec gry", -120, colour=self.red)
            self.put_message("Pamiętaj, ze oprocz przyciskow sa jeszcze skroty klawiszowe!", 5, "small")
            self.put_message("Nacisnij SPACE, aby kontynuować lub ESC, aby wyjść do menu", 50, "small")
            self.button("Gra", self.screen_width / 3 - 100 + 25, 500, 200, 80, self.green, self.light_green, action="reset")
            self.button("Menu", self.screen_width / 3 * 2 - 100 - 25, 500, 200, 80, self.red, self.light_red, action="menu")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        main()

    def text_to_button(self, msg, colour, buttonx, buttony, buttonwidth, buttonheight, size="mid"):
        if size == "mini":
            text = self.game_font_mini.render(msg, True, colour)
        else:
            text = self.game_font_m.render(msg, True, colour)
        middle = text.get_rect()
        middle.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
        self.game_display.blit(text, middle)

    def button(self, text, x, y, width, height, inactive_color, active_color, action=None, size="medium"):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            if click[0] == 1 and action is not None:
                if action == "play":
                    self.intro = False
                elif action == "controls":
                    self.game_controls()
                elif action == "quit":
                    pygame.quit()
                    quit()
                elif action == "reset":
                    self.reset_game()
                elif action == "description":
                    self.description()
                elif action == "menu":
                    main()
                elif action == "ret_menu":
                    self.reset_game()
                elif action == "pause":
                    self.pause_game()
                elif action == "continue":
                    self.paused = False
                elif action == "scores":
                    self.print_scores()
                elif action == "up":
                    if self.choice < 2:
                        self.choice += 1
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
                elif action == "down":
                    if self.choice > 0:
                        self.choice -= 1
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
                elif action == "updiff":
                    if self.difficulty < 2:
                        self.difficulty += 1
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
                elif action == "downdiff":
                    if self.difficulty > 0:
                        self.difficulty -= 1
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
                elif action == "speedup":
                    if self.speed < 25:
                        self.speed += 5
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
                elif action == "speeddown":
                    if self.speed > 10:
                        self.speed -= 5
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/change.wav"))
            pygame.draw.rect(self.game_display, active_color, (x, y, width, height))
        else:
            pygame.draw.rect(self.game_display, inactive_color, (x, y, width, height))

        self.text_to_button(text, self.black, x, y, width, height, size)

    # Reset variables to a new game in case of playing again
    def reset_game(self):
        self.snake.reset_snake()
        self.game_over = False
        self.descrpt = False
        self.paused = False
        self.gcont = False
        self.while_scores = False
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.flip()

    def game_controls(self):
        self.gcont = True
        while self.gcont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.choice > 0:
                            self.choice -= 1
                        break
                    elif event.key == pygame.K_RIGHT:
                        if self.choice < 2:
                            self.choice += 1
                        break

            self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
            self.button("Menu", 320 - 200, 300, 200, 80, self.red, self.light_red, action="ret_menu")
            self.button("Opis gry", 320 - 200, 400, 200, 80, self.yellow, self.light_yellow, action="description")
            self.put_message("Ustawienia:", -300, "large", colour=self.black)
            self.put_message("Trudności:", -200, "small", colour=self.black)
            self.put_message("Tryb:", -50, "small", colour=self.black)
            self.put_message("Szybkość:", 100, "small", colour=self.black)
            self.button("+", self.screen_width / 2 + 160, 200, 20, 80, self.green, self.light_green, action="updiff")
            self.button("-", self.screen_width / 2 - 180, 200, 20, 80, self.green, self.light_green, action="downdiff")
            self.button("+", self.screen_width/2+160, 350, 20, 80, self.green, self.light_green, action="up")
            self.button("-", self.screen_width/2-180, 350, 20, 80, self.green, self.light_green, action="down")
            self.button("+",  self.screen_width/2+160, 500, 20, 80, self.green, self.light_green, action="speedup")
            self.button("-",  self.screen_width/2-180, 500, 20, 80, self.green, self.light_green, action="speeddown")

            if self.difficulty == 0:
                self.button("Krawedzie", self.screen_width / 2 - 150, 200, 300, 80, self.green, self.light_green)
            if self.difficulty == 1:
                self.button("Bez krawedzi", self.screen_width / 2 - 150, 200, 300, 80, self.green, self.light_green)
            if self.difficulty == 2:
                self.button("Niespodzianka", self.screen_width / 2 - 150, 200, 300, 80, self.green, self.light_green)

            if self.choice == 0:
                self.button("Solo", self.screen_width/2-150, 350, 300, 80, self.green, self.light_green)
            if self.choice == 1:
                self.button("AI", self.screen_width/2-150, 350, 300, 80, self.green, self.light_green)
            if self.choice == 2:
                self.button("2 graczy", self.screen_width/2-150, 350, 300, 80, self.green, self.light_green)

            if self.speed == 10:
                self.button("Wolno", self.screen_width/2-150, 500, 300, 80, self.green, self.light_green)
            if self.speed == 15:
                self.button("Umiarkowanie", self.screen_width/2-150, 500, 300, 80, self.green, self.light_green)
            if self.speed == 20:
                self.button("Normalnie", self.screen_width/2-150, 500, 300, 80, self.green, self.light_green)
            if self.speed == 25:
                self.button("Szybko", self.screen_width/2-150, 500, 300, 80, self.green, self.light_green)

            pygame.display.update()
            self.clock.tick(10)

    def draw_score(self):
        text = self.game_font_mini.render("Wynik: " + str(len(self.snake.segments)-1), True, self.black)
        self.game_display.blit(text, (0, 0))

    def save_score(self):
        highscores = []
        with open("../data/scores.txt", "r") as get:
            for line in get:
                highscores.append(int(line))

        highscores.append(len(self.snake.segments)-1)
        highscores.sort()
        highscores.reverse()
        plik = open("../data/scores.txt", 'w')
        if len(highscores) <= 10:
            leng = len(highscores)
        else:
            leng = 10
        for i in range(leng):
            plik.writelines((str(highscores[i])+'\n'))
        plik.close()

    def print_scores(self):
        self.while_scores = True

        while self.while_scores:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
            self.button("Menu", self.screen_width / 3 * 2 - 25, 600, 200, 80, self.red, self.light_red, action="ret_menu")
            self.put_message("Najlepsze wyniki: ", -280)
            plik = open("../data/scores.txt", 'r')
            y = -170
            i = 1
            for line in plik:
                self.put_message((str(i)+". " + str(line.strip())), y, font="small")
                y += 50
                i += 1
            plik.close()
            pygame.display.update()
            self.clock.tick(15)

    def description(self):
        self.descrpt = True
        while self.descrpt:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
            self.button("Menu", self.screen_width / 3 * 2 + 100, 300, 200, 80, self.red, self.light_red, action="ret_menu")
            self.put_message("Klawisze: ", -280)
            self.put_message("Sterowanie : klawisze/WSAD", -180, "small", colour=self.black)
            self.put_message("Pauza: Spacja", -130, "small", colour=self.black)
            self.put_message("Wyjście z gry: Q", -80, "small", colour=self.black)
            self.put_message("Uruchamianie gry: C", -30, "small", colour=self.black)
            self.put_message("Opis gry:", 100, "large", colour=self.black)
            self.put_message("Graj wężem, jedz jabłka i nie pozwól, aby Twój ogromny gad został zniszczony", 220, "small", colour=self.black)
            pygame.display.update()
            self.clock.tick(15)

    # draw snake segments
    def draw_snake(self, object):
        if object.segments[0].direction == "right":
            self.game_display.blit(pygame.transform.rotate(self.head, 270),
                                   [object.segments[0].pos_x, object.segments[0].pos_y, object.block_size, object.block_size])
        elif object.segments[0].direction == "left":
            self.game_display.blit(pygame.transform.rotate(self.head, 90),
                                   [object.segments[0].pos_x, object.segments[0].pos_y, object.block_size, object.block_size])
        elif object.segments[0].direction == "up":
            self.game_display.blit(pygame.transform.rotate(self.head, 0),
                                   [object.segments[0].pos_x, object.segments[0].pos_y, object.block_size, object.block_size])
        elif object.segments[0].direction == "down":
            self.game_display.blit(pygame.transform.rotate(self.head, 180),
                                   [object.segments[0].pos_x, object.segments[0].pos_y, object.block_size, object.block_size])
        for s in object.segments[1:]:
            if s.direction == "right":
                self.game_display.blit(pygame.transform.rotate(self.part, 270),
                                       [s.pos_x, s.pos_y, object.block_size, object.block_size])
            if s.direction == "left":
                self.game_display.blit(pygame.transform.rotate(self.part, 90),
                                       [s.pos_x, s.pos_y, object.block_size, object.block_size])
            elif s.direction == "up":
                self.game_display.blit(pygame.transform.rotate(self.part, 0),
                                       [s.pos_x, s.pos_y, object.block_size, object.block_size])
            elif s.direction == "down":
                self.game_display.blit(pygame.transform.rotate(self.part, 180),
                                       [s.pos_x, s.pos_y, object.block_size, object.block_size])

    def draw_fruit(self, fruit):
        self.game_display.blit(self.apple, [fruit.pos_x, fruit.pos_y, fruit.block_size, fruit.block_size])

    def explosion(self, x, y, object):
        if object.explode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            color_choices = [self.red, self.light_red, self.yellow, self.light_yellow]

            magnitude = 1

            while magnitude < 50:
                exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
                exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

                pygame.draw.circle(self.game_display, color_choices[random.randrange(0, 4)],
                                   (int(exploding_bit_x), int(exploding_bit_y)), random.randrange(1, 5))
                magnitude += 1

                pygame.display.update()
                self.clock.tick(100)

    @staticmethod
    def exit_game():
        pygame.quit()
        quit()


class Game2(Game):
    def __init__(self, screen_width, screen_height, block_size, diff):
        super().__init__(screen_width, screen_height, block_size, diff)
        self.difficulty = diff
        self.computer = sn.AI(self.game_display, self.block_size)
        self.foo1 = 1
        self.foo2 = 1

    def main_loop(self):
        pygame.mixer.music.load("../music/game_1.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            self.foo1 = 0
            self.foo2 = 0
            # Handle game over situation
            if self.game_over:
                self.explosion(self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, self.snake)
                self.game_over_dialog()

            for event in pygame.event.get():
                # Handle exit through x corner button
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle KeyDown events. Note that it will works with arrows and WSAD
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.turn_left()
                        break
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.turn_right()
                        break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.turn_up()
                        break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.turn_down()
                        break

                    # handle pause game
                    if event.key == pygame.K_SPACE:
                        self.pause_game()

            # execute snake logic
            self.computer.target(self.fruit.pos_x, self.fruit.pos_y)
            self.computer.move()
            self.snake.move()
            # Check collision with boundaries
            if self.difficulty == 0:
                self.game_display.blit(pygame.image.load('../graphics/background3.png'), (0, 0))
                if self.check_collision(self.snake) or self.check_collision_between(self.snake, self.computer):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collision(self.computer):
                    if self.computer.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.computer.moving = False
                    self.explosion(self.computer.segments[0].pos_x, self.computer.segments[0].pos_y, self.computer)
                    self.computer.explode = False
            elif self.difficulty == 2:
                self.game_display.blit(pygame.image.load('../graphics/background5.png'), (0, 0))
                if self.check_collision(self.snake) or self.check_collision_between(self.snake, self.computer):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collision(self.computer) or self.check_collisions_special(self.computer):
                    if self.computer.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.computer.moving = False
                    self.explosion(self.computer.segments[0].pos_x, self.computer.segments[0].pos_y, self.computer)
                    self.computer.explode = False
                if self.check_collisions_special(self.snake):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
            else:
                self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
                if self.check_collision_without_walls(self.snake) or self.check_collision_between(self.snake,
                                                                                                  self.computer):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collision_without_walls(self.computer):
                    if self.computer.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.computer.moving = False
                    self.explosion(self.computer.segments[0].pos_x, self.computer.segments[0].pos_y, self.computer)
                    self.computer.explode = False

            # check if eaten fruit
            if self.check_fruit_collision(self.snake):
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.foo1 = 0
                pygame.mixer.Sound.play(pygame.mixer.Sound("../music/eat.wav"))
            if self.check_fruit_collision(self.computer):
                self.computer.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.foo2 = 0
                pygame.mixer.Sound.play(pygame.mixer.Sound("../music/eat.wav"))

            self.draw_score()
            self.draw_score2()
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            self.draw_snake(self.computer)
            self.button("Pauza", 0, 30, 60, 24, self.red, self.light_red, action="pause", size="mini")
            pygame.display.update()

            self.clock.tick(self.speed)

    def draw_score2(self):
        text = self.game_font_mini.render("Wynik: "+str(len(self.computer.segments)-1), True, self.black)
        self.game_display.blit(text, (1185, 0))
        text = self.game_font_mini.render("(AI)", True, self.black)
        self.game_display.blit(text, (1215, 30))

    def reset_game(self):
        self.snake.reset_snake()
        self.computer.reset_snake()
        self.game_over = False
        self.gcont = True
        self.computer.moving = True
        self.computer.explode = True
        self.snake.speed = 1
        self.computer.speed = 1
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.update()


class Game3(Game):
    def __init__(self, screen_width, screen_height, block_size, diff):
        super().__init__(screen_width, screen_height, block_size, diff)
        self.difficulty = diff
        self.snake2 = sn.Snake2(self.game_display, self.block_size)
        self.foo1 = 1
        self.foo2 = 1

    def main_loop(self):
        pygame.mixer.music.load("../music/game_2.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            self.foo1 = 1
            self.foo2 = 1
            # Handle game over situation
            if self.game_over:
                self.game_over_dialog()

            for event in pygame.event.get():
                # Handle exit through x corner button
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle KeyDown events. Note that it will works with arrows and WSAD
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.turn_left()
                        break

                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn_right()
                        break
                    elif event.key == pygame.K_UP:
                        self.snake.turn_up()
                        break
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn_down()
                        break
                    if event.key == pygame.K_a:
                        self.snake2.turn_left()
                        break
                    elif event.key == pygame.K_d:
                        self.snake2.turn_right()
                        break
                    elif event.key == pygame.K_w:
                        self.snake2.turn_up()
                        break
                    elif event.key == pygame.K_s:
                        self.snake2.turn_down()
                        break

                    # handle pause game
                    if event.key == pygame.K_SPACE:
                        self.pause_game()

            # execute snake logic
            self.snake2.move()
            self.snake.move()
            # Check collision with boundaries
            if self.difficulty == 0:
                self.game_display.blit(pygame.image.load('../graphics/background3.png'), (0, 0))
                if (self.check_collision(self.snake) and self.check_collision(self.snake2)) or self.check_collision_between(self.snake, self.snake2):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collision(self.snake):
                    if self.snake.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake.moving = False
                    self.explosion(self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, self.snake)
                    self.snake.explode = False
                if self.check_collision(self.snake2):
                    if self.snake2.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake2.moving = False
                    self.explosion(self.snake2.segments[0].pos_x, self.snake2.segments[0].pos_y, self.snake2)
                    self.snake2.explode = False
            elif self.difficulty == 2:
                self.game_display.blit(pygame.image.load('../graphics/background5.png'), (0, 0))
                if (self.check_collision(self.snake) and self.check_collision(self.snake2)) or \
                        self.check_collision_between(self.snake, self.snake2):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                if self.check_collision(self.snake) or self.check_collisions_special(self.snake):
                    if self.snake.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake.moving = False
                    self.explosion(self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, self.snake)
                    self.snake.explode = False
                if self.check_collision(self.snake2) or self.check_collisions_special(self.snake2):
                    if self.snake2.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake2.moving = False
                    self.explosion(self.snake2.segments[0].pos_x, self.snake2.segments[0].pos_y, self.snake2)
                    self.snake2.explode = False
            else:
                self.game_display.blit(pygame.image.load('../graphics/background4.png'), (0, 0))
                if (self.check_collision_without_walls(self.snake) and self.check_collision_without_walls(self.snake2))\
                        or self.check_collision_between(self.snake, self.snake2):
                    pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.game_over = True
                    self.save_score()
                if self.check_collision_without_walls(self.snake):
                    if self.snake.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake.moving = False
                    self.explosion(self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, self.snake)
                    self.snake.explode = False
                if self.check_collision_without_walls(self.snake2):
                    if self.snake2.moving:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("../music/dead.wav"))
                    self.snake2.moving = False
                    self.explosion(self.snake2.segments[0].pos_x, self.snake2.segments[0].pos_y, self.snake2)
                    self.snake2.explode = False

            # check if eaten fruit
            if self.check_fruit_collision(self.snake):
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.foo1 = 0
                pygame.mixer.Sound.play(pygame.mixer.Sound("../music/eat.wav"))
            if self.check_fruit_collision(self.snake2):
                self.snake2.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.foo2 = 0
                pygame.mixer.Sound.play(pygame.mixer.Sound("../music/eat.wav"))

            # first you draw, then you update to see changes
            self.draw_score()
            self.draw_score2()
            self.draw_fruit(self.fruit)

            self.draw_snake(self.snake)
            self.draw_snake(self.snake2)
            self.button("Pauza", 0, 60, 60, 24, self.red, self.light_red, action="pause", size="mini")
            pygame.display.update()

            self.clock.tick(self.speed)

    def draw_score2(self):
        text = self.game_font_mini.render("Wynik: " + str(len(self.snake2.segments)-1), True, self.black)
        self.game_display.blit(text, (1190, 0))
        text = self.game_font_mini.render("(WSAD)", True, self.black)
        self.game_display.blit(text, (1190, 30))

    def draw_score(self):
        text = self.game_font_mini.render("Wynik: " + str(len(self.snake.segments)-1), True, self.black)
        self.game_display.blit(text, (0, 0))
        text = self.game_font_mini.render("(Strzałki)", True, self.black)
        self.game_display.blit(text, (0, 30))

    def reset_game(self):
        self.snake.reset_snake()
        self.snake2.reset_snake()
        self.game_over = False
        self.snake.moving = True
        self.snake2.moving = True
        self.gcont = True
        self.snake.explode = True
        self.snake2.explode = True
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.flip()


def main():
    game = Game(1280, 720, 15, 0)

    diff, speed = game.game_intro()
    if game.choice == 0:
        game = Game(1280, 720, speed, diff)
        game.main_loop()
    if game.choice == 1:
        game2 = Game2(1280, 720, speed, diff)
        game2.main_loop()
    if game.choice == 2:
        game3 = Game3(1280, 720, speed, diff)
        game3.main_loop()


if __name__ == "__main__":
    main()