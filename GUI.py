import os
import subprocess
import tkinter as tk
import threading
import time

# Define JAR games and their launch commands
GAMES = [
    ("Pong", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Pong.jar"),
    ("Breakout", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Breakout.jar"),
    ("Tetris", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Tetris.jar"),
    ("Snake", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Snake.jar"),
    ("Pacman", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Pacman.jar"),
    ("Chess", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Chess.jar"),
    ("Minesweeper", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar Minesweeper.jar"),
    ("Space Invaders", "java --module-path /path/to/javafx-sdk-17/lib --add-modules javafx.controls,javafx.fxml -jar SpaceInvaders.jar")
]

processes = {}
hold_keys = set()

# Initialize Tkinter
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Track selected game
selected_index = 0

def update_menu():
    """Update menu display"""
    menu_text.delete("1.0", tk.END)
    for i, (game, _) in enumerate(GAMES):
        if i == selected_index:
            menu_text.insert(tk.END, f"{game}\n", "selected")
        else:
            menu_text.insert(tk.END, f"{game}\n")

# Function to launch a selected game
def launch_game(index):
    if 0 <= index < len(GAMES):
        command = GAMES[index][1]
        process = subprocess.Popen(command, shell=True)
        processes[index] = process

def navigate(direction):
    """Change selection based on direction"""
    global selected_index
    if direction == "up":
        selected_index = (selected_index - 1) % len(GAMES)
    elif direction == "down":
        selected_index = (selected_index + 1) % len(GAMES)
    update_menu()

def close_games():
    """Close all running games if all keys 1-8 are held for 5 seconds"""
    time.sleep(5)
    if hold_keys == set(map(str, range(1, 9))):
        for proc in processes.values():
            proc.terminate()
        processes.clear()

def on_key(event):
    """Handle key press events"""
    if event.keysym in ["Up", "w"]:
        navigate("up")
    elif event.keysym in ["Down", "s"]:
        navigate("down")
    elif event.keysym.isdigit():
        index = int(event.keysym) - 1
        launch_game(index)
        hold_keys.add(event.keysym)
        if len(hold_keys) == 8:
            threading.Thread(target=close_games, daemon=True).start()
    elif event.keysym == "Escape":
        root.destroy()

def on_key_release(event):
    """Handle key release events"""
    if event.keysym in hold_keys:
        hold_keys.remove(event.keysym)

# Create a canvas for background
canvas = tk.Canvas(root, bg="black")
canvas.pack(expand=True, fill=tk.BOTH)

# Add a title at the top
title = tk.Label(canvas, text="PROJECT GREENPI", font=("Courier", 36), bg="black", fg="green")
title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Add a colorful frame around the menu
frame = tk.Frame(canvas, bg="blue", bd=10)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.6)

# Create a text widget to display menu
menu_text = tk.Text(frame, font=("Courier", 24), bg="black", fg="white", padx=20, pady=20)
menu_text.tag_configure("selected", background="blue", foreground="white")
menu_text.pack(expand=True, fill=tk.BOTH)

# Bind keys
root.bind("<KeyPress>", on_key)
root.bind("<KeyRelease>", on_key_release)
update_menu()
root.mainloop()
