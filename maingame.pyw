import pickle, socket
import tkinter as tk
from random import randint
from CharClasses import *
from BattleClasses import *
from TkCustomClasses import *
from getpass import getuser
from tkinter import messagebox

class RPGMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = ("Times", 24, "bold")
        self.wm_geometry("900x700")
        self.minsize("900", "700")
        self.maxsize("900", "700")
        self.title("RPG GAME")
        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.toolbar = ToolBar(self)
        container.pack(side="bottom", fill="both", expand=True)
        self.toolbar.pack(side="top", fill="x")

        self.bank = 100
        self.team_list = []

        self.frames = {}

        for F in (AddPage, DeletePage, GroupPage, MultiplayerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("GroupPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.event_generate("<<CharPopulate>>")
        frame.event_generate("<<CurrentBank>>")
        frame.tkraise()

    def upgrade_team(self, enemy_total_level):
        lvl_up = enemy_total_level-(sum((ally.lvl for ally in self.team_list))//len(self.team_list))
        lvl_up = 1 if lvl_up < 1 else lvl_up
        self.bank += randint(10, 100)
        for ally in self.team_list:
            ally.health += 5*lvl_up
            ally.mana += 5*lvl_up
            ally.lvl += lvl_up

    def upgrade_team_loss(self):
        lvl_up = 1
        self.bank += randint(0, 10)
        for ally in self.team_list:
            ally.health += 5
            ally.mana += 5
            ally.lvl += lvl_up
    
    def add_character(self, char):
        if len(self.team_list)>2:
            messagebox.showwarning(title="No More!", message="You cannot have more than 3 characters in your team at once")
            return
        elif image_chars[char].amount > self.bank:
            messagebox.showwarning(title="Not Enough!", message="You do not have the funds to purchase this character.")
            return
        obj=chars[char]()
        self.bank -= obj.amount
        message = "{} named {} has successfully been bought!".format(obj.type, obj.name)
        self.team_list += [obj]
        messagebox.showinfo(title="Character Bought", message=message)

    def delete_character(self, parent, char):
        selling_price = (char.amount*char.lvl)//2
        message="{} named {} has successfully been sold for £{}".format(char.type, char.name, selling_price)
        self.bank += selling_price
        self.team_list.remove(char)
        messagebox.showinfo(title="Character Sold", message=message)
        parent.destroy()

    def save_all(self):
        with open("save_file.Prgp", "wb") as file:
            data = {"team_list": self.team_list, "gold": self.bank}
            pickle.dump(data, file)
        messagebox.showinfo(title="Data Saved", message="Successfully saved your data")

    def load_all(self):
        try:
            with open("save_file.Prgp", "rb") as file:
                data = pickle.load(file)
                self.team_list = data["team_list"]
                self.bank = data["gold"]
        except FileNotFoundError:
            messagebox.showerror(title="Error!", message="Sorry it seems there is no save file to load")
            return
        self.frames["DeletePage"].char_populate()
        self.frames["GroupPage"].display_bank()
        messagebox.showinfo(title="Data Loaded", message="Succesfully loaded your save file")
            
class GroupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="lightgoldenrod1")
        self.bind("<<CurrentBank>>", self.display_bank)

        self.title=tk.Label(self, text="", font=self.controller.font, bg="pale green",
                            borderwidth=2, relief="groove")
        self.display_bank()
        self.title.pack(side="top", pady=10, padx=10)
        self.outer_frame=tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.outer_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.top_frame = tk.Frame(self.outer_frame, bg="pale green")
        self.top_frame.pack(side="top", fill="both", expand=True)

        self.add_button = HomeButton(self.top_frame, self.controller, "Buy New Character", "AddPage")
        self.add_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.delete_button = HomeButton(self.top_frame, self.controller, "Sell Character", "DeletePage")
        self.delete_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.multi_button = HomeButton(self.outer_frame, self.controller, "Play Multiplayer", "MultiplayerPage")
        self.multi_button.pack(side="bottom", padx=5, pady=5, fill="both", expand=True)
        
    def display_bank(self, event=None):
        self.title.config(text="Welcome {}, Money: £{}".format(getuser(), self.controller.bank))
        
class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.counter=0
        self.config(bg="lightgoldenrod1")

        self.title = tk.Button(self, text="Buy a New Character", bg="pale green", font=self.controller.font,
                               borderwidth=2, relief="groove", command=lambda: self.controller.add_character(self.counter))
        self.title.pack(side="top", pady=5, padx=5, expand=True)

        self.left_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.right_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.bottom_frame=tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")

        for x in range(7):
            tk.Label(self.right_frame, text="TEST",
                     font=("Times", 12, "bold"), bg="pale green").pack(anchor="w", pady=5, padx=5)

        self.char_image = tk.PhotoImage(file="")
        self.char_image_label = tk.Label(self.left_frame, image=self.char_image)
        self.char_image_label.image = self.char_image
        self.char_image_label.pack(fill="both", expand=True)

        self.bottom_frame.pack(side="bottom", fill="x", expand=True, pady=5, padx=10)
        self.left_frame.pack(side="left", fill="x", pady=5, padx=10)
        self.right_frame.pack(side="right", fill="both", pady=5, padx=10, expand=True)

        self.right_arrow = tk.Button(self.bottom_frame, width=10, text="→", borderwidth=0,
                                     font=self.controller.font, bg="pale green", command=lambda: self.right_shift())
        self.left_arrow = tk.Button(self.bottom_frame, width=10, text="←", borderwidth=0,
                                    font=self.controller.font, bg="pale green", command=lambda: self.left_shift())
        self.name_plate = tk.Label(self.bottom_frame, text="", font=self.controller.font, bg="pale green")

        self.right_arrow.pack(side="right", pady=5, padx=5)
        self.left_arrow.pack(side="left", pady=5, padx=5)
        self.name_plate.pack(pady=5, padx=5)
        self.stats_populate()

    def stats_populate(self):
        current_char=image_chars[self.counter]
        self.char_image.config(file="imgres/"+current_char.type+".png")
        children=self.right_frame.winfo_children()

        self.name_plate.config(text=current_char.type)
        self.title.config(text="Buy {}, Amount: £{}".format(current_char.type, current_char.amount))

        for data, child  in zip(current_char, children):
            child.config(text="{}{}".format(data[0],data[1]))

    def right_shift(self):
        if self.counter==len(image_chars)-1:
            self.counter=0
        else:
            self.counter+=1
        self.stats_populate()

    def left_shift(self):
        if self.counter==0:
            self.counter=len(image_chars)-1
        else:
            self.counter-=1
        self.stats_populate()

class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="lightgoldenrod1")
        self.bind("<<CharPopulate>>", self.char_populate)

        self.list_frame = FrameScrollBar(self, "top", "right")
        self.list_frame.locate()
        self.char_populate()

    def char_populate(self, event=None):
        children=self.list_frame.inner_frame.winfo_children()
        team_list=self.controller.team_list

        for child in children:
            child.destroy()
        
        for char in team_list:
            temp = DeleteTab(self.list_frame.inner_frame, self.controller, char)
            temp.pack(side="top", fill="x", expand=True)

class MultiplayerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="lightgoldenrod1")
        self.bind("<<UpdateLabel>>", self.update_label)

        self.title_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.title_frame.pack(side="top", padx=10, pady=10, fill="both")

        self.name_label = tk.Label(self.title_frame, text="", font=self.controller.font, bg="pale green")
        self.name_label.pack(side="left", padx=5, pady=5)
        self.outer_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.button_frame = tk.Frame(self.outer_frame, bg="pale green")

        self.outer_frame.pack(side="bottom", padx=10, pady=10, fill="both", expand=True)
        self.button_frame.pack(side="top", padx=10, pady=10)

        self.join_title = tk.Button(self.button_frame, text="Join Game", bg="pale green", borderwidth=2,
                                    relief="groove", font=self.controller.font,
                                    command=lambda: self.create_game("Join"))
        self.join_title.pack(side="left", padx=10, pady=10) 
        self.create_title = tk.Button(self.button_frame, text="Create Game", bg="pale green", borderwidth=2,
                                    relief="groove", font=self.controller.font,
                                    command=lambda: self.create_game("Create"))
        self.create_title.pack(side="right", padx=10, pady=10)

        self.ip_label = PropEntry(self.outer_frame, "Server IP:", "192.168.56.1", ("Times", 16, "bold"))
        self.port_label = PropEntry(self.outer_frame, "Port: ", "5000", ("Times", 16, "bold"))
        self.ip_label.pack(padx=5, pady=10, fill="x")
        self.port_label.pack(padx=5, pady=10, fill="x")

        self.update_label()

    def update_label(self):
        ip_addr = socket.gethostbyname(socket.gethostname())
        self.name_label.config(text="Username: {}, Your IP: {}".format(getuser(), ip_addr))

    def create_game(self, _type):
        try:
            IP = self.ip_label.prop_entry.get()
            PORT = int(self.port_label.prop_entry.get())
            if len(self.controller.team_list) < 1: raise ValueError
        except ValueError:
            messagebox.showerror(title="Bad Entry", message="Please check you have entered the information correctly\n or that you have at least one character in your team")
            return

        if _type == "Join":
            PlayerObject = BattleClientSide(self.controller, IP, PORT)
        else:
            PlayerObject = BattleServerSide(self.controller, IP, PORT)
        self.controller.update_idletasks()

if __name__ == "__main__":
    root = RPGMain()
    root.mainloop()
