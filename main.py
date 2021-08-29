import discord
from discord.errors import DiscordException
from discord.ext import commands
import json
import os
import sys

from selenium import webdriver
from bs4 import BeautifulSoup
import warnings

with open("config.json") as config_file:
    data = json.load(config_file)

token = data["token"]
prefix = data["prefix"]

client = commands.Bot(command_prefix=prefix)

sys.tracebacklimit = 0

warnings.filterwarnings('ignore', category=DeprecationWarning)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

@client.command()
async def ping(ctx):
    await ctx.send("pong")

@client.command()
async def loo(ctx):
    word = ctx.message.content[5:]

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
    driver.get(f"http://lootranslator.infinityfreeapp.com/lootranslator.php?text={word}&mode=thai2loo")
    r = driver.page_source

    soup = BeautifulSoup(r, 'lxml')

    result = soup.find("div").text

    embed=discord.Embed(title=result, color=0xffff00)
    await ctx.send(embed=embed)
    
    driver.close()

@client.event
async def on_ready():
    print(f"login as {client.user}")

client.run(token)