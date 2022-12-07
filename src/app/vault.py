from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, W, BOTH
from assets.ui import Colors, Fonts
from assets.logic import clear
from src.app import authentifiants


class Navbar(CTkFrame):
    def __init__(self, window: CTk, vault: CTkFrame):
        super().__init__(window, width=230, fg_color=Colors.Mirage, corner_radius=0)
        self.pack(side="left", fill="y")

        self.window = window
        self.vault = vault

        self.view()
    
    def view(self):
        self.NavbarLabel = CTkLabel(
            self, 
            text="SECURITY", 
            font=Fonts().BannerFont, 
            bg_color=Colors.Mirage, 
            text_color=Colors.White,
            width=230,
            height=80)
        self.NavbarLabel.pack()

        self.NavButtonsFrame = CTkFrame(
            self,
            fg_color=Colors.Mirage)
        self.NavButtonsFrame.place(x=0, y=160, relwidth=1)

        self.PasswordsButton = CTkButton(
            self.NavButtonsFrame, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Mots de passes", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.DarkTeal,
            command=lambda: [self.select(self.PasswordsButton), authentifiants.Authentifiants(self.window, self.vault)], 
            anchor=W,
            height=60)
        self.PasswordsButton.pack(fill="x")

        self.NotesButton = CTkButton(
            self.NavButtonsFrame, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Notes sécurisées", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.NotesButton)], 
            anchor=W,
            height=60)
        self.NotesButton.pack(fill="x")
        
        self.PersonalDataButton = CTkButton(
            self.NavButtonsFrame, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Données personnelles", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.PersonalDataButton)], 
            anchor=W,
            height=60)
        self.PersonalDataButton.pack(fill="x")

        self.PaymentMethodsButton = CTkButton(
            self.NavButtonsFrame, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Moyens de paiement", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.PaymentMethodsButton)], 
            anchor=W,
            height=60)
        self.PaymentMethodsButton.pack(fill="x")

        self.IdentityPiecesButton = CTkButton(
            self.NavButtonsFrame, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Pièces d'identité", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.IdentityPiecesButton)], 
            anchor=W,
            height=60)
        self.IdentityPiecesButton.pack(fill="x")

        self.SettingsButton = CTkButton(
            self, 
            text_color=Colors.White, 
            fg_color=Colors.Mirage,
            text="Paramètres", 
            font=Fonts().NavButtonFont,
            hover_color=Colors.Teal,
            command=lambda: [self.select(self.SettingsButton)], 
            anchor=W,
            height=60)
        self.SettingsButton.pack(side="bottom", fill="x")

        self.PasswordsButton.invoke()

    def select(self, button: CTkButton):
        for widget in self.winfo_children() + self.NavButtonsFrame.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(fg_color=Colors.Mirage)
        button.configure(fg_color=Colors.Teal)

class Vault(CTkFrame):
    def __init__(self, window: CTk) -> None:
        self.window = window

        window.resizable(1, 0)
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight() - 70}")
        window.state("zoomed")

        clear(window)

        super().__init__(window, 
            width=window.winfo_screenwidth()-230,
            corner_radius=0,
            fg_color=Colors.White)
        self.place(x=230, y=0, relheight=1)
        Navbar(window, self)