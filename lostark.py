from replit import db

defaultLostArkDict = {"default":
  {
  "name": "name",
  "role": "role",
  }
}

if len(db) == 0:
  db["lostark"] = {
    "run": defaultLostArkDict,
    "dontrun": defaultLostArkDict,
  }

async def lostark(message):
  await message.channel.send("Please use !run or !dontrun")

async def lostarkrun(message):
  runList = []
  for player in db["lostark"]["run"].keys():
    runList.append(db["lostark"]["run"][player]["name"] + " " + db["lostark"]["run"][player]["role"])
  runList = "\n".join(runList)
  await message.channel.send(runList)

async def lostarkdontrun(message):
  runList = []
  for player in db["lostark"]["dontrun"].keys():
    runList.append(db["lostark"]["dontrun"][player]["name"] + " " + db["lostark"]["dontrun"][player]["role"])
  runList = "\n".join(runList)
  await message.channel.send(runList)

async def runadd(message, msgArgs):
  if len(msgArgs) == 3:
    tempdict = {
      "name": msgArgs[1],
      "role": msgArgs[2],
    }
    db["lostark"]["run"][msgArgs[1]] = tempdict
    print(db["lostark"]["run"])
    await message.channel.send(msgArgs[1] + " has been added to the run list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!runadd Name Role")
    
async def runremove(message, msgArgs):
  if len(msgArgs) >= 2:
    if msgArgs[1] in db["lostark"]["run"].keys():
      del db["lostark"]["run"][msgArgs[1]]
      await message.channel.send(msgArgs[1] + " has been removed from the run list")
    else:
      await message.channel.send(msgArgs[1] + " is not in the run list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!runremove Name")

async def dontrunadd(message, msgArgs):
  if len(msgArgs) == 3:
    tempdict = {
      "name": msgArgs[1],
      "role": msgArgs[2],
    }
    db["lostark"]["dontrun"][msgArgs[1]] = tempdict
    print(db["lostark"]["dontrun"])
    await message.channel.send(msgArgs[1] + " has been added to the dontrun list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!runadd Name Role")

async def dontrunremove(message, msgArgs):
  if len(msgArgs) >= 2:
    if msgArgs[1] in db["lostark"]["dontrun"].keys():
      del db["lostark"]["dontrun"][msgArgs[1]]
      await message.channel.send(msgArgs[1] + " has been removed from the dontrun list")
    else:
      await message.channel.send(msgArgs[1] + " is not in the dontrun list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!dontrunremove Name")




    
# if msgArgs[0] == "!hello":
#   for values in db["lostark"]["run"].values():
#     print(values)
#   #print(db["lostark"]["run"])