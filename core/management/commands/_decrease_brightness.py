from PIL import Image, ImageOps
import os

def decrease_brightness(filepath):
    # Open the image file
    image = Image.open(filepath)

    source = image.split()

    R, G, B = 0, 1, 2
    constant = 2.5 # constant by which each pixel is divided

    Red = source[R].point(lambda i: i/constant)
    Green = source[G].point(lambda i: i/constant)
    Blue = source[B].point(lambda i: i/constant)

    im = Image.merge(image.mode, (Red, Green, Blue))

    # Save the modified image
    output_filepath = os.path.join('bookquotes-images', os.path.basename(filepath))
    im.save(output_filepath)

    return True

def main():
    images = os.listdir('random-images')
    if not os.path.exists('bookquotes-images'):
        os.mkdir('bookquotes-images')
    for image in images:
        image = os.path.join('random-images', image)
        decrease_brightness(image)


if __name__ == '__main__':
    main()
