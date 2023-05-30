import os
import numpy as np

import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
from screeninfo import get_monitors
from time import strftime

from databaseHandler import *


class Win(tk.Tk):
    FONT = "Arial"
    GRAY = "#a6a7a9"
    CYAN = "#58b8c6"
    DARK_CYAN = "#2b5f67"
    
    def __init__(self):
        tk.Tk.__init__(self, None)

        self.title("RAC RBS")                           # changes title
        self.overrideredirect(True)                     # removes titlebar
        self.resizable(False, False)                    # makes window unsizeable
        self.attributes('-topmost', True)               # makes window always ontop
        
        for monitor in get_monitors():                  # finds main monitor and saves screenSize
            if monitor.is_primary:
                self.screenWidth = monitor.width
                self.screenHeight = monitor.height
                # self.screenWidth = 1920               # testing different screensizes
                # self.screenHeight = 1080              # testing different screensizes
                self.screenX = monitor.x
                self.screenY = monitor.y
                self.geometry(('{w}x{h}+{x}+{y}'.format(w=self.screenWidth, h=self.screenHeight, x=self.screenX, y=self.screenY)))
                break
            
        # set some variables for later use
        self.borderSize = round(self.screenWidth / 512)
        
        self.h1Size = round(self.screenWidth / 50)
        self.h1Size = round(self.screenWidth / 75)
        self.h3Size = round(self.screenWidth / 100)
        
        self.btn1Size = round(self.screenWidth / 70)
        self.timeSize = round(self.screenWidth / 70)
        
        # Style
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Horizontal.TProgressbar", foreground=self.DARK_CYAN, background=self.DARK_CYAN, troughcolor=self.GRAY, darkcolor=self.GRAY, lightcolor=self.GRAY, bordercolor=self.GRAY)
        
        # giving the programm an escape ;)    
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        # Log into Database
        self.databaseHandler = DatabaseHandler("C125", 6, 10)
        
        # start with default screen
        self.DefaultScreen()
        
        
        
    def Background(self):
        # Loading in Background Image       
        self.canvas = tk.Canvas(self, bg='SkyBlue4')        
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        bgImg = Image.open("Assets\Background2.png")
        bgImg = bgImg.resize((self.screenWidth, self.screenHeight), Image.LANCZOS)
        bgImg = ImageTk.PhotoImage(bgImg)
        
        bgImgPanel = tk.Label(self.canvas, image=bgImg)
        bgImgPanel.image = bgImg
        bgImgPanel.place(x=-2, y=-2)
        
        
        # Clock Bottom Left        
        self.clock = tk.Label(self.canvas, text="00:00", font=(self.FONT, self.timeSize, "bold"), bg=self.GRAY, fg="White", padx=self.borderSize*2, pady=self.borderSize, highlightbackground="White", highlightthickness=self.borderSize)
        self.clock.place(relx=0.01, rely=0.92)

        self.UpdateClock()



    def UpdateClock(self):                            # takes the clock on the bottom left and updates it every second
        time = strftime('%H:%M')                      #add %A for weekday name
        self.clock.config(text=time)
        self.after(1000, self.UpdateClock)
        
        
        
    def DefaultScreen(self):
        # Update background
        self.Background()
        
        # Settings Button
        settingsBtn = tk.Button(self.canvas, text="⚙️", font=(self.FONT, self.btn1Size, "bold"), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid")
        settingsBtn.place(relx=0.01, rely=0.02)
        
        # Default Panel
        defaultPanel = tk.Frame(self.canvas, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        defaultPanel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

        # Titlebar
        titlePanel = tk.Label(defaultPanel, text="C125 - Leise - 5/7", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg="Green", fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        titlePanel.pack(side="top", fill="x")

        # Display
        displayPanel = tk.Frame(defaultPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        displayPanel.place(relx=0.15, rely=0.165, relwidth=0.7, relheight=0.6)
        
        # Display Current Entries
        bar = []
        for i in range(10):
            pb = ttk.Progressbar(displayPanel, orient="horizontal", mode="determinate", maximum=90, value=0, style="Horizontal.TProgressbar")
            pb.place(relx=0, rely=i/10, relwidth=1, relheight=0.1)
            pbLabel = tk.Label(pb, text="",  font=(self.FONT, self.h3Size, "bold"), fg="White", bg=self.DARK_CYAN)
            pbLabel.place(relx=0, rely=0.065)

            entryName = "entry" + str(i)
            entry = {entryName: {"pb": pb, "label": pbLabel}}
            bar.append(entry)

        # Buttons
        btnPanel = tk.Frame(defaultPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        einloggBtn = tk.Button(btnPanel, text="EINLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid")
        einloggBtn.pack(side="left", padx=self.borderSize*5)

        ausloggBtn = tk.Button(btnPanel, text="AUSLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid")
        ausloggBtn.pack(side="left", padx=self.borderSize*5)




def main():
    root = Win()    
    root.mainloop()


if __name__ == "__main__":
    main()