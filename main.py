import pygame

# pygame setup
pygame.init()

# initialization of the screen
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# fps tracking
clock = pygame.time.Clock()
fps = 120

# list of background images
images = [
    pygame.image.load("Images/BackgroundStandsWithPeople.png"),
    pygame.image.load("Images/BackgroundStandsWithPeople.png")
]


# class for handling background events
class Background:
    def __init__(self, x_position, y_position, background_images):
        self.x = x_position
        self.y = y_position
        self.images = background_images

    def display_background(self):
        for image in self.images:
            screen.blit(image, (self.x, self.y))


# class for handling player events
class Player:
    def __init__(self, display, sprites, height, x_position, y_position):
        self.height = height
        self.screen = display
        self.sprites = sprites
        self.x_position = x_position
        self.y_position = y_position

    def draw_player(self):
        pygame.draw.rect(self.screen, (75, 75, 75), (self.x_position, self.y_position, 50, self.height))

    # movement handling
    def move_player_left(self):
        # restrict player's movement to stay inside the left screen boundary
        if self.x_position > 0:
            self.x_position -= 1

    def move_player_right(self):
        # restrict player's movement to stay inside the right screen boundary
        if self.x_position < self.screen.get_width() - 50:
            self.x_position += 1

    def move_player_up(self):
        # restrict player's movement to stay inside the top screen boundary
        if self.y_position > 0:
            self.y_position -= 1

    def move_player_down(self):
        # restrict player's movement to stay inside the bottom screen boundary
        if self.y_position < self.screen.get_height() - self.height:
            self.y_position += 1


# basketball class initialization
class Basketball:
    def __init__(self, display, position_x, position_y, bounce):
        self.position_x = position_x
        self.position_y = position_y
        # the boundary for the bounce of the ball in pixels
        self.bounce = bounce
        # the help variable
        self.help = 0
        self.up = True
        self.down = False
        self.screen = display

    def draw_the_ball(self):
        pygame.draw.circle(self.screen, "orange", (self.position_x, self.position_y), 11)

    # dribbling handling
    def move_the_ball(self):
        # Мяч движется вверх, пока не достигнет максимальной верхней точки
        if self.up and self.help < self.bounce:
            self.position_y -= 1
            self.help += 1
        # Если достиг верхней точки, меняем направление на вниз
        elif self.up and self.help >= self.bounce:
            self.up = False
            self.down = True
            self.help = 0
        # Мяч движется вниз, пока не достигнет начальной точки
        elif self.down and self.help < self.bounce:
            self.position_y += 1
            self.help += 1
        # Если достиг начальной точки, меняем направление на вверх
        elif self.down and self.help >= self.bounce:
            self.down = False
            self.up = True
            self.help = 0


# player initialization
player = Player(screen, None, 70, screen_width/2, screen_height/2)

# basketball initialization
ball = Basketball(screen, player.x_position+48, player.y_position+55, 30)

# background initialization
background = Background(0, 0, images)

# game engine variable initialization
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the pressed key
    pressed_key = pygame.key.get_pressed()

    # ball movement
    ball.move_the_ball()

    # movement handling
    if pressed_key[pygame.K_a]:
        player.move_player_left()
    elif pressed_key[pygame.K_d]:
        player.move_player_right()
    elif pressed_key[pygame.K_s]:
        player.move_player_down()
    elif pressed_key[pygame.K_w]:
        player.move_player_up()

    # diagonal movement
    if pressed_key[pygame.K_w] and pressed_key[pygame.K_d]:
        player.move_player_up()
        player.move_player_right()

    # fill the screen with the white collor
    screen.fill("white")

    # displaying game background
    background.display_background()

    # displaying the player
    player.draw_player()

    # displaying the ball
    ball.draw_the_ball()

    # apply the fps rate
    clock.tick(fps)

    # update the screen
    pygame.display.flip()

# quit the application
pygame.quit()
