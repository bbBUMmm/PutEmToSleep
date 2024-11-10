import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Однократная анимация игрока при нажатии пробела")

# Класс игрока с анимацией
class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_folder, scale_factor=4, animation_speed=0.1):
        super().__init__()
        self.frames = []
        self.load_frames(sprite_folder, scale_factor)
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.last_update = pygame.time.get_ticks()
        self.animating = False  # Флаг, чтобы отслеживать, идет ли анимация

    def load_frames(self, sprite_folder, scale_factor):
        # Загрузка всех кадров из папки
        for i in range(1, 14):  # Предполагаем, что у нас 13 кадров Sprite-0001.png, ..., Sprite-0013.png
            image = pygame.image.load(f"{sprite_folder}/Sprite-{str(i).zfill(4)}.png").convert_alpha()
            image = pygame.transform.scale(image, (16 * scale_factor, 16 * scale_factor))
            self.frames.append(image)

    def start_animation(self):
        # Запуск анимации с первого кадра
        if not self.animating:
            self.animating = True
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

    def update(self):
        # Обновление анимации только если флаг animating установлен в True
        if self.animating:
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 * self.animation_speed:
                self.last_update = now
                self.current_frame += 1

                # Проверка окончания анимации
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.animating = False  # Остановить анимацию
                else:
                    self.image = self.frames[self.current_frame]

# Создаем группу спрайтов и игрока
all_sprites = pygame.sprite.Group()
player = Player("png", scale_factor=8, animation_speed=0.1)
all_sprites.add(player)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.start_animation()  # Запускаем анимацию при нажатии на пробел

    # Обновление всех спрайтов
    all_sprites.update()

    # Заливка фона
    screen.fill((150, 150, 150))

    # Отображение всех спрайтов
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()
