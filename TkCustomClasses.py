import pickle
import tkinter as tk
from CharClasses import *
from BattleClasses import *
from getpass import getuser
from tkinter import messagebox

class MoveMenu(object):
    def __init__(self, parent, txtval):
        self.parent = parent
        
        self.menu = tk.Menu(self.parent, tearoff=0)
        self.menulabel = tk.Button(self.parent, text=txtval, bg="pale green", borderwidth=2,
                                   relief="groove", font=("Times", 14, "bold"))
        self.menulabel.bind("<Button-1>", self.display_menu)

    def display_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def add_entry(self, move, move_func):
        ftext = "{}, Power: {}, Cost: {}".format(*move)
        self.menu.add_command(label=ftext, font=("Times", 12),
                              command=lambda: move_func(move))

    def remove_all(self):
        self.menu.delete(0, tk.END)
    
    def locate(self):
        self.menulabel.pack(side="left", padx=5, pady=5, fill="both", expand=True)

class ToolBar(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.config(bg="pale goldenrod", borderwidth=4, relief="groove")

        self.save_button=tk.Button(self, text="Save", width=10, font=self.controller.font, bg="pale goldenrod",
                                   command=lambda: self.controller.save_all())
        self.load_button=tk.Button(self, text="Load", width=10, font=self.controller.font, bg="pale goldenrod",
                                   command=lambda: self.controller.load_all())
        self.home_button=tk.Button(self, text="Home", width=10, font=self.controller.font,
                                   bg="pale goldenrod", command=lambda: self.controller.show_frame("GroupPage"))

        self.save_button.pack(side="left", pady=5, padx=5)
        self.load_button.pack(side="left", pady=5, padx=5)
        self.home_button.pack(side="right", pady=5, padx=5)

class DeleteTab(tk.Frame):
    def __init__(self, parent, controller, obj):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="pale green", borderwidth=0)
        self.info_label = tk.Label(self, text="Name: {}, Level: {}".format(obj.name, obj.lvl),
                                   bg="pale green", font=self.controller.font)
        self.delete_button = tk.Button(self, text="Sell "+obj.type, command=lambda: self.controller.delete_character(self, obj),
                                       bg="pale green", borderwidth=2, relief="groove", font=self.controller.font)
        self.info_label.pack(side="left", fill="x", expand=True)
        
        self.profile_image = tk.PhotoImage(file="imgres/"+obj.type+"_profile.png")
        self.profile_label = tk.Label(self, image=self.profile_image)
        self.profile_label.image = self.profile_image
        self.profile_label.pack(side="right", fill="x")
        self.delete_button.pack(side="right", fill="x", expand=True, pady=5, padx=5)

class HomeButton(tk.Button):
    def __init__(self, parent, controller, name, page):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="pale green", text=name, font=self.controller.font,
                    command=lambda: self.controller.show_frame(page), borderwidth=0)

class FrameScrollBar(tk.Frame):
     def __init__(self, parent, turn, turn_scroll):
         super().__init__(parent)
         self.turn = turn
         self.turn_scroll = turn_scroll
         self.wid_canvas = tk.Canvas(self, bg="pale green", borderwidth=0, highlightthickness=0)
         self.inner_frame = tk.Frame(self.wid_canvas, bg="pale green")
         self.scroll = tk.Scrollbar(self, bg="pale green", orient="vertical", command=self.wid_canvas.yview)

         self.config(bg="pale green")
         self.wid_canvas.configure(yscrollcommand=self.scroll.set)
         self.wid_canvas.create_window((80,0), window=self.inner_frame, anchor="nw")
         self.inner_frame.bind("<Configure>", self.configureCanvas)
         
     def configureCanvas(self, event):
         self.wid_canvas.config(scrollregion=self.wid_canvas.bbox("all"))

     def locate(self):
         self.pack(side=self.turn, fill="both", expand=True, pady=20, padx=20)
         self.scroll.pack(side=self.turn_scroll, fill="y")
         self.wid_canvas.pack(side="left", fill="both", expand=True, pady=10)

class PropEntry(tk.Frame):
     def __init__(self, parent, label, value, font=("Times", 12, "bold")):
         super().__init__(parent)
         self.config(bg="pale green")

         self.prop_label = tk.Label(self, text=label, font=font, bg="pale green")
         self.prop_entry = tk.Entry(self, font=font, width=20)
         self.prop_entry.insert(0, value)
         self.prop_label.pack(side="top", fill="x", expand=True, pady=5)
         self.prop_entry.pack(padx=5)
