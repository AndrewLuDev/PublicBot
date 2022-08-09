from messages import deleteCommand
import re as regex
import requests
import json
import os
import random

async def createPoll(message, client):
    custom_emojis = regex.findall(r'<:\w*:\d+>', message.content)

    await message.channel.send(message.content)
  
    async for tempMessage in message.channel.history(limit=5):
      if tempMessage.author.id == client.user.id:
        for emoji in custom_emojis:
          await tempMessage.add_reaction(emoji)
        break
    await deleteCommand(message, message.id)

  
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

    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" %
                     (search_term, apikey, maxNumGifs))

    if r.status_code == 200:
        thisgif = str(
            json.loads(r.content)['results'][random.randint(
                0, maxNumGifs)]['media'][0]['gif']['url'])
        #print(thisgif)
        await message.channel.send("> " + message.author.name + '#' +
                                   message.author.discriminator + ': ' +
                                   search_term)
        await message.channel.send(thisgif)
    else:
        await message.channel.send("No results found for the search term: " +
                                   search_term)
    await deleteCommand(message, message.id)