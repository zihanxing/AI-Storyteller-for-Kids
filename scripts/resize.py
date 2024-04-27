from PIL import Image
import os

def resize_images(directory, output_directory, size=(1024, 1024)):
    """
    Resize all images in a directory to a specific size and save them to an output directory.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            # Open the image file
            img_path = os.path.join(directory, filename)
            with Image.open(img_path) as img:
                # Resize the image using LANCZOS resampling
                img_resized = img.resize(size, Image.Resampling.LANCZOS)
                
                # Save the resized image to the output directory
                output_path = os.path.join(output_directory, filename)
                img_resized.save(output_path)
                print(f"Resized and saved: {output_path}")

input_directory = '../data/disney_original_images/'
output_directory = '../data/disney_resized_images/'

resize_images(input_directory, output_directory)
