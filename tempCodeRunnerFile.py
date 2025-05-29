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

# ----- UI Button Class -----
class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color=000000):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, win):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(win, color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, self.text_color)
        win.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() / 2,
                self.rect.centery - text_surface.get_height() / 2
            )
        )

    def is_hovered(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


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

# Menu start
def show_start_screen():
    play_button = Button(WIDTH // 2 - 100, 200, 200, 60, "Play", WORD_FONT, (200, 200, 200), (170, 170, 170))
    exit_button = Button(WIDTH // 2 - 100, 300, 200, 60, "Exit", WORD_FONT, (200, 200, 200), (170, 170, 170))

    while True:
        win.fill(WHITE)
        title_text = TITLE_FONT.render("HANGABUBU", True, BLACK)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        play_button.is_hovered(mouse_pos)
        exit_button.is_hovered(mouse_pos)
        play_button.draw(win)
        exit_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos):
                    return  # Start game
                elif exit_button.is_clicked(mouse_pos):
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
