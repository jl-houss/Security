from src.view import *
from src.view.assets import colors
from src.view.Connections import login_view
from src.model import *
from src.model.Connections import signin_model

#Pages
def signin_page():
    view_commands.center_window(650, 420, config.app)

    view_commands.clear(config.app)

    MainFrame = Frame(config.app, bg=config.app.cget('bg'))
    MainFrame.place(width=650, height=420)

    BannerFrame = Frame(config.app, bg=colors.mirage, width=650, height=35)
    BannerFrame.place(x=0, y=0)

    BannerLabel = Label(BannerFrame, text="Bienvenue dans Security", font=Font(
        family='Roboto', size=12, weight="bold"), borderwidth=0, justify='center', fg=config.app.cget('bg'), bg=colors.mirage)
    BannerLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    HeaderLabel = Label(
        config.app, text="Créez votre compte Security",
        font=Font(family='Roboto', size=14, weight="bold"), bg=config.app.cget('bg')).place(x=152, y=103)
    DescLabel = Label(config.app, font=Font(family='Roboto', size=13, weight="normal"),
                      text="Vous n’aurez plus qu’à vous souvenir de cet e-mail et de\nce mot de passe, on se charge du reste !", justify="left", fg=colors.comments_grey, bg="white").place(x=150, y=132)

    EmailEntry = Entry(config.app, highlightthickness=2,
                       highlightbackground="black", highlightcolor="black")
    EmailEntry.place(x=152, y=215, width=354, height=24)

    PasswordEntry = Entry(
        config.app,
        show="*",
        highlightthickness=2,
        highlightbackground="black",
        highlightcolor="black"
    )
    PasswordEntry.place(x=152, y=269, width=172, height=24)

    RepeatPasswordEntry = Entry(
        config.app,
        show="*",
        highlightthickness=2,
        highlightbackground="black",
        highlightcolor="black"
    )
    RepeatPasswordEntry.place(x=334, y=269, width=172, height=24)

    FooterFrame = Frame(config.app, bg="#F7F7F7", width=652, height=65,
                        highlightthickness=1,
                        highlightbackground="grey",
                        highlightcolor="grey").place(x=-1, y=355)

    SigninButton = Button(config.app, command=lambda: signin_model.signin(EmailEntry.get(), PasswordEntry.get(), RepeatPasswordEntry.get()), text="Suivant", font=Font(
        family='Roboto', size=12, weight="bold"), bg=colors.mirage, fg=config.app.cget('bg'), relief=FLAT, anchor=CENTER)
    SigninButton.place(x=550, y=369, width=70, height=36)

    LoginButton = Button(config.app, command=lambda:  login_view.login_page(), text="J’ai déja un compte", font=Font(family='Roboto', size=11, weight="normal"),
                         borderwidth=0, justify='center', fg=colors.comments_grey, bg="#F7F7F7")
    LoginButton.place(x=30, y=375)

    # Bindings
    Entries = {
            EmailEntry: "Entrez votre adresse e-mail",
            PasswordEntry: "Créez un mot de passe fort",
            RepeatPasswordEntry: "Confirmez votre mot de passe"}

    MainFrame.bind(
        "<Button-1>", lambda event: [view_commands.leave_all(Entries)])
    config.app.bind("<FocusOut>", lambda event: [
                    view_commands.leave_all(Entries)])

    EmailEntry.bind("<Button-1>", lambda event: [view_commands.click(event, Entries)])
    PasswordEntry.bind(
        "<Button-1>", lambda event: [view_commands.click(event, Entries, hide="*")])
    RepeatPasswordEntry.bind(
        "<Button-1>", lambda event: [view_commands.click(event, Entries, hide="*")])
    view_commands.leave_all(Entries)

def finishing_page():
    view_commands.center_window(650, 420, config.app)

    view_commands.clear(config.app)

    MainFrame = Frame(config.app, bg=config.app.cget('bg'))
    MainFrame.place(width=650, height=420)

    BannerFrame = Frame(config.app, bg=colors.mirage, width=650, height=35)
    BannerFrame.place(x=0, y=0)

    BannerLabel = Label(BannerFrame, text="Bienvenue dans Security", font=Font(
        family='Roboto', size=12, weight="bold"), borderwidth=0, justify='center', fg=config.app.cget('bg'), bg=colors.mirage)
    BannerLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    AlertFrame = Frame(config.app, bg=colors.success_alert_bg, width=650, height=35)
    AlertFrame.place(x=0, y=35)

    AlertLabel = Label(AlertFrame, text="Compte crée !", font=Font(
        family='Roboto', size=12, weight="bold"), borderwidth=0, justify='center', fg=colors.success_alert_fg, bg=colors.success_alert_bg)
    AlertLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    HeaderLabel = Label(
        config.app, text="Votre compte a bien été crée !",
        font=Font(family='Roboto', size=14, weight="bold"), bg="white").place(x=160, y=183)
    DescLabel = Label(config.app, font=Font(family='Roboto', size=13, weight="normal"),
                      text="Il ne vous reste plus qu’a vous connectez a votre compte\npour bénéficer de toutes les fonctionalités de Security !", justify="left", fg=colors.comments_grey, bg="white").place(x=160, y=212)

    FooterFrame = Frame(config.app, bg="#F7F7F7", width=652, height=65,
                        highlightthickness=1,
                        highlightbackground="grey",
                        highlightcolor="grey").place(x=-1, y=355)

    SigninButton = Button(config.app, command=lambda: login_view.login_page(), text="Se Connecter", font=Font(
        family='Roboto', size=12, weight="bold"), bg='#131B23', fg='white', relief=FLAT, anchor=CENTER)
    SigninButton.place(x=210, y=369, width=230, height=36)

#Alerts
def alert(txt):
    ErreurLabel = Label(config.app, text=txt, bg=colors.eror_alert_bg, fg=colors.error_alert_fg, anchor=CENTER, padx=36, font=Font(
                    family="Roboto", size=10, weight="bold")).place(x=0, y=35, width=650, height=40)
