import pygame, sys

class Ball(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y, scale=4, gravity=0.5):
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
        # Setting the top-left position of the ball sprite
        self.rect.topleft = [self.position_x, self.position_y]

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        # If the ball is active, apply gravity and update its position
        if self.active:
            self.velocity_y += self.gravity  # Gravity affecting the vertical speed
            self.position_y += self.velocity_y  # Update position based on velocity
            self.rect.topleft = [self.position_x, self.position_y]  # Update sprite's position

            # Check if the ball has collided with the floor (based on floor's rect)
            if self.rect.colliderect(floor.rect) and self.rect.bottom >= floor.rect.top:
                self.velocity_y *= -0.8  # Reverse and reduce speed (damping effect)
                self.position_y = floor.rect.top - self.rect.height  # Make sure the ball is on top of the floor
                self.rect.topleft = [self.position_x, self.position_y]  # Update position after bounce


# noinspection DuplicatedCode
class Floor(pygame.sprite.Sprite):
    def __init__(self, position_y, floor_width):
        super().__init__()
        self.position_y = position_y
        self.floor_width = floor_width
        self.image = pygame.Surface((floor_width, 20))
        self.image.fill((0, 0, 0))  # Black color for the floor
        self.rect = self.image.get_rect()
        self.rect.y = position_y

pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sprite Animation')

# Create sprite groups
moving_sprites = pygame.sprite.Group()
stack_sprites = pygame.sprite.Group()

# Create floor and ball objects
floor = Floor(380, screen_width)
ball = Ball(180, 100)
ball.activate()  # Make the ball active

# Add floor and ball to the sprite groups
moving_sprites.add(ball)
stack_sprites.add(floor)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    # Clear the screen and redraw everything
    screen.fill((255, 255, 255))
    moving_sprites.draw(screen)  # Draw the ball
    moving_sprites.update()  # Update ball's position and velocity
    stack_sprites.draw(screen)  # Draw the floor
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Maintain a consistent frame rate
