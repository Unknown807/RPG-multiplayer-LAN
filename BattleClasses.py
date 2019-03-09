import tkinter as tk
from CharClasses import *
from TkCustomClasses import MoveMenu
from multiprocessing.connection import Listener, Client
from tkinter import messagebox
import socket, pickle, sys

class TopLevelArena(tk.Toplevel):
    def __init__(self, controller, IP, PORT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.IP = IP
        self.PORT = PORT
        self.Arenafont = ("Times", 14, "bold")
        self.foe_index=0
        self.ally_index=0
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.geometry("900x700")
        self.title("LAN PvP Battle")
        self.config(bg="lightgoldenrod1")
        self.minsize("900", "700")
        self.maxsize("900", "700")

        self.top_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")
        self.battle_frame = tk.Frame(self, bg="lightgoldenrod1")
        self.battle_frame_l= tk.Frame(self.battle_frame, bg="pale green", borderwidth=2, relief="groove")
        self.battle_frame_r = tk.Frame(self.battle_frame, bg="pale green", borderwidth=2, relief="groove")
        self.bottom_frame = tk.Frame(self, bg="pale green", borderwidth=2, relief="groove")

        self.top_frame.pack(padx=10, pady=5, fill="both")
        self.battle_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.battle_frame_l.pack(side="left", padx=10, pady=5)
        self.battle_frame_r.pack(side="right", padx=10, pady=5)
        self.bottom_frame.pack(padx=10, pady=5, fill="both")

        self.ally_profile = tk.PhotoImage(file="")
        self.ally_profile_label = tk.Label(self.battle_frame_l, image=self.ally_profile)
        self.ally_profile_label.image = self.ally_profile
        self.ally_profile_label.pack(side="left", padx=5, pady=5)

        self.foe_profile = tk.PhotoImage(file="")
        self.foe_profile_label = tk.Label(self.battle_frame_r, image=self.foe_profile)
        self.foe_profile_label.image = self.foe_profile
        self.foe_profile_label.pack(side="right", padx=5, pady=5)

        self.ally_frame = tk.Frame(self.top_frame, bg="pale green")
        self.ally_frame_top = tk.Frame(self.ally_frame, bg="pale green")
        self.ally_frame_bottom = tk.Frame(self.ally_frame, bg="pale green")

        self.foe_frame = tk.Frame(self.top_frame, bg="pale green")
        self.foe_frame_top = tk.Frame(self.foe_frame, bg="pale green")
        self.foe_frame_bottom = tk.Frame(self.foe_frame, bg="pale green")

        self.ally_frame.pack(side="left", padx=5, pady=1, fill="both")
        self.ally_frame_top.pack(side="top", padx=5, pady=1, fill="both", expand=True)
        self.ally_frame_bottom.pack(side="bottom", padx=5, pady=1, fill="both", expand=True)
        
        self.foe_frame.pack(side="right", padx=5, pady=1, fill="both")
        self.foe_frame_top.pack(side="top", padx=5, pady=1, fill="both", expand=True)
        self.foe_frame_bottom.pack(side="bottom", padx=5, pady=1, fill="both", expand=True)

        self.ally_name = tk.Label(self.ally_frame_top, text="MYNAME", bg="pale green", font=self.Arenafont)
        self.ally_cooldown = tk.Label(self.ally_frame_top, text="Cooldown: 0", bg="pale green", font=self.Arenafont)
        self.ally_health = tk.Label(self.ally_frame_bottom, text="Health: 100", bg="pale green", font=self.Arenafont)
        self.ally_mana = tk.Label(self.ally_frame_bottom, text="Mana: 100", bg="pale green", font=self.Arenafont)

        self.ally_name.pack(side="left", padx=3, pady=1, fill="x")
        self.ally_cooldown.pack(side="left", padx=3, pady=1, fill="x")
        self.ally_health.pack(side="left", padx=3, pady=1, fill="x")
        self.ally_mana.pack(side="left", padx=3, pady=1, fill="x")

        self.vs_label = tk.Label(self.top_frame, text="VS", bg="pale green", font=self.controller.font)
        self.vs_label.pack(padx=1, pady=1, fill="both", expand=True)

        self.foe_name = tk.Label(self.foe_frame_top, text="FOENAME", bg="pale green", font=self.Arenafont)
        self.foe_cooldown = tk.Label(self.foe_frame_top, text="Cooldown: 0", bg="pale green", font=self.Arenafont)
        self.foe_health = tk.Label(self.foe_frame_bottom, text="Health: 100", bg="pale green", font=self.Arenafont)
        self.foe_mana = tk.Label(self.foe_frame_bottom, text="Mana: 100", bg="pale green", font=self.Arenafont)

        self.foe_name.pack(side="left", padx=3, pady=1, fill="x")
        self.foe_cooldown.pack(side="left", padx=3, pady=1, fill="x")
        self.foe_health.pack(side="left", padx=3, pady=1, fill="x")
        self.foe_mana.pack(side="left", padx=3, pady=1, fill="x")

        self.attack_button = tk.Button(self.bottom_frame, text="Attack", bg="pale green",borderwidth=2,
                                       relief="groove", font=self.Arenafont, command=self.execute_attack)
        self.quit_button = tk.Button(self.bottom_frame, text="Concede", bg="pale green", borderwidth=2,
                                     relief="groove", font=self.Arenafont, command=self.quit_game)
        self.spells_menu = MoveMenu(self.bottom_frame, "Spells")
        self.special_menu = MoveMenu(self.bottom_frame, "Specials")
        self.buffs_menu = MoveMenu(self.bottom_frame, "Buffs")

        self.attack_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.spells_menu.locate()
        self.buffs_menu.locate()
        self.special_menu.locate()
        self.quit_button.pack(side="left", padx=5, pady=5, fill="both", expand=True)

    def initiate_fields(self, enemy_list):
        self.enemy_list = enemy_list
        self.ally_list = self.controller.team_list

        self.foe_name.config(text=self.enemy_list[0].name)
        self.foe_health.config(text="Health: {:03}".format(self.enemy_list[0].health))
        self.foe_mana.config(text="Mana: {:03}".format(self.enemy_list[0].mana))

        self.ally_profile.config(file="imgres/"+self.ally_list[0].type+".png")
        self.foe_profile.config(file="imgres/"+self.enemy_list[0].type+"_flip.png")

        self.ally_name.config(text=self.ally_list[0].name)
        self.ally_health.config(text="Health: {:03}".format(self.ally_list[0].health))
        self.ally_mana.config(text="Mana: {:03}".format(self.ally_list[0].mana))
        self.currentAlly = self.ally_list[0]
        self.multiplier = self.currentAlly.multiplier
        
        for spell in self.ally_list[0].spells:
            self.spells_menu.add_entry(spell, self.execute_spell)

        for special in self.ally_list[0].specials:
            self.special_menu.add_entry(special, self.execute_special)

        for buff in self.ally_list[0].buffs:
            self.buffs_menu.add_entry(buff, self.execute_buff)

    def construct_data(self, keys, vals):
        send_dict = {}
        for key, val in zip(keys, vals):
            send_dict[key] = val
        return send_dict

    def cooldown_check(self):
        foe_cooldown = int(self.foe_cooldown.cget("text").split(" ")[1])
        ally_cooldown = int(self.ally_cooldown.cget("text").split(" ")[1])
        if foe_cooldown > 0:
            self.foe_cooldown.config(text="Cooldown: {}".format(foe_cooldown-1))
        if ally_cooldown > 0:
            self.ally_cooldown.config(text="Cooldown: {}".format(ally_cooldown-1))

    def execute_buff(self, buff):
        old_mana = int(self.ally_mana.cget("text").split(" ")[1])
        old_health = int(self.ally_health.cget("text").split(" ")[1])
        if buff[-1] == "Heal":
            if buff[2]>old_mana:
                messagebox.showwarning(title="Not Enough!", message="You need more mana to cast that buff")
                return
            yourmessage = "You cast the buff {}, restoring {} health, with a multiplier of x{}".format(buff[0], buff[1], self.multiplier)
            messagebox.showinfo(title="Buff Performed!", message=yourmessage)
            send_message = "{} used the buff {}, healing himself for {} health".format(self.currentAlly.name, buff[0], buff[1])
            new_mana = old_mana - buff[2]
            new_health = old_health + buff[1]
            new_health = new_health if new_health <= self.currentAlly.health else self.currentAlly.health
            
        elif buff[-1] == "Mana":
            if buff[2]>=old_health:
                messagebox.showwarning(title="Not Enough!", message="You need more health to cast that buff")
                return
            yourmessage = "You cast the buff {}, restoring {} mana, with a multiplier of x{}".format(buff[0], buff[1], self.multiplier)
            messagebox.showinfo(title="Buff Performed!", message=yourmessage)
            send_message = "{} used the buff {}, recovering {} mana".format(self.currentAlly.name, buff[0], buff[1])
            new_mana = old_mana + buff[1]
            new_mana = new_mana if new_mana <= self.currentAlly.mana else self.currentAlly.mana
            new_health = old_health - buff[2]
            
        elif buff[-1] == "MultM":
            if buff[2]>old_mana:
                messagebox.showwarning(title="Not Enough!", message="You need more mana to cast that buff")
                return
            yourmessage = "You cast the buff {}, boosting your multiplier by {}".format(buff[0], buff[1])
            messagebox.showinfo(title="Buff Performed!", message=yourmessage)
            send_message = "{} used the buff {}, boosting their multiplier by {}".format(self.currentAlly.name, buff[0], buff[1])
            self.multiplier += buff[1]
            new_mana = old_mana - buff[2]
            new_health = old_health
            
        elif buff[-1] == "MultH":
            if buff[2]>=old_health:
                messagebox.showwarning(title="Not Enough!", message="You need more health to cast that buff")
                return
            yourmessage = "You cast the buff {}, boosting your multiplier by {}".format(buff[0], buff[1])
            messagebox.showinfo(title="Buff Performed!", message=yourmessage)
            send_message = "{} used the buff {}, boosting their multiplier by {}".format(self.currentAlly.name, buff[0], buff[1])
            self.multiplier += buff[1]
            new_health = old_health - buff[2]
            new_mana = old_mana

        self.ally_health.config(text="Health: {:03}".format(new_health))
        self.ally_mana.config(text="Mana: {:03}".format(new_mana))

        keys = ("type", "message", "foemana", "foehealth")
        vals = ("buff", send_message, new_mana, new_health)
        try:
            sendData = pickle.dumps(self.construct_data(keys, vals))
            self.sock.send_bytes(sendData)
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(title="Disconnected", message="It seems like your opponent disconnected from the game")
            self.destroy()
            return
        
        self.check_data_type()

    def get_buff(self, response):
        self.foe_health.config(text="Health: {:03}".format(response["foehealth"]))
        self.foe_mana.config(text="Mana: {:03}".format(response["foemana"]))
        messagebox.showinfo(title="Buff Performed!", message=response["message"])

    def execute_spell(self, spell):
        old_mana = int(self.ally_mana.cget("text").split(" ")[1])
        if spell[2]>old_mana:
            messagebox.showwarning(title="Not Enough!", message="You need more mana to cast that spell")
            return
        
        new_mana = old_mana - spell[2]
        damage = self.multiplier * spell[1]
        foe_health = int(self.foe_health.cget("text").split(" ")[1]) - damage
        
        self.foe_health.config(text="Health: {:03}".format(foe_health))
        self.ally_mana.config(text="Mana: {:03}".format(new_mana))
        yourmessage = "You cast the spell {}, dealing {} damage to your foe with a multiplier of x{}".format(spell[0], damage, self.multiplier)
        messagebox.showinfo(title="Spell Cast!", message=yourmessage)
        send_message = "{} used the spell {}, dealing {} damage to you with a multiplier of x{}".format(self.currentAlly.name,
                                                                          spell[0], damage, self.multiplier)
        keys = ("type", "message", "damage", "foemana")
        vals = ("spell", send_message, damage, new_mana)
        try:
            sendData = pickle.dumps(self.construct_data(keys, vals))
            self.sock.send_bytes(sendData)
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(title="Disconnected", message="It seems like your opponent disconnected from the game")
            self.destroy()
            return
        self.switch_foe(foe_health)
        self.multiplier = self.currentAlly.multiplier
        self.check_data_type()

    def get_spell(self, response):
        old_health = int(self.ally_health.cget("text").split(" ")[1])

        new_health = old_health - response["damage"]
        self.ally_health.config(text="Health: {:03}".format(new_health))
        self.foe_mana.config(text="Mana: {:03}".format(response["foemana"]))
        
        messagebox.showinfo(title="Spell Cast!", message=response["message"])

    def execute_special(self, sp):
        current_cool = int(self.ally_cooldown.cget("text").split(" ")[1])
        if current_cool > 0:
            messagebox.showwarning(title="Cooldown!", message="You need to wait a few turns before you can use that ability")
            return

        damage = self.multiplier * sp[1]
        foe_health = int(self.foe_health.cget("text").split(" ")[1]) - damage
        new_cooldown = current_cool + sp[2]

        self.ally_cooldown.config(text="Cooldown: {}".format(new_cooldown))
        self.foe_health.config(text="Health: {:03}".format(foe_health))

        yourmessage = "You evoked the special {}, dealing {} damage to your foe with a multiplier of x{}".format(sp[0], damage, self.multiplier)
        messagebox.showinfo(title="Special Evoked!", message=yourmessage)
        send_message = "{} used the special {}, dealing {} damage to you with a multiplier of x{}".format(self.currentAlly.name,
                                                                                 sp[0], damage, self.multiplier)
        keys = ("type", "message", "damage", "foecooldown")
        vals = ("special", send_message, damage, new_cooldown)
        try:
            sendData = pickle.dumps(self.construct_data(keys, vals))
            self.sock.send_bytes(sendData)
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(title="Disconnected", message="It seems like your opponent disconnected from the game")
            self.destroy()
            return
        self.switch_foe(foe_health)
        self.multiplier = self.currentAlly.multiplier
        self.check_data_type()

    def get_special(self, response):
        old_health = int(self.ally_health.cget("text").split(" ")[1])

        new_health = old_health - response["damage"]
        self.ally_health.config(text="Health: {:03}".format(new_health))
        self.foe_cooldown.config(text="Cooldown: {}".format(response["foecooldown"]))

        messagebox.showinfo(title="Special Evoked!", message=response["message"])
        
    def execute_attack(self):
        damage = self.multiplier * self.currentAlly.attack
        foe_health = int(self.foe_health.cget("text").split(" ")[1]) - damage
        self.foe_health.config(text="Health: {:03}".format(foe_health))

        yourmessage = "You attacked, dealing {} damage to your foe with a multiplier of x{}".format(damage, self.multiplier)
        messagebox.showinfo(title="Melee Attack!", message=yourmessage)
        send_message = "{} used an attack, dealing {} damage to you with a multiplier of x{}".format(self.currentAlly.name,
                                                                                    damage, self.multiplier)
        keys = ("type", "message", "damage")
        vals = ("attack", send_message, damage)
        try:
            sendData = pickle.dumps(self.construct_data(keys, vals))
            self.sock.send_bytes(sendData)
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(title="Disconnected", message="It seems like your opponent disconnected from the game")
            self.destroy()
            return
        self.switch_foe(foe_health)
        self.multiplier = self.currentAlly.multiplier
        self.check_data_type()

    def get_attack(self, response):
        old_health = int(self.ally_health.cget("text").split(" ")[1])

        new_health = old_health - response["damage"]
        self.ally_health.config(text="Health: {:03}".format(new_health))

        messagebox.showinfo(title="Melee Attack!", message=response["message"])

    def quit_game(self):
        messagebox.showinfo(title="Conceded!", message="You quit the game")
        self.controller.upgrade_team_loss()
        keys = ("type",)
        vals = ("quit",)
        sendData = pickle.dumps(self.construct_data(keys, vals))
        self.sock.send_bytes(sendData)
        self.destroy()
        self.sock.close()

    def get_quit(self):
        messagebox.showinfo(title="Conceded!", message="Your opponent quit the game")
        enemy_total_level = sum((enemy.lvl for enemy in self.enemy_list))//len(self.enemy_list)
        self.controller.upgrade_team(enemy_total_level)
        self.sock.close()
        self.destroy()
    
    def check_data_type(self):
        try:
            response = pickle.loads(self.sock.recv_bytes())
        except (EOFError, ConnectionAbortedError, ConnectionResetError):
            self.destroy()
            return
        
        move = response["type"]
        if move == "spell":
            self.get_spell(response)
            self.cooldown_check()
        elif move == "special":
            self.get_special(response)
        elif move == "buff":
            self.get_buff(response)
            self.cooldown_check()
        elif move == "attack":
            self.get_attack(response)
            self.cooldown_check()
        elif move == "quit":
            self.get_quit()
            return
            
        self.switch_ally()

    def switch_foe(self, foe_health):
        if foe_health >= 1:
            return
        
        self.foe_index+=1
        if self.foe_index > len(self.enemy_list)-1:
            self.victory()
            return
        
        self.foe_profile.config(file="imgres/"+self.enemy_list[self.foe_index].type+"_flip.png")
        self.foe_name.config(text=self.enemy_list[self.foe_index].name)
        self.foe_health.config(text="Health: {:03}".format(self.enemy_list[self.foe_index].health))
        self.foe_mana.config(text="Mana: {:03}".format(self.enemy_list[self.foe_index].mana))
        self.foe_cooldown.config(text="Cooldown: 0")

    def switch_ally(self):
        ally_health = int(self.ally_health.cget("text").split(" ")[1])
        if ally_health >= 1:
            return
        
        self.ally_index+=1
        if self.ally_index > len(self.ally_list)-1:
            self.gameover()
            return

        self.currentAlly = self.ally_list[self.ally_index]
        self.multiplier = self.currentAlly.multiplier
        self.ally_profile.config(file="imgres/"+self.ally_list[self.ally_index].type+".png")
        self.ally_name.config(text=self.ally_list[self.ally_index].name)
        self.ally_health.config(text="Health: {:03}".format(self.ally_list[self.ally_index].health))
        self.ally_mana.config(text="Mana: {:03}".format(self.ally_list[self.ally_index].mana))
        self.ally_cooldown.config(text="Cooldown: 0")
        
        self.spells_menu.remove_all()
        self.special_menu.remove_all()
        self.buffs_menu.remove_all()
                
        for spell in self.ally_list[self.ally_index].spells:
            self.spells_menu.add_entry(spell, self.execute_spell)

        for special in self.ally_list[self.ally_index].specials:
            self.special_menu.add_entry(special, self.execute_special)

        for buff in self.ally_list[self.ally_index].buffs:
            self.buffs_menu.add_entry(buff, self.execute_buff)

    def gameover(self):
        messagebox.showinfo(title="Defeat", message="You failed!")
        self.sock.close()
        self.controller.upgrade_team_loss()
        self.destroy()

    def victory(self):
        messagebox.showinfo(title="Victory!", message="You won!")
        enemy_total_level = sum((enemy.lvl for enemy in self.enemy_list))//len(self.enemy_list)
        self.controller.upgrade_team(enemy_total_level)
        self.destroy()

    def on_closing(self):
        pass
    
class BattleClientSide(TopLevelArena):
    def __init__(self, controller, IP, PORT):
        super().__init__(controller, IP, PORT)
        self.controller = controller
        self.startbox=True

        self.startClient()
            
        if self.startbox:
            messagebox.showinfo(title="Begin!", message="You start first")
            self.transient(self.controller)
            self.grab_set()
            self.controller.wait_window(self)

    def startClient(self):
        try:
            self.sock = Client((self.IP, self.PORT))
        except ConnectionRefusedError:
            self.destroy()
            self.startbox=False
            messagebox.showerror(title="Bad Connection", message="There is currently no game to join")
            return

        sendData = pickle.dumps(self.controller.team_list)
        self.sock.send_bytes(sendData)
        rcvdData = pickle.loads(self.sock.recv_bytes())
        self.initiate_fields(rcvdData)

class BattleServerSide(TopLevelArena):
    def __init__(self, controller, IP, PORT):
        super().__init__(controller, IP, PORT)
        self.controller = controller

        try:
            self.startServer()
            messagebox.showinfo(title="Wait!", message="Please wait for your opponent to make a move")
            self.check_data_type()        
            self.transient(self.controller)
            self.grab_set()
            self.controller.wait_window(self)
        except Exception:
            pass

    def startServer(self):
        listener = Listener((self.IP, self.PORT))
        self.sock = listener.accept()
        rcvdData = pickle.loads(self.sock.recv_bytes())
        sendData = pickle.dumps(self.controller.team_list)
        self.sock.send_bytes(sendData)
        self.initiate_fields(rcvdData)

