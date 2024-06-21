#!/usr/bin/env python

from PIL import Image, ImageEnhance
import os
import math
import sys

# Function to create the output directory if it doesn't exist
def create_output_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# Function to crop the center square based on a percentage of the image's width
def crop_center_square(img, crop_percentage):
    width, height = img.size
    square_size = int(width * crop_percentage)
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = (width + square_size) // 2
    bottom = (height + square_size) // 2
    img = img.crop((left, top, right, bottom))
    return img

# Function to automatically tile images with adjustable crop size and add borders
def tile_images_with_borders(image_directory, output_directory, crop_percentages, border_size=10, border_color='black', grid=None):
    image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()

    if not image_files:
        raise ValueError("No image files found in the directory.")
    
    # Create the output directory if it doesn't exist
    create_output_directory(output_directory)

    output_file_paths = []

    for crop_percentage in crop_percentages:
        with Image.open(os.path.join(image_directory, image_files[0])) as img:
            cropped_image = crop_center_square(img, crop_percentage)
            img_width, img_height = cropped_image.size

        if grid is None:
            num_images = len(image_files)
            grid_cols = math.ceil(math.sqrt(num_images))
            grid_rows = math.ceil(num_images / grid_cols)
        else:
            grid_cols, grid_rows = grid

        # The size of the tiled image needs to account for borders between the images
        tiled_image = Image.new('RGB', ((img_width + border_size) * grid_cols - border_size, 
                                        (img_height + border_size) * grid_rows - border_size), 
                                color=border_color)

        for index, filename in enumerate(image_files):
            with Image.open(os.path.join(image_directory, filename)) as img:
                cropped_img = crop_center_square(img, crop_percentage)
                # Calculate the position where the image will be pasted, accounting for the borders
                x = (index % grid_cols) * (img_width + border_size)
                y = (index // grid_cols) * (img_height + border_size)
                # Paste the cropped image onto the tiled image at the calculated position
                tiled_image.paste(cropped_img, (x, y))

        # Adjust brightness
        enhancer = ImageEnhance.Brightness(tiled_image)
        tiled_image = enhancer.enhance(1.3)  # Increase brightness slightly

        # Save the tiled image
        output_filename = f'tiled_image_with_borders_{int(crop_percentage*100)}_percent.jpg'
        tiled_image_path = os.path.join(output_directory, output_filename)
        tiled_image.save(tiled_image_path)
        output_file_paths.append(tiled_image_path)
    
    return output_file_paths



# Path to the directory containing the images
if len(sys.argv) >1:
    if sys.argv[1][:-1] == "/": image_directory = sys.argv[1]
    else: image_directory = sys.argv[1] + "/"
else:
    print("need file name as argument")
    sys.exit()

# Path to the directory to save the output tiled images
output_directory = image_directory+'output/'

# Crop percentages for the two tiled images
crop_percentages = [0.25, 0.9]

# Size of the border to add between images
border_size = 2  # pixels

# Color of the border
border_color = 'black'

# Call the function to tile the images with borders and get the paths to the tiled images
tiled_image_paths_with_borders = tile_images_with_borders(image_directory, output_directory, crop_percentages, border_size, border_color)

# Return the paths to the saved tiled images
tiled_image_paths_with_borders
