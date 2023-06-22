import os
import numpy as np

import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
from screeninfo import get_monitors
from time import strftime
import datetime

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
        self.h2Size = round(self.screenWidth / 75)
        self.h3Size = round(self.screenWidth / 100)
        
        self.btn1Size = round(self.screenWidth / 70)
        self.btn2Size = round(self.screenWidth / 101)
        
        self.timeSize = round(self.screenWidth / 70)
        self.panelSize = round(self.screenWidth / 5)
        
        # Style
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Horizontal.TProgressbar", foreground=self.DARK_CYAN, background=self.DARK_CYAN, troughcolor=self.GRAY, darkcolor=self.GRAY, lightcolor=self.GRAY, bordercolor=self.GRAY)
        
        # giving the programm an escape ;)    
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        # Log into Database
        self.databaseHandler = DatabaseHandler("C125", 6, 10)
        
        # Loadup Screens
        # self.Background()
        self.DefaultScreen()
        self.IdScreen()
        self.EntryScreen()
        self.SettingsScreen()
        self.MessageScreen()
        
        
        # Start with the Default Screen
        self.SelectMessageFrame()
        
        
        
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
        self.after(60000, self.UpdateClock)
        
        
        
    def DefaultScreen(self):
        # Defualt Frame
        self.defautlFrame = tk.Frame(self)
        
        # Settings Button
        settingsBtn = tk.Button(self.defautlFrame, text="⚙️", font=(self.FONT, self.btn1Size, "bold"), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(0))
        settingsBtn.place(relx=0.01, rely=0.02)
        
        # Default Panel
        defaultPanel = tk.Frame(self.defautlFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        defaultPanel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

        # Titlebar
        self.titlePanel = tk.Label(defaultPanel, text="C125 - Leise - 5/7", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg="Green", fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.titlePanel.pack(side="top", fill="x")

        # Display
        displayPanel = tk.Frame(defaultPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        displayPanel.place(relx=0.15, rely=0.165, relwidth=0.7, relheight=0.6)
        
        # Display Current Entries
        self.bar = []
        for i in range(10):
            pb = ttk.Progressbar(displayPanel, orient="horizontal", mode="determinate", maximum=90, value=0, style="Horizontal.TProgressbar")
            pb.place(relx=0, rely=i/10, relwidth=1, relheight=0.1)
            pbLabel = tk.Label(pb, text="",  font=(self.FONT, self.h3Size, "bold"), fg="White", bg=self.DARK_CYAN)
            pbLabel.place(relx=0, rely=0.065)

            entry = {"pb": pb, "label": pbLabel}
            self.bar.append(entry)

        # Buttons
        btnPanel = tk.Frame(defaultPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        self.einloggBtn = tk.Button(btnPanel, text="EINLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.einloggBtn.pack(side="left", padx=self.borderSize*5)

        ausloggBtn = tk.Button(btnPanel, text="AUSLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        ausloggBtn.pack(side="left", padx=self.borderSize*5)
        
        # Updates the values with database
        self.UpdateDefaultScreen()
        
        
        
    def IdScreen(self):
        # Id Frame
        self.idFrame = tk.Frame(self)
        
        # Panel
        idPanel = tk.Frame(self.idFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        idPanel.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.6)
        
        # Titlebar
        titlePanel = tk.Label(idPanel, text="Hochschul-ID auflegen!", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        titlePanel.pack(side="top", fill="x")
        
        # image
        idImg = Image.open("Assets\idImg.png")
        idImg = idImg.resize((self.panelSize, self.panelSize), Image.LANCZOS)
        idImg = ImageTk.PhotoImage(idImg)
        
        idImgPanel = tk.Label(self.idFrame, image=idImg, background=self.CYAN)
        idImgPanel.image = idImg
        idImgPanel.place(x=(self.screenWidth-self.panelSize)/2, y=(self.screenHeight-self.panelSize)/2)
        
        
        
    def EntryScreen(self):
        # Entry Frame
        self.entryFrame = tk.Frame(self)
        
        # Entry Panel
        entryPanel = tk.Frame(self.entryFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        entryPanel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

        # Titlebar
        titlePanel = tk.Label(entryPanel, text="Einloggen", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        titlePanel.pack(side="top", fill="x")
        
        # Loud Quiet panel
        lqPanel = tk.Frame(entryPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        lqPanel.place(relx=0.025, rely=0.2, relwidth=0.95, relheight=0.15)
        
        # subdividing panel
        lqLeftPanel = tk.Frame(lqPanel, bg=self.GRAY)
        lqLeftPanel.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        lqRightPanel = tk.Frame(lqPanel, bg=self.GRAY)
        lqRightPanel.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)
        
        # left side heading
        typePanel = tk.Label(lqLeftPanel, text="Lernart", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        typePanel.pack(side="left", fill="x", padx=self.borderSize*5)
        
        # right side buttons
        self.loudBtn = tk.Button(lqRightPanel, text="Loud", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.loudBtn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.quietBtn = tk.Button(lqRightPanel, text="Quiet", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.quietBtn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        
        # Time panel
        timePanel = tk.Frame(entryPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        timePanel.place(relx=0.025, rely=0.4, relwidth=0.95, relheight=0.3)
        
        # subdividing panel
        timeLeftPanel = tk.Frame(timePanel, bg=self.GRAY)
        timeLeftPanel.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        timeRightTopPanel = tk.Frame(timePanel, bg=self.GRAY)
        timeRightTopPanel.place(relx=0.35, rely=0, relwidth=0.65, relheight=0.5)
        
        timeRightBotPanel = tk.Frame(timePanel, bg=self.GRAY)
        timeRightBotPanel.place(relx=0.35, rely=0.5, relwidth=0.65, relheight=0.5)
        
        # left side heading
        timeHeadPanel = tk.Label(timeLeftPanel, text="Lerndauer", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        timeHeadPanel.pack(side="left", fill="x", padx=self.borderSize*5)
        
        # right top side buttons
        self.t15Btn = tk.Button(timeRightTopPanel, text="15 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.t15Btn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.t30Btn = tk.Button(timeRightTopPanel, text="30 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.t30Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        self.t45Btn = tk.Button(timeRightTopPanel, text="45 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.t45Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        
        # right bot side buttons
        self.t60Btn = tk.Button(timeRightBotPanel, text="60 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.t60Btn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.t75Btn = tk.Button(timeRightBotPanel, text="75 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.t75Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        self.t90Btn = tk.Button(timeRightBotPanel, text="90 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.t90Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        
        # Confirm deny buttons
        btnPanel = tk.Frame(entryPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        self.EntryConfirmBtn = tk.Button(btnPanel, text="BESTÄTIGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.EntryConfirmBtn.pack(side="left", padx=self.borderSize*5)

        denyBtn = tk.Button(btnPanel, text="ABBRECHEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        denyBtn.pack(side="left", padx=self.borderSize*5)
        
        
    def SettingsScreen(self):
        # Admin Frame
        self.settingsFrame = tk.Frame(self)
        
        # Entry Panel
        settingsPanel = tk.Frame(self.settingsFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        settingsPanel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

        # Titlebar
        titlePanel = tk.Label(settingsPanel, text="Settings", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        titlePanel.pack(side="top", fill="x")

        # Loud seats panel
        loudPanel = tk.Frame(settingsPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        loudPanel.place(relx=0.025, rely=0.128, relwidth=0.95, relheight=0.15)

        # subdividing panel
        loudLeftPanel = tk.Frame(loudPanel, bg=self.GRAY)
        loudLeftPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        loudRightPanel = tk.Frame(loudPanel, bg=self.GRAY)
        loudRightPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # left side heading
        loudHeadPanel = tk.Label(loudLeftPanel, text="Laute Plätze", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        loudHeadPanel.pack(side="left", fill="x", padx=self.borderSize*5)

        # right side buttons
        self.loudSeatsPanel = tk.Label(loudRightPanel, text="8", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*10, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.loudSeatsPanel.pack(side="left", padx=[self.borderSize*2.5, self.borderSize*15], anchor="center")
        
        self.addLoudBtn = tk.Button(loudRightPanel, text="+", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.addLoudBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.redactLoudBtn = tk.Button(loudRightPanel, text="-", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.redactLoudBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # quiet seats panel
        quietPanel = tk.Frame(settingsPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        quietPanel.place(relx=0.025, rely=0.30, relwidth=0.95, relheight=0.15)

        # subdividing panel
        quietLeftPanel = tk.Frame(quietPanel, bg=self.GRAY)
        quietLeftPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        quietRightPanel = tk.Frame(quietPanel, bg=self.GRAY)
        quietRightPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # left side heading
        quietHeadPanel = tk.Label(quietLeftPanel, text="Leise Plätze", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        quietHeadPanel.pack(side="left", fill="x", padx=self.borderSize*5)

        # right side buttons
        self.quietSeatsPanel = tk.Label(quietRightPanel, text="2", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*10, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.quietSeatsPanel.pack(side="left", padx=[self.borderSize*2.5, self.borderSize*15], anchor="center")
        
        self.addQuietBtn = tk.Button(quietRightPanel, text="+", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.addQuietBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.redactQuietBtn = tk.Button(quietRightPanel, text="-", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.redactQuietBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # block panel
        blockPanel = tk.Frame(settingsPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        blockPanel.place(relx=0.025, rely=0.47, relwidth=0.95, relheight=0.15)

        # subdividing panel
        blockLeftPanel = tk.Frame(blockPanel, bg=self.GRAY)
        blockLeftPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        blockRightPanel = tk.Frame(blockPanel, bg=self.GRAY)
        blockRightPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # left side heading
        blockHeadPanel = tk.Label(blockLeftPanel, text="Raum blockieren", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        blockHeadPanel.pack(side="left", fill="x", padx=self.borderSize*5)

        # right side buttons        
        self.t30BlockBtn = tk.Button(blockRightPanel, text="30 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.t30BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.t60BlockBtn = tk.Button(blockRightPanel, text="60 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.t60BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        self.t90BlockBtn = tk.Button(blockRightPanel, text="90 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.t90BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # shutdown panel
        shutdownPanel = tk.Frame(settingsPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        shutdownPanel.place(relx=0.025, rely=0.64, relwidth=0.95, relheight=0.15)

        # subdividing panel
        shutdownLeftPanel = tk.Frame(shutdownPanel, bg=self.GRAY)
        shutdownLeftPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        shutdownRightPanel = tk.Frame(shutdownPanel, bg=self.GRAY)
        shutdownRightPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # left side heading
        shutdownHeadPanel = tk.Label(shutdownLeftPanel, text="Herunterfahren", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        shutdownHeadPanel.pack(side="left", fill="x", padx=self.borderSize*5)

        # right side buttons        
        self.yShutdownBtn = tk.Button(shutdownRightPanel, text="Ja", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.yShutdownBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.nShutdownBtn = tk.Button(shutdownRightPanel, text="Nein", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        self.nShutdownBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # Confirm deny buttons
        btnPanel = tk.Frame(settingsPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        self.settingsConfirmBtn = tk.Button(btnPanel, text="BESTÄTIGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.settingsConfirmBtn.pack(side="left", padx=self.borderSize*5)

        denyBtn = tk.Button(btnPanel, text="ABBRECHEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        denyBtn.pack(side="left", padx=self.borderSize*5)
        
        
    
    def MessageScreen(self):
        # Message Frame
        self.messageFrame = tk.Frame(self)
        
        # Message Panel
        messagePanel = tk.Frame(self.messageFrame, bg=self.DARK_CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        messagePanel.place(relx=0.25, rely=0.375, relwidth=0.5, relheight=0.25)

        # Titlebar
        titlePanel = tk.Label(messagePanel, text="Erfolgreich eingeloggt. Bitte loggen Sie sich wieder aus, wenn Sie den Raum verlassen.", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", justify="center")
        titlePanel.bind('<Configure>', lambda e: titlePanel.config(wraplength=titlePanel.winfo_width()*0.9))
        titlePanel.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        
        
    def UpdateDefaultScreen(self):
        self.databaseHandler.DeleteExpiredEntries()
        
        # Update Titlebar Background Color
        roomState = self.databaseHandler.GetProperty("roomState")
        if roomState == "Blocked":
            self.titlePanel.config(bg=self.GRAY)
            roomSeats = 0
        elif roomState == "Loud":
            self.titlePanel.config(bg="Yellow")
            roomSeats = self.databaseHandler.GetProperty("loudSeats")
        elif roomState == "Quiet":
            self.titlePanel.config(bg="Blue")
            roomSeats = self.databaseHandler.GetProperty("quietSeats")
        else:
            self.titlePanel.config(bg="Green")
            roomSeats = self.databaseHandler.GetProperty("loudSeats")
            
        # Update Titlebar Label
        roomId = self.databaseHandler.GetRoomId()
        roomCurrSeats = self.databaseHandler.GetEntryCount()
        
        self.titlePanel.config(text="{roomId} - {roomState} - {roomCurrSeats}/{roomSeats}".format(roomId=roomId, roomState=roomState, roomCurrSeats=roomCurrSeats, roomSeats=roomSeats))
        
        # Disable button if full
        if roomCurrSeats >= int(roomSeats) or roomState == "Blocked":
            self.einloggBtn.config(state="disabled")
        else:
            self.einloggBtn.config(state="normal")
            
        # Display current entries
        exitTimes = self.databaseHandler.GetExitTimes()
        for i in range(10):
            if i < len(exitTimes):    
                self.bar[i]["label"].config(text=exitTimes[i])
                
                timeDelta =  datetime.combine(datetime.today(), datetime.strptime(exitTimes[i], '%H:%M').time()) - datetime.combine(datetime.today(), datetime.now().time())
                minuteDelta = timeDelta.seconds // 60
                self.bar[i]["pb"].config(value=minuteDelta)
            elif i < len(self.bar):
                self.bar[i]["label"].config(text="")
                self.bar[i]["pb"].config(value=0)
            
        self.after(60000, self.UpdateDefaultScreen) # update every minute
        
        
    def LookForId(self, route:int):
        pass
        
    
    def DeselectAllFrames(self):
        self.defautlFrame.forget()
        self.idFrame.forget()
        self.entryFrame.forget()
        self.settingsFrame.forget()
        self.messageFrame.forget()
        
        
    def SelectDefaultFrame(self):
        self.DeselectAllFrames()
        self.defautlFrame.pack(fill=tk.BOTH, expand=True)
        
        
    def SelectIdFrame(self, route:int):
        self.DeselectAllFrames()
        self.idFrame.pack(fill=tk.BOTH, expand=True)
        self.LookForId(route)
        
    def SelectEntryFrame(self):
        self.DeselectAllFrames()
        self.entryFrame.pack(fill=tk.BOTH, expand=True)
        
    def SelectSettingsFrame(self):
        self.DeselectAllFrames()
        self.settingsFrame.pack(fill=tk.BOTH, expand=True)
        
    def SelectMessageFrame(self):
        self.DeselectAllFrames()
        self.messageFrame.pack(fill=tk.BOTH, expand=True)







def main():
    root = Win()    
    root.mainloop()


if __name__ == "__main__":
    main()