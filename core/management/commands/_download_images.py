import requests
import os
import random
import string

# Define function to generate random image URL from Unsplash API
def random_image_url():
    url = "https://source.unsplash.com/random/800x500"
    return url

# Define function to download image from URL and save to directory
def download_image(url, directory):
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + '.jpg'
    filepath = os.path.join(directory, filename)
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return os.path.join(directory, filename)

def main():
    # Call download function 50 times with randomly generated image URLs
    for i in range(300):
        url = random_image_url()
        download_image(url, 'random-images/')

if __name__ == '__main__':
    main()