import os, sys
from dotenv import load_dotenv
import setproctitle
import subprocess
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import bot
import logging
import re


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


def check_if_string_in_file(file_name: str, string: str):
    """Checks if string is contained as line in file_name

    Args:
        file_name (str]): file to check
        string (str): string to search

    Returns:
        bool: True if string is in file_name, False if not
    """
    with open(file_name, "r") as file:
        for line in file:
            if string in line:
                return True
    return False

def rewrite_contents_of_file(file_name:str,string:str):
    with open(file_name, "w") as file:
        file.truncate()
        file.write(string)
        file.close()

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

            # Write to file
            rewrite_contents_of_file("status.txt", "offline")

            tmp2=await message.channel.send("Comprobando si se ha cambiado la ip...")

            stream= os.popen('ping -c 1 fordfairlane2.ddns.net') 
            output = stream.read()

            ip_address = re.search('.net ((.*)) 56', output)
            ip_address=str(ip_address.group(1))
            ip_address=ip_address.replace('(','')
            ip_address=ip_address.replace(')','')

            if check_if_string_in_file("ip.txt",ip_address):
                await tmp2.edit(content="La ip no ha cambiado, sigue siendo: "+ ip_address+":"+port)

            else:
                await tmp2.edit(content="La nueva ip es: "+ip_address+":"+port)
                rewrite_contents_of_file("ip.txt",ip_address)


        else: 
            logging.info("Server is accesible")
            result = subprocess.check_output("nmap -p "+port +" "+host, shell=True)


            if 'open' in str(result) :
                status = "El server está abierto. La ip y puerto es: "+host+":"+port
                logging.info("Server and port open")
                rewrite_contents_of_file("status.txt", "online")

            else:
                status = "El server no está operativo"
                logging.info("Port closed")
                rewrite_contents_of_file("status.txt", "offline")



            await tmp.edit(content=status)




   



bot.run(TOKEN)




