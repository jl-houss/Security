from customtkinter import CTk
from assets.ui import Colors
from src.auth.login import Login
from os import environ as env
import sqlite3

class App(CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=Colors.White)

        self.title("Security")
        self.resizable(False, False)

        env['DB'] = "main.db"
        
        with sqlite3.connect(env['DB']) as conn:
            curr = conn.cursor()

            try:
                curr.execute("SELECT * FROM 'Users'")
            except:
                curr.execute("""CREATE TABLE "Users" (
                    "userId"	INTEGER NOT NULL UNIQUE,
                    "username"	TEXT NOT NULL,
                    "password"	TEXT NOT NULL,
                    PRIMARY KEY("userId" AUTOINCREMENT)
                );""")

            try:
                curr.execute("SELECT * FROM 'Authentifiants'")
            except:
                curr.execute("""CREATE TABLE "Authentifiants" (
                        "authId"	INTEGER NOT NULL UNIQUE,
                        "parentId"	INTEGER,
                        "title"	    TEXT,
                        "domain"	TEXT,
                        "username"	TEXT,
                        "email"	    TEXT,
                        "password"	TEXT,
                        "category"	TEXT,
                        "note"	    TEXT,
                        FOREIGN KEY("parentId") REFERENCES "Users"("userId"),
                        PRIMARY KEY("authId" AUTOINCREMENT)
                    )""")
            
            

        Login(self)

        self.mainloop()

if __name__ == "__main__":
    App()