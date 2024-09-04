import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Typing Game")

# Fonts and colors
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game variables
words = ["python", "pygame", "code", "keyboard", "mouse", "program", "computer", "developer", "bonus", "extra"]
special_words = ["bonus", "extra"]
word_speed = 2
word_delay = 2000
last_word_time = pygame.time.get_ticks()
score = 0
lives = 3
level = 1
level_threshold = 10
game_over = False

# Sounds
pygame.mixer.init()
typing_sound = pygame.mixer.Sound("type_sound.wav")
correct_sound = pygame.mixer.Sound("correct.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
life_loss_sound = pygame.mixer.Sound("life_loss.wav")  # New life loss sound

# Game word list
active_words = []
typed_word = ""
typing_active = False  # New flag to track typing activity

# Function to add a new word
def add_word():
    word = random.choice(words)
    x = random.randint(50, WIDTH - 150)
    y = 0
    active_words.append({"word": word, "x": x, "y": y})

# Function to reset the game
def reset_game():
    global score, lives, level, word_speed, word_delay, game_over
    score = 0
    lives = 3
    level = 1
    word_speed = 2
    word_delay = 2000
    game_over = False
    active_words.clear()

# Main game loop
while True:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()

    if not game_over:
        # Check if it's time to add a new word
        if current_time - last_word_time > word_delay:
            add_word()
            last_word_time = current_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]
                    if typed_word == "":
                        typing_sound.stop()
                        typing_active = False
                elif event.key == pygame.K_RETURN:
                    typed_word = ""
                    typing_sound.stop()
                    typing_active = False
                else:
                    if not typing_active:  # Play sound when typing starts
                        typing_sound.play(loops=-1)
                        typing_active = True
                    typed_word += event.unicode

            elif event.type == pygame.KEYUP:
                if typing_active and not typed_word:
                    typing_sound.stop()
                    typing_active = False

        # Update words position
        for word_obj in active_words:
            word_obj["y"] += word_speed
            word_text = FONT.render(word_obj["word"], True, WHITE)
            screen.blit(word_text, (word_obj["x"], word_obj["y"]))

            # Check if the typed word matches any word
            if typed_word == word_obj["word"]:
                correct_sound.play()
                typing_sound.stop()  # Stop sound after correct word typed
                typing_active = False

                if word_obj["word"] in special_words:
                    score += 5  # Bonus points for special words
                else:
                    score += 1

                active_words.remove(word_obj)
                typed_word = ""

                # Level up and increase difficulty at each checkpoint
                if score >= level * level_threshold:
                    level += 1
                    word_speed += 1  # Increase word speed
                    word_delay = max(500, word_delay - 250)  # Increase word frequency (lower delay)

        # Render typed word
        typed_text = FONT.render(typed_word, True, RED)
        screen.blit(typed_text, (10, HEIGHT - 40))

        # Game over if any word reaches the bottom
        for word_obj in active_words:
            if word_obj["y"] > HEIGHT:
                lives -= 1
                life_loss_sound.play()  # Play sound on life loss
                active_words.remove(word_obj)
                if lives == 0:
                    game_over_sound.play()
                    game_over = True

        # Display score and lives
        score_text = FONT.render(f"Score: {score}", True, GREEN)
        lives_text = FONT.render(f"Lives: {lives}", True, RED)
        level_text = FONT.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))
        screen.blit(lives_text, (WIDTH - 150, 40))
        screen.blit(level_text, (WIDTH - 150, 70))

    else:
        # Display game over message
        game_over_text = LARGE_FONT.render("GAME OVER", True, RED)
        score_text = FONT.render(f"Final Score: {score}", True, GREEN)
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))

        # Restart game on key press
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                reset_game()

    pygame.display.flip()
    pygame.time.delay(30)
