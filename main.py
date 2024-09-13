import os
import pygame
import random
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Character size
CHARACTER_SIZE = (64, 64)  # Adjust this size as needed for your game

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gods of Asgard")

# Load soundtracks and sound effects
def load_music(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)  # Loop background music

# Start with the new background music
load_music('Trials of the Nine Worlds.mp3')

# Character Data
class Character(pygame.sprite.Sprite):
    def __init__(self, name, ability, image_path):
        super().__init__()
        self.name = name
        self.ability = ability
        # Load and scale the image
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - CHARACTER_SIZE[0]), 
                             random.randint(0, SCREEN_HEIGHT - CHARACTER_SIZE[1]))
        self.cooldown = 0
        self.max_cooldown = 60  # 1 second at 60 FPS

    def use_ability(self, game):
        if self.cooldown == 0:
            if self.name == "Odin":
                self.teleport()
            elif self.name == "Loki":
                self.create_illusion(game)
            elif self.name == "Thor":
                self.thunder_strike(game)
            self.cooldown = self.max_cooldown
            print(f"{self.name} uses {self.ability}")
        else:
            print(f"{self.name}'s ability is on cooldown")

    def teleport(self):
        # Teleport Odin a short distance
        dx = random.randint(-100, 100)
        dy = random.randint(-100, 100)
        self.rect.x += dx
        self.rect.y += dy
        # Ensure Odin stays within screen bounds
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def create_illusion(self, game):
        # Create a temporary clone of Loki
        illusion = Character("Loki's Illusion", "None", "loki.png")
        illusion.rect.topleft = (self.rect.x + random.randint(-50, 50), 
                                 self.rect.y + random.randint(-50, 50))
        game.all_sprites.add(illusion)
        # Remove the illusion after 3 seconds
        pygame.time.set_timer(pygame.USEREVENT, 3000, once=True)

    def thunder_strike(self, game):
        # Create a thunder effect and damage nearby enemies
        thunder = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(thunder, (255, 255, 0, 128), (100, 100), 100)
        game.screen.blit(thunder, (self.rect.centerx - 100, self.rect.centery - 100))
        pygame.display.flip()
        # Check for nearby enemies and damage them
        for sprite in game.all_sprites:
            if isinstance(sprite, Enemy) and self.rect.colliderect(sprite.rect):
                sprite.take_damage(50)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy
        # Ensure the character stays within screen bounds
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(screen_rect)

# Create characters: Odin, Loki, Thor
odin = Character("Odin", "Teleportation", "odin.png")
loki = Character("Loki", "Illusion", "loki.png")
thor = Character("Thor", "Thunder Strike", "thor.png")

# Group the characters
characters = [odin, loki, thor]
current_character = 0

# Generate background if it doesn't exist
if not os.path.exists("background.jpg"):
    subprocess.run(["python", "generate_background.py"])

# Load and scale background image
try:
    original_background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(original_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    print("Make sure 'background.jpg' is in the working directory.")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(WHITE)  # Fallback to a white background

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
            # Volume control
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + 0.1, 1.0))
            if event.key == pygame.K_MINUS:
                pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.1, 0.0))

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
