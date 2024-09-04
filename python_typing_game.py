import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

# Fonts and colors
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Word settings
words = ["python", "pygame", "code", "keyboard", "mouse", "program", "computer", "developer"]
word_speed = 2
word_delay = 2000
last_word_time = pygame.time.get_ticks()

# Game variables
running = True
active_words = []
typed_word = ""

# Function to add a new word
def add_word():
    word = random.choice(words)
    x = random.randint(50, WIDTH - 150)
    y = 0
    active_words.append({"word": word, "x": x, "y": y})

# Main game loop
while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()

    # Check if it's time to add a new word
    if current_time - last_word_time > word_delay:
        add_word()
        last_word_time = current_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            else:
                typed_word += event.unicode

    # Update words position
    for word_obj in active_words:
        word_obj["y"] += word_speed
        word_text = FONT.render(word_obj["word"], True, WHITE)
        screen.blit(word_text, (word_obj["x"], word_obj["y"]))

        # Check if the typed word matches any word
        if typed_word == word_obj["word"]:
            active_words.remove(word_obj)
            typed_word = ""

    # Render typed word
    typed_text = FONT.render(typed_word, True, RED)
    screen.blit(typed_text, (10, HEIGHT - 40))

    # Game over if any word reaches the bottom
    for word_obj in active_words:
        if word_obj["y"] > HEIGHT:
            running = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
