import random


class Fruit:
    def __init__(self, screen_width, screen_height, block_size):
        self.block_size = block_size
        self.pos_x = random.randrange(self.block_size, (screen_width - self.block_size), self.block_size)
        self.pos_y = random.randrange(self.block_size, (screen_height - self.block_size), self.block_size)
        self.pos_x = self.pos_x // self.block_size * self.block_size
        self.pos_x = self.pos_x // self.block_size * self.block_size

    def respawn(self, screen_width, screen_height, snake):
        nice_location = False
        while not nice_location:
            self.pos_x = random.randrange(self.block_size, (screen_width - self.block_size), self.block_size)
            self.pos_y = random.randrange(self.block_size, (screen_height - self.block_size), self.block_size)
            self.pos_x = self.pos_x//self.block_size * self.block_size
            self.pos_x = self.pos_x//self.block_size * self.block_size
            for s in snake.segments:
                if self.pos_y == s.pos_y and self.pos_x == s.pos_x:
                    nice_location = False
                    break
                if (200 <= self.pos_x <= 460 or 800 <= self.pos_x <= 1060) and (
                        200 <= self.pos_y <= 220 or 460 < self.pos_y <= 480):
                    nice_location = False
                    break
                if (200 <= self.pos_x <= 220 or 1040 <= self.pos_x <= 1060) and 200 <= \
                        self.pos_y <= 480:
                    nice_location = False
                    break
                else:
                    nice_location = True