import pygame
import random
import json  # For loading and saving high scores

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythmic-cat")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PEACH = (255,229,180)
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
main_menu_bg = pygame.image.load('background_main.png')  # Background for the main menu
game_bg = pygame.image.load('background_game.jpg')  # Background for the game
song_select_bg = pygame.image.load('background_selection.png')

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
score = 0
misses = 0
combo = 0
max_misses = 5
last_spawn_time = pygame.time.get_ticks()
compliment = ""
compliment_timer = 0
compliment_alpha = 255
current_song = 0
songs = ["Song1.mp3", "Song2.mp3", "Song3.mp3"]
bpms = [78, 85, 87]  # Example BPMs for the songs

# High scores dictionary
high_scores = {}

# High score file path
high_score_file = 'high_scores.json'

# Function to load high scores
def load_high_scores():
    try:
        with open(high_score_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {song: 0 for song in songs}  # Initialize with zero if file not found

# Function to save high scores
def save_high_scores():
    with open(high_score_file, 'w') as file:
        json.dump(high_scores, file)

# Load the high scores when the game starts
high_scores = load_high_scores()

# Calculate seconds per beat for the current song
seconds_per_beat = 60 / bpms[current_song]

# Add the new variables
n = 85  # Number of beats it takes for an arrow to reach the target
arrow_speed = HEIGHT / (seconds_per_beat * n)  # Calculate arrow speed

# Main menu buttons
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)

def draw_text_centered(text, font, color, surface, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_play_button():
    pygame.draw.rect(screen, WHITE, play_button_rect, border_radius=12)  # White button with rounded corners
    pygame.draw.rect(screen, BLACK, play_button_rect, 4, border_radius=12)  # Black border
    draw_text_centered("Play", BUTTON_FONT, BLACK, screen, play_button_rect)  # Text on the button

def draw_main_menu():
    screen.blit(main_menu_bg, (0, 0))
    draw_play_button()

def draw_songs_screen():
    screen.blit(song_select_bg, (0, 0))  # Draw the song selection background image
    draw_text_centered("Select a Song", FONT, WHITE, screen, pygame.Rect(WIDTH // 2, 50, 0, 0))
    song_rects = []
    for i, song in enumerate(songs):
        rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 50, 200, 40)
        pygame.draw.rect(screen, WHITE, rect)
        draw_text_centered(song.replace(".mp3", ""), FONT, BLACK, screen, rect)
        # Display the high score for the song
        high_score_text = FONT.render(f"High Score: {high_scores[song]}", True, PEACH)
        screen.blit(high_score_text, (WIDTH - 250, 150 + i * 50))  # Adjust position if necessary
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
    global current_song, last_spawn_time, arrows, score, misses, combo, compliment, compliment_timer, compliment_alpha, main_menu

    pygame.mixer.music.load(songs[current_song])
    pygame.mixer.music.play(-1)
    
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
                main_menu = False  # Ensure that the game exits
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

        # Spawn arrows based on the beat
        current_time = pygame.time.get_ticks()
        time_since_last_spawn = current_time - last_spawn_time
        if time_since_last_spawn > (seconds_per_beat * 1000):  # Convert to milliseconds
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
            # Save high score if it's the best for this song
            if score > high_scores[songs[current_song]]:
                high_scores[songs[current_song]] = score
                save_high_scores()  # Save updated high scores to file

            game_over_text = FONT.render("Game Over! Returning to Main Menu...", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 300, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Delay for 2 seconds
            running = False  # Exit the game loop and return to the main menu

        pygame.display.flip()
        pygame.time.delay(30)

    pygame.mixer.music.stop()  # Stop the music before returning to the main menu

def draw_play_button():
    pygame.draw.rect(screen, WHITE, play_button_rect, border_radius=12)  # White button with rounded corners
    pygame.draw.rect(screen, BLACK, play_button_rect, 4, border_radius=12)  # Black border
    draw_text_centered("Play", BUTTON_FONT, BLACK, screen, play_button_rect)  # Text on the button

def draw_main_menu():
    screen.blit(main_menu_bg, (0, 0))
    draw_play_button()

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

    while show_songs:
        song_rects = draw_songs_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_songs = False
                main_menu = False  # Exit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, song_rect in enumerate(song_rects):
                    if song_rect.collidepoint(mouse_pos):
                        current_song = i
                        show_songs = False
                        game_loop()  # Start the game loop with the selected song
                        main_menu = True  # Return to the main menu after the game loop

pygame.quit()
