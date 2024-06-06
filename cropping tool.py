import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import shutil

class ImageCropperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper")

        self.label = tk.Label(master, text="Select a folder containing images:")
        self.label.pack()

        self.select_button = tk.Button(master, text="Browse", command=self.browse_folder)
        self.select_button.pack()

        self.crop_button = tk.Button(master, text="Crop", command=self.crop_images, state=tk.DISABLED)
        self.crop_button.pack()

        self.folder_path = None
        self.parts_var = tk.StringVar(master)
        self.parts_var.set("3")  # Default to 3 parts
        self.parts_label = tk.Label(master, text="Select number of vertical parts:")
        self.parts_label.pack()
        self.parts_menu = tk.OptionMenu(master, self.parts_var, "3", "4", "5", "6", "9")
        self.parts_menu.pack()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.label.config(text=f"Selected folder: {folder_path}")
            self.crop_button.config(state=tk.NORMAL)

    def crop_images(self):
        if self.folder_path:
            try:
                num_parts = int(self.parts_var.get())
                if num_parts not in [3, 4, 5, 6, 9]:
                    messagebox.showerror("Error", "Please select a valid number of parts (3, 4, 5, 6, or 9).")
                    return

                # Create a folder for saving the output images
                output_folder = os.path.join(self.folder_path, "cropped_images")
                os.makedirs(output_folder, exist_ok=True)

                # Get a list of image files sorted by modification time
                image_files = []
                for filename in os.listdir(self.folder_path):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_path = os.path.join(self.folder_path, filename)
                        image_files.append((file_path, os.path.getmtime(file_path)))
                image_files.sort(key=lambda x: x[1])  # Sort by modification time

                # Iterate over sorted image files
                for file_path, _ in image_files:
                    image = Image.open(file_path)
                    width, height = image.size
                    crop_height = height // num_parts
                    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

                    # Crop and save the image
                    for i in range(num_parts):
                        box = (0, i * crop_height, width, (i + 1) * crop_height)
                        cropped_image = image.crop(box)
                        new_filename = f"{file_name}_part_{i+1}{file_extension}"
                        cropped_image.save(os.path.join(output_folder, new_filename))

                    # Remove the original image file
                    os.remove(file_path)

                # Move cropped images to original folder
                for cropped_filename in os.listdir(output_folder):
                    cropped_file_path = os.path.join(output_folder, cropped_filename)
                    shutil.move(cropped_file_path, self.folder_path)

                # Remove created folder
                os.rmdir(output_folder)

                messagebox.showinfo("Success", "Images cropped successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please select a folder first.")

def main():
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
