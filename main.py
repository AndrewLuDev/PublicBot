import discord
import asyncio
import os
from replit import db

from keepAlive import keepAlive
from emotes import *
from extraCommands import *
from lostark import *
from messages import *


from datetime import datetime
from pytz import timezone

import random

friendsIds = {}
friendsList = []

##########################################################################################
#  TO DO:
#############################################
#  add !help function
#  add !lostark command
#  change format of db (emotes)
##########################################################################################

for userInfo in os.getenv('friendsList').split(", "):
    #friendsIds format:
    #name1: id1, name2: id2, name3: id3, etc.
    userInfo = userInfo.split(': ')
    friendsList.append(userInfo[0])
    friendsIds[userInfo[0]] = int(userInfo[1])

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        msg = message.content
        msgID = message.author.id
        msgArgs = msg.split()

        #################################################################
        #logs messages into the console (as a temporary audit log)
        # t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        # print(current_time, message.author.name + '#' + message.author.discriminator, ': ', message.content)
        tz = timezone("US/Eastern")
        date = datetime.now(tz)

        current_time = date.strftime("%h %d %Y %I:%M%p")
        print(current_time,
              message.author.name + '#' + message.author.discriminator, ': ',
              message.content)
        #################################################################
        #print(len(db))
        defaultLostArkDict = {"default":
          {
          "name": "name",
          "role": "role",
          }
        }

        if "lostark" not in db.keys():
          db["lostark"] = {
            "run": defaultLostArkDict,
            "dontrun": defaultLostArkDict,
          }
        if "emotes" not in db.keys():
          db["emotes"] = {}

      
        #admin-specific commands
        deleteCheck = False

        if msgID in friendsIds.values():
          if msg.startswith("!add "):
            await addEmote(message, msg, msgID, msgArgs)

          elif msg.startswith("!remove "):
            await removeEmote(message, msg, msgID, msgArgs)

          elif msg.lower() == "!clear emotes":
            await clearAllEmotes(message)

          elif len(msgArgs) >= 2:
            if msg.startswith("!del "):
                deleteCheck = True
                await deleteMsg(message, msg, msgID, msgArgs)

        #commands all members can use
        if msg.startswith("!pfp"):
          await getAvatar(message, msgArgs)
        elif msg == "!emotes":
          await listAllEmotes(message)
        elif msg.startswith("!e ") and len(msgArgs) == 2:
          #format of emote: <:emoteName:emoteID>
          msgArgs = msgArgs[1].lower().replace('<', '').replace('>', '').replace(':', '', 1)
          if ':' in msgArgs:
            msgArgs = msgArgs.split(':')
            await sendEmote(message, msg, msgID, msgArgs[0])
          else:
            await sendEmote(message, msg, msgID, msgArgs)
        elif msg.startswith("!gif"):
          await sendGif(message)
        elif msg.startswith("!del") and ("me" in msg) and (deleteCheck == False):
          await deleteMsg(message, msg, msgID, msgArgs)

        elif msg.startswith("!poll"):
          await createPoll(message)

        # elif msg.startswith("!faketest"):
        #   emotesList = list(db.keys())
        #   tempList = []
        #   for emoteName in emotesList:
        #     emote = emoteName + " " + db["emotes"][emoteName]
        #     tempList.append(emote)
        #   tempList = ", ".join(tempList)
        #   await message.channel.send(tempList)

        elif msg.startswith("!fake"):
          await message.channel.send(db["emotes"])
        elif msg.startswith("clear"):
          db.clear()
        
        if len(db) == 0:
          db["lostark"] = {
            "run": defaultLostArkDict,
            "dontrun": defaultLostArkDict,
          }
        
        if msgArgs[0] == "!lostark":
          await lostark(message)
        
        if msgArgs[0] == "!run":
          await lostarkrun(message)
        
        if msgArgs[0] == "!dontrun":
          await lostarkdontrun(message)
        
        if msgArgs[0] == "!runadd":
          await runadd(message, msgArgs)
          
        if msgArgs[0] == "!runremove":
          await runremove(message, msgArgs)
        
        if msgArgs[0] == "!dontrunadd":
          await dontrunadd(message, msgArgs)
          
        if msgArgs[0] == "!dontrunremove":
          await dontrunremove(message, msgArgs)
                    
        if msgArgs[0] == "!hello":
          for values in db["lostark"]["run"].values():
            print(values)
          #print(db["lostark"]["run"])

try:
    keepAlive()
    client.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")

    os.system("kill 1")
    os.system("python restarter.py")
    #system("busybox reboot")
