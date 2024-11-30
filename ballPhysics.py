import random

import pygame, sys
from pygame.sprite import collide_rect


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
    def __init__(self, position_x, position_y, floor_group, hoop_group, trigger_group, scale=1.5, gravity=0.5):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Ball-0001.png'))

        # Scale the image
        self.image = pygame.transform.scale(self.sprites[0], (int(16 * scale), int(16 * scale)))

        self.rect = self.image.get_rect()
        self.gravity = gravity

        # Ball's initial position and velocity
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = 0
        self.velocity_y = 0

        self.score = 0

        self.active = False  # Is the ball active (in motion)?
        self.thrown = False  # Has the ball been thrown?
        self.throw_time = pygame.time.get_ticks() # Time when the ball was thrown
        self.last_collision_time = 0  # Time of the last collision

        self.floor_group = floor_group
        self.hoop_group = hoop_group
        self.trigger_group = trigger_group

        # Create a mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # Setting the top-left position of the ball sprite
        self.rect.topleft = [self.position_x, self.position_y]

    def set_activate(self):
        self.active = True

    def return_to_the_player_position(self, player_position):
        """Returns the ball to the player's position."""
        self.position_x, self.position_y = player_position
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False
        self.thrown = False
        self.rect.topleft = [self.position_x, self.position_y]


    def set_shooting_position(self, shooting_position):
        """Sets the ball at a shooting position."""
        self.position_x, self.position_y = shooting_position
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False
        self.thrown = False
        self.rect.topleft = [self.position_x, self.position_y]

    def throw(self, direction_x, direction_y):
        """Throws the ball with a given velocity."""
        if not self.thrown:
            self.velocity_x = direction_x
            self.velocity_y = direction_y
            self.active = True
            self.thrown = True
            self.throw_time = pygame.time.get_ticks()  # Save the time when the ball was thrown


    def deactivate(self):
        self.active = False
        self.thrown = False

    def get_score(self):
        return self.score

    def check_collision(self, trigger_group):
        current_time = pygame.time.get_ticks()

        # Check if 0.5 seconds have passed since the last collision
        if current_time - self.last_collision_time >= 500:
            for trigger in trigger_group:
                if pygame.sprite.collide_mask(self, trigger):
                    self.score += 1
                    net_sound.play()  # Play the sound when the ball hits the trigger
                    self.last_collision_time = current_time  # Update the last collision time
                    break

    def update(self):
        if self.active:
            # Apply gravity to vertical velocity
            self.velocity_y += self.gravity

            # Update position based on velocity
            self.position_x += self.velocity_x
            self.position_y += self.velocity_y
            self.rect.topleft = [self.position_x, self.position_y]

            # Check for collision with any floor in the group
            for floor in self.floor_group:
                if pygame.sprite.collide_mask(self, floor):

                    # Adjust the ball's position to stay on top of the floor
                    self.position_y = floor.rect.top - self.rect.height
                    self.rect.topleft = [self.position_x, self.position_y]

                    # Reverse and reduce vertical velocity for realistic bounce
                    self.velocity_y *= -0.75  # Simulates energy loss (damping factor)

                    if abs(self.velocity_y) >= 3:
                        ball_sound.play()

                    # Stop bouncing if the vertical velocity is negligible
                    if abs(self.velocity_y) < 0.5:
                        self.velocity_y = 0
                        self.position_y = floor.rect.top - self.rect.height
                        self.rect.topleft = [self.position_x, self.position_y]

                        # Stop horizontal movement if the ball slows down
                        self.velocity_x *= 0.95  # Simulate friction
                        if abs(self.velocity_x) < 0.5:
                            self.velocity_x = 0
                            self.active = False
                        break
            for hoop in self.hoop_group:
                if pygame.sprite.collide_mask(self, hoop):
                    self.velocity_x*=-0.7

            self.check_collision(self.trigger_group)

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

class Trigger(pygame.sprite.Sprite):
    def __init__(self, position_y):
        super().__init__()
        self.position_y = position_y
        self.image = pygame.Surface((45, 1))
        self.image.set_alpha(1)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.y = position_y
        self.rect.x = 858

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

pygame.mixer.init()  # Initialize the mixer for sound playback

# Load sound effects
ball_sound = pygame.mixer.Sound('Sounds/ballSound.mp3')
net_sound = pygame.mixer.Sound('Sounds/netSound.mp3')

pygame.mixer.music.load('Sounds/soundTrack.mp3')
pygame.mixer.music.play(-1)
# Set the volume of the background music
pygame.mixer.music.set_volume(0.3)

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
trigger_group = pygame.sprite.Group()

# Create floor ball and hoop objects
floor = Floor(385, screen_width)
ball = Ball(495, 110, floor_group, hoop_group, trigger_group)
ball.set_activate()  # Make the ball active
hoop = Hoop(718, 35)
trigger = Trigger(200)

# Add floor and ball to the sprite groups
ball_group.add(ball)
floor_group.add(floor)
hoop_group.add(hoop)
trigger_group.add(trigger)

# Load second hoop
left_hoop = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/Hoop-0001.png'), (265, 340)), True, False)

# Load player
player_standing = pygame.transform.scale(pygame.image.load('Images/MainPlayer-0001.png'), (50, 100))
player_shooting = pygame.transform.scale(pygame.image.load('Images/MainPlayer-0002.png'), (50, 100))

# Load emoji
emoji = pygame.transform.scale(pygame.image.load('Images/Emogi-0001.png'), (50, 50))

# Scale and load court and hoop images
court = pygame.transform.scale(pygame.image.load('Images/Court-0001.png'), (screen_width, 150))

ball_img_main_menu = pygame.transform.scale(pygame.image.load('Images/Ball-0001.png'), (50,50))

# Load and scale table
table = pygame.transform.scale(pygame.image.load('Images/tablo.png'), (150,150))

zero = pygame.transform.scale(pygame.image.load('Images/zero.png'), (50,50))
one = pygame.transform.scale(pygame.image.load('Images/one.png'), (50,50))
two = pygame.transform.scale(pygame.image.load('Images/two.png'), (50,50))
three = pygame.transform.scale(pygame.image.load('Images/three.png'), (50,50))
four = pygame.transform.scale(pygame.image.load('Images/four.png'), (50,50))
five = pygame.transform.scale(pygame.image.load('Images/five.png'), (50,50))
six = pygame.transform.scale(pygame.image.load('Images/six.png'), (50,50))
seven = pygame.transform.scale(pygame.image.load('Images/seven.png'), (50,50))
eight = pygame.transform.scale(pygame.image.load('Images/eight.png'), (50,50))
nine = pygame.transform.scale(pygame.image.load('Images/nine.png'), (50,50))


# Array of buttons
buttons = []

Button(screen_width/2-50, screen_height/2-30, 100, 50, 'Play', hide_menu)
Button(screen_width/2-70, screen_height/2+30, 140, 50, 'Print the ball', display_random_ball, True)

# Initialization of the menu
menu = MainMenu((29, 41, 58), None, screen, buttons)

score = 0

is_shooting_ball = False

range_left = -16.0
range_right = -8.0

old_score = 0

finished = False
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

        # Draw the player
        if pygame.key.get_pressed()[pygame.K_RETURN] and not finished:
            is_shooting_ball = True
        else:
            is_shooting_ball = False
        # Check the current score
        score = ball_group.sprites()[0].get_score()
        # Blit the score table
        screen.blit(table, (415, 140))
        screen.blit(zero, (435, 170))
        match score:
            case 0:
                screen.blit(zero, (498, 170))
            case 1:
                screen.blit(one, (498, 170))
            case 2:
                screen.blit(two, (498, 170))
            case 3:
                screen.blit(three, (498, 170))
            case 4:
                screen.blit(four, (498, 170))
            case 5:
                screen.blit(five, (498, 170))
            case 6:
                screen.blit(six, (498, 170))
            case 7:
                screen.blit(seven, (498, 170))
            case 8:
                screen.blit(eight, (498, 170))
            case 9:
                screen.blit(nine, (498, 170))
            case _:
                # Handle any case where the score is not between 0 and 9
                pass

        if is_shooting_ball and not finished:
            # Handle the ball position
            ball = ball_group.sprites()[0]
            ball.return_to_the_player_position((692, 330))
            ball.set_shooting_position((710, 268))


            random_y_force = random.uniform(range_left, range_right)
            ball.throw(5, random_y_force)

            # With every made basket make the range closer to the ideal range of -11 and -13
            if old_score != score:
                old_score = score
                if range_right > -11 and range_left < -13:
                    range_right-=1
                    range_left+=1
            screen.blit(player_shooting, (670, 270))
            screen.blit(emoji, (700, 220))
        else:
            screen.blit(player_standing, (670, 290))
        ball_group.draw(screen)  # Draw the ball

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            ball = ball_group.sprites()[0]
            # ball.roll_the_ball_test()
            ball.return_to_the_player_position((692, 330))
        ball_group.update()  # Update ball's position and velocity

        # Draw the left hoop
        screen.blit(left_hoop, (18, 35))

        floor_group.draw(screen)  # Draw the floor
        hoop_group.draw(screen)
        trigger_group.draw(screen)

        if score == 10:
            finished = True
            screen.fill((29, 41, 58))
            message = font.render("You did it! You truly put them to sleep.", True, (255, 255, 255))
            message2 = font.render(
                "Nine threes is a good result. Keep practicing and maybe you will become Stephen Curry.", True,
                (255, 255, 255))
            exit_button = pygame.Rect(screen_width/2-50, screen_height/2, 100, 50)
            # Draw the final message
            screen.blit(message, (50, 200))
            screen.blit(message2, (50, 250))

            mouse_position = pygame.mouse.get_pos()
            # Draw the exit button
            pygame.draw.rect(screen, (255,255,255), exit_button)

            # Change color on hover
            if exit_button.collidepoint(mouse_position):
                pygame.draw.rect(screen, (102,102,102), exit_button)

            exit_text = font.render('Exit', True, (0, 0, 0))
            screen.blit(exit_text, (exit_button.x+33, exit_button.y+10))

            # Check for button click to exit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain a consistent frame rate
