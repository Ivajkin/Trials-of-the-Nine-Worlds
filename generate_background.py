from PIL import Image, ImageDraw

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)

def generate_background(filename="background.jpg"):
    # Create a new image with the specified dimensions
    image = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), SKY_BLUE)
    draw = ImageDraw.Draw(image)
    
    # Draw the grass
    draw.rectangle([0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT], fill=GRASS_GREEN)
    
    # Save the image
    image.save(filename)
    print(f"Background image saved as {filename}")

if __name__ == "__main__":
    generate_background()