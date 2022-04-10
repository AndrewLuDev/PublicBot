import discord
import os

friendsIds = {}
friendsList = []

for userInfo in os.getenv('friendsList').split(", "):
  #friendsIds format:
  #name1: id1, name2: id2, name3: id3, etc.
  userInfo = userInfo.split(': ')
  friendsList.append(userInfo[0])
  friendsIds[userInfo[0]] = int(userInfo[1])

print(friendsIds)

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
      print(msgID)
      if len(msgArgs) >= 2:

        #deleting messages
        await deleteMsg(message, msg, msgID, msgArgs)
        

async def deleteMsg(message, msg, msgID, msgArgs):
  if msg.startswith("!del "):
    msgArgs[1] = int(msgArgs[1])
    if msgArgs[1] >= 1 and msgArgs[1] <= 10:
      await message.channel.purge(limit=msgArgs[1]+1)
    else:
      await message.channel.send('Please enter a number from 1 to 10')

client.run(os.getenv('TOKEN'))