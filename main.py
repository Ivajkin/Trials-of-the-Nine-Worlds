import os
import pygame
import random
import subprocess
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Character size
CHARACTER_SIZE = (48, 48)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gods of Asgard")

# Load soundtracks and sound effects
def load_music(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)  # Loop background music

# Start with the new background music
load_music('Trials of the Nine Worlds.mp3')

class Character(pygame.sprite.Sprite):
    def __init__(self, name, ability, image_path):
        super().__init__()
        self.name = name
        self.ability = ability
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_initial_position()
        self.cooldown = 0
        self.max_cooldown = 60  # 1 second at 60 FPS
        self.z_position = 0  # For depth sorting
        self.footstep_particles = []

    def get_initial_position(self):
        if self.name == "Odin":
            return (SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHARACTER_SIZE[1] - 50)
        elif self.name == "Loki":
            return (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        elif self.name == "Thor":
            return (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
        else:
            return (random.randint(0, SCREEN_WIDTH - CHARACTER_SIZE[0]), 
                    random.randint(0, SCREEN_HEIGHT - CHARACTER_SIZE[1]))

    def draw(self, surface, light_sources, environment_color, wind_direction):
        # Apply environmental lighting and reflections
        env_lit_image = self.apply_environmental_lighting(environment_color)
        reflected_image = self.apply_reflections(env_lit_image, surface)
        
        # Apply dynamic lighting from light sources
        lit_image = self.apply_dynamic_lighting(reflected_image, light_sources)
        
        # Apply wind effect
        wind_affected_image = self.apply_wind_effect(lit_image, wind_direction)
        
        # Draw character
        surface.blit(wind_affected_image, self.rect)
        
        # Draw shadows
        self.draw_shadows(surface, light_sources)
        
        # Draw footstep particles
        self.update_footstep_particles(surface)

    def apply_environmental_lighting(self, environment_color):
        env_lit_image = self.image.copy()
        for x in range(CHARACTER_SIZE[0]):
            for y in range(CHARACTER_SIZE[1]):
                color = env_lit_image.get_at((x, y))
                env_color = [int(c * e / 255) for c, e in zip(color[:3], environment_color)]
                env_lit_image.set_at((x, y), env_color + [color[3]])
        return env_lit_image

    def apply_reflections(self, image, environment):
        reflected_image = image.copy()
        for x in range(CHARACTER_SIZE[0]):
            for y in range(CHARACTER_SIZE[1]):
                env_x = self.rect.x + x
                env_y = self.rect.y + y
                if 0 <= env_x < SCREEN_WIDTH and 0 <= env_y < SCREEN_HEIGHT:
                    env_color = environment.get_at((env_x, env_y))
                    char_color = reflected_image.get_at((x, y))
                    reflected_color = [(c1 + c2) // 2 for c1, c2 in zip(char_color[:3], env_color[:3])]
                    reflected_image.set_at((x, y), reflected_color + [char_color[3]])
        return reflected_image

    def apply_dynamic_lighting(self, image, light_sources):
        lit_image = image.copy()
        for x in range(CHARACTER_SIZE[0]):
            for y in range(CHARACTER_SIZE[1]):
                color = lit_image.get_at((x, y))
                light_intensity = self.calculate_light_intensity(x, y, light_sources)
                lit_color = [int(c * light_intensity) for c in color[:3]] + [color[3]]
                lit_image.set_at((x, y), lit_color)
        return lit_image

    def calculate_light_intensity(self, x, y, light_sources):
        max_intensity = 0
        for light in light_sources:
            dx = x - (light[0] - self.rect.x)
            dy = y - (light[1] - self.rect.y)
            distance = (dx**2 + dy**2)**0.5
            intensity = 1 - min(distance / light[2], 1)
            max_intensity = max(max_intensity, intensity)
        return max(0.2, max_intensity)  # Ambient light of 0.2

    def apply_wind_effect(self, image, wind_direction):
        wind_image = image.copy()
        wind_strength = 2
        for x in range(CHARACTER_SIZE[0]):
            for y in range(CHARACTER_SIZE[1]):
                offset_x = int(wind_direction[0] * wind_strength * (y / CHARACTER_SIZE[1]))
                offset_y = int(wind_direction[1] * wind_strength * (y / CHARACTER_SIZE[1]))
                src_x = (x - offset_x) % CHARACTER_SIZE[0]
                src_y = (y - offset_y) % CHARACTER_SIZE[1]
                wind_image.set_at((x, y), image.get_at((src_x, src_y)))
        return wind_image

    def draw_shadows(self, surface, light_sources):
        for light in light_sources:
            shadow_offset_x = (self.rect.centerx - light[0]) // 10
            shadow_offset_y = (self.rect.centery - light[1]) // 10
            shadow_surface = pygame.Surface(CHARACTER_SIZE, pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 50))  # Semi-transparent black
            surface.blit(shadow_surface, (self.rect.x + shadow_offset_x, self.rect.y + shadow_offset_y))

    def update_footstep_particles(self, surface):
        new_particles = []
        for particle in self.footstep_particles:
            particle[1] -= 1  # Move particle up
            particle[2] -= 0.1  # Reduce opacity
            if particle[2] > 0:
                pygame.draw.circle(surface, (100, 100, 100, int(particle[2] * 255)), particle[0], 2)
                new_particles.append(particle)
        self.footstep_particles = new_particles

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.z_position = self.rect.bottom  # Update z-position for depth sorting
        # Add footstep particles
        if dx != 0 or dy != 0:
            self.footstep_particles.append([(self.rect.centerx, self.rect.bottom), 10, 1.0])

    # ... (other methods remain the same) ...

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

# Create a surface for the fog overlay
fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

def draw_fog():
    fog_surface.fill((0, 0, 0, 0))  # Clear the surface
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
        radius = random.randint(20, 50)
        gfxdraw.filled_circle(fog_surface, x, y, radius, (255, 255, 255, 5))

def get_average_color(surface, rect):
    color_sum = [0, 0, 0]
    count = 0
    for x in range(rect.width):
        for y in range(rect.height):
            color = surface.get_at((rect.x + x, rect.y + y))[:3]
            color_sum = [sum(t) for t in zip(color_sum, color)]
            count += 1
    return [c // count for c in color_sum]

# Game loop
running = True
clock = pygame.time.Clock()
light_sources = [
    [SCREEN_WIDTH // 2, 0, 300],  # x, y, radius
    [0, SCREEN_HEIGHT // 2, 200],
    [SCREEN_WIDTH, SCREEN_HEIGHT // 2, 200]
]
wind_direction = [0.5, 0.1]  # Slight diagonal wind

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ... (rest of the event handling remains the same) ...

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        characters[current_character].move(dx=-5, dy=0)
    if keys[pygame.K_RIGHT]:
        characters[current_character].move(dx=5, dy=0)
    if keys[pygame.K_UP]:
        characters[current_character].move(dx=0, dy=-5)
    if keys[pygame.K_DOWN]:
        characters[current_character].move(dx=0, dy=5)
    
    # Redraw background
    screen.blit(background, (0, 0))
    
    # Draw fog
    draw_fog()
    screen.blit(fog_surface, (0, 0))
    
    # Sort characters by z-position for proper depth rendering
    characters.sort(key=lambda x: x.z_position)
    
    # Draw all characters with advanced lighting, shadows, and effects
    for character in characters:
        env_color = get_average_color(screen, character.rect)
        character.draw(screen, light_sources, env_color, wind_direction)

    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
