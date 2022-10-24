import discord
async def help(message):

    helpEmbed = discord.Embed(title = "!help")
    helpEmbed.add_field(name="!del #", value="Purges the most recent # of messages\n**Note: Only admins can use this command**")
    helpEmbed.add_field(name="!del # @user", value="Deletes the most recent # of messages from the tagged user\n**Note: Only admins can use this command**")
    helpEmbed.add_field(name="!del # me", value="Deletes your own messages")
    helpEmbed.add_field(name="!lostark", value="Lists all lostark commands")
    helpEmbed.add_field(name="!emotes", value="Lists all emotes")
    helpEmbed.add_field(name="!poll <insert message here> <emotes>", value="Creates a poll using your specified emotes\nSample usage: !poll Coming to eat sushi on Sunday at 2pm? Yes: <:poggies:777310362793541682> No: <:sadge:777451612938567680>")
    await message.channel.send(embed=helpEmbed)
    
  
#commands:
##list of commands:
#deleteMsg, del, poll
#lostark, lostarkrun, lostarkdontrun, runadd, runremove, dontrunadd, dontrunremove