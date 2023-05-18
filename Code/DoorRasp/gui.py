import os
import numpy as np

import tkinter as tk

from PIL import ImageTk, Image
from screeninfo import get_monitors
from time import strftime


class Win(tk.Tk):
    FONT = "Arial"
    
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
        self.h1Size = round(self.screenWidth / 70)
        
        # giving the programm an escape ;)    
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        
        # Loading in Background Image       
        self.bgCanvas = tk.Canvas(self, bg='SkyBlue4', highlightthickness=0)        
        self.bgCanvas.pack(fill=tk.BOTH, expand=True)
        
        bgImg = Image.open("Assets\Background2.png")
        bgImg = bgImg.resize((self.screenWidth, self.screenHeight), Image.LANCZOS)
        bgImg = ImageTk.PhotoImage(bgImg)
        
        bgImgPanel = tk.Label(self.bgCanvas, image=bgImg)
        bgImgPanel.image = bgImg
        bgImgPanel.place(x=-2, y=-2)
        
        
        # Clock Bottom Left        
        clockPanel = tk.Frame(self.bgCanvas, background="White")

        self.clock = tk.Label(clockPanel, text=" 00:00 ", font=(self.FONT, self.h1Size, "bold"), bg="#a6a7a9", fg="White")
        self.clock.pack(padx=self.borderSize, pady=self.borderSize)
        
        clockPanel.pack(anchor="sw", side="bottom", padx=(self.screenWidth / 75), pady=(self.screenHeight / 50))
        self.UpdateClock()
        
        # start with default panel
        self.DefaultPanel()



    def UpdateClock(self):                              # takes the clock on the bottom left and updates it every second
        time = strftime(' %H:%M ')                      #add %A for weekday name
        self.clock.config(text=time)
        self.after(1000, self.UpdateClock)
        
        
        
    def DefaultPanel(self):
        # sets the main panel in place
        defaultPanel = tk.Frame(self.bgCanvas, background="Gray", highlightbackground="White", highlightthickness=self.borderSize)
        defaultPanel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)

        # heading of the panel
        label1 = tk.Label(defaultPanel, text="C125 - Leise - 5/7", font=(self.FONT, self.h1Size, "bold"), padx=5, pady=5, bg="Green", fg="White", highlightbackground="White", highlightthickness=self.borderSize)
        label1.pack(side="top", fill="x")


        # buttons on the bottom
        buttonFrame = tk.Frame(defaultPanel, bg="Gray")
        buttonFrame.pack(side="top", pady=10)

        button1 = tk.Button(buttonFrame, text="Button 1", fg="White", bg="Blue")
        button1.pack(side="left", padx=5)

        button2 = tk.Button(buttonFrame, text="Button 2", fg="White", bg="Blue")
        button2.pack(side="left", padx=5)




def main():
    root = Win()    
    root.mainloop()


if __name__ == "__main__":
    main()