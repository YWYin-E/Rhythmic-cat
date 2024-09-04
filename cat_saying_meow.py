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
GRAY = (50, 50, 50)  # Line color

FONT = pygame.font.Font("gamingfont2.otf", 30)  # Main font for score and text
BUTTON_FONT = pygame.font.Font("gamingfont4.otf", 30)  # Font for buttons

# Load a special gaming font for compliments and combo
COMPLIMENT_FONT = pygame.font.Font("gamingfont3.otf", 30)  # Custom font for compliments
COMBO_FONT = pygame.font.Font("gamingfont2.otf", 30)  # Custom font for combo

# Arrow images
arrow_up = pygame.image.load('up.png')
arrow_down = pygame.image.load('down.png')
arrow_left = pygame.image.load('left.png')
arrow_right = pygame.image.load('right.png')

arrow_images = [arrow_up, arrow_down, arrow_left, arrow_right]
arrow_positions = [(430, 0), (630, 0), (230, 0), (30, 0)]
arrow_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

# Background images
main_menu_bg = pygame.image.load('background.png')  # Background for the main menu
game_bg = pygame.image.load('background.jpg')  # Background for the game

# Load border images for each arrow
border_up = pygame.image.load('up1.png')
border_down = pygame.image.load('down1.png')
border_left = pygame.image.load('left1.png')
border_right = pygame.image.load('right1.png')

border_positions = {
    'up': (430, HEIGHT - 150),
    'down': (630, HEIGHT - 150),
    'left': (230, HEIGHT - 150),
    'right': (30, HEIGHT - 150)
}

# Line positions between columns
line_positions = [
    (200, 0, 200, HEIGHT),  # Line between left and up arrows
    (400, 0, 400, HEIGHT),  # Line between up and down arrows
    (600, 0, 600, HEIGHT),  # Line between down and right arrows
]

# Game variables
arrows = []
arrow_speed = 5
score = 0
misses = 0
combo = 0  # Track the current combo
max_misses = 5
spawn_rate = 1000  # milliseconds between spawns
last_spawn_time = pygame.time.get_ticks()
compliment = ""  # To store compliment messages
compliment_timer = 0  # Timer to show compliments
compliment_alpha = 255  # Alpha value for fading
current_song = 0
songs = ["Cute Meow.mp3", "Blinding Lights by cat.mp3", "As it was by cat.mp3"]  # List of song files

# Main menu buttons
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)

def draw_text_centered(text, font, color, surface, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_main_menu():
    screen.blit(main_menu_bg, (0, 0))
    draw_text_centered("Play", BUTTON_FONT, WHITE, screen, play_button_rect)

def draw_songs_screen():
    screen.fill(BLACK)
    draw_text_centered("Select a Song", FONT, WHITE, screen, pygame.Rect(WIDTH // 2, 50, 0, 0))
    song_rects = []
    for i, song in enumerate(songs):
        rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 50, 200, 40)
        pygame.draw.rect(screen, WHITE, rect)
        draw_text_centered(song.replace(".mp3", ""), FONT, BLACK, screen, rect)
        song_rects.append(rect)
    return song_rects

def spawn_arrow():
    direction = random.randint(0, 3)
    x, y = arrow_positions[direction]
    arrows.append({"direction": direction, "x": x, "y": y})

def reset_game():
    global score, misses, combo, arrows, last_spawn_time, compliment, compliment_alpha
    score = 0
    misses = 0
    combo = 0  # Reset combo
    arrows = []
    last_spawn_time = pygame.time.get_ticks()
    compliment = ""
    compliment_alpha = 255

def game_loop():
    global current_song, last_spawn_time, arrows, score, misses, combo, compliment, compliment_timer, compliment_alpha

    pygame.mixer.music.load(songs[current_song])
    pygame.mixer.music.play(-1)

    # Initialize game variables
    last_spawn_time = pygame.time.get_ticks()
    arrows = []
    score = 0
    misses = 0
    combo = 0
    compliment = ""
    compliment_timer = 0
    compliment_alpha = 255

    running = True
    while running:
        screen.blit(game_bg, (0, 0))

        # Draw vertical lines between arrow columns
        for line in line_positions:
            pygame.draw.line(screen, GRAY, line[:2], line[2:], 5)  # Adjust the line thickness as needed

        # Draw the borders for each arrow direction
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
                            combo += 1
                            arrows.remove(arrow)
                            compliment = random.choice(["Great!", "Awesome!", "Perfect!", "Nice!"])
                            compliment_timer = pygame.time.get_ticks()
                            compliment_alpha = 255  # Reset alpha value
                            break
                else:
                    misses += 1
                    combo = 0  # Reset combo on miss

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
                combo = 0  # Reset combo on miss

        # Draw arrows
        for arrow in arrows:
            screen.blit(arrow_images[arrow['direction']], (arrow['x'], arrow['y']))

        # Draw score, misses, and combo
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        misses_text = FONT.render(f"Misses: {misses}", True, RED)
        combo_text = COMBO_FONT.render(f"Combo: {combo}", True, YELLOW)  # Display combo
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (10, 50))
        screen.blit(combo_text, (10, 90))  # Adjust position as needed

        # Show compliments with fading effect using the gaming font
        if compliment:
            time_since_compliment = current_time - compliment_timer
            if time_since_compliment < 1000:  # Show for 1 second
                compliment_surface = COMPLIMENT_FONT.render(compliment, True, GREEN)
                compliment_surface.set_alpha(compliment_alpha)
                screen.blit(compliment_surface, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
                compliment_alpha -= 5  # Reduce alpha for fading effect
                if compliment_alpha < 0:
                    compliment_alpha = 0
            else:
                compliment = ""

        # Check for game over
        if misses >= max_misses:
            game_over_text = FONT.render("Game Over! Press R to Restart", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()

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


# Main loop
main_menu = True
show_songs = False

while main_menu:
    draw_main_menu()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                show_songs = True
                main_menu = False

# Songs screen loop
while show_songs:
    song_rects = draw_songs_screen()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_songs = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, song_rect in enumerate(song_rects):
                if song_rect.collidepoint(mouse_pos):
                    current_song = i
                    show_songs = False
                    game_loop()  # Start the game loop with the selected song

pygame.quit()
