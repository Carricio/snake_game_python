import config
import pygame
from pygame import Vector2
from random import randrange

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont('Arial', 18)

def score(score):
    text = smallfont.render("PONTOS " + str(score), True, "black")  # Use a fonte smallfont aqui
    screen.blit(text, [0,0])

time = None
snake_rect = None
snake_lenght = None
snake_parts = None
snake_direction = None

food_rect = None

running = True
begin = True
bait = True

while running:
    if begin:
        begin = False
        time = 0
        snake_rect = pygame.rect.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             config.SNAKE_PART_SIZE,
             config.SNAKE_PART_SIZE])
        snake_lenght = 1
        snake_parts = []
        snake_direction = Vector2(0, 0)

    if bait:
        bait = False
        food_rect = pygame.rect.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             config.FOOD_SIZE,
             config.FOOD_SIZE])

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running == False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction[1] > 0:
                snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_DOWN and not snake_direction[1] < 0:
                snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_LEFT and not snake_direction[0] > 0:
                snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)
            if event.key == pygame.K_RIGHT and not snake_direction[0] < 0:
                snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)
    time_now = pygame.time.get_ticks()

    screen.fill(config.BG_COLOR)

    #Vertical lines in window with "pygame.draw.line"
    for i in range(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE):
        pygame.draw.line(screen, config.GRID_COLOR, (i,0), (i, config.SCREEN_SIZE))
        pygame.draw.line(screen, config.GRID_COLOR, (0,i), (config.SCREEN_SIZE, i))

    if time_now - time > config.DELAY:
        time = time_now
        snake_rect.move_ip(snake_direction)
        snake_parts.append(snake_rect.copy())
        snake_parts = snake_parts[-snake_lenght:]

    pygame.draw.rect(screen, config.FOOD_COLOR, food_rect, 0, 100)

    [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part, 8, 4)
     for snake_part in snake_parts]

    if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
            snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE or
            len(snake_parts) != len(set(snake_part.center for snake_part in snake_parts))):
        begin = True

    if snake_rect.center == food_rect.center:
        snake_lenght += 1
        bait = True

    score(snake_lenght-1)

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quite()

#happyhappy
