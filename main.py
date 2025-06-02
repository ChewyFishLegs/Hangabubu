import pygame
import math
import random
from Animation import create_sprite_animation
# Initialize Pygame and set up display
pygame.init()
WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Constants
RADIUS = 30
GAP = 20
FPS = 60
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
# FontsC:\Users\bddel\Documents\GitHub\Hangabubu\main.py
font_path = 'C:\\Users\\bddel\\Documents\\Github\\Hangabubu\\LuckiestGuy-Regular.ttf'
#Kamo lay adjust ani guys hahahaha

LETTER_FONT = pygame.font.Font(font_path, 40)
WORD_FONT = pygame.font.Font(font_path, 60)
TITLE_FONT = pygame.font.Font(font_path, 100)
HINT_FONT = pygame.font.Font(font_path, 30)  # Smaller size

# Load and play background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)


# Load sound effects

correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
lose_sound = pygame.mixer.Sound("lose.mp3")



# Game variables
hangman_status = 0
current_level = 1
max_level = 5
guessed = []

# Background image
try:
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(WHITE)

# The hanging noose
try:
    logo = pygame.image.load("Noose.png").convert_alpha()
    logo = pygame.transform.scale(logo, (1100, 700))  # Adjust size as needed
except Exception as e:
    print("Failed to load logo image:", e)
    logo = None

animation_data = [
    ("hangabubu_idle_spritesheet3.png", 98, 98, 11),
    ("hangabubu_nervous_spritesheet.png", 98, 98, 11),
    ("hangabubu_nervous_spritesheet.png", 98, 98, 11),
    ("hangabubu_scared.png", 200, 200, 2),
    ("hangabubu_scared.png", 200, 200, 2),
    ("hangabubu_scared.png", 200, 200, 2),
    ]

desired_width = 250
desired_height = 250

animations = []
for path, fw, fh, steps in animation_data:
    scale_x = desired_width / fw
    scale_y = desired_height / fh
    # if you want to preserve aspect ratio, use min(scale_x, scale_y)
    scale = min(scale_x, scale_y)
    
    frames = create_sprite_animation(path, fw, fh, scale, steps, BLACK)
    animations.append(frames)

# Animation control variables
frame_indices = [0] * len(animations)  # current frame per animation
animation_cooldown = 100  # ms between frames, adjust as needed
last_update = pygame.time.get_ticks()

letters = []
RADIUS = 30
GAP = 20
A = 65
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)  # 13 letters per row
starty = 550  # vertical position

for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


import random

HOVER_COLORS = [   
    (143, 224, 255),    
    (255, 173, 143),   
    (255, 243, 100),  
    (143, 166, 255),
    (143, 193, 255),   
    (255, 237, 143), 
    (207, 240, 255)
]

hover_color_cache = {}

def draw_button(win, x, y, letter, is_hovered):
    if is_hovered:
        # If we already assigned a hover color for this letter, use it
        if letter not in hover_color_cache:
            hover_color_cache[letter] = random.choice(HOVER_COLORS)
        color = hover_color_cache[letter]
    else:
        # Clear cache when not hovered
        if letter in hover_color_cache:
            del hover_color_cache[letter]
        color = (255, 180, 100)

    button_rect = pygame.Rect(x - RADIUS, y - RADIUS, RADIUS * 2, RADIUS * 2)

    # Draw rounded rectangle
    pygame.draw.rect(win, color, button_rect, border_radius=12)
    pygame.draw.rect(win, (40, 17, 7), button_rect, 3, border_radius=12)

    # Center and draw letter using helper function
    text = LETTER_FONT.render(letter, True, (40, 17, 7))
    draw_centered_text(text, button_rect)



# Draw everything
def draw():
    global last_update
    win.blit(background, (0, 0))
    title = TITLE_FONT.render(f"LEVEL {current_level}", 1, (40, 17, 7))
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 20))

    # Display the current word
    display_word = ""
    for letter in word:
        display_word += (letter + " ") if letter in guessed else ("  " if letter == " " else "_  ")

    # Render the combined string
    word_text = WORD_FONT.render(display_word.strip(), True, (40, 17, 7))  

    # Center the text horizontally at y=600 (you can adjust y as needed)
    word_rect = word_text.get_rect(center=(1280 // 2, 400)) 

    # Draw it
    win.blit(word_text, word_rect)


     # Get mouse position for hover detection
    m_x, m_y = pygame.mouse.get_pos()

    for x, y, ltr, visible in letters:
        if visible:
            dist = math.hypot(x - m_x, y - m_y)
            is_hovered = dist < RADIUS
            draw_button(win, x, y, ltr, is_hovered)

    if logo:
        win.blit(logo, (350, 20))  # Adjust (x, y) position as needed


    # Draw hint
    hint_text = HINT_FONT.render(f"Hint: {hint}", 1, (40, 17, 7))
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, HEIGHT / 2 + 100))

    # Another window from 'Menu' Top-Right
    menu_x, menu_y = 50, 30  # example position
    menu_width, menu_height = 200, 60  # example size

    menu_button_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = menu_button_rect.collidepoint(mouse_pos)

    # Choose color based on hover state
    menu_color = (255, 180, 100) if is_hovered else (100, 150, 255)

    # Draw the button background (optional)
    pygame.draw.rect(win, menu_color, menu_button_rect, border_radius=10)
    pygame.draw.rect(win, (40, 17, 7), menu_button_rect, 3, border_radius=10)


    menu_text = LETTER_FONT.render("Menu", True, (40, 17, 7))
    draw_centered_text(menu_text, menu_button_rect)

    
    # Update animation frame timing
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        # advance current animation frame
        frame_indices[hangman_status] = (frame_indices[hangman_status] + 1) % len(animations[hangman_status])
        last_update = current_time

    # Draw current animation frame
    current_frame = animations[hangman_status][frame_indices[hangman_status]]
    
    # Position the animation (adjust to your UI)
    pos = (790, 300)

    win.blit(current_frame, pos)


    pygame.display.update()
    return menu_button_rect



# Words and hints
level_words = {
    1: ["LOOP", "MAC", "JAVA", "UNO", "CPU", "BIT", "DFA", "NFA"],
    2: ["PYTHON", "DATABASE", "AUTOMATA", "BINARY", "TEKTOKS"],
    3: ["ALGORITHM", "KEYBOARD", "FUNCTION", "VARIABLE", "HASH TABLE"],
    4: ["ALEX EALA", "DEBUGGING", "SIR RYAN", "INDUSTRY", "SABESHII", "CHICKEN JOCKEY"],
    5: ["ENCAPSULATION", "MICROPROCESSOR", "MULTITHREADING","SYNCHRONIZATION","LINKED LIST", "OPERATING SYSTEM"]
}

level_hints = {
    "CPU":"The brain of the computer",
    "BIT":"Smallest data unit",
    "DFA":"Department of Foreign Affairs",
    "NFA":"Nondeterministic Foreign Affairs",
    "LOOP": "Repeats code",
    "MAC": "Hindi Bintana",
    "JAVA": "Rice, Minecraft",
    "UNO": "Favorite grade",
    "PYTHON": "Snake",
    "DATABASE": "Organized data storage tool",
    "AUTOMATA": "Machine that works alone",
    "BINARY": "1 or 0",
    "ALGORITHM": "Steps to solve a problem",
    "KEYBOARD": "Ginagamit ng mga online warriors",
    "FUNCTION": "Group of code that runs",
    "VARIABLE": "x, y, z, i",
    "ALEX EALA": "Tennis Player",
    "SABESHII" : "Favorite word sa CMSC 106",
    "TEKTOKS":"Byte-sized buzz, inspiring breakthroughs",
    "DEBUGGING": "Using Pesticides in code",
    "SIR RYAN": "Best Prof",
    "INDUSTRY":"The industry",
    "CHICKEN JOCKEY":"I AM STEVE",
    "HASH TABLE":"Last topic sa CMSC 123 - A of Batch 2023",
    "ENCAPSULATION": "Hides data in code",
    "MULTITHREADING": "Many tasks at once",
    "SYNCHRONIZATION": "Manages timing between threads",
    "OPERATING SYSTEM": "The conductor of digital harmony",
    "MICROPROCESSOR": "Small chip that runs computer",
    "LINKED LIST": "Nodes connected one by one",
}


# Show a message (win/lose)
def display_message(message):
    pygame.time.delay(1000)
    win.blit(background, (0, 0))
    
    text = WORD_FONT.render(message, 1, (40, 17, 7))
    center_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    draw_centered_text(text, center_rect, y_offset=0)

    pygame.display.update()
    pygame.time.delay(3000)

def draw_centered_text(text_surf, rect, y_offset=5):
    text_rect = text_surf.get_rect(center=rect.center)
    text_rect.centery += y_offset
    win.blit(text_surf, text_rect)

def draw_menu():
    win.blit(background, (0, 0))

    logo_image = pygame.image.load("logo.png")
    logo_ratio = logo_image.get_width() / logo_image.get_height()
    new_height = 250  # fit within screen height
    new_width = int(new_height * logo_ratio)
    logo_image = pygame.transform.scale(logo_image, (new_width, new_height))

    # Center the logo horizontally
    logo_x = (WIDTH - logo_image.get_width()) // 2
    logo_y = 50  # vertical offset from top
    win.blit(logo_image, (logo_x, logo_y))

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Buttons
    play_rect = pygame.Rect(WIDTH / 2 - 120, 300, 240, 70)
    exit_rect = pygame.Rect(WIDTH / 2 - 120, 400, 240, 70)


     # --- START button ---
    play_hover = play_rect.collidepoint(mouse_pos)
    play_color = (239, 175, 48) if play_hover else (255, 216, 143)  # green on hover
    pygame.draw.rect(win, play_color, play_rect, border_radius=12)
    pygame.draw.rect(win, (40, 17, 7), play_rect, width=3, border_radius=12)

    play_text = WORD_FONT.render("Start", True, (40, 17, 7))
    draw_centered_text(play_text, play_rect)



    # --- EXIT button ---
    exit_hover = exit_rect.collidepoint(mouse_pos)
    exit_color = (68, 180, 236) if exit_hover else (207, 240, 255)  # red on hover
    pygame.draw.rect(win, exit_color, exit_rect, border_radius=12)
    pygame.draw.rect(win, (40, 17, 7), exit_rect, width=3, border_radius=12)

    exit_text = WORD_FONT.render("Exit", True, (40, 17, 7))
    draw_centered_text(exit_text, exit_rect)


    pygame.display.update()
    return play_rect, exit_rect


def show_start_screen():
    while True:
        play_rect, exit_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return  # Start game
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def confirm_menu_return():
    dialog_width, dialog_height = 600, 300
    dialog_rect = pygame.Rect(WIDTH / 2 - dialog_width / 2, HEIGHT / 2 - dialog_height / 2, dialog_width, dialog_height)

    yes_rect = pygame.Rect(dialog_rect.left + 60, dialog_rect.bottom - 80, 120, 50)
    no_rect = pygame.Rect(dialog_rect.right - 180, dialog_rect.bottom - 80, 120, 50)

    while True:
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Dim background for focus effect
        dim_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim_overlay.fill((0, 0, 0, 100))  # Semi-transparent (40, 17, 7)
        win.blit(dim_overlay, (0, 0))

        # Draw dialog box with rounded corners
        pygame.draw.rect(win, (255, 255, 255), dialog_rect, border_radius=16)
        pygame.draw.rect(win, (40, 17, 7), dialog_rect, 3, border_radius=16)

        # Draw message text
        msg = WORD_FONT.render("Return to menu?", True, (40, 17, 7))
        win.blit(msg, (dialog_rect.centerx - msg.get_width() // 2, dialog_rect.top + 40))

        # Determine button colors with hover effect
        yes_color = (0, 204, 0) if yes_rect.collidepoint(mouse_pos) else (100, 255, 100)
        no_color = (204, 0, 0) if no_rect.collidepoint(mouse_pos) else (255, 100, 100)

        # Draw buttons with rounded corners and hover colors
        pygame.draw.rect(win, yes_color, yes_rect, border_radius=12)
        pygame.draw.rect(win, no_color, no_rect, border_radius=12)

        # Button labels
        yes_text = LETTER_FONT.render("Yes", True, (40, 17, 7))
        no_text = LETTER_FONT.render("No", True, (40, 17, 7))

       
        draw_centered_text(yes_text, yes_rect)
        draw_centered_text(no_text, no_rect)

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    return True
                elif no_rect.collidepoint(event.pos):
                    return False


# Main game loop
def main():
    global hangman_status, guessed, word, hint, current_level

    hangman_status = 0
    guessed = []
    word = random.choice(level_words[current_level]).upper()
    hint = level_hints.get(word, "No hint available")

    # Reset letters
    for letter in letters:
        letter[3] = True
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        menu_button_rect = draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()

                # Handle menu button click
                if menu_button_rect.collidepoint((m_x, m_y)):
                    if confirm_menu_return():
                        current_level = 1
                        show_start_screen()
                        return
                    continue  # Skip checking letters if menu was clicked

                # Handle letter button clicks
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible and math.hypot(x - m_x, y - m_y) < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
                            wrong_sound.play()
                        if ltr in word:
                            correct_sound.play()

        # Check for win
        if all(l in guessed or l == " " for l in word):
        # Show full word briefly before proceeding
            guessed = list(set(guessed + [l for l in word]))  # Ensure full word is shown
            draw()  # Redraw screen with the full word visible
            pygame.display.update()
            pygame.time.delay(1500)  # Wait 1.5 seconds

    # Proceed to next level or end game
            if current_level < max_level:
                display_message(f"The word was {word}!")
                display_message("Next Level")
                current_level += 1
            else:
                display_message(f"The word was {word}!")
                display_message("🎉 You beat all levels!")
                current_level = 1
                show_start_screen()
                return
            pygame.event.clear()
            return

        # Check for loss
        if hangman_status == 6:
            pygame.mixer.music.stop()  # Stop the background music
            lose_sound.play()
            display_message(f"You died! The word was: {word}")
            current_level = 1
            show_start_screen()
            return

# Game loop
show_start_screen()
while True:
    main()