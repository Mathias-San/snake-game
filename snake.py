import pygame
import random

pygame.init()

# --- settings ---
WINDOW_SIZE = 600
CELL_SIZE = 20
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
FPS = 10

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("arial", 36)
font_small = pygame.font.SysFont("arial", 24)

# --- food ---
def spawn_food(snake):
    while True:
        x = random.randrange(0, WINDOW_SIZE, CELL_SIZE)
        y = random.randrange(0, WINDOW_SIZE, CELL_SIZE)
        if [x, y] not in snake:
            return [x, y]

# --- draw grid (optional visual touch) ---
def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_SIZE, y))

# --- reset game state ---
def reset_game():
    snake = [[300, 300], [280, 300], [260, 300]]  # start with 3 blocks
    direction = [CELL_SIZE, 0]
    food = spawn_food(snake)
    score = 0
    game_over = False
    return snake, direction, food, score, game_over

# --- initialise ---
snake, direction, food, score, game_over = reset_game()
high_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                # prevent reversing into yourself
                if event.key == pygame.K_UP and direction != [0, CELL_SIZE]:
                    direction = [0, -CELL_SIZE]
                if event.key == pygame.K_DOWN and direction != [0, -CELL_SIZE]:
                    direction = [0, CELL_SIZE]
                if event.key == pygame.K_LEFT and direction != [CELL_SIZE, 0]:
                    direction = [-CELL_SIZE, 0]
                if event.key == pygame.K_RIGHT and direction != [-CELL_SIZE, 0]:
                    direction = [CELL_SIZE, 0]

            # restart on R
            if event.key == pygame.K_r and game_over:
                snake, direction, food, score, game_over = reset_game()

    if not game_over:
        # --- move snake ---
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        snake.insert(0, new_head)

        # --- wall collision ---
        if (new_head[0] < 0 or new_head[0] >= WINDOW_SIZE or
                new_head[1] < 0 or new_head[1] >= WINDOW_SIZE):
            game_over = True
            if score > high_score:
                high_score = score

        # --- self collision ---
        if new_head in snake[1:]:
            game_over = True
            if score > high_score:
                high_score = score

        # --- food collision ---
        if new_head == food:
            score += 1
            food = spawn_food(snake)
            # speed increases every 5 points
            FPS = 10 + (score // 5) * 2
        else:
            snake.pop()

    # --- drawing ---
    screen.fill(BLACK)
    draw_grid()

    # draw food (with inner highlight)
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (255, 80, 80), (food[0] + 4, food[1] + 4, 6, 6))

    # draw snake (head brighter than body)
    for i, block in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (block[0] + 1, block[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    # draw score
    score_text = font_small.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # draw game over screen
    if game_over:
        # dark overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        over_text = font_big.render("GAME OVER", True, RED)
        score_end = font_small.render(f"Your score: {score}", True, WHITE)
        high_text = font_small.render(f"High score: {high_score}", True, WHITE)
        restart_text = font_small.render("Press R to play again", True, GRAY)

        screen.blit(over_text, over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 60)))
        screen.blit(score_end, score_end.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)))
        screen.blit(high_text, high_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 36)))
        screen.blit(restart_text, restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 80)))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
