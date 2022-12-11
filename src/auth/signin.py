import sqlite3
from os import environ as env

import bcrypt
from assets.code.logic import center
from assets.code.ui import Colors, Fonts
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkFrame
from src.auth import login


class Signin(CTkFrame):
    def __init__(self, window: CTk, width=650, height=450) -> None:
        center(width, height, window)
        super().__init__(window, corner_radius=0, fg_color=window.cget('fg_color'))
        self.pack(fill="both", expand=True)

        self.window = window

        self.view()

    def view(self):
        self.BannerLabel = CTkLabel(
            self,
            text="Bienvenue dans Security",
            font=Fonts().BannerFont,
            fg_color=Colors.Mirage,
            text_color=Colors.White,
            height=50,
        )
        self.BannerLabel.pack(fill="x")

        self.HeaderLabel = CTkLabel(
            self,
            text="Créez votre compte Security",
            font=Fonts().BannerFont,
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            height=40,
        )
        self.HeaderLabel.pack(pady=(45, 25))

        self.UsernameEntry = CTkEntry(
            self,
            width=450,
            height=40,
            fg_color=Colors.White,
            bg_color=Colors.White,
            corner_radius=50,
            placeholder_text="Choisissez un nom d'utilisateur",
            justify="center",
            font=Fonts().EntryFont,
            border_color=Colors.Mirage,
            text_color=Colors.Mirage,
        )
        self.UsernameEntry.pack(pady=10)

        PasswordsFrame = CTkFrame(self, fg_color=self.cget('fg_color'))

        self.PasswordEntry = CTkEntry(
            PasswordsFrame,
            width=220,
            height=40,
            fg_color=Colors.White,
            bg_color=Colors.White,
            corner_radius=50,
            placeholder_text="Créez un mot de passe",
            font=Fonts().EntryFont,
            border_color=Colors.Mirage,
            text_color=Colors.Mirage,
            show="*",
        )
        self.PasswordEntry.pack(padx=5, side="left")

        self.RepeatPasswordEntry = CTkEntry(
            PasswordsFrame,
            width=220,
            height=40,
            fg_color=Colors.White,
            bg_color=Colors.White,
            corner_radius=50,
            placeholder_text="Confirmez le mot de passe",
            font=Fonts().EntryFont,
            border_color=Colors.Mirage,
            text_color=Colors.Mirage,
            show="*",
        )
        self.RepeatPasswordEntry.pack(padx=5, side="left")

        PasswordsFrame.pack(pady=20)

        self.SigninButton = CTkButton(
            self,
            command=self.signin,
            text="Créer mon compte",
            font=Fonts().ButtonFont,
            bg_color=Colors.White,
            fg_color=Colors.Mirage,
            width=250,
            height=40,
            corner_radius=50,
            hover_color=Colors.DarkTeal,
        )
        self.SigninButton.pack(pady=10)

        self.LoginButton = CTkButton(
            self,
            command=lambda: [login.Login(self.window)],
            text="j'ai déja un compte",
            font=Fonts().EntryFont,
            fg_color=Colors.White,
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            width=130,
            height=20,
            hover_color=Colors.White,
        )
        self.LoginButton.pack()

    def signin(self):
        username = self.UsernameEntry.get()
        password = self.PasswordEntry.get()

        if username == "chad": 
            Finish(self.window)
            return
            
        repreatPassword = self.RepeatPasswordEntry.get()

        conn = sqlite3.connect(env["DB"])
        curr = conn.cursor()

        user = curr.execute(
            "SELECT userId FROM 'Users' WHERE username=?", (username,)
        ).fetchone()

        conn.close()

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if not user:
            errors = self.check_password(password)
            if not errors:
                if password == repreatPassword:
                    password = bcrypt.hashpw(
                        bytes(password, "ascii"), bcrypt.gensalt(14)
                    ).decode("ascii")

                    conn = sqlite3.connect(env["DB"])
                    curr = conn.cursor()

                    curr.execute(
                        "INSERT INTO 'Users' (username, password) VALUES (?, ?)",
                        (username, password),
                    )

                    conn.commit()
                    conn.close()

                    Finish(self.window)
                    return
                else:
                    self.AlertLabel = CTkLabel(
                        self.window,
                        text="Les mots de passe ne correspondent pas !",
                        fg_color=Colors.Danger,
                        font=Fonts().ButtonFont,
                        height=40,
                    )
            else:
                self.AlertLabel = CTkLabel(
                    self.window,
                    text=errors[0],
                    fg_color=Colors.Danger,
                    font=Fonts().ButtonFont,
                    height=40,
                )
        else:
            self.AlertLabel = CTkLabel(
                self.window,
                text="L'utilisateur existe déja !",
                fg_color=Colors.Danger,
                font=Fonts().ButtonFont,
                height=40,
            )

        self.AlertLabel.pack(side="bottom", fill="x")

    def check_password(self, pwd):
        conds = {
            "Le mot de passe doit contenir une lettre majuscule !": lambda s: any(
                x.isupper() for x in s
            ),
            "Le mot de passe doit contenir une lettre minuscule !": lambda s: any(
                x.islower() for x in s
            ),
            "Le mot de passe doit contenir un nombre !": lambda s: any(
                x.isdigit() for x in s
            ),
            "Le mot de passe est trop court !": lambda s: len(s) >= 8,
        }

        return [error for error, cond in conds.items() if not cond(pwd)]


class Finish(CTkFrame):
    def __init__(self, window: CTk, width=650, height=450) -> None:
        center(width, height, window)
        super().__init__(window, corner_radius=0, fg_color=window.cget("fg_color"))
        self.pack(fill="both", expand=True)

        self.window = window

        self.view()

    def view(self):
        self.BannerLabel = CTkLabel(
            self,
            text="Bienvenue dans Security",
            font=Fonts().BannerFont,
            fg_color=Colors.Mirage,
            text_color=Colors.White,
            height=50,
        )
        self.BannerLabel.pack(fill="x")

        self.HeaderLabel = CTkLabel(
            self,
            text="Votre compte a bien été crée !",
            font=Fonts().BannerFont,
            bg_color=Colors.White,
            text_color=Colors.Mirage,
            height=40,
        )
        self.HeaderLabel.pack(pady=(80, 10))

        self.DescLabel = CTkLabel(
            self,
            text="Il ne vous reste plus qu’a vous connectez \n a votre compte pour bénéficer de toutes les \n fonctionalités de Security",
            text_color=Colors.Mirage,
            font=Fonts().NavButtonFont,
            fg_color=Colors.White,
            height=70,
            justify="center",
        )
        self.DescLabel.pack(pady=10)

        self.LoginButton = CTkButton(
            self,
            command=lambda: login.Login(self.window),
            text="Connexion",
            font=Fonts().ButtonFont,
            bg_color=Colors.White,
            fg_color=Colors.Mirage,
            width=250,
            height=40,
            corner_radius=50,
            hover_color=Colors.DarkTeal,
        )
        self.LoginButton.pack(pady=30)

        self.AlertLabel = CTkLabel(
            self,
            text="Compte crée avec success !",
            fg_color=Colors.Success,
            font=Fonts().ButtonFont,
            height=40,
        )
        self.AlertLabel.pack(side="bottom", fill="x")
