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

if msgArgs[0] == "!lostark":
  await message.channel.send("Please use !run or !dontrun")

if msgArgs[0] == "!run":
  runList = []
  for player in db["lostark"]["run"].keys():
    runList.append(db["lostark"]["run"][player]["name"] + " " + db["lostark"]["run"][player]["role"])
  runList = "\n".join(runList)
  await message.channel.send(runList)

if msgArgs[0] == "!dontrun":
  runList = []
  for player in db["lostark"]["dontrun"].keys():
    runList.append(db["lostark"]["dontrun"][player]["name"] + " " + db["lostark"]["dontrun"][player]["role"])
  runList = "\n".join(runList)
  await message.channel.send(runList)

if msgArgs[0] == "!runadd":
  if len(msgArgs) == 3:
    tempdict = {
      "name": msgArgs[1],
      "role": msgArgs[2],
    }
    db["lostark"]["run"][msgArgs[1]] = tempdict
    print(db["lostark"]["run"])
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!runadd Name Role")
if msgArgs[0] == "!runremove":
  if len(msgArgs) >= 2:
    if msgArgs[1] in db["lostark"]["run"].keys():
      del db["lostark"]["run"][msgArgs[1]]
      await message.channel.send(msgArgs[1] + " has been removed from the run list")
    else:
      await message.channel.send(msgArgs[1] + " is not in the run list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!runremove Name")

if msgArgs[0] == "!dontrunadd":
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
if msgArgs[0] == "!dontrunremove":
  if len(msgArgs) >= 2:
    if msgArgs[1] in db["lostark"]["dontrun"].keys():
      del db["lostark"]["dontrun"][msgArgs[1]]
      await message.channel.send(msgArgs[1] + " has been removed from the dontrun list")
    else:
      await message.channel.send(msgArgs[1] + " is not in the dontrun list")
  else:
    await message.channel.send("Incorrect format!\nThe correct format is:\n!dontrunremove Name")




    
if msgArgs[0] == "!hello":
  for values in db["lostark"]["run"].values():
    print(values)
  #print(db["lostark"]["run"])