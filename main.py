import discord
import os

client = discord.Client()

@client.event   
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  
  @client.event

  async def on_message(message):
    pass
client.run(os.getenv('TOKEN'))