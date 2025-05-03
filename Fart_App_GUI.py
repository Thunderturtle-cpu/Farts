import os
import random
import tkinter as tk
from tkinter import messagebox, ttk 

#def radnom_fart
#    sounds = ["PFFT", "BRAP", "POOT", "THPPTPHTPHPHHPH"]
#    return

class FartApp:
    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)   
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.root.title("Fart Central™ GUI Edition")
        self.tab_data = {}
        self.tab_count = 1
        self.drag_item = None

        self.font = ("DejaVu Sans", 12) if os.name == "posix" else ("Arial", 12)
        self.farts_dir = os.path.join(os.getcwd(), "farts")
        if not os.path.exists(self.farts_dir):
            os.makedirs(self.farts_dir, mode=0o777)

        self.plus_tab = tk.Frame(self.notebook)
        self.notebook.add(self.plus_tab, text="+")
        self.add_tab("Fart Tab 1")
        self.notebook.bind("<ButtonPress-1>", self.on_tab_click)


    def add_tab(self, title):
        tab = tk.Frame(self.notebook)

        listbox= tk.Listbox(tab, font=self.font)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        entry = tk.Entry(tab, font=self.font)
        entry.pack(fill=tk.X, padx=5, pady=5)

        button_frame = tk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(button_frame, text="Add Fart",
        command=lambda:self.add_fart(entry, listbox)).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Remove Fart",
        command=lambda: self.remove_fart(listbox)).pack(side=tk.LEFT)
        tk.Button(button_frame, text="✖", font=(self.font[0], 14, "bold"), command=lambda: self.close_tab(tab)).pack(side=tk.RIGHT, anchor="ne")

        file_name = os.path.join(self.farts_dir,f"farts_{title.lower().replace(' ', '_')}.txt")
        tab_id = len(self.notebook.tabs()) -1

        self.tab_data[tab_id] = {
            "listbox": listbox,
            "farts": self.load_farts(file_name),
            "file": file_name,
            "frame": tab
        }
        self.notebook.insert(tab_id, tab, text=title)
        self.update_listbox(listbox, self.tab_data[tab_id]["farts"])

        listbox.bind("<ButtonPress-3>", lambda e: self.on_drag_start(e))
        listbox.bind("<B3-Motion>", lambda e: self.on_drag_motion(e))
        listbox.bind("<ButtonRelease-3>", lambda e: self.on_drop(e))
        
    def close_tab(self, tab):
        tab_index = None
        for tab_id, data in self.tab_data.items():
            if data["frame"] == tab:
                tab_index = tab_id
                break

        if tab_index is None:
            return           

        self.notebook.forget(tab_index)
        if os.path.exists(self.tab_data[tab_index]["file"]):
            os.remove(self.tab_data[tab_index]["file"])
        del self.tab_data[tab_index]

        new_data = {}
        for new_id, tab_id in enumerate(sorted(self.tab_data.keys())):
            new_data[new_id]= self.tab_data[tab_id]
        self.tab_data = new_data

    def add_fart(self, entry_widget, listbox):
        tab_data = self.get_current_tab_data()
        if not tab_data:
            return

        fart = entry_widget.get()
        if fart:
            tab_data["farts"].append(fart)
            self.save_farts(tab_data["farts"], tab_data["file"])
            self.update_listbox(listbox, tab_data["farts"])
            entry_widget.delete(0, tk.END)
            messagebox.showinfo("Added", f"💨 {fart}")  
    def remove_fart(self, listbox):
        tab_data = self.get_current_tab_data() 
        if not tab_data:
            return

        try:
            index = listbox.curselection()[0]
            removed_fart = tab_data["farts"].pop(index)
            self.save_farts(tab_data["farts"], tab_data["file"])
            self.update_listbox(listbox, tab_data["farts"])
            messagebox.showinfo("Removed",)
        except IndexError:    
            messagebox.showinfo("Error", "No fart selected! 🫢")

    def load_farts(self, file_name):
        try:
            if not os.path.exists(file_name):
                return []
            with open(file_name, "r") as file:
                return file.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't load farts: {str(e)}")
            return []

    def save_farts(self, farts, file_name):
        
        try:
            with open(file_name, "w") as file:
                file.write("\n".join(farts))
        except Exception as e:
                messagebox.showerror("Error", f"Couldn't save farts:\n{str(e)}")

    def update_listbox(self, listbox, farts):
        listbox.delete(0, tk.END)
        for fart in farts:
            listbox.insert(tk.END, fart)

    def get_current_tab_data(self):
        current = self.notebook.index(self.notebook.select())
        return self.tab_data.get(current, None) 

    def on_drag_start(self, event):
        self.drag_item = event.widget.nearest(event.y)

    def on_drag_motion(self, event):
        if self.drag_item is not None:
            widget = event.widget
            hover_index = widget.nearest(event.y)
            if hover_index != self.drag_item:
                widget.selection_clear(0, tk.END)
                widget.selection_set(hover_index)

    def on_drop(self, event):
        widget = event.widget
        tab_data = self.get_current_tab_data()
        if not tab_data or self.drag_item is None:
            return

        drop_index = widget.nearest(event.y)
        if drop_index != self.drag_item:
            fart = tab_data["farts"].pop(self.drag_item) 
            tab_data["farts"].insert(drop_index, fart)
            self.save_farts(tab_data["farts"], tab_data["file"])
            self.update_listbox(widget, tab_data["farts"])
        self.drag_item = None

    def on_tab_click(self,event):
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")
            if tab_index == len(self.notebook.tabs()) -1:
                self.tab_count += 1
                self.add_tab(f"Fart Tab {self.tab_count}")
        except tk.TclError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = FartApp(root)
    root.mainloop()                                                                                                        