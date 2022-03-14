from src.model import *
from src.view.Connections import signin_view
from validate_email_address import validate_email
import bcrypt

def validate_password(password):
    conds = {
            "Le mot de passe doit contenir une lettre majuscule": lambda s: any(x.isupper() for x in s),
            "Le mot de passe doit contenir une lettre minuscule": lambda s: any(x.islower() for x in s),
            "Le mot de passe doit contenir un nombre": lambda s: any(x.isdigit() for x in s),
            "Le mot de passe est trop court": lambda s: len(s) >= 8
    }

    valid = True
    errors = []
    for error, cond in conds.items():
        if not cond(password):
            errors.append(error)
            valid = False

    return valid, errors

def create_account(email, password):
    conn, c = db_commands.db_connect()

    c.execute("INSERT INTO Users (email, password) VALUES(?, ?)",
              (email, bcrypt.hashpw(bytes(password, "ascii"), bcrypt.gensalt(16)).decode("ascii")))
    conn.commit()

    id = (c.execute("SELECT id FROM Users WHERE email=?",
          (email,)).fetchone())[0]
    
    print("signed in!")

def signin(email, password, password_confirmation):
    conn, c = db_commands.db_connect()

    if not c.execute("SELECT id FROM Users WHERE email=?", (email,)).fetchone():
        if validate_email(email):
            if validate_password(password)[0]:
                if password == password_confirmation:
                    print("signed")
                    create_account(email, password)
                    signin_view.finishing_page()
                else:
                    signin_view.alert("Les mots de passe ne correspondent pas")
            else:
                signin_view.alert(validate_password(password)[1][0])
        else:
            signin_view.alert("Email invalide")
    else:
        signin_view.alert("Email déja utilisé")
