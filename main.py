import random
import pygame
from os import listdir
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init() # это команда, которая запускает pygame. Инициализация pygame

# pygame.mixer.music.load("MYGAME\sounds\main_theme.mp3")
# pygame.mixer.music.play(-1)

FPS = pygame.time.Clock()

screen = width, heigth = 1000, 800 # Размер экрана
main_surface = pygame.display.set_mode(screen) # Экран

# ---------- Цвета-----------
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
PINK = 255, 0, 255
LIGHTBLUE = 0, 255, 255
GREY = 155, 155, 155

# ___________Шрифт____________

font = pygame.font.SysFont('Caslon', 20)

# -------------Игрок-------------
IMG_PASS = 'img\piggeon'
# player = pygame.Surface((20, 20)) # Новый объект с размерами (таппл)
# player.fill((RED)) # Цвет
player_imgs = [pygame.image.load(IMG_PASS + '/' + file).convert_alpha() for file in listdir('img\piggeon')]
player = player_imgs[0]
# player = pygame.image.load('MYGAME\img\player.png').convert_alpha()
player_rect = player.get_rect()
player_speed = 10

#-------------- Враг------------
IMG_ENEM = 'img\enemy'
enemy_imgs = [pygame.image.load(IMG_ENEM + '/' + file).convert_alpha() for file in listdir('img\enemy')]

def create_enemy(): # Функция
     # enemy = pygame.Surface((20, 20))
    # enemy.fill(PINK)
    # enemy = pygame.image.load('MYGAME\img\enemy.png').convert_alpha()
    enemy = enemy_imgs[0]
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size()) # Распаковать 
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed] # (список)
 
# -------------Бонус-------------
def create_bonus(): # Функция
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(LIGHTBLUE)
    bonus = pygame.image.load('img/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size()) # Распаковать  -bonus.get_height()
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed] # [0] [1] [2] (список)


# -------------Задник------------------

bg = pygame.transform.scale(pygame.image.load('img/background.jpg').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

# --------Ивенты и списки----------
CREATE_ENEMY = pygame.USEREVENT + 1 # Добавляем ивент
pygame.time.set_timer(CREATE_ENEMY, 1500) # Время добавляение ивента 1.5 секунды

CREATE_BONUS = pygame.USEREVENT + 2 # Добавляем 2й ивент
pygame.time.set_timer(CREATE_BONUS, 1500) # 

CHANGE_IMGS = pygame.USEREVENT + 3 
pygame.time.set_timer(CHANGE_IMGS, 125) # 

CHANGE_ENEMY = pygame.USEREVENT + 4 
pygame.time.set_timer(CHANGE_ENEMY, 100) # 

img_index = 0
enemy_index = 0

scores = 0

enemies = []
bonuses = []

# ----------------------------
is_working = True  
while is_working:
    FPS.tick(60) # Фреймы

    for event in pygame.event.get(): # Для элемента в ивенте
        if event.type == QUIT: # Если ивент = выход
            is_working = False # Выйти
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy()[0:3]) # Добавляет нового врага
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus()) # Добавляет новый бонус

        if event.type == CHANGE_IMGS:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]    

        if event.type == CHANGE_ENEMY:
            enemy_index += 1
            if enemy_index == len(enemy_imgs):
                enemy_index = 0
            enemy = enemy_imgs[enemy_index]

    pressed_keys = pygame.key.get_pressed() # Если клавиша нажата

    # main_surface.fill((GREY)) # Сделали экран серым
    # main_surface.blit(bg, (0, 0))

 # ------------Движение заднего фона--------------
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width(): 
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, (player_rect)) # Отобразить игрока 
    main_surface.blit(font.render(str(scores), True, RED), (width -30, 0)) # Отобразить мяч

    # if player_rect.bottom >= heigth or player_rect.top <= 0: # Если больше высоты или верха 
    #     player.fill((GREEN)) # При ударе меняет цвет
    #     player_speed[1] = -player_speed[1] # то по игреку меняется на обратное значение

    # if player_rect.right >= width or player_rect.left <= 0: # Если больше ширины или левой стороны 
    #     player.fill((BLUE)) # При ударе меняет цвет
    #     player_speed[0] = -player_speed[0] # то по иксу меняется на обратное значение

   
    # ----------Движение врагов-------------
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        enemy[0] = enemy_imgs[enemy_index] # Обновление спрайта врага
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False
            print('You lose!' )
            
     # ------------Движение бонусов--------------
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1]) # Отобразить бонус 

        if bonus[1].bottom >= heigth: # Если позиция бонуса больше высоты
            bonuses.pop(bonuses.index(bonus)) # Мы находим индекс бонуса в списке и удаляем его

        if player_rect.colliderect(bonus[1]): # Если игрок прикаcается к бонусу
            bonuses.pop(bonuses.index(bonus))
            scores += 5


    # ------------Движение игрока--------------
    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth: # Если нажата клавиша 
        player_rect = player_rect.move(0, player_speed) # Вниз  
    if pressed_keys[K_UP]and not player_rect.top <= 0: 
        player_rect = player_rect.move(0, -player_speed) # Вверх
    if pressed_keys[K_RIGHT]and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0) # Вправо
    if pressed_keys[K_LEFT]and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0) #Влево

    # print(len(enemies)) # Вывод длинны списка с врагами


    pygame.display.update() # добавить эту команду
    pygame.display.flip() # Обновить экран

 




