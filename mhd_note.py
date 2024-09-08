import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

class NoteManager :
    def __init__(self):
        self.notes = []
        self.note_count = 0
        self.load_notes()

    def add_note(self, title, content):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        self.notes.append({"title": title, "content": content, "timestamp": timestamp})
        self.note_count += 1
        self.save_notes()

    def load_notes(self):
        try:
            with open("notes.json", "r") as file:
                self.notes = json.load(file)
                self.note_count = len(self.notes)
        except FileNotFoundError:
            self.notes = []
            self.note_count = 0

    def save_notes(self):
        with open("notes.json", "w") as file:
            json.dump(self.notes, file)

    def get_note_titles(self):
        return [note["title"] for note in self.notes]

    def get_note_content(self, title):
        for note in self.notes:
            if note["title"] == title:
                return note["content"]
        return None

    def get_note_timestamp(self, title):
        for note in self.notes:
            if note["title"] == title:
                return note["timestamp"]
        return None

    def update_note_content(self, title, new_title, new_content):
        for note in self.notes:
            if note["title"] == title:
                note["title"] = new_title
                note["content"] = new_content
                note["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return True
        return False

    def delete_note_content(self, title):
        for note in self.notes:
            if note["title"] == title:
                self.notes.remove(note)
                self.note_count -= 1
                self.save_notes()
                return True
        return False

class NoteApp:
    def __init__(self, root, note_manager):
        self.root = root
        self.note_manager = note_manager
        self.root.title("Note App")
        self.root.geometry("500x510")

        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Arial", 12))
        self.style.configure("TEntry", padding=6, font=("Arial", 12))
        self.style.configure("TFrame", background="#f0f0f0")

        self.search_window = None

        self.main_frame = ttk.Frame(root, padding=(20, 20))
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.add_button = tk.Button(self.main_frame, text="Add Note", width=15, bg="green", padx=10, pady=10, command=self.add_note)
        self.add_button.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.edit_button = tk.Button(self.main_frame, text="Edit Note", width=15, bg="blue", padx=10, pady=10, command=self.show_edit_note_titles)
        self.edit_button.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.note_count_label = tk.Label(self.main_frame, text=f"Total Notes: {len(self.note_manager.notes)}", font=("Arial", 12))
        self.note_count_label.grid(row=2, column=0, pady=10, padx=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

    def add_note(self):
        def save_note():
            note_title = note_title_entry.get()
            note_content = note_content_entry.get("1.0", tk.END)
            if note_title.strip() != "" and note_content.strip() != "":
                self.note_manager.add_note(note_title, note_content)
                top.destroy()
                self.update_note_count()
                messagebox.showinfo("Success", "Note added successfully!")
            else:
                messagebox.showwarning("Warning", "Please enter both title and content for the note!")

        top = tk.Toplevel(self.root)
        top.title("Add Note")

        note_title_label = tk.Label(top, text="Note Title:")
        note_title_label.pack(pady=5)
        note_title_entry = ttk.Entry(top)
        note_title_entry.pack(pady=5)

        note_content_label = tk.Label(top, text="Note Content:")
        note_content_label.pack(pady=5)
        note_content_entry = tk.Text(top, wrap=tk.WORD, width=40, height=10, font=("Arial", 12))
        note_content_entry.pack(padx=10, pady=10)

        save_button = tk.Button(top, text="Save Note", width=15, bg="green", padx=10, pady=10, command=save_note)
        save_button.pack(pady=5)

    def show_edit_note_titles(self):
        note_titles = self.note_manager.get_note_titles()
        if note_titles:
            self.search_window = tk.Toplevel(self.root)
            self.search_window.title("Select Note to Edit")
            self.search_window.geometry("400x510")

            button_colors = ["#3a86ff",  "#3bb273" , "#ff006e", "#8338ec", "#fb5607", "#480ca8" , "#ffbe0b"]

            self.search_frame = ttk.Frame(self.search_window, padding=(20, 20))
            self.search_frame.pack(side=tk.TOP, fill=tk.X)

            self.search_entry = ttk.Entry(self.search_frame)
            self.search_entry.pack(side=tk.LEFT, padx=10)

            self.search_button = tk.Button(self.search_frame, text="Search", width=15, bg="lightblue", padx=10, pady=10, command=self.search_notes)
            self.search_button.pack(side=tk.LEFT, padx=10)

            self.scrollbar = ttk.Scrollbar(self.search_window, orient=tk.VERTICAL)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.note_frame = ttk.Frame(self.search_window)
            self.note_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            self.note_canvas = tk.Canvas(self.note_frame, yscrollcommand=self.scrollbar.set)
            self.note_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar.config(command=self.note_canvas.yview)

            self.inner_frame = ttk.Frame(self.note_canvas)
            self.note_canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

            for index, title in enumerate(note_titles):
                note_title_button = tk.Button(self.inner_frame, text=title, width=30, bg=button_colors[index % len(button_colors)], padx=10, pady=10, command=lambda t=title: self.edit_note_content(t))
                note_title_button.pack(side=tk.TOP, padx=5, pady=2)

            self.note_canvas.update_idletasks()
            self.note_canvas.config(scrollregion=self.note_canvas.bbox("all"))
        else:
            messagebox.showinfo("Info", "No notes available!")

    def edit_note_content(self, title):
        original_title = title
        original_content = self.note_manager.get_note_content(title)
        original_timestamp = self.note_manager.get_note_timestamp(title)

        if original_content:
            top = tk.Toplevel(self.root)
            top.title("Edit Note")
            top.geometry("500x510")

            def check_changes(event=None):
                if note_title_entry.get() != original_title or note_content_entry.get("1.0", tk.END).strip() != original_content.strip():
                    save_button.pack(side=tk.LEFT, padx=5)
                else:
                    save_button.pack_forget()

            def save_changes():
                new_title = note_title_entry.get()
                new_content = note_content_entry.get("1.0", tk.END)
                if new_title.strip() != "" and new_content.strip() != "":
                    self.note_manager.update_note_content(original_title, new_title, new_content)
                    top.destroy()
                    self.update_note_count()
                    messagebox.showinfo("Success", "Note updated successfully!")
                else:
                    messagebox.showwarning("Warning", "Please enter both title and content for the note!")

            def delete_note():
                if self.note_manager.delete_note_content(original_title):
                    top.destroy()
                    self.update_note_count()
                    messagebox.showinfo("Success", "Note deleted successfully!")
                else:
                    messagebox.showerror("Error", f"Note '{original_title}' not found!")

            note_title_label = tk.Label(top, text="Note Title:")
            note_title_label.pack(pady=5)
            note_title_entry = ttk.Entry(top)
            note_title_entry.insert(0, original_title)
            note_title_entry.pack(pady=5)
            note_title_entry.bind("<KeyRelease>", check_changes)

            note_content_label = tk.Label(top, text="Note Content:")
            note_content_label.pack(pady=5)
            note_content_entry = tk.Text(top, wrap=tk.WORD, width=40, height=10, font=("Arial", 12))
            note_content_entry.insert(tk.END, original_content)
            note_content_entry.pack(padx=10, pady=10)
            note_content_entry.bind("<KeyRelease>", check_changes)

            timestamp_label = tk.Label(top, text=f"Saved on: {original_timestamp}", font=("Arial", 10, "italic"))
            timestamp_label.pack(pady=5)

            button_frame = ttk.Frame(top)
            button_frame.pack(pady=5)

            save_button = tk.Button(button_frame, text="Save Changes", width=15, bg="green", padx=10, pady=10, command=save_changes)
            save_button.pack_forget()

            delete_button = tk.Button(button_frame, text="Delete Note", width=15, bg="red", padx=10, pady=10, command=delete_note)
            delete_button.pack(side=tk.LEFT, padx=5)

    def update_note_count(self):
        self.note_count_label.config(text=f"Total Notes: {len(self.note_manager.notes)}")

    def search_notes(self, event=None):
        search_term = self.search_entry.get().lower()
        note_titles = self.note_manager.get_note_titles()
        if search_term:
            filtered_titles = [title for title in note_titles if search_term in title.lower()]
            if filtered_titles:
                self.show_notes(filtered_titles)
            else:
                messagebox.showinfo("Info", "No notes found with this title.")
        else:
            self.show_notes(note_titles)

    def show_notes(self, note_titles):
        if self.search_window:
            self.search_window.destroy()

        top = tk.Toplevel(self.root)
        top.title("Select Note to Edit")
        top.geometry("400x510")

        button_colors = ["blue", "green", "yellow", "coral", "salmon", "cyan"]

        note_canvas = tk.Canvas(top)
        note_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL, command=note_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        inner_frame = ttk.Frame(note_canvas)
        note_canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

        for index, title in enumerate(note_titles):
            note_frame = ttk.Frame(inner_frame)
            note_frame.pack(pady=5)

            note_title_button = tk.Button(note_frame, text=title, width=30, bg=button_colors[index % len(button_colors)], padx=10, pady=10, command=lambda t=title: self.edit_note_content(t))
            note_title_button.pack(side=tk.TOP, padx=5, pady=2)

        note_canvas.bind("<Configure>", lambda e: note_canvas.configure(scrollregion=note_canvas.bbox("all")))
        note_canvas.configure(yscrollcommand=scrollbar.set)

if __name__ == "__main__":
    root = tk.Tk()
    note_manager = NoteManager()
    app = NoteApp(root, note_manager)
    root.mainloop()
