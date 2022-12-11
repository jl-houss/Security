import sqlite3
from os import environ as env

import bcrypt
from assets.code.logic import center
from assets.code.ui import Colors, Fonts
from customtkinter import BooleanVar, CTk, CTkButton, CTkCheckBox, CTkEntry, CTkLabel, CTkFrame
from src.app import manager
from src.auth import signin


class Login(CTkFrame):
    def __init__(self, window: CTk, width=350, height=450) -> None:
        center(width, height, window)
        super().__init__(window, corner_radius=0, fg_color=window.cget("fg_color"))
        self.pack(fill="both", expand=True)

        self.window = window

        self.view()

    def view(self):
        CTkLabel(
            self,
            text="SECURITY",
            font=Fonts().BannerFont,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            height=100,
        ).pack(fill="x")

        self.UsernameEntry = CTkEntry(
            self,
            width=250,
            height=40,
            fg_color=Colors.White,
            bg_color=Colors.White,
            corner_radius=50,
            placeholder_text="Nom d'utilisateur",
            justify="center",
            border_width=3,
            font=Fonts().EntryFont,
            border_color=Colors.Mirage,
            text_color=Colors.Black,
        )
        self.UsernameEntry.pack(pady=(30, 10))

        self.PasswordEntry = CTkEntry(
            self,
            width=250,
            height=40,
            fg_color=Colors.White,
            bg_color=Colors.White,
            justify="center",
            corner_radius=50,
            placeholder_text="Mot de passe",
            border_width=3,
            font=Fonts().EntryFont,
            border_color=Colors.Mirage,
            show="*",
            text_color=Colors.Mirage,
        )
        self.PasswordEntry.pack(pady=10)

        self.ForgotPasswordButton = CTkButton(
            self,
            text="Mot de passe oublié ?",
            font=Fonts().EntryFont,
            fg_color=Colors.White,
            text_color=Colors.Mirage,
            bg_color=Colors.White,
            hover_color=Colors.White,
            width=140,
            height=20,
        )
        self.ForgotPasswordButton.pack(padx=50, pady=10)

        self.SessionCheckButton = CTkCheckBox(
            self,
            text="Garder ma session ouverte durant 14 jours",
            variable=BooleanVar(),
            font=Fonts().CheckFont,
            onvalue=True,
            offvalue=False,
            text_color=Colors.Mirage,
            bg_color=Colors.White,
            border_color=Colors.Mirage,
            corner_radius=50,
            width=250,
            height=20,
            hover_color=Colors.DarkTeal,
            fg_color=Colors.Teal,
        )
        self.SessionCheckButton.pack(pady=5)

        self.LoginButton = CTkButton(
            self,
            command=self.login,
            text="Connexion",
            font=Fonts().ButtonFont,
            bg_color=Colors.White,
            fg_color=Colors.Mirage,
            width=250,
            height=40,
            corner_radius=50,
            hover_color=Colors.DarkTeal,
        )
        self.LoginButton.pack(pady=10)

        self.SinginButton = CTkButton(
            self,
            command=lambda: signin.Signin(self.window),
            text="Créer un compte ?",
            font=Fonts().EntryFont,
            fg_color=Colors.White,
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            width=115,
            height=20,
            hover_color=Colors.White,
        )
        self.SinginButton.pack()

        self.UsernameEntry.bind("<Return>", lambda event: self.login())
        self.PasswordEntry.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.UsernameEntry.get()
        passwd = self.PasswordEntry.get()
        try:
            self.AlertLabel.destroy()
        except:
            pass
        if username:
            conn = sqlite3.connect(env["DB"])
            curr = conn.cursor()
            user = curr.execute(
                "SELECT userId, password FROM 'Users' WHERE username=?", (username,)
            ).fetchone()
            conn.close()

            if user:
                userId, userPassword = user
                if bcrypt.checkpw(bytes(passwd, "utf-8"), bytes(userPassword, "utf-8")):
                    env["USERID"] = str(userId)
                    env["USERPASSWORD"] = passwd
                    manager.Manager(self.window)
                    return
                else:
                    self.AlertLabel = CTkLabel(
                        self,
                        text="Mot de passe incorrect!",
                        fg_color=Colors.Danger,
                        font=Fonts().ButtonFont,
                        height=40,
                    )
            else:
                self.AlertLabel = CTkLabel(
                    self,
                    text="Nom d'utilisateur incorrect!",
                    fg_color=Colors.Danger,
                    font=Fonts().ButtonFont,
                    height=40,
                )

            self.AlertLabel.pack(side="bottom", fill="x")
            # self.AlertLabel.place(relwidth=1, y=self.window.winfo_height()-40)
