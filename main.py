import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gods of Asgard")

# Load soundtracks and sound effects
pygame.mixer.music.load('amazing_soundtrack.mp3')  # Make sure you have the audio file
pygame.mixer.music.play(-1)  # Loop background music

# Character Data
class Character(pygame.sprite.Sprite):
    def __init__(self, name, image_path, ability, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.ability = ability
        self.health = 100
    
    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy
    
    def use_ability(self):
        print(f"{self.name} uses {self.ability}")

# Create characters: Odin, Loki, Thor
odin = Character("Odin", "odin.png", "Teleportation", 100, 500)
loki = Character("Loki", "loki.png", "Illusion", 200, 500)
thor = Character("Thor", "thor.png", "Thunder Strike", 300, 500)

# Group the characters
characters = [odin, loki, thor]
current_character = 0

# Load background image
background = pygame.image.load("background.jpg").convert()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Switch characters
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                current_character = (current_character + 1) % 3  # Cycle through Odin, Loki, Thor

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        characters[current_character].move(dx=-5)
    if keys[pygame.K_RIGHT]:
        characters[current_character].move(dx=5)
    if keys[pygame.K_UP]:
        characters[current_character].move(dy=-5)
    if keys[pygame.K_DOWN]:
        characters[current_character].move(dy=5)
    
    # Redraw background
    screen.blit(background, (0, 0))
    
    # Draw all characters
    for character in characters:
        screen.blit(character.image, character.rect)

    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
