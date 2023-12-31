# This file is part of ColorCatcher, a color palette extraction tool.
# Copyright (C) 2023 Serg
#
# ColorCatcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.


import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import pyperclip
import configparser
import os
import sys

def load_and_resize_image(image_path, base_width=300):
    try:
        img = Image.open(image_path)
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img_resized = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        return img, img_resized
    except IOError:
        print(f"Error: Unable to load image '{image_path}'. Check if the file exists and is an image.")
        return None, None

def extract_color_palette(img_data, num_colors=5):
    try:
        kmeans = KMeans(n_clusters=num_colors, n_init=10)
        kmeans.fit(img_data)
        return kmeans.cluster_centers_ / 255.0
    except ValueError as e:
        print(f"Error in color extraction: {e}")
        return None

def onclick_copy_rgb(event, img, palette, num_colors, ax_image, ax_palette):
    if event.inaxes == ax_image:
        x, y = int(event.xdata), int(event.ydata)
        color = img.getpixel((x, y))
        normalized_color = tuple(c / 255.0 for c in color)
    elif event.inaxes == ax_palette:
        ax_width = ax_palette.get_xlim()[1] - ax_palette.get_xlim()[0]
        rel_x = (event.xdata - ax_palette.get_xlim()[0]) / ax_width
        index = int(rel_x * num_colors)
        if 0 <= index < num_colors:
            normalized_color = palette[index]
            color = tuple(int(round(c * 255)) for c in normalized_color)
        else:
            return
    else:
        return

    if event.button == 1:  # LMB - Copy normalized RGB
        color_str = f"{normalized_color[0]:.2f}, {normalized_color[1]:.2f}, {normalized_color[2]:.2f}"
    elif event.button == 3:  # RMB - Copy HEX
        color_str = '#%02x%02x%02x' % color
    else:
        #print (color)
        color_str = f"{color[0]}, {color[1]}, {color[2]}"

    pyperclip.copy(color_str)
    print(f"Copied to clipboard: {color_str}")

def display_image_and_palette(img, palette, num_colors):
    # Set the DPI for the figure
    dpi = 100  # Adjust this value as needed

    # Set the figure size (width, height) in inches
    fig_width, fig_height = 12, 7  # Adjust these values as needed

    # Create a figure with the specified size and DPI
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

    # Define the grid layout
    gs = gridspec.GridSpec(1, 4)  # 1 row, 4 columns

    # Assign the subplots to parts of the grid
    ax_image = fig.add_subplot(gs[0, :3])  # Image occupies first 3 columns
    ax_palette = fig.add_subplot(gs[0, 3])  # Palette occupies the last column

    # Adjust subplot parameters
    fig.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97, wspace=0.03)

    # Plot the original image
    ax_image.imshow(img)
    ax_image.axis('off')  # Turn off the axis for the original image
    ax_image.set_title('Original Image')

    # Plot the color palette
    ax_palette.imshow([palette])
    ax_palette.axis('off')  # Make sure the axis is off for the palette
    ax_palette.set_title('Color Palette (Normalized)')

    # Connect the onclick event
    onclick_handler = lambda event: onclick_copy_rgb(event, img, palette, num_colors, ax_image, ax_palette)
    fig.canvas.mpl_connect('button_press_event', onclick_handler)

    plt.show()

def create_gui_and_get_input():
    config = configparser.ConfigParser()

    # Check if the script is running as a standalone executable
    if getattr(sys, 'frozen', False):
        # If it's an executable, the path is set to the directory of the executable
        application_path = os.path.dirname(sys.executable)
    else:
        # If it's a script, the path is set to the directory of the script
        application_path = os.path.dirname(os.path.abspath(__file__))

    config_file = os.path.join(application_path, 'config.ini')

    try:
        with open(config_file, 'r') as f:
            config.read_file(f)
    except FileNotFoundError:
        print(f"Error: '{config_file}' not found. Using default values.")
        default_num_colors = 7
    else:
        default_num_colors = config.getint('DEFAULT', 'num_colors', fallback=7)

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Image and Palette Settings")

    # Variables to store the number of colors and the image path
    num_colors_var = tk.IntVar(value=default_num_colors)  # Default value set to 7
    image_path_var = tk.StringVar()

    # Function to open file dialog
    def select_image():
        file_path = filedialog.askopenfilename(
            parent=root,
            filetypes=[("Image Files", "*.jpeg;*.jpg;*.png;*.bmp;*.gif"), ("All Files", "*.*")])
        if file_path:  # Update only if a file is selected
            image_path_var.set(file_path)

    # UI Elements
    label_num_colors = tk.Label(root, text="Number of colors in the palette:")
    label_num_colors.pack(pady=5)

    spinbox = tk.Spinbox(root, from_=1, to=20, textvariable=num_colors_var)
    spinbox.pack(pady=5)

    label_image_path = tk.Label(root, text="Image path:")
    label_image_path.pack(pady=5)

    entry_frame = tk.Frame(root)
    entry_image_path = tk.Entry(entry_frame, textvariable=image_path_var, width=40)
    entry_image_path.pack(side=tk.LEFT, padx=(0, 5))
    button_select_image = tk.Button(entry_frame, text="...", command=select_image)
    button_select_image.pack(side=tk.LEFT)
    entry_frame.pack(pady=5)

    # Function to handle Process button click
    def on_process():
        if image_path_var.get():
            root.quit()
            root.destroy()
        else:
            messagebox.showinfo("Info", "Please select an image or enter a path.")

    process_button = tk.Button(root, text="Process", command=on_process)
    process_button.pack(pady=10)

    # Run the Tkinter loop until the window is closed
    root.mainloop()

    return num_colors_var.get(), image_path_var.get()

def main():
    while True:
        num_colors, image_path = create_gui_and_get_input()
        if image_path:
            img, img_resized = load_and_resize_image(image_path)
            img_data = np.array(img_resized).reshape((-1, 3))
            palette = extract_color_palette(img_data, num_colors)
            display_image_and_palette(img, palette, num_colors)
        else:
            print("No image selected or program terminated.")
            break

if __name__ == "__main__":
    main()