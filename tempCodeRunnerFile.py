import pygame
import math
import random

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
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font_path = 'D:\GitHub\Hangabubu\LuckiestGuy-Regular.ttf'
LETTER_FONT = pygame.font.Font(font_path, 40)
WORD_FONT = pygame.font.Font(font_path, 60)
TITLE_FONT = pygame.font.Font(font_path, 100)
HINT_FONT = pygame.font.Font(font_path, 30)  # Smaller size



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

# Hangman images
images = []
for i in range(7):
    try:
        image = pygame.image.load(f"hangman{i}.png")
    except:
        print(f"Missing image: hangman{i}.png")
        image = pygame.Surface((100, 100))  # Placeholder
    images.append(image)

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
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
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
        color = GREY

    button_rect = pygame.Rect(x - RADIUS, y - RADIUS, RADIUS * 2, RADIUS * 2)

    # Draw rounded rectangle
    pygame.draw.rect(win, color, button_rect, border_radius=12)
    pygame.draw.rect(win, BLACK, button_rect, 3, border_radius=12)

    # Center and draw letter
    text = LETTER_FONT.render(letter, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    win.blit(text, text_rect)



# Draw everything
def draw():
    win.fill(WHITE)
    title = TITLE_FONT.render(f"LEVEL {current_level}", 1, BLACK)
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 20))

    # Display the current word
    display_word = ""
    for letter in word:
        display_word += (letter + " ") if letter in guessed else ("  " if letter == " " else "_ ")
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))

     # Get mouse position for hover detection
    m_x, m_y = pygame.mouse.get_pos()



    for x, y, ltr, visible in letters:
        if visible:
            dist = math.hypot(x - m_x, y - m_y)
            is_hovered = dist < RADIUS
            draw_button(win, x, y, ltr, is_hovered)


    # Draw hangman
    win.blit(images[hangman_status], (150, 100))

    # Draw hint
    hint_text = HINT_FONT.render(f"Hint: {hint}", 1, BLACK)
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, HEIGHT / 2 + 100))

    menu_text = LETTER_FONT.render("Menu", True, BLACK)
    text_width, text_height = menu_text.get_size()

    # Padding around text inside the button
    padding_x = 15
    padding_y = 8

    # Button size based on text size + padding
    button_width = text_width + padding_x * 2
    button_height = text_height + padding_y * 2

    # Margins from edges
    margin_right = 40
    margin_top = 30

    # Position button top-right but inset by margin
    menu_button_rect = pygame.Rect(
        WIDTH - margin_right - button_width,
        margin_top,
        button_width,
        button_height
    )

    # Draw button background
    pygame.draw.rect(win, GREY, menu_button_rect, border_radius=8)

    # Draw text centered inside button
    win.blit(menu_text, (
        menu_button_rect.centerx - text_width // 2,
        menu_button_rect.centery - text_height // 2
    ))

    pygame.display.update()
    return menu_button_rect



# Words and hints
level_words = {
    1: ["CAT", "DOG", "CAR", "TREE"],
    2: ["PYTHON", "ROCKET", "PLANET", "MOUSE"],
    3: ["ELEPHANT", "NOTEBOOK", "PYRAMID", "GIRAFFE"],
    4: ["ASTRONOMER", "BACKPACKING", "CONTROLLER"],
    5: ["INCONCEIVABLE", "MICROPROCESSOR", "EXTRAORDINARY"]
}

level_hints = {
    "CAT": "A small pet animal.",
    "DOG": "Man's best friend.",
    "CAR": "A vehicle with four wheels.",
    "TREE": "A tall plant with branches and leaves.",
    "PYTHON": "A popular programming language.",
    "ROCKET": "A vehicle used for space travel.",
    "PLANET": "A large celestial body orbiting a star.",
    "MOUSE": "A small rodent or a computer device.",
    "ELEPHANT": "A large mammal with a trunk.",
    "NOTEBOOK": "A type of portable computer.",
    "PYRAMID": "A triangular-shaped structure, often seen in Egypt.",
    "GIRAFFE": "A tall animal with a long neck.",
    "ASTRONOMER": "A scientist who studies the stars.",
    "BACKPACKING": "Traveling with a backpack, often hiking.",
    "CONTROLLER": "A device used to control something, like a game console.",
    "INCONCEIVABLE": "Something unimaginable or unbelievable.",
    "MICROPROCESSOR": "The brain of a computer, which executes instructions.",
    "EXTRAORDINARY": "Something very unusual or remarkable."
}


# Show a message (win/lose)
def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


# def draw_menu():
#     win.fill(WHITE)
    
#     # Title (centered horizontally, near top)
#     title = TITLE_FONT.render("HANGABUBU", True, (0, 0, 0))
#     title_x = WIDTH // 2 - title.get_width() // 2
#     title_y = HEIGHT // 5 + 80# ~16% down
#     win.blit(title, (title_x, title_y))
    
#     # Button sizes
#     button_width, button_height = 200, 60
#     button_x = WIDTH // 2 - button_width // 2
    
#     # Position buttons lowered vertically (~65% height start)
#     start_y = int(HEIGHT * 0.65)
    
#     # Play button
#     play_rect = pygame.Rect(button_x, start_y, button_width, button_height)
#     pygame.draw.rect(win, (200, 200, 200), play_rect, border_radius=8)
#     play_text = WORD_FONT.render("Play", True, (0, 0, 0))
#     play_text_x = WIDTH // 2 - play_text.get_width() // 2
#     play_text_y = start_y + (button_height - play_text.get_height()) // 2
#     win.blit(play_text, (play_text_x, play_text_y))
    
#     # Exit button (20px below Play)
#     exit_rect = pygame.Rect(button_x, start_y + button_height + 20, button_width, button_height)
#     pygame.draw.rect(win, (200, 200, 200), exit_rect, border_radius=8)
#     exit_text = WORD_FONT.render("Exit", True, (0, 0, 0))
#     exit_text_x = WIDTH // 2 - exit_text.get_width() // 2
#     exit_text_y = start_y + button_height + 20 + (button_height - exit_text.get_height()) // 2
#     win.blit(exit_text, (exit_text_x, exit_text_y))
    
#     pygame.display.update()
#     return play_rect, exit_rect

def draw_menu():
    win.fill(WHITE)

    # Title
    title = TITLE_FONT.render("HANGABUBU", True, (0, 0, 0))
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 180))  # lowered title

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Buttons
    play_rect = pygame.Rect(WIDTH / 2 - 120, 300, 240, 70)
    exit_rect = pygame.Rect(WIDTH / 2 - 120, 400, 240, 70)


     # --- PLAY button ---
    play_hover = play_rect.collidepoint(mouse_pos)
    play_color = (100, 255, 100) if play_hover else (200, 200, 200)  # green on hover
    pygame.draw.rect(win, play_color, play_rect, border_radius=12)
    pygame.draw.rect(win, BLACK, play_rect, width=3, border_radius=12)

    play_text = WORD_FONT.render("Start", True, BLACK)
    win.blit(play_text, (
        play_rect.centerx - play_text.get_width() / 2,
        play_rect.centery - play_text.get_height() / 2
    ))

    # --- EXIT button ---
    exit_hover = exit_rect.collidepoint(mouse_pos)
    exit_color = (255, 120, 120) if exit_hover else (200, 200, 200)  # red on hover
    pygame.draw.rect(win, exit_color, exit_rect, border_radius=12)
    pygame.draw.rect(win, BLACK, exit_rect, width=3, border_radius=12)

    exit_text = WORD_FONT.render("Exit", True, BLACK)
    win.blit(exit_text, (
        exit_rect.centerx - exit_text.get_width() / 2,
        exit_rect.centery - exit_text.get_height() / 2
    ))

    pygame.display.update()
    return play_rect, exit_rect


# # Show start menu loop
# def show_start_screen():
#     while True:
#         play_rect, exit_rect = draw_menu()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 m_x, m_y = pygame.mouse.get_pos()
#                 if play_rect.collidepoint((m_x, m_y)):
#                     return
#                 if exit_rect.collidepoint((m_x, m_y)):
#                     pygame.quit()
#                     exit()

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

        # Dim background for focus effect
        dim_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim_overlay.fill((0, 0, 0, 100))  # Semi-transparent black
        win.blit(dim_overlay, (0, 0))

        # Draw dialog box with rounded corners
        pygame.draw.rect(win, (255, 255, 255), dialog_rect, border_radius=16)
        pygame.draw.rect(win, (0, 0, 0), dialog_rect, 3, border_radius=16)

        # Draw message text
        msg = WORD_FONT.render("Return to menu?", True, BLACK)
        win.blit(msg, (dialog_rect.centerx - msg.get_width() // 2, dialog_rect.top + 40))

        # Draw buttons with rounded corners
        pygame.draw.rect(win, (100, 255, 100), yes_rect, border_radius=12)  # green
        pygame.draw.rect(win, (255, 100, 100), no_rect, border_radius=12)   # red

        # Button labels
        yes_text = LETTER_FONT.render("Yes", True, BLACK)
        no_text = LETTER_FONT.render("No", True, BLACK)

        win.blit(yes_text, (yes_rect.centerx - yes_text.get_width() // 2, yes_rect.centery - yes_text.get_height() // 2))
        win.blit(no_text, (no_rect.centerx - no_text.get_width() // 2, no_rect.centery - no_text.get_height() // 2))

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

        # Check for win
        if all(l in guessed or l == " " for l in word):
            pygame.time.delay(500)  # prevents double-click skipping
            if current_level < max_level:
                display_message(f"You WON Level {current_level}!")
                current_level += 1
            else:
                display_message("🎉 You beat all levels!")
                current_level = 1
            pygame.event.clear()
            return

        # Check for loss
        if hangman_status == 6:
            display_message(f"You LOST! The word was: {word}")
            current_level = 1
            show_start_screen()
            return

# Game loop
show_start_screen()
while True:
    main()