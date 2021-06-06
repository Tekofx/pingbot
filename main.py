import os, sys
from dotenv import load_dotenv
import setproctitle
import subprocess
from discord.ext import commands, tasks
from discord.ext.commands import bot
import logging


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')
setproctitle.setproctitle("pingbot") # <-- setting the process name

def setupLogs():
    logging.basicConfig(filename="logs",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    logging.info("\n\n\n\n\n\nRunning Pingbot")


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    setupLogs()


@bot.event
async def on_message(message):
    if message.content.lower()=='ping':
        logging.info(str(message.author)+' used command ping')
        tmp = await message.channel.send('Comprobando ping...')


        with open('network.txt') as f:
            host = f.readline().rstrip()
            port = f.readline()

        # ping to host
        stream= os.popen('ping -c 1 {}'.format(host)) 
        output = stream.read()

        # Check if server is accesible, if not dont check the port
        if "Unreachable" in str(output):
            status="El server no está operativo"
            logging.info("Server is not accessible")
            await tmp.edit(content=status)

        else: 
            logging.info("Server is accesible")
            result = subprocess.check_output("nmap -p "+port +" "+host, shell=True)

            if 'open' in str(result) :
                status = "El server está abierto"
                logging.info("Server and port open")
            else:
                status = "El server no está operativo"
                logging.info("Port closed")


            await tmp.edit(content=status)

   

bot.run(TOKEN)




