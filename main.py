import discord
import os, sys
from dotenv import load_dotenv
import setproctitle
import subprocess
import socket
from discord.ext import commands, tasks
from discord.ext.commands import bot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')
setproctitle.setproctitle("pingbot") # <-- setting the process name

channel = bot.get_channel(790955067414151188)
serverOpen=True
path = os.path.dirname(sys.argv[0])




@tasks.loop(minutes=1)
async def change_status():
    await bot.wait_until_ready()
    channel = bot.get_channel(790955067414151188)
    global serverOpen

    with open(path+'network.txt') as f:
        host = f.readline().rstrip()
        if host.upper().isupper():
            host=socket.gethostbyname(host)
        port = f.readline()
        
    result = subprocess.check_output("nmap -p "+ port+" " +host, shell=True)


    if 'open' in str(result) and not serverOpen: #Server becomes accesible
        serverOpen = True
        await channel.send("El server está abierto")
        
        
    if 'open' in str(result)  and serverOpen: # Server keeps accessible
        pass

    if 'closed' in str(result)  and serverOpen: # Server becomes inaccesible
        serverOpen = False
        await channel.send("El server no está operativo")

    if 'closed' in str(result) and not serverOpen: # Server still inaccessible
        pass










@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    serverOpen=True
    change_status.start()






@bot.event
async def on_message(message):
    if message.content.lower()=='ping':
        with open('network.txt') as f:
            host = f.readline().rstrip()
            if host.upper().isupper():
                host=socket.gethostbyname(host)
            port = f.readline()


        
        result = subprocess.check_output("nmap -p 46570 firewolfnetwork.com", shell=True)
        print(result)

        if 'open' in str(result) :
            status = "El server está abierto"
        else:
            status = "El server no está operativo"

        await message.channel.send(status)

   

""" bot.loop.create_task(my_background_task()) """
bot.run(TOKEN)




