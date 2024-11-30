import random

import pygame, sys


class Button:
    def __init__(self,x,y,width,height, button_text, onclick_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclick_function
        self.onePress = one_press
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(button_text, True, (20, 20, 20))

        # Append itself to the buttons list
        buttons.append(self)
    def process(self):
        mouse_position = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_position):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0] == 1:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # Blit the text onto the buttonSurface and then this surface onto the screen
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

# Class to handle Main Menu logic
class MainMenu:
    def __init__(self, background_color, soundtrack, window, buttons):
        self.background_color = background_color
        self.soundtrack = soundtrack
        self.window = window
        self.active = True
        self.buttons = buttons
        self.filled = False

    def draw_the_menu(self):
        if not self.filled:
            self.window.fill(self.background_color)
            self.filled = True

        self.display_buttons()
        pygame.display.flip()

    def display_buttons(self):
        for button in self.buttons:
            button.process()

    def set_active(self):
        self.active = True

    def disable(self):
        self.active = False

# Class to handle Ball logic
class Ball(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y, floor_group, scale=1.5, gravity=0.5):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Ball-0001.png'))

        # Scale the image
        self.image = pygame.transform.scale(self.sprites[0], (16 * scale, 16 * scale))

        self.rect = self.image.get_rect()
        self.gravity = gravity

        # Ball's initial position and velocity
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = 0
        self.velocity_y = 0

        self.active = False

        self.floor_group = floor_group

        # Create a mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # Setting the top-left position of the ball sprite
        self.rect.topleft = [self.position_x, self.position_y]

    def set_activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def roll_the_ball_test(self):
        self.velocity_x+=65
        self.position_x+=self.velocity_x
        # first tries to implement rotation
        # for n in range(1, 45):
        #     self.image = pygame.transform.rotate(self.image, n)

    def update(self):
        if self.active:
            # Apply gravity to vertical velocity
            self.velocity_y += self.gravity
            self.position_y += self.velocity_y
            self.rect.topleft = [self.position_x, self.position_y]

            # Check for collision with any floor in the group
            for floor in self.floor_group:
                if pygame.sprite.collide_mask(self, floor):
                    # Adjust the ball's position to stay on top of the floor
                    self.position_y = floor.rect.top - self.rect.height
                    self.rect.topleft = [self.position_x, self.position_y]

                    # Reverse and reduce vertical velocity for realistic bounce
                    self.velocity_y *= -0.8  # Simulates energy loss (damping factor)

                    # Stop bouncing if the vertical velocity is negligible
                    if abs(self.velocity_y) < 0.5:  # Stop threshold
                        self.velocity_y = 0
                        self.position_y = floor.rect.top - self.rect.height
                        self.rect.topleft = [self.position_x, self.position_y]
                        self.active = False  # Deactivate the ball to stop movement
                        break


# noinspection DuplicatedCode
class Floor(pygame.sprite.Sprite):
    def __init__(self, position_y, floor_width):
        super().__init__()
        self.position_y = position_y
        self.floor_width = floor_width
        self.image = pygame.Surface((floor_width, 20))
        # make floor invisible
        self.image.set_alpha(1)
        self.image.fill((0,0,0))  # Black color for the floor
        self.rect = self.image.get_rect()
        self.rect.y = position_y

# Class to handle hoop logic (
# collisions with the ball
# count of the successful baskets
# )
class Hoop(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        # Already scaled up image of the hoop
        self.image = pygame.transform.scale(pygame.image.load('Images/Hoop-0001.png'), (265, 340))
        self.rect = self.image.get_rect()

        self.position_x = position_x
        self.position_y = position_y

        self.rect.topleft = (self.position_x, self.position_y)

def hide_menu():
    menu.disable()

def display_random_ball():
    global last_update_time
    current_time = pygame.time.get_ticks()

    # Check and do the code every  ms
    if current_time - last_update_time >= 100:
        last_update_time = current_time

        random_angle = random.randint(-360, 360)
        random_x = random.randint(0, 1000)
        random_y = random.randint(0, 600)
        screen.blit(
            pygame.transform.rotate(ball_img_main_menu, random_angle),
            (random_x, random_y)
        )

# Initialization of the pygame
pygame.init()

# Creating variable to track fps and time
clock = pygame.time.Clock()

# Variable to control last update time
last_update_time = 0

# Basic fonts for the buttons text
font = pygame.font.SysFont('Arial', 24)

# Screen dimensions
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sprite Animation')

# Create sprite groups
ball_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
hoop_group = pygame.sprite.Group()

# Create floor ball and hoop objects
floor = Floor(385, screen_width)
ball = Ball(180, 110, floor_group)
ball.set_activate()  # Make the ball active
hoop = Hoop(718, 35)

# Add floor and ball to the sprite groups
ball_group.add(ball)
floor_group.add(floor)
hoop_group.add(hoop)

# Load second hoop
left_hoop = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/Hoop-0001.png'), (265, 340)), True, False)

# Load player
player_standing = pygame.transform.scale(pygame.image.load('Images/MainPlayer-0001.png'), (50, 100))
player_shooting = pygame.transform.scale(pygame.image.load('Images/MainPlayer-0002.png'), (50, 100))

# Scale and load court and hoop images
court = pygame.transform.scale(pygame.image.load('Images/Court-0001.png'), (screen_width, 150))

ball_img_main_menu = pygame.transform.scale(pygame.image.load('Images/Ball-0001.png'), (50,50))

# Array of buttons
buttons = []

Button(screen_width/2-50, screen_height/2-30, 100, 50, 'Play', hide_menu)
Button(screen_width/2-70, screen_height/2+30, 140, 50, 'Print the ball', display_random_ball, True)

# Initialization of the menu
menu = MainMenu((29, 41, 58), None, screen, buttons)

pressed = False
is_shooting_ball = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if menu.active:
        menu.draw_the_menu()
    else:
        # Clear the screen and redraw everything
        screen.fill((175,175,175))
        screen.blit(court, (0, 290))

        ball_group.draw(screen)  # Draw the ball
        if pygame.key.get_pressed()[pygame.K_SPACE] and not pressed:
            ball = ball_group.sprites()[0]
            ball.roll_the_ball_test()
            pressed = True
        ball_group.update()  # Update ball's position and velocity

        # Draw the left hoop
        screen.blit(left_hoop, (18, 35))


        floor_group.draw(screen)  # Draw the floor
        hoop_group.draw(screen)

        # Draw the player
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            is_shooting_ball = True
        else:
            is_shooting_ball = False
        if is_shooting_ball:
            screen.blit(player_shooting, (670, 270))
        else:
            screen.blit(player_standing, (670, 290))
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain a consistent frame rate
