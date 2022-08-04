

async def deleteMsg(message, msg, msgID, msgArgs):
    numMsgs = int(msgArgs[1])
    minNumMsgs = 1
    maxNumMsgs = 15
    maxLogMsgs = 50
    counter = 0

    if len(msgArgs) == 3:
        taggedUser = msgArgs[2]
        if taggedUser == "me":
            taggedUser = msgID
        elif (('<@' in taggedUser) and ('>' in taggedUser)):
            maxLogMsgs = 200
            taggedUser = int(
                taggedUser.replace('<', '').replace('>', '').replace('@', ''))
        else:
            message.channel.send(
                "Please end the !del command with 'me' or by tagging a user")
            return
        await deleteHelper(message, numMsgs, taggedUser, minNumMsgs,
                           maxNumMsgs, maxLogMsgs, counter)
    else:
        if numMsgs >= minNumMsgs and numMsgs <= maxNumMsgs:
            await message.channel.purge(limit=numMsgs + 1)
        else:
            await message.channel.send('Please enter a number from ' +
                                       str(minNumMsgs) + ' to ' +
                                       str(maxNumMsgs))


async def deleteHelper(message, numMsgs, taggedUser, minNumMsgs, maxNumMsgs,
                       maxLogMsgs, counter):
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