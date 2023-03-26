import json
from PIL import Image
import io
import os
import requests
import re


def remove_special_chars(input_string):
    # Define the regular expression pattern to match special characters
    pattern = r'[^\w\s]'

    # Use the sub() function to replace all special characters with an empty string
    output_string = re.sub(pattern, '', input_string)

    return output_string


# Create a directory to save the images in
if not os.path.exists('Images'):
    os.mkdir('Images')

# Open the JSON file and load its contents into a Python object
with open('books_data/books_data.json') as file:
    links_data = json.load(file)

images_saved = []
with open('images_saved.txt') as f:
    for line in f.readlines():
        images_saved.append(line.strip())

print(images_saved)

# Print the links to the console
try:
    for link in links_data:
        if link['book_name'] in images_saved:
            continue
        response = requests.get(link["image_src"])

        # Create a PIL image object from the binary data
        pil_image = Image.open(io.BytesIO(response.content))

        # Save the image as a WEBP file
        cleaned_str = "Images/" + remove_special_chars(link["book_name"]) + " Image.webp"
        pil_image.save(cleaned_str, format="webp")

        images_saved.append(link['book_name'])

except Exception:
    with open('images_saved.txt', 'w') as f:
        for image in images_saved:
            f.write(image + '\n')