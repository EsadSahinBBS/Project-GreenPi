import os
import subprocess
import tkinter as tk

dir_path = os.path.dirname(os.path.abspath(__file__))
javafx_path = "/home/pi/Downloads/javafx-sdk-23.0.2/lib"

# Alle JAR-Dateien im aktuellen Ordner finden
jar_files = [f for f in os.listdir(dir_path) if f.endswith(".jar")]
selected_index = 0  # Aktuelle Auswahl

def update_selection():
    for i, label in enumerate(labels):
        if i == selected_index:
            label.config(bg="yellow", fg="black")
        else:
            label.config(bg="black", fg="white")

def launch_jar():
    if jar_files:
        jar_path = os.path.join(dir_path, jar_files[selected_index])
        cmd = [
            "java", "--module-path", javafx_path, "--add-modules", "javafx.controls,javafx.fxml",
            "-jar", jar_path
        ]
        subprocess.Popen(cmd)

def on_key(event):
    global selected_index
    if event.keysym in ("Up", "w"):
        selected_index = (selected_index - 1) % len(jar_files)
    elif event.keysym in ("Down", "s"):
        selected_index = (selected_index + 1) % len(jar_files)
    elif event.keysym in ("Return", "space"):
        launch_jar()
    update_selection()

# Tkinter-Fenster erstellen
root = tk.Tk()
root.title("Project-GreenPi")
root.configure(bg="black")
root.attributes('-fullscreen', True)
root.bind("<KeyPress>", on_key)

# Titel
title_label = tk.Label(root, text="Project-GreenPi", font=("Arial", 20, "bold"), bg="black", fg="white")
title_label.pack(pady=20)

labels = []
for jar in jar_files:
    label = tk.Label(root, text=jar, font=("Arial", 14), bg="black", fg="white")
    label.pack(pady=5)
    labels.append(label)

update_selection()
root.mainloop()
