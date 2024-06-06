# ImageCropperApp

## Overview

ImageCropperApp is a Python-based desktop application that allows users to crop images vertically into multiple parts. Users can select a folder containing images, choose the number of vertical parts to crop each image into, and save the cropped images back into the original folder.

## Features

- Select a folder containing images.
- Choose the number of vertical parts to crop each image into (3, 4, 5, 6, or 9).
- Crop all images in the selected folder and save the cropped images.
- Remove the original images after cropping.

## Requirements

- Python 3.x
- Pillow
- Tkinter
- shutil

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/image-cropper-app.git
   cd image-cropper-app
   ```

2. **Install the required Python packages:**
   ```bash
   pip install pillow
   ```

## Usage

1. **Run the application:**
   ```bash
   python image_cropper_app.py
   ```

2. **Use the application:**
   - Click the "Browse" button to select a folder containing images.
   - Choose the number of vertical parts to crop each image into from the dropdown menu.
   - Click the "Crop" button to start the cropping process.
   - The cropped images will be saved in the original folder, and the original images will be removed.

## Script Explanation

### Importing Libraries
```python
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import shutil
```
- **tkinter**: For creating the graphical user interface.
- **Pillow**: For handling image processing.
- **os**: For file and directory operations.
- **shutil**: For moving files.

### ImageCropperApp Class
#### Initialization
```python
class ImageCropperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper")
        ...
```
- Initializes the main window and sets up the user interface.

#### Browsing for Folder
```python
def browse_folder(self):
    folder_path = filedialog.askdirectory()
    if folder_path:
        self.folder_path = folder_path
        self.label.config(text=f"Selected folder: {folder_path}")
        self.crop_button.config(state=tk.NORMAL)
```
- Allows the user to select a folder containing images and enables the "Crop" button.

#### Cropping Images
```python
def crop_images(self):
    if self.folder_path:
        try:
            num_parts = int(self.parts_var.get())
            if num_parts not in [3, 4, 5, 6, 9]:
                messagebox.showerror("Error", "Please select a valid number of parts (3, 4, 5, 6, or 9).")
                return

            output_folder = os.path.join(self.folder_path, "cropped_images")
            os.makedirs(output_folder, exist_ok=True)

            image_files = []
            for filename in os.listdir(self.folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(self.folder_path, filename)
                    image_files.append((file_path, os.path.getmtime(file_path)))
            image_files.sort(key=lambda x: x[1])

            for file_path, _ in image_files:
                image = Image.open(file_path)
                width, height = image.size
                crop_height = height // num_parts
                file_name, file_extension = os.path.splitext(os.path.basename(file_path))

                for i in range(num_parts):
                    box = (0, i * crop_height, width, (i + 1) * crop_height)
                    cropped_image = image.crop(box)
                    new_filename = f"{file_name}_part_{i+1}{file_extension}"
                    cropped_image.save(os.path.join(output_folder, new_filename))

                os.remove(file_path)

            for cropped_filename in os.listdir(output_folder):
                cropped_file_path = os.path.join(output_folder, cropped_filename)
                shutil.move(cropped_file_path, self.folder_path)

            os.rmdir(output_folder)

            messagebox.showinfo("Success", "Images cropped successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Error", "Please select a folder first.")
```
- Crops images into the selected number of vertical parts and saves the cropped images in the original folder.

### Main Loop
```python
def main():
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```
- Creates the main application window and starts the Tkinter event loop.

## License

This project is licensed under the MIT License.
