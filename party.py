import ctypes
import os
import random
import tkinter as tk
from tkinter import messagebox
import keyboard

# Flag to control wallpaper change on/off
wallpaper_changing = False

# Function to change desktop wallpaper color (only works with plain colors)
def change_wallpaper(hex_color):
    # Convert hex color to RGB format
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Access Windows API function to set background color
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    # Set the color to be used as wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    # Print the RGB color value for confirmation
    print(f"Wallpaper color changed to RGB: {rgb_color}")

# Function to read all color codes from the file
def read_colors_from_file(file_path):
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return None

    with open(file_path, 'r') as file:
        color_codes = file.readlines()

    # Clean up the codes (remove newlines and extra spaces)
    color_codes = [code.strip() for code in color_codes if code.strip() and code.startswith('#')]
    
    return color_codes

# Function to stop wallpaper changes and show goodbye message
def stop_and_exit():
    print("Goodbye!")
    messagebox.showinfo("Goodbye", "Thank you for using the application!")
    window.quit()

# Function to change wallpaper to a random color and repeat every 0.5 seconds
def change_random_wallpaper():
    global wallpaper_changing
    if wallpaper_changing:
        file_path = "color_codes.txt"  # Change this to the path of your color code file
        color_codes = read_colors_from_file(file_path)

        if color_codes:
            # Randomly choose a color code from the list
            chosen_color = random.choice(color_codes)
            change_wallpaper(chosen_color)
            # Call this function again after 500ms (0.5 seconds)
            window.after(500, change_random_wallpaper)  # Repeating every 0.5 seconds
        else:
            print("Failed to read colors or no valid color codes found.")

# Toggle wallpaper change on/off
def toggle_wallpaper_change():
    global wallpaper_changing
    wallpaper_changing = not wallpaper_changing
    if wallpaper_changing:
        change_random_wallpaper()  # Start changing the wallpaper if it's not already
        toggle_button.config(text="Stop Wallpaper Change")  # Update button text
    else:
        toggle_button.config(text="Start Wallpaper Change")  # Update button text

# Function to handle the hotkey press for toggle
def setup_hotkey():
    hotkey = hotkey_entry.get().lower()
    keyboard.add_hotkey(hotkey, toggle_wallpaper_change)  # Bind the hotkey to toggle wallpaper change
    print(f"Hotkey {hotkey} is set to toggle wallpaper change.")

# Function to animate button on hover
def on_enter(event):
    event.widget['background'] = 'lightblue'

def on_leave(event):
    event.widget['background'] = 'lightgray'

# Create the main window
window = tk.Tk()
window.title("Wallpaper Changer")
window.geometry("400x300")

# Add hotkey input field and button to set hotkey
hotkey_label = tk.Label(window, text="Enter hotkey (e.g., 'f'): ")
hotkey_label.grid(row=0, padx=10, pady=10)
hotkey_entry = tk.Entry(window)
hotkey_entry.grid(row=0, column=1, padx=10, pady=10)
set_hotkey_button = tk.Button(window, text="Set Hotkey", width=20, height=2, command=setup_hotkey)
set_hotkey_button.grid(row=0, column=2, padx=10, pady=10)

# Create and place the buttons
toggle_button = tk.Button(window, text="Start Wallpaper Change", width=20, height=2, command=toggle_wallpaper_change)
toggle_button.grid(row=1, padx=10, pady=20)

# Add animations for buttons
toggle_button.bind("<Enter>", on_enter)
toggle_button.bind("<Leave>", on_leave)

exit_button = tk.Button(window, text="Exit", width=20, height=2, command=stop_and_exit)
exit_button.grid(row=2, padx=10, pady=10)

# Add animations for exit button
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Run the Tkinter event loop
window.mainloop()
