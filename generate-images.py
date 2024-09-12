from PIL import Image, ImageDraw

# Create a 100x100 placeholder image for Odin
image_size = (100, 100)
odin_image = Image.new("RGBA", image_size, (255, 255, 255, 0))
draw = ImageDraw.Draw(odin_image)
draw.ellipse((25, 25, 75, 75), fill=(0, 0, 255))  # Blue circle for Odin
odin_image.save("odin.png")

# Create a placeholder image for Loki
loki_image = Image.new("RGBA", image_size, (255, 255, 255, 0))
draw = ImageDraw.Draw(loki_image)
draw.ellipse((25, 25, 75, 75), fill=(0, 255, 0))  # Green circle for Loki
loki_image.save("loki.png")

# Create a placeholder image for Thor
thor_image = Image.new("RGBA", image_size, (255, 255, 255, 0))
draw = ImageDraw.Draw(thor_image)
draw.ellipse((25, 25, 75, 75), fill=(255, 0, 0))  # Red circle for Thor
thor_image.save("thor.png")

print("Placeholder images saved as 'odin.png', 'loki.png', and 'thor.png'")
