import random

# Game settings
FPS = 15
WIDTH = 400
HEIGHT = 400
CELL = 20
START = (200, 200)


def random_cell(rng=random):
    """Pick a random grid position for food."""
    return (rng.randrange(0, WIDTH, CELL), rng.randrange(0, HEIGHT, CELL))


def place_food(snake, rng=random):
    """Pick a food position that isn't on the snake."""
    while True:
        pos = random_cell(rng)
        if pos not in snake:
            return pos


def change_direction(current, requested):
    """Return the new direction, ignoring a request to reverse into yourself."""
    if requested == (-current[0], -current[1]) and current != (0, 0):
        return current
    return requested


def hits_wall(head):
    return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT


def step(snake, snake_dir, food, score, rng=random):
    """Advance the game one tick.

    Returns (snake, food, score, died). The snake list is not modified in place.
    """
    if snake_dir == (0, 0):
        return snake, food, score, False

    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake = [head] + snake
    if head == food:
        score += 1
        food = place_food(snake, rng)
    else:
        snake.pop()

    died = head in snake[1:] or hits_wall(head)
    return snake, food, score, died


def main():
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    snake = [START]
    snake_dir = (0, 0)
    food = random_cell()
    score = 0
    running = True

    key_dirs = {
        pygame.K_UP: (0, -CELL),
        pygame.K_DOWN: (0, CELL),
        pygame.K_LEFT: (-CELL, 0),
        pygame.K_RIGHT: (CELL, 0),
    }

    # Run main game loop
    while running:
        # Handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update snake direction from keyboard
        keys = pygame.key.get_pressed()
        for key, direction in key_dirs.items():
            if keys[key]:
                snake_dir = change_direction(snake_dir, direction)
                break

        # Move snake and check collisions
        snake, food, score, died = step(snake, snake_dir, food, score)
        if died:
            snake = [START]
            snake_dir = (0, 0)
            food = random_cell()
            score = 0

        # Render game graphics
        screen.fill((0, 0, 0))
        for pos in snake:
            pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], CELL, CELL))
        pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], CELL, CELL))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    # Clean up and exit game
    pygame.quit()


if __name__ == "__main__":
    main()
