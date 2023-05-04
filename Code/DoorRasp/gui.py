import os
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors


class Win(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, None)
        
        self.overrideredirect(True)                     # removes titlebar
        self.resizable(False, False)                    # makes window unsizeable
        self.attributes('-topmost', True)               # makes window always ontop
        
        self.config(bg='SkyBlue4')                      # sets backgroundcolor
        
        for monitor in get_monitors():                  # finds main monitor and saves screenSize
            if monitor.is_primary:
                self.geometry(('{w}x{h}'.format(w=monitor.width, h=monitor.height)))
                break
        
        self.bind('<Escape>', lambda e: self.destroy())         # close window on esc


def main():
    root = Win()

    root.mainloop()


if __name__ == "__main__":
    main()
