class SnakeSegment:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction


class Snake:
    def __init__(self, display, block_size, pos_x=665, pos_y=400, direction="right"):
        self.display = display
        self.block_size = block_size
        self.x_velocity = self.block_size
        self.y_velocity = 0
        self.direction = direction
        self.segments = []
        self.segments.append(SnakeSegment(pos_x, pos_y, direction))
        self.prev_x_vel = 0
        self.prev_y_vel = 0
        self.moving = True
        self.explode = True

    def turn_left(self):
        if self.x_velocity > 0:
            return
        self.x_velocity = (-1)*self.block_size
        self.y_velocity = 0
        self.direction = "left"

    def turn_right(self):
        if self.x_velocity < 0:
            return
        self.x_velocity = self.block_size
        self.y_velocity = 0
        self.direction = "right"

    def turn_down(self):
        if self.y_velocity < 0:
            return
        self.y_velocity = self.block_size
        self.x_velocity = 0
        self.direction = "down"

    def turn_up(self):
        if self.y_velocity > 0:
            return
        self.y_velocity = (-1)*self.block_size
        self.x_velocity = 0
        self.direction = "up"

    def add_segment(self):
        self.segments.append(SnakeSegment(self.segments[-1].pos_x, self.segments[-1].pos_y, self.segments[-1].direction))

    def move(self):
        if self.moving:
            next_x_pos = self.segments[0].pos_x + self.x_velocity
            next_y_pos = self.segments[0].pos_y + self.y_velocity
            self.segments.pop()
            self.segments.insert(0, SnakeSegment(next_x_pos, next_y_pos, self.direction))

    # reset snake to initial values
    def reset_snake(self):
        self.segments = []
        self.segments.append(SnakeSegment(665, 400, "right"))
        self.direction = "right"
        self.x_velocity = self.block_size
        self.y_velocity = 0


class AI(Snake):
    def __init__(self, display, block_size):
        super().__init__(display, block_size, pos_x=600, pos_y=320, direction="left")
        self.x_velocity = -self.block_size
        self.y_velocity = 0

    def reset_snake(self):
        self.segments = []
        self.segments.append(SnakeSegment(600, 320, "left"))
        self.direction = "left"
        self.x_velocity = -self.block_size
        self.y_velocity = 0

    def target(self, dx, dy):
        if dx - 10 < self.segments[0].pos_x < dx + 10:
            if self.segments[0].pos_y < dy:
                self.turn_down()
            if self.segments[0].pos_y > dy:
                self.turn_left()
                self.turn_up()
        if self.segments[0].pos_x > dx:
            self.turn_down()
            self.turn_left()

        if self.segments[0].pos_x < dx:
            self.turn_up()
            self.turn_right()


class Snake2(Snake):
    def __init__(self, display, block_size):
        super().__init__(display, block_size, pos_x=600, pos_y=320, direction="left")
        self.x_velocity = -self.block_size
        self.y_velocity = 0
        self.moving = True

    def reset_snake(self):
        self.segments = []
        self.segments.append(SnakeSegment(600, 320, "left"))
        self.direction = "left"
        self.x_velocity = -self.block_size
        self.y_velocity = 0
