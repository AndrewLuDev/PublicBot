from replit import db
import discord

async def addEmote(message, msg, msgID, msgArgs):
    #format of new emote: <:emoteName:emoteID>
    POSSIBLE_EMOTE_LENGTHS = [18, 19]
    if (msgArgs[1].count('<') == 1 and msgArgs[1].count('>') == 1
            and msgArgs[1].count(':') == 2 and msgArgs[1].count('\\') == 0):
        newEmote = msgArgs[1].lower().replace('<',
                                              '').replace('>', '').replace(
                                                  ':', '', 1).split(':')
        if len(newEmote[1]) in POSSIBLE_EMOTE_LENGTHS:
            if newEmote[0] not in db["emotes"].keys():
                db["emotes"][newEmote[0]] = newEmote[1]
                await message.channel.send('Emote has been added')
            else:
                await message.channel.send('Emote has already been added')
    else:
        await message.channel.send('Invalid emote ID')


async def removeEmote(message, msg, msgID, msgArgs):
    if msgArgs[1].lower() in db["emotes"].keys():
        del db["emotes"][msgArgs[1]]
        await message.channel.send(msgArgs[1] + " has been removed")
    else:
        await message.channel.send(msgArgs[1] + " is not in the emotes list")


async def clearAllEmotes(message):
    for emoteName in db["emotes"].keys():
        del db["emotes"][emoteName]
    await message.channel.send('All emotes have been removed')


async def sendEmote(message, msg, msgID, emoteName):
    if emoteName.lower() in db["emotes"].keys():
        tempString = '<:' + emoteName + ':' + db["emotes"][emoteName] + '>'

        temp = await message.channel.fetch_message(message.id)
        #await asyncio.sleep(1)
        await temp.delete()
        await message.channel.send(tempString)
    elif emoteName[0].lower() not in db["emotes"].keys():
        await message.channel.send('Emote is not in the emotes list')


async def listAllEmotes(message):
    emotesList = list(db["emotes"].keys())
    emotesList.sort()

    await message.channel.send("Getting all emotes...", delete_after=2)
  
    tempList = []
    for emoteName in emotesList:
        emote = "<:" + emoteName + ":" + db["emotes"][emoteName] + ">"
        tempList.append(emoteName + ": " + emote)
    tempList = ", ".join(tempList)
    await message.channel.send(tempList)

async def addall(message):
  emotesList = {"minapout": "962922566048170004", "ratge": "1003864628016709702", "donowall": "1001665099066527897", "seocringe": "983894841475891240", "sadgecry": "999753988482277388", "smoge": "942669134817267733", "naruge": "962040365936963605", "noooo": "962111822142525501", "shyggers": "1001229635704606900", "cocka": "963273264384339998", "minaheart": "963246634068766771", "okaygebusiness": "995562005987606601", "sadge": "777451612938567680", "minagasm": "963246645972205568", "susge": "975601891033612348", "booba": "963273543393628231", "despairge": "1002256106229342319", "fishinge": "989308544706805780", "madge": "778701970583715840", "yumekono": "1003664916345008139", "johnchina": "1003666661615870063", "okayge": "969721860013051905", "yumekogun": "1003664837987016784", "starege": "975894479221436476", "wokege": "917171164223262811", "gonyuck": "1003664995659292723", "dcolon": "662760009909665815", "holdl": "965704234018439228", "pausechamp": "1003686226139807774", "wicked": "964282331433144350", "poggies": "777310362793541682"}
  for key in emotesList.keys():
    print(key, emotesList[key])
    if key not in db["emotes"].keys():
      db["emotes"][key] = emotesList[key]
  await message.channel.send("all emotes have been added")