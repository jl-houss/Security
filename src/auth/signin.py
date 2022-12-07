from customtkinter import CTkLabel, CTkEntry, CTkButton, CTk
from assets.logic import center
from assets.ui import Colors, Fonts
from src.auth import login
from os import environ as env
import sqlite3, bcrypt

class Signin:
    def __init__(self, window: CTk) -> None:
        self.window = window

        center(650, 450, window)

        self.view()

    def view(self):
        self.BannerLabel = CTkLabel(
            self.window, 
            text="Bienvenue dans Security", 
            font=Fonts().BannerFont,  
            fg_color=Colors.Mirage, 
            text_color=Colors.White,
            width=650, 
            height=50)
        self.BannerLabel.pack()

        self.HeaderLabel = CTkLabel(
            self.window, 
            text="Créez votre compte Security",
            font=Fonts().BannerFont, 
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            width=450, 
            height=40)
        self.HeaderLabel.place(x=100, y=95)

        self.UsernameEntry = CTkEntry(
            self.window, 
            width=450, 
            height=40, 
            fg_color=Colors.White, 
            bg_color=Colors.White,  
            corner_radius=50,
            placeholder_text="Choisissez un nom d'utilisateur", 
            font=Fonts().EntryFont, 
            border_color=Colors.Mirage, 
            text_color=Colors.Mirage)
        self.UsernameEntry.place(x=100, y=170)

        self.PasswordEntry = CTkEntry(
            self.window, 
            width=220, 
            height=40, 
            fg_color=Colors.White, 
            bg_color=Colors.White,  
            corner_radius=50,
            placeholder_text="Créez un mot de passe", 
            font=Fonts().EntryFont, 
            border_color=Colors.Mirage, 
            text_color=Colors.Mirage,
            show="*")
        self.PasswordEntry.place(x=100, y=240)

        self.RepeatPasswordEntry = CTkEntry(
            self.window, 
            width=220, 
            height=40, 
            fg_color=Colors.White, 
            bg_color=Colors.White,  
            corner_radius=50,
            placeholder_text="Confirmez le mot de passe", 
            font=Fonts().EntryFont, 
            border_color=Colors.Mirage, 
            text_color=Colors.Mirage,
            show="*")
        self.RepeatPasswordEntry.place(x=330, y=240)

        self.SigninButton = CTkButton(
            self.window, 
            command=self.signin, 
            text="Créer mon compte", 
            font=Fonts().ButtonFont, 
            bg_color=Colors.White, 
            fg_color=Colors.Mirage, 
            width=250, 
            height=40, 
            corner_radius=50, 
            hover_color=Colors.DarkTeal)
        self.SigninButton.place(x=200, y=310)

        self.LoginButton = CTkButton(
            self.window, 
            command=lambda: [login.Login(self.window)], 
            text="j'ai déja un compte", 
            font=Fonts().EntryFont, 
            fg_color=Colors.White, 
            bg_color=Colors.White, 
            text_color=Colors.Mirage, 
            width=130, 
            height=20, 
            hover_color=Colors.White)
        self.LoginButton.place(x=260, y=360)

    def signin(self):
        username = self.UsernameEntry.get()
        password = self.PasswordEntry.get()
        repreatPassword = self.RepeatPasswordEntry.get()
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()
            user = curr.execute("SELECT userId FROM 'Users' WHERE username=?", (username,)).fetchone()
            
            

        if not user:
            errors = self.errors_in_password(password)
            if not errors:
                if password == repreatPassword:
                    password = bcrypt.hashpw(bytes(password, "ascii"), bcrypt.gensalt(14)).decode("ascii")
                    with sqlite3.connect(env['DB']) as conn:
                        curr = conn.cursor()
                        curr.execute("INSERT INTO 'Users' (username, password) VALUES (?, ?)",
                            (username, password))
                        
                        
                    Finish(self.window)
                    return
                else:
                    self.AlertLabel = CTkLabel(
                        self.window, 
                        text="Les mots de passe ne correspondent pas !", 
                        fg_color=Colors.Danger, 
                        font=Fonts().ButtonFont, 
                        height=40)
            else:
                self.AlertLabel = CTkLabel(
                    self.window, 
                    text=errors[0], 
                    fg_color=Colors.Danger, 
                    font=Fonts().ButtonFont,  
                    height=40)
        else:
            self.AlertLabel = CTkLabel(
                self.window, 
                text="L'utilisateur existe déja !", 
                fg_color=Colors.Danger, 
                font=Fonts().ButtonFont, 
                height=40)

        self.AlertLabel.place(relwidth=1, y=self.window.winfo_height()-40)

    def errors_in_password(self, pwd):
        conds = {
            "Le mot de passe doit contenir une lettre majuscule !": lambda s: any(x.isupper() for x in s),
            "Le mot de passe doit contenir une lettre minuscule !": lambda s: any(x.islower() for x in s),
            "Le mot de passe doit contenir un nombre !": lambda s: any(x.isdigit() for x in s),
            "Le mot de passe est trop court !": lambda s: len(s) >= 8
        }

        return [error for error, cond in conds.items() if not cond(pwd)]


class Finish:
    def __init__(self, window) -> None:
        self.window = window

        center(650, 450, window)

        self.view()

    def view(self):
        self.BannerLabel = CTkLabel(
            self.window, 
            text="Bienvenue dans Security", 
            font=Fonts().BannerFont,  
            fg_color=Colors.Mirage, 
            text_color=Colors.White,
            height=50,)
        self.BannerLabel.pack(fill="x")

        self.HeaderLabel = CTkLabel(
            self.window, 
            text="Votre compte a bien été crée !",
            font=Fonts().BannerFont, 
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            height=40)
        self.HeaderLabel.place(x=0, y=95, relwidth=1)

        self.DescLabel = CTkLabel(
            self.window,
            text="Il ne vous reste plus qu’a vous connectez \n a votre compte pour bénéficer de toutes les \n fonctionalités de Security",
            text_color=Colors.Mirage,
            font=Fonts().NavButtonFont,
            fg_color=Colors.White,
            height=70,
            justify="center")
        self.DescLabel.place(x=0, y=155, relwidth=1)

        self.LoginButton = CTkButton(
            self.window, 
            command=lambda: login.Login(self.window), 
            text="Se Connecter", 
            font=Fonts().ButtonFont, 
            bg_color=Colors.White, 
            fg_color=Colors.Mirage, 
            width=250, 
            height=40, 
            corner_radius=50, 
            hover_color=Colors.DarkTeal)
        self.LoginButton.place(x=200, y=300)

        self.AlertLabel = CTkLabel(
            self.window, 
            text="Compte crée avec success !", 
            fg_color=Colors.Success, 
            font=Fonts().ButtonFont, 
            height=40)
        self.AlertLabel.pack(side="bottom", fill="x")