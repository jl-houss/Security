import webbrowser
from customtkinter import CTk, CTkFrame, CTkButton, CTkEntry, CTkScrollbar, W, CENTER, NO, E, CTkToplevel, CTkLabel, StringVar, CTkProgressBar, IntVar, CTkSlider, CTkCheckBox, BooleanVar
from tkinter.ttk import Style, Treeview
from tkinter import Event, Menu
from assets.ui import Colors, Fonts
from assets.logic import clear, center, password_decrypt, password_encrypt
from os import environ as env
import sqlite3
from password_strength import PasswordStats
from win10toast import ToastNotifier
import pyperclip
from random import choice
import string


class Authentifiant:
    def __init__(self, authId, parentId, title, domain, login, email, password, category, note) -> None:
        self.authId = authId
        self.parentId = parentId
        self.title = title
        self.domain = domain
        self.login = login
        self.email = email
        self.password = password
        self.category = category
        self.note = note

    def check(self, search):
        return any(map(lambda x: search in x, [self.title, self.domain, self.login, self.email, self.category]))

    def update(self):
        pass

    def delete(self):
        pass

class Authentifiants:
    def __init__(self, window: CTk, vault: CTkFrame):
        clear(vault)
        
        self.window = window
        self.vault = vault

        self.view()

    def view(self):
        self.AddButton = CTkButton(
            self.vault, 
            text="Ajouter", 
            fg_color=Colors.Teal, 
            text_color=Colors.White, 
            font=Fonts().ButtonFont,
            hover_color=Colors.DarkTeal,
            width=150,
            height=40)
        self.AddButton.place(x=40,y=20)

        self.GenerateButton = CTkButton(
            self.vault, 
            text="Générer un mot de passe",
            command=lambda: GeneratePassword(self.window),
            hover_color=Colors.DarkTeal,
            fg_color=Colors.Mirage, 
            text_color=Colors.White, 
            font=Fonts().ButtonFont,
            width=200,
            height=40)
        self.GenerateButton.place(x=210, y=20)

        self.ExportButton = CTkButton(
            self.vault, 
            text="Exporter", 
            fg_color=Colors.White, 
            text_color=Colors.Mirage,
            border_width=2,
            hover_color=Colors.DarkTeal,
            border_color=Colors.Mirage,
            font=Fonts().ButtonFont,
            width=150,
            height=40)
        self.ExportButton.place(x=430, y=20)

        self.DeleteButton = CTkButton(
            self.vault, 
            text="Supprimer cet identifiant", 
            bg_color=Colors.White,
            fg_color=Colors.Danger, 
            text_color=Colors.White,
            font=Fonts().ButtonFont, 
            command=lambda: self.delete(),
            hover_color=Colors.DarkDanger,
            width=230, 
            height=40)
        self.DeleteButton.place(x=430+20+150, y=20)

        self.AuthTable = AuthentifiantsTable(self)
        self.AuthTable.place(x=40, y=100, width=self.vault.winfo_width() - 40, height=self.vault.winfo_height() - 100)

    def delete(self):
        with sqlite3.connect(env['DB']) as conn:
            selected = self.AuthTable.Table.item(self.AuthTable.Table.selection()[0])
            curr = conn.cursor()
            curr.execute("DELETE FROM 'Authentifiants' WHERE authId=?", (selected['tags'][0],))
            conn.commit()
            
        self.AuthTable.search()

class AuthentifiantsTable(CTkFrame):
    def __init__(self, page: Authentifiants):
        super().__init__(page.vault)
        self.page = page
        self.vault = page.vault

        self.style = Style()

        self.style.configure(
            "Treeview",       
            rowheight=50,
            font=Fonts().EntryFont
        )

        self.style.configure(
            'Treeview.Heading',
            foreground=Colors.Teal,
            font=Fonts().NavButtonFont
            )
            
        self.style.configure(
            'Treeview.Cell', 
            foreground="red")

        self.style.map(
            "Treeview",
            background=[('selected', Colors.Teal)]
        )

        self.view()

    def view(self):
        self.SearchEntry = CTkEntry(
            self,
            height=30,
            fg_color=Colors.White,
            bg_color=Colors.Mirage,
            font=Fonts().EntryFont,
            placeholder_text="Rechercher...",
            text_color=Colors.Black)
        self.SearchEntry.pack(fill="x")

        self.TableScroll = CTkScrollbar(
            self,
            width=15,
            corner_radius=0,
            fg_color=Colors.Mirage,
            orientation="vertical",
            button_color=Colors.Teal,
            button_hover_color=Colors.DarkTeal)
        self.TableScroll.pack(fill="y", side="right")

        self.Table = Treeview(self, yscrollcommand=self.TableScroll.set)

        self.TableScroll.configure(command=self.Table.yview)

        self.Table['columns'] = ("Title", "Login", "Category", "Website", "Actions")

        self.Table.column("#0", anchor=W, width=0, stretch=NO)
        self.Table.column("Title", anchor=W, width=200)
        self.Table.column("Login", anchor=W, width=280)
        self.Table.column("Category", anchor=W, width=150)
        self.Table.column("Website", anchor=E, width=250)
        self.Table.column("Actions", anchor=CENTER, width=55)

        self.Table.heading("#0", text="", anchor=W)
        self.Table.heading("Title", text="Nom", anchor=W)
        self.Table.heading("Login", text="", anchor=W)
        self.Table.heading("Category", text="Catégorie", anchor=W)
        self.Table.heading("Website", text="", anchor=CENTER)
        self.Table.heading("Actions", text="", anchor=CENTER)

        self.Table.place(x=0, y=30, height=self.vault.winfo_height() - 100, width=self.vault.winfo_width() - 55)           

        # Bindings
        self.Table.bind("<Double-1>", lambda event: self.action(event, "<Double-1>"))
        self.Table.bind("<Button-1>", lambda event: self.action(event, "<Button-1>"))
        self.Table.bind("<Button-3>", lambda event: self.action(event, "<Button-3>"))

        self.vault.bind("<Button-1>", lambda event: self.Table.selection_remove(*self.Table.selection()))

        self.SearchEntry.bind("<KeyRelease>", lambda event: self.search())

        #default invoke
        self.search()

    def search(self):
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()
            records = curr.execute(f"SELECT * FROM 'Authentifiants' WHERE parentId = ?", (env['USERID'])).fetchall()
            conn.commit()
            
        self.Table.delete(*self.Table.get_children())

        for i, record in enumerate(records):
            auth = Authentifiant(*record)
            if auth.check(self.SearchEntry.get()):
                values = (auth.title, auth.login if auth.login else auth.email, auth.category, "", "...")
                self.Table.insert(parent="", index="end", iid=i, values=values, tags=[auth.authId, auth.domain])

    def action(self, event: Event, action: str):
        region = self.Table.identify("region", event.x, event.y)
        if action == "<Double-1>":
            if region == "cell" and event.x >= 718 and event.x < 996:
                selected = self.Table.item(self.Table.selection()[0])
                tags = selected['tags']
                webbrowser.open("https://www." + tags[1])
            else:
                selected = self.Table.item(self.Table.selection()[0])
                tags = selected['tags']
                #ModifyPassword(self.master, tags[0], self.Table)
        elif region == "cell" and ((action == "<Button-1>" and event.x >= 996) or action == "<Button-3>"):
            row = self.Table.identify_row(event.y)
            tags = self.Table.item(row, 'tags')
            ActionPopup(self.page, event.x, event.y, tags)


class GeneratePassword(CTkToplevel):
    def __init__(self, window) -> None:
        super().__init__(window, fg_color=Colors.White)
        self.resizable(0, 0)
        self.title("Générateur de mots de passe")
        center(500, 600, self)

        self.window = window
        
        self.view()

    def view(self):
        self.BannerLabel = CTkLabel(
            self, 
            text="Générer un mot de passe", 
            font=Fonts().BannerFont, 
            justify='center', 
            text_color=Colors.White,
            fg_color=Colors.Mirage,
            height=150)
        self.BannerLabel.pack(fill="x")
        
        self.PasswordBox = CTkEntry(
            self,
            bg_color=Colors.White,
            fg_color=Colors.White,
            font=Fonts().TextBoxFont,
            text_color=Colors.Mirage,
            corner_radius=20,
            border_color=Colors.Mirage,
            border_width=3,
            state="disabled",
            width=400,
            height=50)
        self.PasswordBox.place(x=50, y=200)

        self.SecurityProgress = CTkProgressBar(
            self,
            width=380,
            height=10,
            border_color=Colors.Mirage,
            border_width=2,
            fg_color=Colors.Mirage,
            bg_color=Colors.White,
            progress_color=Colors.Teal,
            corner_radius=10,
        )
        self.SecurityProgress.place(x=60, y=270)

        self.SecurityLevel = CTkLabel(
            self,
            font=Fonts().NavButtonFont,
            text="Tres sécurisé !",
            text_color=Colors.Mirage,
            height=25
        )
        self.SecurityLevel.place(x=0, y=305, relwidth=1)

        self.LengthSlider = CTkSlider(
            self,
            width=380,
            height=15,
            corner_radius=10,
            number_of_steps=25,
            fg_color=Colors.Mirage,
            bg_color=Colors.White,
            progress_color=Colors.Teal,
            button_color=Colors.Teal,
            button_hover_color=Colors.Teal,
            button_corner_radius=50,
            from_=5,
            to=30,
            variable=IntVar()
        )
        self.LengthSlider.place(x=60, y=360)
        self.LengthSlider.set(12)

        self.minLength = CTkLabel(
            self,
            font=Fonts().EntryFont,
            text="5",
            text_color=Colors.Mirage,
            width=8,
            height=16
        )
        self.minLength.place(x=56, y=380)

        self.LengthBox = CTkEntry(
            self,
            bg_color=Colors.White,
            fg_color=Colors.White,
            font=Fonts().EntryFont,
            text_color=Colors.Mirage,
            corner_radius=20,
            border_color=Colors.Mirage,
            border_width=3,
            textvariable=StringVar(value="12"),
            state="disabled",
            width=50,
            height=30)
        self.LengthBox.place(x=225, y=375)

        self.maxLength = CTkLabel(
            self,
            font=Fonts().EntryFont,
            text="30",
            text_color=Colors.Mirage,
            width=16,
            height=16
        )
        self.maxLength.place(x=430, y=380)

        self.UpperCheck = CTkCheckBox(
            self, 
            text='Majuscules (p. ex. AB)', 
            variable=BooleanVar(), 
            font=Fonts().EntryFont, 
            onvalue=False, 
            offvalue=True,
            text_color=Colors.Mirage, 
            bg_color=Colors.White, 
            border_color=Colors.Mirage, 
            corner_radius=5, 
            width=170, 
            height=30, 
            hover_color=Colors.Teal, 
            fg_color=Colors.Teal)
        self.UpperCheck.place(x=50, y=420)

        self.NumbersCheck = CTkCheckBox(
            self, 
            text='Chiffres (p. ex. 123)', 
            variable=BooleanVar(), 
            font=Fonts().EntryFont, 
            onvalue=False, 
            offvalue=True,
            text_color=Colors.Mirage, 
            bg_color=Colors.White, 
            border_color=Colors.Mirage, 
            corner_radius=5, 
            width=170, 
            height=30, 
            hover_color=Colors.Teal, 
            fg_color=Colors.Teal)
        self.NumbersCheck.place(x=50, y=450)

        self.SymbolsCheck = CTkCheckBox(
            self, 
            text='Symboles (p. ex. @!$)', 
            variable=BooleanVar(), 
            font=Fonts().EntryFont, 
            onvalue=False, 
            offvalue=True, 
            text_color=Colors.Mirage, 
            bg_color=Colors.White, 
            border_color=Colors.Mirage, 
            corner_radius=5, 
            width=170, 
            height=30, 
            hover_color=Colors.Teal, 
            fg_color=Colors.Teal)
        self.SymbolsCheck.place(x=50, y=480)

        self.GenerateButton = CTkButton(
            self, 
            command=self.generate,
            text="Générer", 
            fg_color=Colors.Teal, 
            text_color=Colors.White, 
            font=Fonts().ButtonFont,
            hover_color=Colors.Mirage,
            width=90,
            height=40)
        self.GenerateButton.place(x=390, y=540)

        self.CopyButton = CTkButton(
            self, 
            text="Copier", 
            fg_color=Colors.Mirage, 
            command=self.copy_generation,
            text_color=Colors.White, 
            font=Fonts().ButtonFont,
            hover_color=Colors.Teal,
            width=90,
            height=40)
        self.CopyButton.place(x=285, y=540)

        self.CancelButton = CTkButton(
            self, 
            text="Annuler", 
            fg_color=Colors.White, 
            text_color=Colors.Mirage,
            border_width=2,
            border_color=Colors.Mirage, 
            font=Fonts().ButtonFont,
            hover_color=Colors.Teal,
            width=80,
            height=40,
            command=lambda: [self.destroy()])
        self.CancelButton.place(x=190, y=540)

        #Bindings
        self.bind('<Return>', lambda event: self.generate())
        self.LengthSlider.bind('<ButtonRelease-1>', lambda event: [self.LengthBox.configure(textvariable=StringVar(value=int(self.LengthSlider.get()))), self.generate()])

        #Init invoke
        self.GenerateButton.invoke()

    def generate(self):
        if not self.UpperCheck.get():
            all_chars = string.ascii_letters
        else:
            all_chars = string.ascii_letters.lower()

        if not self.NumbersCheck.get():
            all_chars += string.digits

        if not self.SymbolsCheck.get():
            all_chars += string.punctuation

        self.password = "".join(choice(all_chars) for i in range(int(self.LengthSlider.get())))
        strength = PasswordStats(self.password).strength()
        self.SecurityProgress.set(strength)
        if strength > 0.6:
            strength = {"text": "Tres fort !", "color": Colors.Success}
        elif strength > 0.4:
            strength = {"text": "Fort !", "color": Colors.Success}
        elif strength > 0.2:
            strength = {"text": "Moyen !", "color": Colors.Warning}
        else:
            strength = {"text": "Faible !", "color": Colors.Danger}

        self.PasswordBox.configure(textvariable=StringVar(value=self.password))
        self.SecurityLevel.configure(text=strength['text'], text_color=strength['color'])
        self.SecurityProgress.configure(progress_color=strength['color'])

    def copy_generation(self):
        pyperclip.copy(self.password)
        ToastNotifier().show_toast("Security", "Le mot de passe a été copié dans la presse papier", duration=3, threaded=True)

class DeletePassword(CTkToplevel):
    def __init__(self, loginId, page: Authentifiants) -> None:
        super().__init__(page.window, fg_color=Colors.White)

        center(550, 200, self)

        self.loginId = loginId
        self.vault = page

        self.view()

    def view(self):
        self.WarningLabel = CTkLabel(
            self, 
            text="Supprimer le mot de passe ?",
            fg_color=Colors.White,
            font=Fonts().NavButtonFont,
            text_color=Colors.Mirage)
        self.WarningLabel.place(x=30, y=40)

        self.ExplainingLabel = CTkLabel(
            self, 
            font=Fonts().EntryFont,
            fg_color=Colors.White,
            text="L’élément va être supprimé définitivement de votre compte.",
            text_color=Colors.Mirage)
        self.ExplainingLabel.place(x=30, y=80)

        self.DeleteButton = CTkButton(
            self, 
            text="Supprimer cet identifiant", 
            bg_color=Colors.White,
            fg_color=Colors.Danger, 
            text_color=Colors.White,
            font=Fonts().ButtonFont, 
            command=lambda: self.delete(),
            hover_color=Colors.DarkDanger,
            width=230, 
            height=40)
        self.DeleteButton.place(x=290, y=130)

        self.CancelButton = CTkButton(
            self, 
            text="Annuler", 
            fg_color=Colors.White, 
            text_color=Colors.Mirage,
            border_width=2,
            hover_color=Colors.DarkTeal,
            border_color=Colors.Mirage, 
            font=Fonts().ButtonFont,
            command=lambda: self.destroy(),
            width=100,
            height=40)
        self.CancelButton.place(x=160, y=130)

    def delete(self):
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()
            curr.execute("DELETE FROM 'Authentifiants' WHERE authId=?", (self.loginId,))
            conn.commit()
            
        self.destroy()
        self.vault.AuthTable.search()

class ActionPopup(Menu):
    def __init__(self, page: Authentifiants, x, y, tags) -> None:
        super().__init__(page.window, tearoff=0)
        self.page = page
        self.x, self.y = x, y
        self.tags = tags
        self.table = page.AuthTable
        self.view()

    def view(self):
        self.add_command(
            label="Voir les détails",
            #command=lambda: EditPassword(self.master, self.parent), 
            activebackground=Colors.Teal, 
            activeforeground=Colors.White, 
            font=Fonts().PopupItemFont)

        self.add_command(
            label="Accéder au site",
            command=lambda: webbrowser.open("https://www." + self.tags[1]), 
            activebackground=Colors.Teal, 
            activeforeground=Colors.White, 
            font=Fonts().PopupItemFont)

        self.add_command(
            label="Copier le mot de passe",
            command= self.copy_password, 
            activebackground=Colors.Teal, 
            activeforeground=Colors.White, 
            font=Fonts().PopupItemFont)

        self.add_command(
            label="Copier l'identifiant",
            command= self.copy_login, 
            activebackground=Colors.Teal, 
            activeforeground=Colors.White, 
            font=Fonts().PopupItemFont)

        self.add_command(
            label="Supprimer",
            command=lambda: DeletePassword(self.tags[0], self.page), 
            activebackground=Colors.Teal, 
            activeforeground=Colors.White, 
            font=Fonts().PopupItemFont)

        try:
            self.tk_popup(self.x+104, self.y+122)
        finally:
            self.grab_release()

    def copy_password(self):
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()
            password = curr.execute(f"SELECT password FROM 'Authentifiants' WHERE authId={self.tags[0]}").fetchone()[0]
            conn.commit()
            

        pyperclip.copy(password_decrypt(password, env['USERPASSWORD']))
        ToastNotifier().show_toast("Security", "Le mot de passe a été copié dans la presse papier", duration=3, threaded=True)

    def copy_login(self):
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()
            username, email = curr.execute(f"SELECT username, email FROM 'Authentifiants' WHERE authId={self.tags[0]}").fetchone()

        if username and not username.isspace():
            pyperclip.copy(username)
            ToastNotifier().show_toast("Security", "Le nom d'utilisateur a été copié dans la presse papier", duration=3, threaded=True)
        else:
            pyperclip.copy(email)
            ToastNotifier().show_toast("Security", "L'email a été copié dans la presse papier", duration=3, threaded=True)

