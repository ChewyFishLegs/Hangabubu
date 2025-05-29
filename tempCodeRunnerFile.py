import pygame
import math
import random

# Setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Load hangman images
images = []
for i in range(7):
    try:
        image = pygame.image.load(f"hangman{i}.png")
    except:
        print(f"Missing image: hangman{i}.png")
        image = pygame.Surface((100, 100))  # placeholder
    images.append(image)

# Game variables
hangman_status = 0
current_level = 1
max_level = 5
guessed = []

# Words organized by difficulty level
level_words = {
    1: ["CAT", "DOG", "CAR", "TREE"],
    2: ["PYTHON", "ROCKET", "PLANET", "MOUSE"],
    3: ["ELEPHANT", "NOTEBOOK", "PYRAMID", "GIRAFFE"],
    4: ["ASTRONOMER", "BACKPACKING", "CONTROLLER"],
    5: ["INCONCEIVABLE", "MICROPROCESSOR", "EXTRAORDINARY"]
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load background image (replace "background.jpg" with your actual image)
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Draw function
def draw():
    # Use the background image  win.blit(background, (0, 0)) 
    win.fill(WHITE)
    # Draw title with current level
    text = TITLE_FONT.render(f"LEVEL {current_level} - HANGABUBU", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter == " ":
            display_word += "  "
        elif letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))

    # Draw letter buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

# Message display
def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Menu of the game
def draw_menu():
    win.fill(WHITE)
    title_text = TITLE_FONT.render("HANGABUBU", 1, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

    # Draw Play button
    play_text = WORD_FONT.render("Play", 1, BLACK)
    play_rect = pygame.Rect(WIDTH / 2 - 100, 200, 200, 60)
    pygame.draw.rect(win, (200, 200, 200), play_rect)
    win.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, 210))

    # Draw Exit button
    exit_text = WORD_FONT.render("Exit", 1, BLACK)
    exit_rect = pygame.Rect(WIDTH / 2 - 100, 300, 200, 60)
    pygame.draw.rect(win, (200, 200, 200), exit_rect)
    win.blit(exit_text, (WIDTH / 2 - exit_text.get_width() / 2, 310))

    pygame.display.update()
    return play_rect, exit_rect

# The start screen of the game:
def show_start_screen():
    while True:
        play_rect, exit_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if play_rect.collidepoint((m_x, m_y)):
                    return  # Start the game
                if exit_rect.collidepoint((m_x, m_y)):
                    pygame.quit()
                    exit()

# Main game loop
def main():
    global hangman_status
    global guessed
    global word
    global current_level

    hangman_status = 0
    guessed = []
    word = random.choice(level_words[current_level]).upper()

    # Reset letter visibility
    for letter in letters:
        letter[3] = True

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        # Win check
        won = True
        for letter in word:
            if letter != " " and letter not in guessed:
                won = False
                break

        if won:
            if current_level < max_level:
                display_message(f"You WON Level {current_level}!")
                current_level += 1
            else:
                display_message("🎉 You beat all levels!")
                pygame.quit()
                return
            break  # Go to the next level

        # Loss check
        if hangman_status == 6:
            display_message(f"You LOST! The word was: {word}")
            current_level = 1  # Reset to Level 1
            break  # Restart the game at Level 1

# Game loop that keeps restarting
while True:
    show_start_screen()
    main()
