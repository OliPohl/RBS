import os
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors


class Win(tk.Tk):
    FONT = "Arial"
    LABEL_SIZE = 20
    TEXT_SIZE = 16
    TIME_SIZE = 37
    
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
                # self.screenWidth = 1920
                # self.screenHeight = 1080
                self.screenX = monitor.x
                self.screenY = monitor.y
                self.geometry(('{w}x{h}+{x}+{y}'.format(w=self.screenWidth, h=self.screenHeight, x=self.screenX, y=self.screenY)))
                break
            
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        # Background        
        bgCanvas = tk.Canvas(self, bg='SkyBlue4', highlightthickness=0)        
        bgCanvas.pack(fill=tk.BOTH, expand=True)
        
        # Loading in Background Image
        bgImg = Image.open("Assets\Background.png")
        bgImg = bgImg.resize((self.screenWidth, self.screenHeight), Image.LANCZOS)
        bgImg = ImageTk.PhotoImage(bgImg)
        
        bgImgPanel = tk.Label(bgCanvas, image=bgImg)
        bgImgPanel.image = bgImg
        bgImgPanel.place(x=-2, y=-2)
        
        # Timer Bottom Left
        time = tk.Label(bgCanvas, text="00:00", font=(self.FONT, self.TIME_SIZE, "bold"), bg="#a6a7a9", fg="White")
        time.pack(anchor="sw", side="bottom", pady=self.screenWidth/49.2, padx=self.screenHeight/16)



    def DefaultScreen(self):
        pass



def main():
    root = Win()
    
    root.DefaultScreen()
    
    root.mainloop()


if __name__ == "__main__":
    main()