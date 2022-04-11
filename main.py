import discord
import os
from keep_alive import keep_alive
import replit
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
        
      elif msg.startswith("!e ") and len(msgArgs)==2:
        msgArgs[1].replace(':', '')
        if msgArgs[1] in db.keys():
          tempString = '<:' + msgArgs[1] + ':' + db[msgArgs[1]] + '>'
          await message.channel.send(tempString)
        elif msgArgs[1] not in db.keys():
          await message.channel.send('Emote is not in the emotes list')
        
      if msg == "!emotes":
        await message.channel.send(db.keys())
        

      if len(msgArgs) >= 2:
        #deleting messages
        await deleteMsg(message, msg, msgID, msgArgs[1])


async def deleteMsg(message, msg, msgID, numMsgs):
  minNumMsgs = 1
  maxNumMsgs = 15
  if msg.startswith("!del "):
    numMsgs = int(numMsgs)
    if numMsgs >= minNumMsgs and numMsgs <= maxNumMsgs:
      await message.channel.purge(limit=numMsgs+1)
    else:
      await message.channel.send('Please enter a number from ' + str(minNumMsgs) + ' to ' + str(maxNumMsgs))

async def addEmote(message, msg, msgID, msgArgs):
  #format of new emote: <:emoteName:emoteID>
  emoteLength = 18
  newEmote = msgArgs[1].lower().replace('<', '').replace('>', '').replace(':', '', 1).split(':')
  if newEmote[0] not in db.keys():
    if len(newEmote[1]) == emoteLength:
      db[newEmote[0]] = newEmote[1]
      await message.channel.send('Emote has been added')
    else:
      await message.channel.send('Invalid emote ID')
  else:
    await message.channel.send('Emote has already been added')



async def removeEmote(message, msg, msgID, msgArgs):
  if msgArgs[1] in db.keys():
    del db[msgArgs[1]]
    await message.channel.send(msgArgs[1] + " has been removed")
  else:
    await message.channel.send(msgArgs[1] + " is not in the emotes list")

keep_alive()
client.run(os.getenv('TOKEN'))