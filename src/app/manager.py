from assets.code.logic import clear
from assets.code.ui import Colors, Fonts
from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel, W
from src.app import authentifiants


class Navbar(CTkFrame):
    def __init__(self, window: CTk):
        super().__init__(window, width=230, fg_color=Colors.Mirage, corner_radius=0)
        self.pack(side="left", fill="y")

        self.vault = CTkFrame(window, fg_color=window.cget('fg_color'), corner_radius=0)
        self.vault.pack(fill="both", expand=True)

        self.window = window

        self.view()

    def view(self):
        CTkLabel(
            self,
            text="SECURITY",
            font=Fonts().BannerFont,
            bg_color=Colors.Mirage,
            text_color=Colors.White,
            width=230,
            height=80,
        ).pack()

        self.PasswordsButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Mots de passes",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.DarkTeal,
            command=lambda: [
                self.select(self.PasswordsButton),
                authentifiants.Authentifiants(self.window, self.vault),
            ],
            anchor="w",
            height=60,
        )
        self.PasswordsButton.pack(fill="x", pady=(80, 0))

        self.NotesButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Notes sécurisées",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.NotesButton)],
            anchor="w",
            height=60,
        )
        self.NotesButton.pack(fill="x")

        self.PersonalDataButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Données personnelles",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.PersonalDataButton)],
            anchor="w",
            height=60,
        )
        self.PersonalDataButton.pack(fill="x")

        self.PaymentMethodsButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Moyens de paiement",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.PaymentMethodsButton)],
            anchor="w",
            height=60,
        )
        self.PaymentMethodsButton.pack(fill="x")

        self.IdentityPiecesButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Pièces d'identité",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.IdentityPiecesButton)],
            anchor="w",
            height=60,
        )
        self.IdentityPiecesButton.pack(fill="x")

        self.SettingsButton = CTkButton(
            self,
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            text="Paramètres",
            corner_radius=0,
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.SettingsButton)],
            anchor="w",
            height=60
        )
        self.SettingsButton.pack(side="bottom", fill="x")

        self.PasswordsButton.invoke()

    def select(self, button: CTkButton):
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(fg_color=Colors.Mirage)
        button.configure(fg_color=Colors.Teal)

class Manager:
    def __init__(self, window: CTk) -> None:
        self.window = window

        window.resizable(1, 0)
        window.geometry(
            f"{window.winfo_screenwidth()}x{window.winfo_screenheight() - 70}"
        )
        window.state("zoomed")

        clear(window)

        Navbar(window)
