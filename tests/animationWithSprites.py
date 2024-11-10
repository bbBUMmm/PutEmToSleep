import pygame, sys


# noinspection DuplicatedCode
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

pygame.init()
clock = pygame.time.Clock()

screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Sprite Animation')

moving_sprites = pygame.sprite.Group()
player = Player(100,100)
moving_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)