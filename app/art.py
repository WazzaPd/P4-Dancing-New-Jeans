import random
from PIL import Image, ImageDraw
import base64
import os


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_house():
    width, height = 256, 256
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw a random building type
    building_type = random.choice(["house", "apartment", "cabin", "mansion"])

    if building_type == "house":
        # draw windows
        draw.rectangle([(64, 128), (192, 240)], fill=random_color())
        draw.polygon([(64, 128), (192, 128), (128, 64)], fill=random_color())
        # draw doors and chimney
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())
    elif building_type == "apartment":

        # draw windows
        draw.rectangle([(64, 64), (192, 240)], fill=random_color())
        for i in range(3):
            draw.rectangle(
                [(80, 80 + 48 * i), (176, 112 + 48 * i)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())

    elif building_type == "cabin":

        # draw windows
        draw.rectangle([(64, 128), (192, 240)], fill=random_color())
        draw.rectangle([(64, 64), (96, 96)], fill=random_color())
        draw.rectangle([(160, 64), (192, 96)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())

    elif building_type == "mansion":

        # draw windows
        draw.rectangle([(64, 64), (192, 240)], fill=random_color())
        for i in range(3):
            draw.rectangle(
                [(80, 80 + 48 * i), (176, 112 + 48 * i)], fill=random_color())
        # draw doors
        draw.rectangle([(96, 192), (128, 240)], fill=random_color())
        draw.rectangle([(160, 192), (192, 240)], fill=random_color())
        draw.rectangle([(128, 64), (160, 96)], fill=random_color())
        # draw roof
        draw.polygon([(64, 64), (192, 64), (128, 32)], fill=random_color())

    # convert pil image to base64
    # save image to temp file and get base64
    image.save("temp.png")
    with open("temp.png", "rb") as image_file:
        # get base 64
        encoded_string = base64.b64encode(image_file.read())
        # print(encoded_string)
        # remove temp file
        # print(encoded_string)
        # remove b prefix and quotes
        encoded_string = str(encoded_string)[2:-1]
        return encoded_string


# # Generate and show a random house
house_image = generate_house()
# house_image.show()
