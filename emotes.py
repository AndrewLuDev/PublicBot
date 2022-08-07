
async def addEmote(message, msg, msgID, msgArgs):
    #format of new emote: <:emoteName:emoteID>
    POSSIBLE_EMOTE_LENGTHS = [18, 19]
    if (msgArgs[1].count('<') == 1 and msgArgs[1].count('>') == 1
            and msgArgs[1].count(':') == 2 and msgArgs[1].count('\\') == 0):
        newEmote = msgArgs[1].lower().replace('<',
                                              '').replace('>', '').replace(
                                                  ':', '', 1).split(':')
        if len(newEmote[1]) in POSSIBLE_EMOTE_LENGTHS:
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
    for emoteName in db.keys():
        del db[emoteName]
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