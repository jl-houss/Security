from customtkinter import CTkFont


class Colors:
    # Main Colors
    Mirage      = "#131B23"
    Teal        = "#1D7874"
    
    # Main Colors (Dark)
    DarkMirage  = "#0A1520"
    DarkTeal    = "#176460"

    # Black & White
    White       = "#ffffff"
    Black       = "#333333"

    # Alert Colors
    Success     = "#198754"
    Warning     = "#eed202"
    Danger      = "#FF002D"

    # Alert Colors (Dark)
    DarkDanger  = "#D0342C"

class Fonts:
    def __init__(self) -> None:
        self.EntryFont = CTkFont(family='Roboto', size=15, weight="normal")
        self.ButtonFont = CTkFont(family='Roboto', size=15, weight="bold")
        self.NavButtonFont = CTkFont(family='Roboto', size=20, weight="bold")
        self.BannerFont = CTkFont(family='Roboto', size=35, weight="bold")
        self.CheckFont = CTkFont(family='Roboto', size=12, weight="normal")
        self.TextBoxFont = CTkFont(family='Roboto', size=25, weight="normal")
        self.PopupItemFont = self.EntryFont