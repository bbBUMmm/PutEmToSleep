import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Параметры окна
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Бросок мяча в корзину")

# Глобальные параметры физики
gravity = 0.23  # Сила гравитации

# Класс игрока (для броска мяча)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 100))  # Простой прямоугольник для игрока
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))

# Класс мяча с физикой
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 165, 0), (8, 8), 8)  # Оранжевый круг для мяча
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False  # Флаг активности мяча
        self.start_position = (x, y)  # Начальная позиция мяча

    def throw(self, angle, power):
        # Расчет начальных скоростей по углу и силе броска
        self.velocity_x = power * math.cos(math.radians(angle))
        self.velocity_y = -power * math.sin(math.radians(angle))
        self.active = True

    def update(self):
        if self.active:
            # Обновление позиции мяча с учетом скорости
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

            # Применение гравитации
            self.velocity_y += gravity

            # Проверка выхода за экран
            if self.rect.top > screen_height:
                self.active = False  # Остановка мяча, если он вышел за нижний край экрана
                self.rect.bottom = screen_height  # Прижимаем мяч к полу

            # Проверка выхода за пределы экрана по бокам
            if self.rect.left < 0:
                self.rect.left = 0
                self.velocity_x = -self.velocity_x  # Отскок от стены
            if self.rect.right > screen_width:
                self.rect.right = screen_width
                self.velocity_x = -self.velocity_x  # Отскок от стены

    def reset(self):
        """Возвращаем мяч в стартовую позицию"""
        self.rect.center = self.start_position
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False

# Класс корзины
class Hoop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 10))  # Простой прямоугольник для обода
        self.image.fill((139, 69, 19))  # Коричневый цвет для обода корзины
        self.rect = self.image.get_rect(center=(x, y))
        self.backboard = pygame.Rect(x - 50, y - 50, 10, 50)  # Прямоугольник для щита

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.backboard)  # Рисуем щит

# Создаем спрайты
player = Player(screen_width // 4, screen_height - 150)
ball = Ball(player.rect.centerx, player.rect.top)
hoop = Hoop(screen_width - 200, screen_height // 3)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)
all_sprites.add(hoop)

# Игровой цикл
angle = 45  # Угол броска
power = 150  # Сила броска

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball.active:
                # Бросок мяча при нажатии на пробел
                ball.throw(angle, power)
            elif event.key == pygame.K_r:
                # Возврат мяча к игроку при нажатии на R
                ball.reset()

    # Обновление мяча и других спрайтов
    ball.update()

    # Проверка столкновений с ободом и щитом
    if ball.active:
        if ball.rect.colliderect(hoop.rect):  # Столкновение с ободом
            ball.velocity_y = -ball.velocity_y * 0.7  # Отскок с потерей скорости
            ball.rect.y = hoop.rect.top - ball.rect.height  # Коррекция позиции мяча
        elif ball.rect.colliderect(hoop.backboard):  # Столкновение с щитом
            ball.velocity_x = -ball.velocity_x * 0.7  # Отскок в обратном направлении

    # Заливка фона
    screen.fill((150, 150, 150))

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)
    hoop.draw(screen)  # Отдельный метод для отрисовки щита

    # Отрисовка пола
    pygame.draw.rect(screen, (0, 255, 0), (0, screen_height - 10, screen_width, 10))  # Зеленый пол

    # Отрисовка стен
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 10, screen_height))  # Левая стена
    pygame.draw.rect(screen, (0, 0, 0), (screen_width - 10, 0, 10, screen_height))  # Правая стена

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)
