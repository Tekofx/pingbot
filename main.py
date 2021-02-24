import discord
import os, sys
from dotenv import load_dotenv
import setproctitle
import subprocess
import socket
from discord.ext import commands, tasks
from discord.ext.commands import bot
import logging


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNELID=os.getenv('CHANNEL')

bot = commands.Bot(command_prefix='.')
setproctitle.setproctitle("pingbot") # <-- setting the process name

global channel
serverOpen=True
path = os.path.dirname(sys.argv[0])




@tasks.loop(seconds=2)
async def checkServerStatus():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNELID))
    global serverOpen

    with open(path+'network.txt') as f:
        host = f.readline().rstrip()
        if host.upper().isupper():
            host=socket.gethostbyname(host)
        port = f.readline()
        
    result = subprocess.check_output("nmap -p "+ port+" " +host, shell=True)


    if 'open' in str(result) and not serverOpen: #Server becomes accesible
        serverOpen = True
        logging.info("El server está abierto")
        await channel.send("El server está abierto")
        
        
    if 'open' in str(result)  and serverOpen: # Server keeps accessible
        pass

    if 'closed' in str(result)  and serverOpen: # Server becomes inaccesible
        serverOpen = False
        logging.info("El server no está operativo")

        await channel.send("El server no está operativo")


    if 'closed' in str(result) and not serverOpen: # Server still inaccessible
        pass



def setupLogs():
    os.system("rm "+path+"logs")
    logging.basicConfig(filename="logs",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    logging.info("Running Pingbot")








@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    setupLogs()

    serverOpen=True
    checkServerStatus.start()






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

   

bot.run(TOKEN)




