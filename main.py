import discord
import asyncio
import os
from replit import db

from keepAlive import keepAlive
from emotes import *
from extraCommands import *
from lostark import *
from messages import *
from help import *

from datetime import datetime
from pytz import timezone

import random

friendsIds = {}
friendsList = []

##########################################################################################
#  TO DO:
#############################################
#  add !help function
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
        tz = timezone("US/Eastern")
        date = datetime.now(tz)

        current_time = date.strftime("%h %d %Y %I:%M%p")
        print(current_time,
              message.author.name + '#' + message.author.discriminator, ': ',
              message.content)
        if message.attachments:
            print(message.attachments)
        #################################################################

        defaultLostArkDict = {
            "default": {
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

        if len(db) == 0:
            db["lostark"] = {
                "run": defaultLostArkDict,
                "dontrun": defaultLostArkDict,
            }

        #admin-specific commands
        deleteCheck = False

        if msgID in friendsIds.values():
            if msg.startswith("!add "):
                await addEmote(message, msg, msgID, msgArgs)

            elif msg.startswith("!remove "):
                await removeEmote(message, msg, msgID, msgArgs)

            elif msg.lower() == "!clear emotes":
                await clearAllEmotes(message)

            elif msg.startswith("!e list"):
              await message.channel.send(db["emotes"])
            # elif msg.startswith("!clear"):
            #   db.clear()
          
            elif msg.startswith("!purge"):
                await purgeChat(message)

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
            msgArgs = msgArgs[1].lower().replace('<',
                                                 '').replace('>', '').replace(
                                                     ':', '', 1)
            if ':' in msgArgs:
                msgArgs = msgArgs.split(':')
                await sendEmote(message, msg, msgID, msgArgs[0])
            else:
                await sendEmote(message, msg, msgID, msgArgs)
        elif msg.startswith("!gif"):
            await sendGif(message)
        elif msg.startswith("!hide"):
            await hideMessages(message, msg, msgID, msgArgs)
        elif msg.startswith("!del") and ("me" in msg) and (deleteCheck == False):
            await deleteMsg(message, msg, msgID, msgArgs)

        elif msg.startswith("!poll") and message.author.id != client.user.id:
            print(message.author.id, client.user.id)
            await createPoll(message, client)

        if msg.startswith("!help"):
            await help(message)

        if msg.startswith("!lostark"):
            await lostark(message)

        elif msg.startswith("!runadd"):
            await runadd(message, msgArgs)

        elif msg.startswith("!runremove"):
            await runremove(message, msgArgs)

        elif msg.startswith("!dontrunadd"):
            await dontrunadd(message, msgArgs)

        elif msg.startswith("!dontrunremove"):
            await dontrunremove(message, msgArgs)

        elif msg.startswith("!run"):
            await lostarkrun(message)

        elif msg.startswith("!dontrun"):
            await lostarkdontrun(message)

        elif msg.startswith("!add all"):
            await addall(message)


try:
    keepAlive()
    client.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")

    os.system("kill 1")
    os.system("python restarter.py")
    #system("busybox reboot")
