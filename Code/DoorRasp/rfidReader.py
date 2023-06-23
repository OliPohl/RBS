import time
import random

class RfidReader:    
    def __init__(self) -> None:
        self.userId = None
    
    
    def ReadId(self):
        self.userId = None
        
        timeEnd = time.time() + 5
        while time.time() < timeEnd:
            i = random.randrange(10000)
            if(i == 5):
                self.userId = "Oli123"
                return
            
        self.userId = "0"
        return
    
    
    def GotPermission(self, userId):
        i = random.randrange(2)
        i = 0
        
        if(i == 0):
            return True
        return False