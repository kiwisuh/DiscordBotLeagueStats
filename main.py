import discord
import os
import requests
import json
import random
from riotwatcher import LolWatcher, ApiError
import pandas as pd


# golbal variables

watcher = LolWatcher(api_key)
my_region = 'na1'
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_insults():
  response = requests.get("https://insult.mattbas.org/api/insult")
  return(response.content)

def get_staturl(test):
  users_list = ""
  for users in test:
    if(users == "$stats"):
      users = ""
    users_list += str(users)


  return users_list

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #print(get_insults())

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$insult'):
    insult = get_insults()
    await message.channel.send(insult)

  if message.content.startswith('$abby'):
    await message.channel.send(file=discord.File('img/image'+str(random.randrange(0,17))+'.jpg'))
    print(str(random.randrange(0,4)))

  if message.content.startswith('$members'):
    members = discord.VoiceChannel.members #finds members connected to the channel

    memids = [] #(list)
    for member in members:
      memids.append(member.id)

    await message.channel.send(memids)

  if message.content.startswith('$stats'):
    stat = get_staturl(message.content.split())

    await message.channel.send(embed=embedVar)
    await message.channel.send(stat)
    me = watcher.summoner.by_name(my_region, stat)
    #print(me)
    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    #print(my_ranked_stats)
    await message.channel.send(me)
    await message.channel.send(my_ranked_stats)


client.run(os.getenv('TOKEN'))
