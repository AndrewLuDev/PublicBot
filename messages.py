#list of commands:
#deleteMsg !del !purge !hide
from pytz import timezone
from datetime import datetime
import os


async def checkTaggedUser(taggedUser, msgID, maxLogMsgs):
    if taggedUser == "me":
        taggedUser = msgID
    elif (('<@' in taggedUser) and ('>' in taggedUser)):
        maxLogMsgs = 200
        taggedUser = int(
            taggedUser.replace('<', '').replace('>', '').replace('@', ''))
    else:
        taggedUser = "Invalid"
    return taggedUser, maxLogMsgs


async def hideMessages(message, msg, msgID, msgArgs):
    numMsgs = 25
    maxLogMsgs = 50
    if len(msgArgs) >= 2:
        taggedUser, maxLogMsgs = await checkTaggedUser(msgArgs[1], msgID,
                                                       maxLogMsgs)
    else:
        taggedUser = msgID
    if taggedUser == "Invalid":
        await message.channel.send(
            "Correct usage: `!hide` or `!hide me` or `!hide @user`")
        return
    await deleteHelper(message, numMsgs, taggedUser, maxLogMsgs)


async def purgeChat(message):
    await message.channel.purge(limit=50)


async def deleteMsg(message, msg, msgID, msgArgs):
    numMsgs = int(msgArgs[1])
    minNumMsgs = 1
    maxNumMsgs = 15
    maxLogMsgs = 50

    if len(msgArgs) >= 3:
        taggedUser, maxLogMsgs = await checkTaggedUser(msgArgs[2], msgID,
                                                       maxLogMsgs)
        if taggedUser == "Invalid":
            await message.channel.send(
                "Please end the !del command with 'me' or by tagging a user")
            return
        await deleteHelper(message, numMsgs, taggedUser, maxLogMsgs)
    else:
        if numMsgs >= minNumMsgs and numMsgs <= maxNumMsgs:
            await message.channel.purge(limit=numMsgs + 1)
        else:
            await message.channel.send('Please enter a number from ' +
                                       str(minNumMsgs) + ' to ' +
                                       str(maxNumMsgs))


async def deleteHelper(message, numMsgs, taggedUser, maxLogMsgs):
    counter = 0
    await deleteCommand(message, message.id)
    async for xMessage in message.channel.history(limit=maxLogMsgs):
        if xMessage.author.id == taggedUser:
            if counter < numMsgs:
                counter += 1
                temp = await message.channel.fetch_message(xMessage.id)
                await temp.delete()
            else:
                break


async def deleteCommand(message, messageID):
    temp = await message.channel.fetch_message(messageID)
    #await asyncio.sleep(0.5)
    await temp.delete()


async def auditLog(message, client):
  tz = timezone("US/Eastern")
  date = datetime.now(tz)
  current_time = date.strftime("%h %d %Y at %I:%M%p")
  
  source = client.get_guild(int(os.getenv('SOURCESERVER')))
  destination = source.get_channel(int(os.getenv('DESTINATIONCHANNEL')))
  auditLog  = current_time + " [#" + message.channel.name + "] \n" + message.author.name + '#' + message.author.discriminator + ': ' + message.content
  if message.author.id != client.user.id:
    await destination.send(auditLog)
    if message.attachments:
      for attachment in message.attachments:
        await destination.send(attachment.url)
