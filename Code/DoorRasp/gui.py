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

        self.clock = tk.Label(clockPanel, text=" 00:00 ", font=(self.FONT, round(self.screenWidth / 70), "bold"), bg="#a6a7a9", fg="White")
        self.clock.pack(padx=(self.screenWidth / 512), pady=(self.screenWidth / 512))
        
        clockPanel.pack(anchor="sw", side="bottom", padx=(self.screenWidth / 75), pady=(self.screenHeight / 50))
        self.UpdateClock()
        
        # start with default panel
        self.DefaultPanel()



    def UpdateClock(self):                              # takes the clock on the bottom left and updates it every second
        time = strftime(' %H:%M ')                      #add %A for weekday name
        self.clock.config(text=time)
        self.after(1000, self.UpdateClock)
        
        
        
    def DefaultPanel(self):
        defaultPanel = tk.Frame(self.bgCanvas, background="White")

        defaultGrid = tk.Frame(defaultPanel, background="Blue")
        defaultGrid.grid(row=5, column=0, sticky=tk.W+tk.E)

        # Add widgets to the grid
        label1 = tk.Label(defaultGrid, text="C125 - Leise - 5/7", font=(self.FONT, round(self.screenWidth / 70), "bold"), padx=5, pady=5, bg="Green", fg="White")
        label1.grid(row=0, column=0)

        label2 = tk.Label(defaultGrid, text="Label 2")
        label2.grid(row=1, column=0)

        label3 = tk.Label(defaultGrid, text="Label 3")
        label3.grid(row=1, column=0, columnspan=2)

        defaultPanel.pack(side="top", pady=200)



def main():
    root = Win()    
    root.mainloop()


if __name__ == "__main__":
    main()