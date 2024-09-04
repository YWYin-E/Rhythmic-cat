import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Arrow Game")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FONT = pygame.font.Font(None, 36)

# Arrow images
arrow_up = pygame.image.load('arrow_up.png')
arrow_down = pygame.image.load('arrow_down.png')
arrow_left = pygame.image.load('arrow_left.png')
arrow_right = pygame.image.load('arrow_right.png')

arrow_images = [arrow_up, arrow_down, arrow_left, arrow_right]
arrow_positions = [(430, 0), (630, 0), (230, 0), (30, 0)]
arrow_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

# Background image
background = pygame.image.load('background.png')  # Ensure this file exists in the same directory

# Load border images for each arrow
border_up = pygame.image.load('border_up.png')
border_down = pygame.image.load('border_down.png')
border_left = pygame.image.load('border_left.png')
border_right = pygame.image.load('border_right.png')

# Positions for the border images (adjust as needed to match arrow positions)
border_positions = {
    'up': (430, HEIGHT - 150),
    'down': (630, HEIGHT - 150),
    'left': (230, HEIGHT - 150),
    'right': (30, HEIGHT - 150)
}

# Game variables
arrows = []
arrow_speed = 5
score = 0
misses = 0
max_misses = 5
spawn_rate = 1000  # milliseconds between spawns
last_spawn_time = pygame.time.get_ticks()
compliment = ""  # To store compliment messages
compliment_timer = 0  # Timer to show compliments

# Load and play music
pygame.mixer.music.load('Cute Meow.mp3')  # Ensure this file exists in the same directory
pygame.mixer.music.play(-1)  # Play the music on a loop

# Function to spawn a new arrow
def spawn_arrow():
    direction = random.randint(0, 3)
    x, y = arrow_positions[direction]
    arrows.append({"direction": direction, "x": x, "y": y})

# Function to reset the game
def reset_game():
    global score, misses, arrows, last_spawn_time, compliment
    score = 0
    misses = 0
    arrows = []
    last_spawn_time = pygame.time.get_ticks()
    compliment = ""

# Main game loop
running = True
while running:
    screen.blit(background, (0, 0))  # Draw the background image

    # Blit the border images for each arrow direction
    screen.blit(border_up, border_positions['up'])
    screen.blit(border_down, border_positions['down'])
    screen.blit(border_left, border_positions['left'])
    screen.blit(border_right, border_positions['right'])

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for arrow in arrows:
                if HEIGHT - 180 < arrow['y'] < HEIGHT - 110:
                    if event.key == arrow_keys[arrow['direction']]:
                        score += 1
                        arrows.remove(arrow)
                        compliment = random.choice(["Great!", "Awesome!", "Perfect!", "Nice!"])
                        compliment_timer = pygame.time.get_ticks()
                        break
            else:
                misses += 1

    # Spawn arrows
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_rate:
        spawn_arrow()
        last_spawn_time = current_time

    # Update arrow positions
    for arrow in arrows:
        arrow['y'] += arrow_speed
        if arrow['y'] > HEIGHT:
            arrows.remove(arrow)
            misses += 1

    # Draw arrows
    for arrow in arrows:
        screen.blit(arrow_images[arrow['direction']], (arrow['x'], arrow['y']))

    # Draw score and misses
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    misses_text = FONT.render(f"Misses: {misses}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(misses_text, (10, 50))

    # Show compliments if available
    if compliment and current_time - compliment_timer < 1000:  # Show for 1 second
        compliment_text = FONT.render(compliment, True, GREEN)
        screen.blit(compliment_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
    else:
        compliment = ""

    # Check for game over
    if misses >= max_misses:
        game_over_text = FONT.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()

        # Wait for player to press R to restart
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        waiting = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
