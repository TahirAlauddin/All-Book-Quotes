from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from core.models import Quote
from django.core.files import File


def add_text_to_image(text, image_file):
    # Get the division factor for font-size
    if len(text) < 100:
        division_factor = 20
    elif len(text) < 150:
        division_factor = 25
    elif len(text) < 250:
        division_factor = 30
    elif len(text) < 350:
        division_factor = 35
    else:
        division_factor = 40

    if division_factor <= 35:
        lines = textwrap.wrap(text, width=int(len(text)/division_factor * 10))
        margin_top = 0
    else:
        margin_top = 50
        lines = textwrap.wrap(text, width=100)

    # open the image file and get its dimensions
    img = Image.open(image_file)
    width, height = img.size

    # create a new image with a transparent background
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # create a drawing object and write the text in the center
    draw = ImageDraw.Draw(new_img)
    font_size = int(min(width, height) / division_factor)  # adjust the font size as desired
    font = ImageFont.truetype("arial.ttf", font_size)

    # get the width and height of the text
    text_height = 0
    text_width = 50
    for line in lines:
        text_width_text, text_height_text = draw.textsize(line, font=font)
        text_height += text_height_text
        text_width += text_width_text
    # calculate the x and y coordinates for center alignment
    y = (img.height - text_height) / 2
    if margin_top:
        y -= margin_top
    # draw each line of the text on the image
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((img.width - line_width) /2, y), line, font=font, fill='white')
        y += line_height + font_size  # add extra space between line

    # combine the original image and the text image
    result = Image.alpha_composite(img.convert('RGBA'), new_img)
    path = image_file.replace('.jpg', '.png')
    # Save the image in file
    result.save(path)
    os.remove(image_file)

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