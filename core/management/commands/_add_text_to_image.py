from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from core.models import Quote
from django.core.files import File
import re
import random
import string
import platform

IMAGE_DIRECTORY = 'quotes-images'

def get_random_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) 
                    for i in range(6)])

def slugify(text):
    # Replace all non-alphanumeric characters with a hyphen
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip().lower()
    # Replace all spaces with a hyphen
    text = re.sub(r'[-\s]+', '-', text)
    return text + '-' + get_random_string()


def add_text_to_image(text, image_file):
    # Get the division factor for font-size
    if len(text) > 300:
        text = text[:300] + '......'

    if len(text) < 100:
        division_factor = 20
    else:
        division_factor = 25

    lines = textwrap.wrap(text, width=division_factor*2)

    # open the image file and get its dimensions
    img = Image.open(image_file)
    width, height = img.size

    # create a new image with a transparent background
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # create a drawing object and write the text in the center
    draw = ImageDraw.Draw(new_img)
    font_size = int(min(width, height) / division_factor)  # adjust the font size as desired
    if platform.system().lower() == 'windows':
        font = ImageFont.truetype("arial.ttf", font_size)
    elif platform.system().lower() == 'linux':
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size-2)
    else:
        font = ImageFont.load_default()

    # get the width and height of the text
    text_height = sum([draw.textsize(line, font=font)[1]
                       for line in lines])

    # calculate the x and y coordinates for center alignment
    y = (img.height - text_height) / 2

    # Remove spacing between lines from y
    y -= (len(lines) -1) * 5

    # draw each line of the text on the image
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((img.width - line_width) /2, y), line, font=font, fill='white')
        y += line_height + 10  # add extra space between line

    # combine the original image and the text image
    result = Image.alpha_composite(img.convert('RGBA'), new_img)
    path = os.path.join(IMAGE_DIRECTORY, f'{slugify(text[:50])}.webp')
    # Save the image in file
    
    result.save(path, format='webp')

    return path


def main():

    images = os.listdir('bookquotes-images')
    quotes = Quote.objects.filter(book__slug='the-hunger-games')

    for image, quote in zip(images, quotes):
        image = os.path.join('bookquotes-images', image)
        image_path = add_text_to_image(quote.text, image)

        with open(image_path, 'rb') as f:
            image_name = os.path.basename(image_path)
            quote.image.save(image_name, File(f))


if __name__ == '__main__':
        main()
