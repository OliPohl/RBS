import os
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors


class Win(tk.Tk):
    FONT = "Arial"
    LABEL_SIZE = 20
    TEXT_SIZE = 16
    
    TRIANGLES_SIZE = 800
    
    def __init__(self):
        tk.Tk.__init__(self, None)

        self.title("RAC RBS")                           # changes title
        self.overrideredirect(True)                     # removes titlebar
        self.resizable(False, False)                    # makes window unsizeable
        self.attributes('-topmost', True)               # makes window always ontop
        
        for monitor in get_monitors():                  # finds main monitor and saves screenSize
            if monitor.is_primary:
                self.geometry(('{w}x{h}+{x}+{y}'.format(w=monitor.width, h=monitor.height, x=monitor.x, y=monitor.y)))
                self.screenWidth = monitor.width
                self.screenHeight = monitor.height
                break
            
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc
        
        # Background        
        bgCanvas = tk.Canvas(self, bg='SkyBlue4', highlightthickness=0)        
        bgCanvas.pack(fill=tk.BOTH, expand=True)
        
        # create the rectangles on the top right and bottom left edges of the screen
        bgCanvas.create_polygon([self.screenWidth, 0, self.screenWidth, self.TRIANGLES_SIZE/2, self.screenWidth - self.TRIANGLES_SIZE, 0], fill="Light Blue")
        bgCanvas.create_polygon([0, self.screenHeight, self.TRIANGLES_SIZE, self.screenHeight, 0, self.screenHeight - self.TRIANGLES_SIZE/2], fill="Light Blue")
        
        # logo
        logo = Image.open("Assets\Logo.png")
        logo = logo.resize((570, 160), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        
        logoPanel = tk.Label(bgCanvas, image=logo)
        logoPanel.image = logo
        logoPanel.place(x=self.screenWidth - 5, y=5, anchor="ne")






    def DefaultScreen(self):
        pass



def main():
    root = Win()
    # root.wm_attributes('-transparentcolor', root['bg'])
    
    root.DefaultScreen()
    
    root.mainloop()


if __name__ == "__main__":
    main()