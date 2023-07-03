import os
import numpy as np
import threading

import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
from screeninfo import get_monitors
from time import strftime
from time import time
from datetime import datetime, timedelta

from databaseHandler import *
from rfidManager import *


class Win(tk.Tk):
    #########################
    #                       #
    #    Initialization     #
    #                       #
    #########################
    
    # Static fonts and colors for later use
    FONT = "Arial"
    
    GRAY = "#a6a7a9"
    DARK_GRAY = "#4f4f4f"
    CYAN = "#58b8c6"
    DARK_CYAN = "#2b5f67"
    
    YELLOW = "#b9a21c"
    GREEN = "#36AE7C"
    BLUE = "#187498"
    
    def __init__(self):
        print("Initializing Tkinter")
        tk.Tk.__init__(self, None)

        # changing attribute of the window
        self.title("RAC RBS")                           # changes title
        self.overrideredirect(True)                     # removes titlebar
        self.resizable(False, False)                    # makes window unsizeable
        self.attributes('-topmost', True)               # makes window always ontop
        
        for monitor in get_monitors():                  # finds main monitor and saves screen Width and Height in variables
            if monitor.is_primary:
                self.screenWidth = monitor.width
                self.screenHeight = monitor.height
                self.screenX = monitor.x
                self.screenY = monitor.y
                self.geometry(('{w}x{h}+{x}+{y}'.format(w=self.screenWidth, h=self.screenHeight, x=self.screenX, y=self.screenY)))
                break
            
        # set some size variables for later use
        self.borderSize = round(self.screenWidth / 512)
        
        self.h1Size = round(self.screenWidth / 50)
        self.h2Size = round(self.screenWidth / 75)
        self.h3Size = round(self.screenWidth / 100)
        
        self.btn1Size = round(self.screenWidth / 70)
        self.btn2Size = round(self.screenWidth / 101)
        
        self.timeSize = round(self.screenWidth / 70)
        self.panelSize = round(self.screenWidth / 5)
        
        # configuring style for buttons
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Horizontal.TProgressbar", foreground=self.DARK_CYAN, background=self.DARK_CYAN, troughcolor=self.GRAY, darkcolor=self.GRAY, lightcolor=self.GRAY, bordercolor=self.GRAY)
        
        # giving the programm an escape ;)    
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        # logging into Database
        self.databaseHandler = DatabaseHandler("C125", 6, 10)
        
        # Initialize RFID Reader
        self.rfidManager = RfidManager()
        
        # Preloading Screens so they can be called later on
        self.Background()
        self.DefaultScreen()
        self.SettingsWheel()
        self.IdScreen()
        self.EntryScreen()
        self.SettingsScreen()
        self.MessageScreen()
        
        # Setting the Background and starting with the Default Screen
        self.bgFrame.pack(fill=tk.BOTH, expand=True)
        self.SelectDefaultFrame()
        
        
        
    #########################
    #                       #
    #       Menu Flow       #
    #                       #
    #########################
    
    def DeselectAllFrames(self):                    # Removing every Frame
        self.defautlFrame.place_forget()
        self.settingsWheelFrame.place_forget()
        self.idFrame.place_forget()
        self.entryFrame.place_forget()
        self.settingsFrame.place_forget()
        self.messageFrame.place_forget()
        
        
    def SelectDefaultFrame(self):                   # Shows the Default Screen
        self.DeselectAllFrames()
        self.settingsWheelFrame.place(relx=0.015, rely=0.025, relwidth=0.055, relheight=0.09)
        self.defautlFrame.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)
        
        
    def SelectIdFrame(self, route:int):             # Shows the ID Screen. Also saves the route (from with screen the user came from)
        self.DeselectAllFrames()
        self.idFrame.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.6)
        self.StartScanIdThread()
        self.ScanId(route)
        
        
    def SelectEntryFrame(self):                     # Shows the Default Screen
        self.DeselectAllFrames()
        self.entryFrame.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)
        self.InitializeEntryScreen()
        
        
    def SelectSettingsFrame(self):                  # Shows the Settings Screen
        self.DeselectAllFrames()
        self.settingsFrame.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)
        self.InitializeSettingsScreen()
        
        
    def SelectMessageFrame(self, route: int):                   # Shows the Message Screen
        self.DeselectAllFrames()
        self.messageFrame.place(relx=0.25, rely=0.375, relwidth=0.5, relheight=0.25)
        self.UpdateMessageScreen(route)
        
        
        
    #########################
    #                       #
    #       Background      #
    #                       #
    #########################
       
    def Background(self):
        self.bgFrame = tk.Frame(self)
        
        # Loading in the Background Image
        self.canvas = tk.Canvas(self.bgFrame, bg='SkyBlue4')        
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        bgImg = Image.open("Background.png")
        bgImg = bgImg.resize((self.screenWidth, self.screenHeight), Image.LANCZOS)
        bgImg = ImageTk.PhotoImage(bgImg)
        
        # Placing in the Background Image
        bgImgPanel = tk.Label(self.canvas, image=bgImg)
        bgImgPanel.image = bgImg
        bgImgPanel.place(x=-2, y=-2)
        

        # Setting up a clock on the bottom left
        self.clock = tk.Label(self.canvas, text="00:00", font=(self.FONT, self.timeSize, "bold"), bg=self.GRAY, fg="White", padx=self.borderSize*2, pady=self.borderSize, highlightbackground="White", highlightthickness=self.borderSize)
        self.clock.place(relx=0.01, rely=0.92)

        # Updating the clock every minute
        self.UpdateClock()


    def UpdateClock(self):                              # takes the clock on the bottom left and updates it every second
        time = strftime('%H:%M')
        self.clock.config(text=time)
        self.after(60000, self.UpdateClock)
        
        
        
    #########################
    #                       #
    #     Default Screen    #
    #                       #
    #########################
        
    def DefaultScreen(self):
        self.defautlFrame = tk.Frame(self)
        mainPanel = tk.Frame(self.defautlFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        mainPanel.pack(fill=tk.BOTH, expand=True)

        # Displaying Titlebar in the main Panel
        self.defaultTitle = tk.Label(mainPanel, text="C125 - Leise - 5/7", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg="Green", fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.defaultTitle.pack(side="top", fill="x")

        # Display Panel displays current Entries
        displayPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        displayPanel.place(relx=0.15, rely=0.165, relwidth=0.7, relheight=0.6)
        
        # Creating 10 Bars in the display Panel to display the Entries
        self.bar = []
        for i in range(10):
            pb = ttk.Progressbar(displayPanel, orient="horizontal", mode="determinate", maximum=90, value=0, style="Horizontal.TProgressbar")
            pb.place(relx=0, rely=i/10, relwidth=1, relheight=0.1)
            pbLabel = tk.Label(pb, text="",  font=(self.FONT, self.h3Size, "bold"), fg="White", bg=self.DARK_CYAN)
            pbLabel.place(relx=0, rely=0.065)

            entry = {"pb": pb, "label": pbLabel}
            self.bar.append(entry)

        # Buttons to login and logout
        btnPanel = tk.Frame(mainPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        self.loginBtn = tk.Button(btnPanel, text="EINLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(1))
        self.loginBtn.pack(side="left", padx=self.borderSize*5)

        logoutBtn = tk.Button(btnPanel, text="AUSLOGGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(2))
        logoutBtn.pack(side="left", padx=self.borderSize*5)
        
        # Updates the values with database every minute
        self.UpdateDefaultScreen(True)
        
        
    def SettingsWheel(self):
        # Making a Settings button to display on the top right on the default screen
        print("Pressed Settings Wheel")
        self.settingsWheelFrame = tk.Frame(self)
        
        settingsBtn = tk.Button(self.settingsWheelFrame, text="⚙️", font=(self.FONT, self.btn1Size, "bold"), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectIdFrame(0))
        settingsBtn.pack(fill=tk.BOTH, expand=True)
        
        
    def UpdateDefaultScreen(self, repeat: bool):
        print("Updating Default Screen")
        self.databaseHandler.DeleteExpiredEntries()
        
        # Update Titlebar Background Color
        self.roomState = self.databaseHandler.GetProperty("roomState")
        if self.roomState == "Blocked":
            self.defaultTitle.config(bg=self.DARK_GRAY)
            currRoomState = "Blockiert"
            roomSeats = 0
        elif self.roomState == "Loud":
            self.defaultTitle.config(bg=self.YELLOW)
            currRoomState = "Laut"
            roomSeats = self.databaseHandler.GetProperty("loudSeats")
        elif self.roomState == "Quiet":
            self.defaultTitle.config(bg=self.BLUE)
            currRoomState = "Leise"
            roomSeats = self.databaseHandler.GetProperty("quietSeats")
        else:
            self.defaultTitle.config(bg=self.GREEN)
            currRoomState = "Leer"
            roomSeats = self.databaseHandler.GetProperty("loudSeats")
            
        # Update Titlebar Label
        roomId = self.databaseHandler.roomId
        roomCurrSeats = self.databaseHandler.GetEntryCount()
        
        self.defaultTitle.config(text="{roomId} - {roomState} - {roomCurrSeats}/{roomSeats}".format(roomId=roomId, roomState=currRoomState, roomCurrSeats=roomCurrSeats, roomSeats=roomSeats))
        
        # Disable button if full
        if roomCurrSeats >= int(roomSeats) or self.roomState == "Blocked":
            self.loginBtn.config(state="disabled")
        else:
            self.loginBtn.config(state="normal")
            
        if roomCurrSeats == 0:
            self.databaseHandler.SetProperty("roomState", "Empty")
            
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
        
        if repeat != True:
            return
        
        self.after(60000, self.UpdateDefaultScreen(True)) # update every minute
                
        
        
    #########################
    #                       #
    #       ID Screen       #
    #                       #
    #########################
        
    def IdScreen(self):
        self.idFrame = tk.Frame(self)
        mainPanel = tk.Frame(self.idFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        mainPanel.pack(fill=tk.BOTH, expand=True)
        
        # Displaying Titlebar in the main Panel
        title = tk.Label(mainPanel, text="Hochschul-ID auflegen!", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        title.pack(side="top", fill="x")
        
        # Loading in the Image that shows the user where to put the id card
        idImg = Image.open("idImg.png")
        idImg = idImg.resize((self.panelSize, self.panelSize), Image.LANCZOS)
        idImg = ImageTk.PhotoImage(idImg)
        
        # Displaying the Image in the center of the panel
        idImgPanel = tk.Label(self.idFrame, image=idImg, background=self.CYAN)
        idImgPanel.image = idImg
        idImgPanel.place(relx=0.05, rely=0.225, relwidth=0.9)
        
        
    def StartScanIdThread(self):
        # Starting a thread to read id parallel to showing the screen
        print("Starting Id Thread")
        self.timeEnd = datetime.now() + timedelta(seconds=10)
        
        self.thread = threading.Thread(target=self.rfidManager.ScanId)
        self.thread.daemon = True 
        self.thread.start()
        
        
    def ScanId(self, route: int):
        print("Updating ScanId")
        if self.rfidManager.userId != None:
            self.userId = self.rfidManager.userId
            
            # Checking if the user id was valid
            if self.userId == "0":
                self.SelectMessageFrame(0)          # Timeout
                return
            
            isUser = self.databaseHandler.ScanUserId(self.userId)

            # Checking which window this request came from and routing accordingly
            if route == 0:
                if(self.rfidManager.CheckPermission(self.userId)):
                    self.SelectSettingsFrame()
                    return
                self.SelectMessageFrame(6)          # Permission Denied
            elif route == 1:
                if isUser == True:
                    self.SelectMessageFrame(1)          # User Id already logged in
                    return
                self.SelectEntryFrame()
            elif route == 2:
                if isUser:
                    self.databaseHandler.DeleteEntry(self.userId)
                    self.UpdateDefaultScreen(False)
                    self.SelectMessageFrame(3)                      # Sucessfully Logged out
                else:
                    self.SelectMessageFrame(8)                      # If user is not logged in
            
        
        if datetime.now() >= self.timeEnd:
            if not self.thread.is_alive:
                self.SelectMessageFrame(0)          # Timeout
                return
            
            self.SelectMessageFrame(0)
            return
        
        self.after(1000, lambda: self.ScanId(route))
            
        
        
    #########################
    #                       #
    #      Entry Screen     #
    #                       #
    #########################
        
    def EntryScreen(self):
        self.entryFrame = tk.Frame(self)
        mainPanel = tk.Frame(self.entryFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        mainPanel.pack(fill=tk.BOTH, expand=True)

        # Displaying Titlebar in the main Panel
        title = tk.Label(mainPanel, text="Einloggen", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        title.pack(side="top", fill="x")
        
        
        # Creating and Dividing a panel with buttons to choose if the user wants the room to be loud or quiet
        roomTypePanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        roomTypePanel.place(relx=0.025, rely=0.2, relwidth=0.95, relheight=0.15)
        
        leftRoomTypePanel = tk.Frame(roomTypePanel, bg=self.GRAY)
        leftRoomTypePanel.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        rightRoomTypePanel = tk.Frame(roomTypePanel, bg=self.GRAY)
        rightRoomTypePanel.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)
        
        # Heading that is placed left to the buttons
        roomTypeHeading = tk.Label(leftRoomTypePanel, text="Lernart", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        roomTypeHeading.pack(side="left", fill="x", padx=self.borderSize*5)
        
        # Buttons to either choose a loud room or quiet room
        self.loudBtn = tk.Button(rightRoomTypePanel, text="Laut", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryRoomState(self.loudBtn, "Loud"))
        self.loudBtn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.quietBtn = tk.Button(rightRoomTypePanel, text="Leise", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryRoomState(self.quietBtn, "Quiet"))
        self.quietBtn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        
        # Creating and Dividing a panel with buttons to choose how many minutes the user plans to stay in the room
        durationPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        durationPanel.place(relx=0.025, rely=0.4, relwidth=0.95, relheight=0.3)
        
        leftDurationPanel = tk.Frame(durationPanel, bg=self.GRAY)
        leftDurationPanel.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        rightTopDurationPanel = tk.Frame(durationPanel, bg=self.GRAY)
        rightTopDurationPanel.place(relx=0.35, rely=0, relwidth=0.65, relheight=0.5)
        
        rightBotDurationPanel = tk.Frame(durationPanel, bg=self.GRAY)
        rightBotDurationPanel.place(relx=0.35, rely=0.5, relwidth=0.65, relheight=0.5)
        
        # Heading that is placed left to the buttons
        durationHeading = tk.Label(leftDurationPanel, text="Lerndauer", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        durationHeading.pack(side="left", fill="x", padx=self.borderSize*5)
        
        # Buttons to choose how long the user expect to be in the room
            # top row
        self.t15Btn = tk.Button(rightTopDurationPanel, text="15 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t15Btn, 15))
        self.t15Btn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.t30Btn = tk.Button(rightTopDurationPanel, text="30 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t30Btn, 30))
        self.t30Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        self.t45Btn = tk.Button(rightTopDurationPanel, text="45 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t45Btn, 45))
        self.t45Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
            # bottom row
        self.t60Btn = tk.Button(rightBotDurationPanel, text="60 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t60Btn, 60))
        self.t60Btn.pack(side="left", padx=self.borderSize*5, anchor="center")

        self.t75Btn = tk.Button(rightBotDurationPanel, text="75 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t75Btn, 75))
        self.t75Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        self.t90Btn = tk.Button(rightBotDurationPanel, text="90 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateEntryDuration(self.t90Btn, 90))
        self.t90Btn.pack(side="left", padx=self.borderSize*5, anchor="center")
        
        
        # Buttons that lets the user confirm or deny his decision
        btnPanel = tk.Frame(mainPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        entryConfirmBtn = tk.Button(btnPanel, text="BESTÄTIGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.LoginEntry())
        entryConfirmBtn.pack(side="left", padx=self.borderSize*5)

        denyBtn = tk.Button(btnPanel, text="ABBRECHEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectMessageFrame(4))
        denyBtn.pack(side="left", padx=self.borderSize*5)
        
    
    def InitializeEntryScreen(self):
        # Reset old state
        self.EnableAllEntryStateBtns()
        self.EnableAllEntryDurationBtns()
    
        # Checking if the current room state is not empty. If not preselecting quiet learning
        self.quietBtn.config(state="disabled")
        if self.roomState != "Empty":
            self.loudBtn.config(state="disabled")
            self.newRoomState = self.roomState
        else:
            self.loudBtn.config(state="normal")
            self.newRoomState = "Quiet"
            
        # Preselecting 15 minutes
        self.t15Btn.config(state="disabled")
        self.duration = 15
        
    
    def UpdateEntryDuration(self, btn: tk.Button, value: int):
        self.EnableAllEntryDurationBtns()
        btn.config(state="disabled")
        self.duration = value
        
    
    def EnableAllEntryDurationBtns(self):
        self.t15Btn.config(state="normal")
        self.t30Btn.config(state="normal")
        self.t45Btn.config(state="normal")
        self.t60Btn.config(state="normal")
        self.t75Btn.config(state="normal")
        self.t90Btn.config(state="normal")
        
    
    def UpdateEntryRoomState(self, btn: tk.Button, value:str):
        self.EnableAllEntryStateBtns()
        
        self.newRoomState = value
        btn.config(state="disabled")
        
        
    def EnableAllEntryStateBtns(self):
        self.loudBtn.config(state="normal")
        self.quietBtn.config(state="normal")
        
        
    def LoginEntry(self):
        print("Login Entry")
        self.databaseHandler.AddEntry(self.userId, datetime.now(), datetime.now() + timedelta(minutes=self.duration))
        self.databaseHandler.SetProperty("roomState", self.newRoomState)
        
        self.SelectMessageFrame(2)
        self.UpdateDefaultScreen(False)

        
        
    #########################
    #                       #
    #    Settings Screen    #
    #                       #
    #########################
        
    def SettingsScreen(self):
        self.settingsFrame = tk.Frame(self)
        mainPanel = tk.Frame(self.settingsFrame, bg=self.CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        mainPanel.pack(fill=tk.BOTH, expand=True)

        # Displaying Titlebar in the main Panel
        title = tk.Label(mainPanel, text="Settings", font=(self.FONT, self.h1Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        title.pack(side="top", fill="x")


        # Creating and Dividing a panel with buttons to change the maximum of loud seats in the room
        loudMaxPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        loudMaxPanel.place(relx=0.025, rely=0.128, relwidth=0.95, relheight=0.15)

        leftLoudMaxPanel = tk.Frame(loudMaxPanel, bg=self.GRAY)
        leftLoudMaxPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        rightLoudMaxPanel = tk.Frame(loudMaxPanel, bg=self.GRAY)
        rightLoudMaxPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # Heading that is placed left to the buttons and current capacity of loud seats next to it
        loudMaxHeading = tk.Label(leftLoudMaxPanel, text="Laute Plätze", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        loudMaxHeading.pack(side="left", fill="x", padx=self.borderSize*5)

        self.currLoudMaxLabel = tk.Label(rightLoudMaxPanel, text="8", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*10, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.currLoudMaxLabel.pack(side="left", padx=[self.borderSize*2.5, self.borderSize*15], anchor="center")
        
        # Buttons to add and subtract from the current loud seat capacity
        addLoudMaxBtn = tk.Button(rightLoudMaxPanel, text="+", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateLoudMaxSettings(1))
        addLoudMaxBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        retractLoudMaxBtn = tk.Button(rightLoudMaxPanel, text="-", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateLoudMaxSettings(-1))
        retractLoudMaxBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # Creating and Dividing a panel with buttons to change the maximum of quiet seats in the room
        quietMaxPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        quietMaxPanel.place(relx=0.025, rely=0.30, relwidth=0.95, relheight=0.15)

        leftQuietMaxPanel = tk.Frame(quietMaxPanel, bg=self.GRAY)
        leftQuietMaxPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        rightQuietMaxPanel = tk.Frame(quietMaxPanel, bg=self.GRAY)
        rightQuietMaxPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # Heading that is placed left to the buttons and current capacity of quiet seats next to it
        quietMaxHeading = tk.Label(leftQuietMaxPanel, text="Leise Plätze", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        quietMaxHeading.pack(side="left", fill="x", padx=self.borderSize*5)

        self.currQuietMaxLabel = tk.Label(rightQuietMaxPanel, text="2", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*10, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        self.currQuietMaxLabel.pack(side="left", padx=[self.borderSize*2.5, self.borderSize*15], anchor="center")
        
        # Buttons to add and subtract from the current quiet seat capacity
        addQuietMaxBtn = tk.Button(rightQuietMaxPanel, text="+", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateQuietMaxSettings(1))
        addQuietMaxBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        redactQuietMaxBtn = tk.Button(rightQuietMaxPanel, text="-", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateQuietMaxSettings(-1))
        redactQuietMaxBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # Creating and Dividing a panel with buttons to block the room for admin use
        blockPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        blockPanel.place(relx=0.025, rely=0.47, relwidth=0.95, relheight=0.15)

        leftBlockPanel = tk.Frame(blockPanel, bg=self.GRAY)
        leftBlockPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        rightBlockPanel = tk.Frame(blockPanel, bg=self.GRAY)
        rightBlockPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # Heading that is placed left to the buttons
        blockHeading = tk.Label(leftBlockPanel, text="Raum blockieren", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        blockHeading.pack(side="left", fill="x", padx=self.borderSize*5)

        # Buttons that let the user choose how much time he wants to block the room from ther usage      
        self.t30BlockBtn = tk.Button(rightBlockPanel, text="30 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateSettingsDuration(self.t30BlockBtn, 30))
        self.t30BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.t60BlockBtn = tk.Button(rightBlockPanel, text="60 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateSettingsDuration(self.t60BlockBtn, 60))
        self.t60BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        self.t90BlockBtn = tk.Button(rightBlockPanel, text="90 min", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 2.5), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateSettingsDuration(self.t90BlockBtn, 90))
        self.t90BlockBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # Creating and Dividing a panel with buttons to shutdown the whole system
        shutdownPanel = tk.Frame(mainPanel, bg=self.GRAY, highlightbackground="White", highlightthickness=self.borderSize)
        shutdownPanel.place(relx=0.025, rely=0.64, relwidth=0.95, relheight=0.15)

        leftShutdownPanel = tk.Frame(shutdownPanel, bg=self.GRAY)
        leftShutdownPanel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        rightShutdownPanel = tk.Frame(shutdownPanel, bg=self.GRAY)
        rightShutdownPanel.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # Heading that is placed left to the buttons
        shutdownHeading = tk.Label(leftShutdownPanel, text="Herunterfahren", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize*15, pady=self.borderSize, bg=self.DARK_GRAY, fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        shutdownHeading.pack(side="left", fill="x", padx=self.borderSize*5)

        # Buttons that let the user choose if They want to shutdown the system
        self.yShutdownBtn = tk.Button(rightShutdownPanel, text="Ja", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateShutdownBtn(self.yShutdownBtn, True))
        self.yShutdownBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")

        self.nShutdownBtn = tk.Button(rightShutdownPanel, text="Nein", font=(self.FONT, self.btn2Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.UpdateShutdownBtn(self.nShutdownBtn, False))
        self.nShutdownBtn.pack(side="left", padx=self.borderSize*2.5, anchor="center")
        
        
        # Buttons that lets the user confirm or deny his decision
        btnPanel = tk.Frame(mainPanel, bg=self.CYAN)
        btnPanel.pack(side="bottom", pady=self.borderSize*10)

        settingsConfirmBtn = tk.Button(btnPanel, text="BESTÄTIGEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.ConfirmSettings())
        settingsConfirmBtn.pack(side="left", padx=self.borderSize*5)

        denyBtn = tk.Button(btnPanel, text="ABBRECHEN", font=(self.FONT, self.btn1Size, "bold"), padx=(self.borderSize * 10), fg="White", bg=self.DARK_CYAN, bd=self.borderSize, relief="solid", command=lambda: self.SelectMessageFrame(4))
        denyBtn.pack(side="left", padx=self.borderSize*5)
        
        
    def InitializeSettingsScreen(self):
        # Reset old state
        self.EnableSettingsShutdownBtns()
        self.EnableSettingsDurationBtns()
        self.blockDuration = 0
        
        # Setting Label in loud and quiet max seats
        self.currLoudMax = self.databaseHandler.GetProperty("loudSeats")
        self.currQuietMax = self.databaseHandler.GetProperty("quietSeats")
        self.currLoudMaxLabel.config(text=self.currLoudMax)
        self.currQuietMaxLabel.config(text=self.currQuietMax)
        
        # Setting Shutdown to No
        self.nShutdownBtn.config(state="disabled")
        self.shutdown = False
        
    
    def UpdateLoudMaxSettings(self, value: int):
        self.currLoudMax += value
        self.currLoudMaxLabel.config(text=self.currLoudMax)
        
        
    def UpdateQuietMaxSettings(self, value: int):
        self.currQuietMax += value
        self.currQuietMaxLabel.config(text=self.currQuietMax)
        
    
    def UpdateSettingsDuration(self, btn: tk.Button, value: int):
        self.EnableSettingsDurationBtns()
        btn.config(state="disabled")
        self.blockDuration = value
        
    
    def EnableSettingsDurationBtns(self):
        self.t30BlockBtn.config(state="normal")
        self.t60BlockBtn.config(state="normal")
        self.t90BlockBtn.config(state="normal")
        
        
    def UpdateShutdownBtn(self, btn: tk.Button, value: bool):
        self.EnableSettingsShutdownBtns()
        
        btn.config(state="disabled")
        self.shutdown = value
        
        
    def EnableSettingsShutdownBtns(self):
        self.yShutdownBtn.config(state="normal")
        self.nShutdownBtn.config(state="normal")
        
    
    def ConfirmSettings(self):
        print("Confirming Settings")
        if self.shutdown:
            self.databaseHandler.Logout()
            self.destroy()
            return
        
        # Set loud and quiet seats
        self.databaseHandler.SetProperty("loudSeats", self.currLoudMax)
        self.databaseHandler.SetProperty("quietSeats", self.currQuietMax)
        
        # Check if the user wants to block the room. If yes delete all entries, and add an entry from said user
        if self.blockDuration > 0:
            self.databaseHandler.SetProperty("roomState", "Blocked")
            self.databaseHandler.DeleteAllEntries()

            self.databaseHandler.AddEntry(self.userId, datetime.now(), datetime.now() + timedelta(minutes=self.blockDuration))
            self.SelectMessageFrame(10)
        else:
            self.SelectMessageFrame(9)
            
        self.UpdateDefaultScreen(False)

    
    
    #########################
    #                       #
    #     Message Screen    #
    #                       #
    #########################
        
    def MessageScreen(self):
        self.messageFrame = tk.Frame(self)
        mainPanel = tk.Frame(self.messageFrame, bg=self.DARK_CYAN, highlightbackground="White", highlightthickness=self.borderSize)
        mainPanel.pack(fill=tk.BOTH, expand=True)

        # Displaying Message
        self.message = tk.Label(mainPanel, text="Erfolgreich eingeloggt. Bitte loggen Sie sich wieder aus, wenn Sie den Raum verlassen.", font=(self.FONT, self.h2Size, "bold"), padx=self.borderSize, pady=self.borderSize, bg=self.DARK_CYAN, fg="White", justify="center")
        self.message.bind('<Configure>', lambda e: self.message.config(wraplength=self.message.winfo_width()*0.9))
        self.message.place(relx=0, rely=0, relwidth=1, relheight=1)
        
    
    def UpdateMessageScreen(self, route: int):
        print("Updating Message Screen")
        if route == 0:
            self.message.config(text="Die vorgegebene Zeit für den ID-Scan ist abgelaufen, und es wurde keine Hochschul-ID erkannt.")
        elif route == 1:
            self.message.config(text="Sie sind bereits in diesem Raum eingeloggt und können daher keine erneute Buchung vornehmen.")
        elif route == 2:
            self.message.config(text="Erfolgreich eingeloggt. Bitte loggen Sie sich wieder aus, wenn Sie den Raum verlassen.")
        elif route == 3:
            self.message.config(text="Erfolgreich ausgeloggt.")
        elif route == 4:
            self.message.config(text="Vorgang wurde abgebrochen.")
        elif route == 5:
            self.message.config(text="Vorgang wurde durch Zeitüberschreitung beim Anmelden abgebrochen.")
        elif route == 6:
            self.message.config(text="Sie haben keine Berechtigung, diese Tür zu verwalten.")
        elif route == 7:
            self.message.config(text="Vorgang wurde durch Zeitüberschreitung beim Anmelden abgebrochen.")
        elif route == 8:
            self.message.config(text="Sie sind nicht in diesem Raum eingeloggt.")
        elif route == 9:
            self.message.config(text="Tür Eigenschaften erfolgreich geändert.")
        elif route == 10:
            self.message.config(text="Raum erfolgreich blockiert.")
                
        # Wait 3 seconds and then go back to the default screen
        self.after(3000, lambda: self.SelectDefaultFrame())



#########################
#                       #
#         Main          #
#                       #
#########################
        
def main():
    root = Win()    
    root.mainloop()


if __name__ == "__main__":
    main()