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

    def move_player_left(self):
        self.x_position -= 1

    def move_player_right(self):
        self.x_position += 1

    def move_player_up(self):
        self.y_position -= 1

    def move_player_down(self):
        self.y_position += 1


# player initialization
player = Player(screen, None, 70, screen_width/2, screen_height/2)

# background initialization
background = Background(0, 0, images)

# game engine variable initialization
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with the white collor
    screen.fill("white")

    # displaying game background
    background.display_background()

    # displaying the player
    player.draw_player()

    # get the pressed key
    pressed_key = pygame.key.get_pressed()

    # apply the fps rate
    clock.tick(fps)

    # update the screen
    pygame.display.flip()

# quit the application
pygame.quit()
