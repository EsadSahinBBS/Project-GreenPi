import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Define the folder containing your JAR files
GAMES_FOLDER = "/home/evo/Desktop/RPi_UI/games/"

class RetroJarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RetroJar - Game Selection")

        # Start in fullscreen mode
        self.root.attributes("-fullscreen", True)

        # Close fullscreen on Escape
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Title label
        self.title_label = tk.Label(
            root, text="RetroJar", font=("Courier", 36, "bold"), fg="yellow", bg="black"
        )
        self.title_label.pack(pady=20)

        # Frame for game list
        self.list_frame = tk.Frame(root, bg="black")
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox for games
        self.game_listbox = tk.Listbox(
            self.list_frame, font=("Courier", 20), bg="black", fg="white",
            selectbackground="yellow", selectforeground="black", activestyle="none"
        )
        self.game_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scroll functionality without scrollbar
        self.game_listbox.bind("<MouseWheel>", self.mouse_scroll)
        self.game_listbox.bind("<Up>", self.navigate_up)
        self.game_listbox.bind("<Down>", self.navigate_down)
        self.game_listbox.bind("<Return>", self.launch_selected_game)
        self.game_listbox.bind("<Double-Button-1>", self.launch_selected_game)

        # Populate game list
        self.populate_game_list()

    def populate_game_list(self):
        """Load JAR games into the listbox."""
        try:
            self.games = [f for f in os.listdir(GAMES_FOLDER) if f.endswith(".jar")]
            if not self.games:
                messagebox.showerror("No Games Found", "No JAR games were found in the specified folder.")
                self.root.quit()
            else:
                for game in self.games:
                    self.game_listbox.insert(tk.END, game)
        except FileNotFoundError:
            messagebox.showerror("Error", "Games folder not found!")
            self.root.quit()

    def launch_selected_game(self, event=None):
        """Launch the selected game."""
        selected_index = self.game_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a game to launch.")
            return

        game_name = self.games[selected_index[0]]
        game_path = os.path.join(GAMES_FOLDER, game_name)

        try:
            subprocess.Popen(["java", "-jar", game_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {game_name}: {e}")

    def navigate_up(self, event):
        """Navigate up in the game list."""
        current_selection = self.game_listbox.curselection()
        if current_selection:
            new_selection = max(0, current_selection[0] - 1)
            self.game_listbox.selection_clear(0, tk.END)
            self.game_listbox.selection_set(new_selection)
            self.game_listbox.activate(new_selection)

    def navigate_down(self, event):
        """Navigate down in the game list."""
        current_selection = self.game_listbox.curselection()
        if current_selection:
            new_selection = min(len(self.games) - 1, current_selection[0] + 1)
            self.game_listbox.selection_clear(0, tk.END)
            self.game_listbox.selection_set(new_selection)
            self.game_listbox.activate(new_selection)

    def mouse_scroll(self, event):
        """Scroll the listbox with the mouse wheel."""
        self.game_listbox.yview_scroll(-1 * (event.delta // 120), "units")

    def exit_fullscreen(self, event):
        """Exit fullscreen mode."""
        self.root.attributes("-fullscreen", False)


if __name__ == "__main__":
    root = tk.Tk()
    app = RetroJarApp(root)
    root.mainloop()
