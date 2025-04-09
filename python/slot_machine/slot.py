import customtkinter as ctk
from customtkinter import CTkImage
import pygame
import random
from PIL import Image
import threading
import time
import os

# Init Pygame
pygame.init()
pygame.mixer.init()

# Paths
pathFile = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(pathFile, "./immagini")

# Sounds
spin_sound = pygame.mixer.Sound(os.path.join(pathFile, "spin.mp3"))
win_sound = pygame.mixer.Sound(os.path.join(pathFile, "win.mp3"))

# Load image symbols
symbol_files = ["cherry.png", "bell.png", "lemon.png", "star.png", "watermelon.png", "seven.png", "diamond.png"]
symbols_images = [Image.open(os.path.join(images_path, f)).resize((60, 60)) for f in symbol_files]
symbols = [CTkImage(light_image=img, size=(60, 60)) for img in symbols_images]

# UI
root = ctk.CTk()
root.title("Slot Machine")
root.geometry("800x600")
ctk.set_appearance_mode("dark")

# Main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=20)

reels_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
reels_frame.grid(row=0, column=0, padx=20)

# Reel containers
reels = []
reel_values = []  # Track the current symbol object
for i in range(5):
    frame = ctk.CTkFrame(reels_frame, fg_color="white", border_color="black", border_width=3, width=80, height=100)
    frame.pack_propagate(False)
    frame.grid(row=0, column=i, padx=10)
    symbol = random.choice(symbols)
    label = ctk.CTkLabel(frame, text="", image=symbol, text_color="black")
    label.pack(expand=True)
    reels.append(label)
    reel_values.append(symbol)

# Global spin state
running = False

def spin_reels():
    global running
    running = True
    spin_sound.play(0, 10)

    spins = [random.randint(10, 20) for _ in range(5)]
    stop_times = [1, 2, 3, 4, 5]

    def stop_reel(index, delay):
        time.sleep(delay)
        spins[index] = 0

    for i in range(5):
        threading.Thread(target=stop_reel, args=(i, stop_times[i]), daemon=True).start()

    while any(spins):
        for i in range(5):
            if spins[i] > 0:
                symbol = random.choice(symbols)
                reels[i].configure(image=symbol)
                reel_values[i] = symbol
        time.sleep(0.1)

    running = False
    check_win()

def check_win():
    spin_sound.stop()
    
    if all(symbol == reel_values[0] for symbol in reel_values):
        pygame.mixer.Sound.play(win_sound)
        result_label.configure(text="🎉 JACKPOT! 🎉", text_color="green")
    elif reel_values[1] == reel_values[2] == reel_values[3]:
        pygame.mixer.Sound.play(win_sound)
        result_label.configure(text="🎉 3 SIMBOLI CENTRALI! 🎉", text_color="green")
    elif reel_values[0] == reel_values[4]:
        pygame.mixer.Sound.play(win_sound)
        result_label.configure(text="🎉 ESTERNI UGUALI! 🎉", text_color="green")
    else:
        result_label.configure(text="Riprova!", text_color="red")

    reset_lever()

# Result label
result_label = ctk.CTkLabel(root, text="", font=("Arial", 20))
result_label.pack(pady=10)

# Global lever state
lever_dragging = False

# Lever canvas
lever_canvas = ctk.CTkCanvas(root, width=100, height=200, bg="gray20", highlightthickness=0)
lever_canvas.place(x=500, y=100)
lever_canvas.create_line(50, 0, 50, 200, fill="silver", width=8)
lever_knob = lever_canvas.create_oval(35, 80, 65, 110, fill="red")

# Lever drag

def on_lever_drag(event):
    global lever_dragging
    lever_dragging = True
    y = min(max(event.y, 80), 170)
    lever_canvas.coords(lever_knob, 35, y, 65, y + 30)

# Lever release

def on_lever_release(event):
    global lever_dragging
    lever_dragging = False
    coords = lever_canvas.coords(lever_knob)
    if coords:
        _, _, _, knob_bottom = coords
        if knob_bottom >= 170:
            threading.Thread(target=spin_reels, daemon=True).start()
        reset_lever()

# Reset lever

def reset_lever():
    def move_knob(y):
        lever_canvas.coords(lever_knob, 35, y, 65, y + 30)
        lever_canvas.update()

    current_y = int(lever_canvas.coords(lever_knob)[1])
    for y in range(current_y, 80, -2):
        # Schedule the knob movement to be handled on the main thread
        lever_canvas.after(10, move_knob, y)
        time.sleep(0.01)  # You can control the speed here


lever_canvas.tag_bind(lever_knob, "<B1-Motion>", on_lever_drag)
lever_canvas.tag_bind(lever_knob, "<ButtonRelease-1>", on_lever_release)

# Fallback spin button
spin_button = ctk.CTkButton(root, text="Spin", command=lambda: threading.Thread(target=spin_reels, daemon=True).start())
spin_button.pack(pady=10)

# Main loop
root.mainloop()