import os
from PIL import ImageGrab
from datetime import datetime

# Screenshot folder path
folder_path = f"C:\Users\{os.getlogin()}\OneDrive\Pictures\Screenshots"

# Saves image in clipboard to specified screenshot folder
def save_clipboard_image(folder_path):

    # Check if the folder exists, create it if necessary
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get image from clipboard
    image = ImageGrab.grabclipboard()
    if image is None:
        return

    # Save the image with a unique file name 
    image.save(os.path.join(folder_path, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))

# Call the function to save the clipboard image
save_clipboard_image(folder_path)
