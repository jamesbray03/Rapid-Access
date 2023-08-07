import os
from PIL import ImageGrab
from datetime import datetime

# if 
def save_clipboard_image(folder_path):
    # Check if the folder exists, create it if necessary
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get image data from clipboard
    image = ImageGrab.grabclipboard()

    # Check if clipboard contains an image
    if image is None:
        print("No image found in clipboard.")
        return

    # Generate a unique filename with a timestamp for the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder_path, f"screenshot_{timestamp}.png")

    # Save the image to the specified folder
    image.save(filename)
    print(f"Image saved as: {filename}")

# Specify the folder path where you want to save the image
folder_path = r"C:\Users\mango\OneDrive\Pictures\Screenshots"

# Call the function to save the clipboard image
save_clipboard_image(folder_path)
