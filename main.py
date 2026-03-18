import pygame
import sys
from ga import create_population
from enemy import bfs_next_step

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Dungeon Game")

font = pygame.font.SysFont(None, 30)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0)
RED = (200,0,0)
BLUE = (0,0,200)
YELLOW = (255,255,0)

# 🔥 Difficulty
difficulty = "easy"
enemy_speed = 10

def set_difficulty():
    global enemy_speed
    if difficulty == "easy":
        enemy_speed = 15
    elif difficulty == "medium":
        enemy_speed = 8
    else:
        enemy_speed = 4

# 🔘 Button UI
def draw_button(text, x, y, w, h, color, hover_color):
    rect = pygame.Rect(x, y, w, h)
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)

    pygame.draw.rect(screen, BLACK, rect, 2)

    txt = font.render(text, True, WHITE)
    screen.blit(txt, txt.get_rect(center=rect.center))

    return rect

# 🎮 Generate map
population = create_population(20)
grid = population[0]

player = [0,0]
enemy = [9,9]
goal = [9,9]

steps = 0
clock = pygame.time.Clock()
enemy_timer = 0

game_state = "menu"

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if grid[r][c] == '#':
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, (200,200,200), rect, 1)

    pygame.draw.rect(screen, GREEN, (player[1]*CELL_SIZE, player[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW, (enemy[1]*CELL_SIZE, enemy[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_menu():
    screen.fill(WHITE)

    title = pygame.font.SysFont(None, 50).render("AI Dungeon Game", True, BLACK)
    screen.blit(title, (150, 80))

    easy = draw_button("EASY", 150, 200, 100, 50, GREEN, (0,255,0))
    med = draw_button("MEDIUM", 260, 200, 100, 50, BLUE, (0,0,255))
    hard = draw_button("HARD", 370, 200, 100, 50, RED, (255,0,0))

    start = draw_button("START", 230, 300, 140, 60, (100,100,255), (50,50,200))

    return start, easy, med, hard

def restart():
    global player, enemy, steps, game_state
    player = [0,0]
    enemy = [9,9]
    steps = 0
    game_state = "playing"
    set_difficulty()

# 🔁 GAME LOOP
while True:
    screen.fill(WHITE)

    if game_state == "menu":
        start_btn, easy_btn, med_btn, hard_btn = draw_menu()

    elif game_state == "playing":
        draw_grid()

        step_text = font.render(f"Steps: {steps}", True, BLACK)
        screen.blit(step_text, (10, 10))

        enemy_timer += 1
        if enemy_timer >= enemy_speed:
            enemy[:] = bfs_next_step(grid, enemy, player)
            enemy_timer = 0

        if player == goal:
            game_state = "win"

        if player == enemy:
            game_state = "lose"

    elif game_state == "win":
        txt = font.render("YOU WIN 🎉", True, GREEN)
        screen.blit(txt, (250, 250))
        restart_btn = draw_button("RESTART", 230, 320, 140, 50, BLUE, (0,0,255))

    elif game_state == "lose":
        txt = font.render("YOU LOST 😢", True, RED)
        screen.blit(txt, (250, 250))
        restart_btn = draw_button("RESTART", 230, 320, 140, 50, BLUE, (0,0,255))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if game_state == "menu":
                if start_btn.collidepoint(mx, my):
                    restart()
                elif easy_btn.collidepoint(mx, my):
                    difficulty = "easy"
                elif med_btn.collidepoint(mx, my):
                    difficulty = "medium"
                elif hard_btn.collidepoint(mx, my):
                    difficulty = "hard"

            elif game_state in ["win", "lose"]:
                if restart_btn.collidepoint(mx, my):
                    restart()

        if event.type == pygame.KEYDOWN and game_state == "playing":
            dr, dc = 0, 0
            if event.key == pygame.K_UP: dr = -1
            if event.key == pygame.K_DOWN: dr = 1
            if event.key == pygame.K_LEFT: dc = -1
            if event.key == pygame.K_RIGHT: dc = 1

            nr = (player[0] + dr) % ROWS   # ✅ player wrap allowed
            nc = (player[1] + dc) % COLS

            if grid[nr][nc] != '#':
                player = [nr, nc]
                steps += 1

    clock.tick(10)