import pygame
import sys
import random
# colours
white = (255, 255, 255)
black = (0, 0, 0)

red = (200,0,0)
light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

green = (34,170,60)
light_green = (0,255,0)


display_width = 1280
display_height = 720
block_size = 20
FPS = 15
AppleThickness = 30

clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.init()
smallfont = pygame.font.SysFont("comicsansms", 30)
medfont = pygame.font.SysFont("inkfree", 50)
largefont = pygame.font.SysFont("comicsansms", 90)

img = pygame.image.load('head.png')
appleimg = pygame.image.load('apple.png')
background = pygame.image.load('tło.png')
background2 = pygame.image.load('tło2.png')
background3 = pygame.image.load('tło3.png')
part = pygame.image.load('part.png')
icon = pygame.image.load('logo.png')
pygame.display.set_caption('Snake')
pygame.display.set_icon(icon)

dead = pygame.mixer.Sound("foghorn.wav")
eat = pygame.mixer.Sound("yipee.wav")
a = pygame.mixer.Sound("start_message1.wav")




# def message_to_screen(msg, color):
#     screen_text = font.render(msg, True, color)
#     gameDisplay.blit(screen_text, [display_width / 2, display_height / 2])
def score(score):
    # plik = open('scores.txt', 'w')
    # plik.writelines("Gracz" + str(score) + '\n')
    # plik.close()
    text = smallfont.render("Score: "+str(score) , True, black)
    gameDisplay.blit(text, [0,0])
    return score

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, width, height, inactive_color, active_color, action = None,size="medium" ):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and  action != None:
            if action == "quit":
                pygame.quit()
                quit()

            elif action == "controls":
                game_controls()

            elif action == "play":
               Game()
            elif action == "main":
                game_intro()
            elif action == "scores":
                scores()
            elif action == "back":
                game_intro()
            elif action == "pauza":
                pause()
            elif action == "continue":
                return 3


    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height,size)
def explosion(x, y):

    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y

        colorChoices = [red, light_red, yellow, light_yellow]

        magnitude = 1

        while magnitude < 50:

            exploding_bit_x = x +random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y +random.randrange(-1*magnitude,magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False


def game_controls():


    gcont = True

    while gcont:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.blit(background2, (0, 0))
     #   message_to_screen("Controls",green,-100,size="large")
        message_to_screen("Sterowanie : klawisze",black,10)
        message_to_screen("Pauza: P",black,50)
        message_to_screen("Uruchamianie gry: C", black, 90)
        message_to_screen("Wyjście: Q", black, 130)


        button("Gra", display_width/4-100, 620,200,80, green, light_green, action="play")
        button("Menu", display_width/2-100,620,200,80, yellow, light_yellow, action="main")
        button("Wyjscie", display_width/4 *3 -100,620,200,80, red, light_red, action ="quit")
        pygame.display.update()
        clock.tick(15)

def scores():


    gcont = True

    while gcont:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.blit(background2, (0, 0))

        message_to_screen(open('scores.txt', 'r'),black,90)


        button("Play", display_width/4-100, 620,200,80, green, light_green, action="play")
        button("Menu", display_width/2-100,620,200,80, yellow, light_yellow, action="main")
        button("Quit", display_width/4 *3 -100,620,200,80, red, light_red, action ="quit")
        pygame.display.update()
        clock.tick(15)
def pause():

    spr=0
    paused = True
    message_to_screen("Wstrzymano",
                      black,
                      -130,
                      size="large")

    message_to_screen("Pamiętaj, ze oprocz przyciskow sa jeszcze skroty klawiszowe!",
                      black,
                      15)
    message_to_screen("Nacisnij C, aby kontynuować lub Q, aby wrocic do menu.",
                      black,
                      55)


    while paused:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    game_intro()
        spr = button("Kontynuuj", display_width / 3 - 100, 520, 200, 80, green, light_green, action="continue")
        button("Menu", display_width / 3 * 2 - 100, 520, 200, 80, red, light_red, action="back")
        pygame.display.update()
        if (spr==3):
            paused = False
        clock.tick(50)

    pygame.mixer.Sound.play(a)



def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)
    # smallfont = pygame.font.SysFont("comicsansms", 30)
    # medfont = pygame.font.SysFont("inkfree", 50)
    # largefont = pygame.font.SysFont("comicsansms", 90)


def game_intro():
    pygame.mixer.music.load("snake_man.mp3")
    pygame.mixer.music.play(-1)
    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(white)

        gameDisplay.blit(background, (0, 0))
        # message_to_screen("Welcome to Slither",
        #                   green,
        #                   -250,
        #                   "large")
        # message_to_screen("The objective of the game is to eat red apples",
        #                   black,
        #                   120,"small")
        #
        # message_to_screen("The more apples you eat, the longer you get",
        #                   black,
        #                   160,"small")
        #
        # message_to_screen("If you run into yourself, or the edges, you die!",
        #                   black,
        #                   200,"small")

        # message_to_screen("Press C to play, P to pause or Q to quit.",
        #                   black,
        #                   300)

        button("Gra", display_width/4-100, 620,200,80, green, light_green, action="play")
        button("Kontrola", display_width/2-100,620,200,80, yellow, light_yellow, action="controls")
        button("Wyjscie", display_width/4 *3 -100,620,200,80, red, light_red, action ="quit")
        button("Scores", display_width / 10 * 3 - 100, 420, 200, 80, red, light_red, action="scores")
        pygame.display.update()
        clock.tick(15)

class Snake:
    def __init__(self):
        self.direction = 'right'
        self.head = pygame.transform.rotate(img, 270)
        self.speed = 1.3
        self.snakeList = []
        self.spr = 0

        self.snakeHead = []
        self.make_longer = True

        self.lead_x = display_width / 2
        self.lead_y = display_height / 2

        self.lead_x_change = 0
        self.lead_y_change = 0
        self.gameOver = False

    def tick(self, level):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.direction = "left"
            self.lead_x_change = -block_size
            self.lead_y_change = 0
        elif pressed[pygame.K_RIGHT]:
            self.direction = "right"
            self.lead_x_change = block_size
            self.lead_y_change = 0
        elif pressed[pygame.K_UP]:
            self.direction = "up"
            self.lead_y_change = -block_size
            self.lead_x_change = 0
        elif pressed[pygame.K_DOWN]:
            self.direction = "down"
            self.lead_y_change = block_size
            self.lead_x_change = 0
        elif pressed[pygame.K_p]:
            pause()
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change
        if level ==1:
            if self.lead_x >= display_width :
                self.lead_x = 0
            elif self.lead_x < 0 :
                self.gameOver = True
                self.lead_x = 1280
            elif self.lead_y >= display_height:
                self.lead_y = 0
            elif self.lead_y < 0:
                self.lead_y = 720
               # pygame.mixer.Sound.play(dead)
                #explosion(int(self.lead_x),int(self.lead_y))
        if self.gameOver is True:
            # makescore()
            message_to_screen("Koniec gry",
                              red,
                              -110,
                              size="large")

            message_to_screen("Pamiętaj, ze oprocz przyciskow sa jeszcze skroty klawiszowe!",
                              black,
                              15)
            message_to_screen("Nacisnij C, aby kontynuować lub Q, aby wrocic do menu.",
                              black,
                              55)

        while self.gameOver is True:
            self.spr = button("Gra", display_width / 3 - 100, 520, 200, 80, green, light_green, action="play")
            button("Menu", display_width / 3 * 2 - 100, 520, 200, 80, red, light_red, action="back")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit(0)
                    elif event.key == pygame.K_c:
                        Game()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                elif event.type == pygame.QUIT:
                    # X and min
                    sys.exit(0)
            if (self.spr == 3):
                self.gameOver = False

        if self.snakeHead in self.snakeList[1:]:
            self.gameOver = True
            pygame.mixer.Sound.play(dead)
            explosion(int(self.lead_x),int(self.lead_y))

    def draw(self):


        self.snakeHead = [self.lead_x, self.lead_y]
        self.snakeList.insert(0, self.snakeHead)
        if self.direction == "right":
            self.head = pygame.transform.rotate(img, 270)

        if self.direction == "left":
            self.head = pygame.transform.rotate(img, 90)

        if self.direction == "up":
            self.head = img

        if self.direction == "down":
            self.head = pygame.transform.rotate(img, 180)

        gameDisplay.blit(self.head, (self.snakeList[0][0], self.snakeList[0][1]))

        if not self.make_longer:
            del self.snakeList[-1]
        else:
            self.make_longer = False
        for XnY in self.snakeList[1:]:
            # pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])
            if self.direction == "right":
                gameDisplay.blit(pygame.transform.rotate(part, 270), [XnY[0], XnY[1], block_size, block_size])


            if self.direction == "left":

                gameDisplay.blit(pygame.transform.rotate(part, 90), [XnY[0], XnY[1], block_size, block_size])

            if self.direction == "up":
                gameDisplay.blit(part, [XnY[0], XnY[1], block_size, block_size])

            if self.direction == "down":
                #self.part = pygame.transform.rotate(part, 180)
                gameDisplay.blit(pygame.transform.rotate(part, 180), [XnY[0], XnY[1], block_size, block_size])

class Apple(object):
    def __init__(self):
        # Same x, y
        # self.randAppleX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
        # self.randAppleY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
        # Not same x,y
        self.randAppleX = round(random.randrange(0, display_width-AppleThickness))
        self.randAppleY = round(random.randrange(0, display_height-AppleThickness))


    def draw(self):
        # hard
        #pygame.draw.rect(gameDisplay, red, [self.randAppleX, self.randAppleY, block_size, block_size])
        # easy
        #pygame.draw.rect(gameDisplay, red, [self.randAppleX, self.randAppleY, AppleThickness, AppleThickness])
        gameDisplay.blit(appleimg, (self.randAppleX, self.randAppleY))


class Game(object):
    def __init__(self):
        pygame.mixer.music.load("snake_music2.mp3")
        pygame.mixer.music.play(-1)
        self.food = Apple()
        self.player = Snake()
        self.snakeLength = 0




        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # X and min
                    sys.exit(0)
                    # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # Ticking

            self.tick()
            clock.tick(FPS)

            # Drawing

            gameDisplay.blit(background3, (0, 0))
            self.draw()

            # Same size
            # if self.player.lead_x == self.food.randAppleX and self.player.lead_y == self.food.randAppleY:
            #    self.food.randAppleX = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            #    self.food.randAppleY = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
            #    self.player.make_longer = True
            # Bigger than
            # if self.food.randAppleX + AppleThickness >= self.player.lead_x >= self.food.randAppleX:
            #     if self.food.randAppleY + AppleThickness >= self.player.lead_y >= self.food.randAppleY:
            #         self.food.randAppleX = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            #         self.food.randAppleY = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
            #         self.player.make_longer = True
            # Not same x, y
            if self.player.lead_x > self.food.randAppleX and self.player.lead_x < self.food.randAppleX + AppleThickness or self.player.lead_x + block_size > self.food.randAppleX and self.player.lead_x + block_size < self.food.randAppleX + AppleThickness:

                if self.player.lead_y > self.food.randAppleY and self.player.lead_y < self.food.randAppleY + AppleThickness:

                    self.food.randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
                    self.food.randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0
                    self.player.make_longer = True
                    pygame.mixer.Sound.play(eat)
                    self.snakeLength += 1

                elif self.player.lead_y + block_size > self.food.randAppleY and self.player.lead_y + block_size < self.food.randAppleY + AppleThickness:

                    self.food.randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
                    self.food.randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0
                    self.player.make_longer = True
                    pygame.mixer.Sound.play(eat)
                    self.snakeLength += 1


    def tick(self):
        self.player.tick(1)

    def draw(self):
        self.player.draw()
        self.food.draw()
        score(self.snakeLength)
        button("Pauza", 5, 40, 80, 30, red, light_red, action="pauza", size="small")
        pygame.display.update()


def main():
    game_intro()
    Game()
main()

# Klasy abstrakcyjne