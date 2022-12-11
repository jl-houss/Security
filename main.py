import sqlite3
from os import environ as env

from customtkinter import CTk

from assets.code.ui import Colors
from src.auth.login import Login


class App(CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=Colors.White)

        self.title("Security")
        self.resizable(False, False)

        env["DB"] = "main.db"

        conn = sqlite3.connect(env["DB"])
        curr = conn.cursor()

        curr.execute(
            """CREATE TABLE if not exists Users (
                "userId"	INTEGER NOT NULL UNIQUE,
                "username"	TEXT NOT NULL,
                "password"	TEXT NOT NULL,
                PRIMARY KEY("userId" AUTOINCREMENT)
            );"""
        )

        curr.execute(
            """CREATE TABLE if not exists Authentifiants (
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
                )"""
        )

        conn.commit()
        conn.close()

        Login(self)

        


if __name__ == "__main__":
    app = App()
    app.mainloop()
