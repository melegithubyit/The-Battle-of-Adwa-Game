import subprocess

import pygame
from subprocess import PIPE


# Initialize Pygame
pygame.init()

# Set the window size
window_width = 700
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("አድዋ የጥቁር ህዝብ ኩራት")

# Load background music for the starting page
pygame.mixer.music.load("sounds/gigi.mp3")
pygame.mixer.music.play(-1)  # Play the music on loop

# Load images for buttons
play_button_image = pygame.image.load("images/play.jpg")
exit_button_image = pygame.image.load("images/exit.jpg")

# Set button positions
play_button_x = 300
play_button_y = 300
exit_button_x = 300
exit_button_y = 400

# Define button rectangles
play_button_rect = play_button_image.get_rect()
play_button_rect.topleft = (play_button_x, play_button_y)

exit_button_rect = exit_button_image.get_rect()
exit_button_rect.topleft = (exit_button_x, exit_button_y)

# Load background image for the starting page
background_image = pygame.image.load("images/adwa.jpg")

# Load font for the text
font = pygame.font.Font(None, 36)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                pygame.quit()
                subprocess.run(['python', 'game.py'])
                running = False
                  # Quit the starting page
            elif exit_button_rect.collidepoint(event.pos):
                running = False

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the buttons on the starting screen
    window.blit(play_button_image, (play_button_x, play_button_y))
    window.blit(exit_button_image, (exit_button_x, exit_button_y))
    
    # Render the text
    # Replace the text and color as desired
    text_surface = font.render("The battle of Adwa", True, (255, 255, 255))
    # Position the text on the screen
    text_rect = text_surface.get_rect(center=(window_width // 2, 200))
    window.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
