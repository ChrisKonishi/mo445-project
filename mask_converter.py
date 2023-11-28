import os
from PIL import Image

def change_pixels_in_folder(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return
    
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    files.sort()
    
    # Iterate through each file in the folder
    for file_name in files:
        # Check if the file is an image (you can add more image extensions if needed)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(folder_path, file_name)
            
            # Open the image
            img = Image.open(file_path)
            
            # Get the image dimensions
            width, height = img.size
            
            # Iterate through each pixel and change pixel values
            for y in range(height):
                for x in range(width):
                    # Get the pixel value
                    pixel_value = img.getpixel((x, y))
                    
                    # If pixel value is 1, change it to 255
                    if pixel_value != 0:
                        img.putpixel((x, y), 255)
            
            # Save the modified image with a new filename
            modified_file_path = os.path.join(folder_path, f"modified_{file_name}")
            img.save(modified_file_path)
            print(f"Modified {file_name} saved as {modified_file_path}")

# Replace "your_folder_path" with the path to your folder containing images
change_pixels_in_folder("./label")