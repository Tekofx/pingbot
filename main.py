import discord
import os
from dotenv import load_dotenv
import socket
import nmap
import setproctitle


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Client()
setproctitle.setproctitle("pingbot") # <-- setting the process name




""" async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(792726813600251914)
    status='True'
    while True:
        with open('ip.txt') as f:
            hostname = f.readline()
        
        response = os.system("ping -c 1 " + hostname)

        if response == 0 and status=='False': #Server becomes accesible
            status = "True"
            
        if response == 0 and status=='True': # Server keeps accessible
            break

        if response==1 and status=='True': # Server becomes inaccesible
            status = "False"

        if response==1 and status=='True': # Server still inaccessible
            break

        await channel.send('uwu')
        await asyncio.sleep(2) # task runs every 60 seconds


 """





@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')



@bot.event
async def on_message(message):
    if message.content.lower()=='ping':
        with open('network.txt') as f:
            host = f.readline().rstrip()
            if host.upper().isupper():
                host=socket.gethostbyname(host)
            port = f.readline()

        nm = nmap.PortScanner()
        nm.scan(host, port)
        result =nm[host]['tcp'][int(port)]['state']

        if 'open' in str(result) :
            status = "El server está abierto"
        else:
            status = "El server no está operativo"

        await message.channel.send(status)



bot.run(TOKEN)




