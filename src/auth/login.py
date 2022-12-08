from customtkinter import CTk, CTkLabel, CTkEntry, CTkCheckBox, CTkButton, BooleanVar
from assets.logic import center
from assets.ui import Colors, Fonts
from src.auth import signin
from src.app import vault
from os import environ as env
import sqlite3, bcrypt


class Login:
    def __init__(self, window: CTk) -> None:
        self.window = window

        center(350, 450, window)

        self.view()

    def view(self):
        CTkLabel(self.window, text="SECURITY", font=Fonts().BannerFont, text_color=Colors.White, fg_color=Colors.Mirage, height=100).pack(fill="x")

        self.UsernameEntry = CTkEntry(
            self.window, 
            width=250, 
            height=40, 
            fg_color=Colors.White, 
            bg_color=Colors.White, 
            corner_radius=50, 
            placeholder_text="Nom d'utilisateur", 
            font=Fonts().EntryFont, 
            border_color=Colors.Mirage, 
            text_color=Colors.Black)
        self.UsernameEntry.place(x=50, y=130)

        self.PasswordEntry = CTkEntry(
            self.window, 
            width=250, 
            height=40, 
            fg_color=Colors.White, 
            bg_color=Colors.White, 
            corner_radius=50, 
            placeholder_text="Mot de passe", 
            font=Fonts().EntryFont, 
            border_color=Colors.Mirage, 
            show="*", 
            text_color=Colors.Mirage)
        self.PasswordEntry.place(x=50, y=190)

        self.ForgotPasswordButton = CTkButton(
            self.window, 
            text="Mot de passe oublié ?", 
            font=Fonts().EntryFont, 
            fg_color=Colors.White, 
            text_color=Colors.Mirage, 
            bg_color=Colors.White, 
            hover_color=Colors.White, 
            width=140, 
            height=20)
        self.ForgotPasswordButton.place(x=50, y=250)

        self.SessionCheckButton = CTkCheckBox(
            self.window, 
            text='Garder ma session ouverte durant 14 jours', 
            variable=BooleanVar(), 
            font=Fonts().CheckFont, 
            onvalue=True, 
            offvalue=False, 
            text_color=Colors.Mirage, 
            bg_color=Colors.White, 
            border_color=Colors.Mirage, 
            corner_radius=50, 
            width=250, 
            height=40, 
            hover_color=Colors.DarkTeal, 
            fg_color=Colors.Teal)
        self.SessionCheckButton.place(x=50, y=280)

        self.LoginButton = CTkButton(
            self.window, 
            command=self.login, 
            text="Connexion", 
            font=Fonts().ButtonFont, 
            bg_color=Colors.White, 
            fg_color=Colors.Mirage, 
            width=250, 
            height=40, 
            corner_radius=50, 
            hover_color=Colors.DarkTeal)
        self.LoginButton.place(x=50, y=330)

        self.SinginButton = CTkButton(
            self.window, 
            command=lambda: signin.Signin(self.window), 
            text="Créer un compte ?", 
            font=Fonts().EntryFont, 
            fg_color=Colors.White, 
            bg_color=Colors.White, 
            text_color=Colors.Mirage, 
            width=115, 
            height=20, 
            hover_color=Colors.White)
        self.SinginButton.place(x=110, y=380)

        self.UsernameEntry.bind('<Return>', lambda event: self.login())
        self.PasswordEntry.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.UsernameEntry.get()
        passwd = self.PasswordEntry.get()
        try:
            self.AlertLabel.destroy()
        except:
            pass
        if username:
            conn =  sqlite3.connect(env['DB'])
            curr = conn.cursor()
            user = curr.execute("SELECT userId, password FROM 'Users' WHERE username=?", (username,)).fetchone() 
            conn.close()
            
            if user:
                userId, userPassword = user
                if bcrypt.checkpw(bytes(passwd, 'utf-8'), bytes(userPassword, 'utf-8')):
                    env['USERID'] = str(userId)
                    env['USERPASSWORD'] = passwd
                    vault.Vault(self.window)
                    return
                else:
                    self.AlertLabel = CTkLabel(
                        self.window, 
                        text="Mot de passe incorrect!", 
                        fg_color=Colors.Danger, 
                        font=Fonts().ButtonFont,
                        height=40)
            else:
                self.AlertLabel = CTkLabel(
                    self.window, 
                    text="Nom d'utilisateur incorrect!", 
                    fg_color=Colors.Danger, 
                    font=Fonts().ButtonFont,
                    height=40)

            self.AlertLabel.pack(side="bottom", fill="x")
            #self.AlertLabel.place(relwidth=1, y=self.window.winfo_height()-40)

