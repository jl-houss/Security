from tkinter import *
import json
from src.controller import cache_controller
from src.controller import config

if __name__ == "__main__":
    config.app = Tk()
    config.app.title("Security")
    config.app.resizable(False, False)
    config.app.config(bg='white')
    
    cache_controller.init_cache()

    config.app.mainloop()
