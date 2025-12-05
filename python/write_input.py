# better than a .sh file?
import os

system = os.getenv("DESKTOP_SESSION")
if system is None:
    system = ""

copier = ""
if "wayland" in system:
    copier = "wl_paste"
elif "xorg" in system:
    copier = "xsel -b"
else:
    print("Not sure what command to use to copy the clipboard in your operating system")
    print("Edit the write_input.py file to accomodate")
    exit()


if os.system(f'{copier} > input') == 0:
    print("wrote clipboard to file ./input")
