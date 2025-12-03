# better than a .sh file?
import os
if os.system('wl-paste > input') == 0:
    print("wrote clipboard to file ./input")
