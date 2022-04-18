import discord
import asyncio
import os
from keep_alive import keep_alive
from replit import db


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

    if msgID in friendsIds.values():
      if msg.startswith("!add "):
        await addEmote(message, msg, msgID, msgArgs)
        
      elif msg.startswith("!remove "):
        await removeEmote(message, msg, msgID, msgArgs)

      elif msg.lower() == "!clear emotes":
        await clearAllEmotes(message)        
      
      elif msg.startswith("!e ") and len(msgArgs)==2:
        msgArgs = msgArgs[1].lower().replace('<', '').replace('>', '').replace(':', '', 1)
        if ':' in msgArgs:
          msgArgs = msgArgs.split(':')
          await sendEmote(message, msg, msgID, msgArgs[0])
        else:
          await sendEmote(message, msg, msgID, msgArgs)
      
      if msg == "!emotes":
        await message.channel.send(db.keys())
        #allValues = []
        #for val in db.values():
        #  allValues.append(val)
        #await message.channel.send(allValues)  
        

      if len(msgArgs) >= 2:
        #deleting messages
        if msg.startswith("!del "):
          await deleteMsg(message, msg, msgID, msgArgs)


async def deleteMsg(message, msg, msgID, msgArgs):
  minNumMsgs = 1
  maxNumMsgs = 15

  numMsgs = int(msgArgs[1])
  deleteThese = []
  counter = 0

  if numMsgs >= minNumMsgs and numMsgs <= maxNumMsgs:
    if len(msgArgs) == 3 and msgArgs[2] == "me":
      async for xMessage in message.channel.history(limit=50):
        if xMessage.author.id == msgID:
          if counter <= numMsgs:
            counter += 1
            deleteThese.append(xMessage.id)
          else:
            break
      for eachMsg in deleteThese:
        temp = await message.channel.fetch_message(eachMsg)
        await temp.delete()
    elif len(msgArgs) >= 2:
      await message.channel.purge(limit=numMsgs+1)
  else:
    await message.channel.send('Please enter a number from ' + str(minNumMsgs) + ' to ' + str(maxNumMsgs))

  await asyncio.sleep(2)



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
  if msgArgs[1].lower in db.keys():
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
    await message.channel.send(tempString)
  elif emoteName[0].lower() not in db.keys():
    await message.channel.send('Emote is not in the emotes list')

keep_alive()
client.run(os.getenv('TOKEN'))