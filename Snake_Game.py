#  Импортиуем библиотеки
import pygame
import time
import random

#  Инициализируем игру
pygame.init()

#  Задаем необходимые цвета в формате RGB
snake_color = (216, 239, 211)
food_color = (250, 112, 122)
background_color = (69, 71, 75)
white = (255, 255, 255)
black = (0, 0, 0)

#  Параметры экрана
dis_width, dis_height = 800, 600

#  Создаем окно
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake_Game')  #  Добавляем заголовок

#  Устанавливаем частоту кадров
clock = pygame.time.Clock()
snake_block, snake_speed = 20, 15  #  Устанавливаем размер и скорость змейки

#  Задаем шрифт для отображения кол-ва набранных очков
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

#  Добавляем счетчик набранных очков
high_score = 0


def display_score(high_score):
    """
    Изображение кол-ва очков на экране
    score_font.render позволяет изобразить Score: high_score на экране
    True - использование сглаживания шрифта
    white - цвет шрифта
    """
    value = score_font.render("Score: " + str(high_score), True, white)
    dis.blit(value, [0, 0])  #  Отображаем строчку с набранными очками в координатах [0, 0]


def display_high_score(high_score):
    """
    Изображение максимального ко-ва набранных очков
    score_font.render позволяет изобразить надпись на экране
    True - активируает сглаживание шрифта
    white - цвет шрифта
    """
    value = score_font.render("High_score: " + str(high_score), True, white)
    dis.blit(value, [dis_width - 200, 0])  #  Отображаем в надпись правом верхнем углу экрана


def our_snake(snake_block, snake_list):
    """
    Используем цикл for и метод draw.rect для отрисовки змейки
    1-ый параметр: где рисуем, 2-ой: цвет змейки, 3-ий: координаты и размер змейки
    4-ый: скругляем углы змейки
    """
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block], border_radius=4)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def game_over_animation():
    #  Создаем эффект мерцания экрана при заверешении игры
    for i in range(5):
        dis.fill(food_color)
        pygame.display.update()
        time.sleep(0.1)
        dis.fill(background_color)
        pygame.display.update()
        time.sleep(0.1)


def start_screen():
    while True:
        dis.fill(background_color)
        message("'C' - start game, 'Q' - quit game", white)
        pygame.display.update()
        for event in pygame.event.get():  #  Получаем все события происходящие в игре
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def gameLoop():
    global high_score

    #  Задаем позиции для змейки и еды
    x1, y1 = dis_width / 2, dis_height / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    score = 0
    paused = False

    while True:
        while paused:
            message("Пауза. Нажмите 'P' для продолжения", white)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.type == pygame.K_p:
                    paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                #  Контролируем движения змейки при помощи клавиш
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    paused = True

        #  Проверка столкновения змейки с границами игрового поля
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over_animation()
            start_screen()

        x1 += x1_change
        y1 += y1_change
        dis.fill(background_color)
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block], border_radius=4)

        snake_Head = [x1, y1]
        snake_list.append(snake_Head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        #  Проверка столкновения змейки с собой
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_over_animation()
                start_screen()

        our_snake(snake_block, snake_list)
        display_score(score)
        display_high_score(high_score)

        pygame.display.update()

        #  Проверка съедения змейкой еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            score += 1
            if score > high_score:
                high_score = score

        clock.tick(snake_speed)


start_screen()
gameLoop()
