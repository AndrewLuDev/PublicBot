import discord
import asyncio
import os
from keep_alive import keep_alive
from replit import db

from datetime import datetime
from pytz import timezone

import requests
import json
import random

friendsIds = {}
friendsList = []

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
    try:
      
      #################################################################
      #logs messages into the console (as a temporary audit log)
      # t = time.localtime()
      # current_time = time.strftime("%H:%M:%S", t)
      # print(current_time, message.author.name + '#' + message.author.discriminator, ': ', message.content)
      tz = timezone("US/Eastern")
      date = datetime.now(tz)

      current_time = date.strftime("%h %d %Y %I:%M%p")
      print(current_time, message.author.name + '#' + message.author.discriminator, ': ', message.content)
      #################################################################
  
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
          if msg.startswith("!del") and len(msgArgs) == 3:
            deleteCheck = True
            maxLogMsgs = 200
            counter = 0
            numMsgs = int(msgArgs[1])
            taggedUser = msgArgs[2]
            if ('<@' in taggedUser) and ('>' in taggedUser):
              taggedUser = taggedUser.replace('<', '').replace('>', '').replace('@', '')
              async for xMessage in message.channel.history(limit=maxLogMsgs):
                if xMessage.author.id == int(taggedUser):
                  if counter < numMsgs:
                    counter +=1
                    await deleteCommand(message, xMessage.id)
                  else:
                    break
          elif msg.startswith("!del "):
            deleteCheck = True
            await deleteMsg(message, msg, msgID, msgArgs)

      

            
      #commands all members can use
      if msg.startswith("!pfp"):
        await getAvatar(message, msgArgs)
      elif msg == "!emotes":
        await listAllEmotes(message)
      elif msg.startswith("!e ") and len(msgArgs)==2:
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
    except:
     pass

    #await asyncio.sleep(2)    



async def addEmote(message, msg, msgID, msgArgs):
  #format of new emote: <:emoteName:emoteID>
  emoteLength = 18
  newEmote = msgArgs[1].lower().replace('<', '').replace('>', '').replace(':', '', 1).split(':')
  if len(newEmote[1]) == emoteLength:
    if newEmote[0] not in db.keys():
      db[newEmote[0]] = newEmote[1]
      await message.channel.send('Emote has been added')
    else:    
      await message.channel.send('Emote has already been added')
  else:
      await message.channel.send('Invalid emote ID')

async def removeEmote(message, msg, msgID, msgArgs):
  if msgArgs[1].lower() in db.keys():
    del db[msgArgs[1]]
    await message.channel.send(msgArgs[1] + " has been removed")
  else:
    await message.channel.send(msgArgs[1] + " is not in the emotes list")

async def clearAllEmotes(message):
  for key in db.keys():
    del db[key]
  await message.channel.send('All emotes have been removed')

async def sendEmote(message, msg, msgID, emoteName):
  if emoteName.lower() in db.keys():
    tempString = '<:' + emoteName + ':' + db[emoteName] + '>'

    temp = await message.channel.fetch_message(message.id)
    #await asyncio.sleep(1)
    await temp.delete()
    await message.channel.send(tempString)
  elif emoteName[0].lower() not in db.keys():
    await message.channel.send('Emote is not in the emotes list')

async def listAllEmotes(message):
  emotesList = list(db.keys())
  emotesList.sort()
  
  tempList = []
  for emoteName in emotesList:
    emote = "<:" + emoteName + ":" + db[emoteName] + ">"
    tempList.append(emoteName + ": " + emote)
  tempList = ", ".join(tempList)
  await message.channel.send(tempList)


async def getAvatar(message, msgArgs):
  if len(msgArgs) == 1:
    avatar = message.author.avatar_url
  elif len(message.mentions) > 0:
    avatar = message.mentions[0].avatar_url
  await message.channel.send(avatar) 

async def sendGif(message):
  apikey = os.getenv('apikey')
  maxNumGifs = 50
  msgArgs = message.content.split(" ", 1)
  search_term = msgArgs[1]
  
  r = requests.get(
    "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, maxNumGifs))
  
  if r.status_code == 200:
    thisgif = str(json.loads(r.content)['results'][random.randint(0, maxNumGifs)]['media'][0]['gif']['url'])
    #print(thisgif)
    await message.channel.send("> " + message.author.name + '#' + message.author.discriminator + ': ' + search_term)
    await message.channel.send(thisgif)
  else:
    await message.channel.send("No results found for the search term: " + search_term)
  await deleteCommand(message, message.id)
  

async def deleteMsg(message, msg, msgID, msgArgs):
  numMsgs = int(msgArgs[1])
  minNumMsgs = 1
  maxNumMsgs = 15
  maxLogMsgs = 50
  counter = 0
  
  if numMsgs >= minNumMsgs and numMsgs <= maxNumMsgs:
    if len(msgArgs) == 3 and msgArgs[2] == "me":
      async for xMessage in message.channel.history(limit=maxLogMsgs):
        if xMessage.author.id == msgID:
          if counter <= numMsgs:
            counter +=1
            await deleteCommand(message, xMessage.id)
          else:
            break
    else:
      await message.channel.purge(limit=numMsgs+1)
  else:
    await message.channel.send('Please enter a number from ' + str(minNumMsgs) + ' to ' + str(maxNumMsgs))

async def deleteCommand(message, messageID):
  temp = await message.channel.fetch_message(messageID)
  #await asyncio.sleep(0.5)
  await temp.delete()



try:
  keep_alive()
  client.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
  print("\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n")
  
  os.system("kill 1")
  os.system("python restarter.py")  
  #system("busybox reboot")