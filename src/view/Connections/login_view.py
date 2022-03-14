from src.view import *
from src.view.assets import colors
from src.view.Connections import signin_view
from src.model import *
from src.model.Connections import login_model

def login_page():
    view_commands.center_window(340, 440, config.app)
    view_commands.clear(config.app)

    MainFrame = Frame(config.app, bg=config.app.cget('bg'))
    MainFrame.place(relwidth=1, relheight=1)

    BannerFrame = Frame(config.app, bg=colors.mirage, width=340, height=97)
    BannerFrame.place(x=0, y=0)

    BannerLabel = Label(BannerFrame, text="SECURITY", font=Font(
        family='Roboto', size=35, weight="bold"), borderwidth=0, justify='center', fg=config.app.cget('bg'), bg=colors.mirage)
    BannerLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    EmailEntry = Entry(config.app, highlightthickness=2,
            highlightbackground="black", highlightcolor="black")
    EmailEntry.place(x=36, y=157, width=268, height=20)

    PasswordEntry = Entry(config.app, highlightthickness=2, highlightbackground="black",
                highlightcolor="black")
    PasswordEntry.place(x=36, y=212, width=268, height=20)

    ForgotPasswordButton = Button(config.app, borderwidth=0, text="Mot de passe oublié?", font=Font(
        family='Roboto', size=11, weight="normal"), fg=colors.comments_grey, bg=config.app.cget('bg')).place(x=38, y=252)

    SessionCheckVar = BooleanVar()
    SessionCheckButton = Checkbutton(config.app, bg=config.app.cget('bg'), text='Garder ma session ouverte durant 14 jours', variable=SessionCheckVar, font=Font(
        family='Roboto', size=10, weight="normal"), onvalue=True, offvalue=False).place(x=36, y=296, width=268)
    LoginButton = Button(config.app, command=lambda: [login_model.login(EmailEntry.get(), PasswordEntry.get(), SessionCheckVar.get())], text="Connexion", font=Font(
        family='Roboto', size=12, weight="bold"), bg=colors.mirage, fg=config.app.cget('bg'), relief=FLAT).place(x=36, y=345, width=268, height=36)

    SinginButton = Button(config.app, command=lambda: [signin_view.signin_page()], text="Créer un compte", font=Font(family='Roboto', size=11, weight="normal"),
                borderwidth=0, justify='center', fg=colors.comments_grey, bg=config.app.cget('bg')).place(relx=0.5, y=400, anchor=CENTER)

    # Bindings
    Entries = {EmailEntry: "Adresse e-mail", PasswordEntry: "Mot de passe"}

    MainFrame.bind(
        "<Button-1>", lambda event: [view_commands.leave_all(Entries)])
    config.app.bind("<FocusOut>", lambda event: [view_commands.leave_all(Entries)])

    EmailEntry.bind("<Button-1>", lambda event: [view_commands.click(event, Entries)])
    PasswordEntry.bind("<Button-1>", lambda event: [view_commands.click(event, Entries, hide="*")])
    view_commands.leave_all(Entries)

#Alerts
def alert():
    ErreurLabel = Label(config.app, text="Identifiants Incorrect", bg=colors.eror_alert_bg, fg=colors.error_alert_fg, anchor=W, padx=36, font=Font(family="Roboto", size=10, weight="bold")).place(x=0, y=97, width=340, height=40)