import os
from PIL import ImageGrab
from datetime import datetime
import shutil

# get screenshots directory
folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# get image data from clipboard
image = ImageGrab.grabclipboard()

# save the image
if image is not None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder_path, f"screenshot_{timestamp}.png")
    image.save(filename)
