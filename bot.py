import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

monsters = {
    "Young Potbelly": "<:YoungPotbelly:1355921268263878898>",
    "Young Mammott": "<:YoungMammott:1355921388262654123>",
    "Young Tweedle": "<:YoungTweedle:1355921462803959897>",
    "Young Toe Jammer": "<:YoungToeJammer:1355921536703397992>",
    "Young Noggin": "<:YoungNoggin:1355921659818676274>"
}

user_data = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hunt(ctx, monster_name):
    if monster_name not in monsters:
        await ctx.send("Unknown monster!")
        return
    
    if ctx.author.id not in user_data:
        user_data[ctx.author.id] = {"hunting": None, "monsters": []}
    
    user_data[ctx.author.id]["hunting"] = monster_name
    await ctx.send(f"Started hunting for {monster_name}!")

@bot.command()
async def hunt_end(ctx):
    user_id = ctx.author.id
    if user_id not in user_data or user_data[user_id]["hunting"] is None:
        await ctx.send("You aren't hunting anything right now!")
        return
    
    monster = user_data[user_id]["hunting"]
    user_data[user_id]["monsters"].append(monster)
    user_data[user_id]["hunting"] = None
    await ctx.send(f"Congratulations! You have hunted a {monster} {monsters[monster]} and added it to your collection.")

@bot.command()
async def monster_completion(ctx, target: discord.User = None):
    if target is None:
        target = ctx.author
    
    if target.id not in user_data:
        await ctx.send(f"{target.name} has not hunted any monsters yet.")
        return
    
    hunted = user_data[target.id]["monsters"]
    remaining = [monster for monster in monsters if monster not in hunted]
    
    embed = discord.Embed(title=f"{target.name}'s Monster Collection", description="Monsters hunted so far:")
    embed.add_field(name="Hunted Monsters", value="\n".join([f"{monsters[monster]} {monster}" for monster in hunted]) or "None")
    embed.add_field(name="Remaining Monsters", value="\n".join([f"{monsters[monster]} {monster}" for monster in remaining]) or "None")
    
    await ctx.send(embed=embed)

bot.run('YOUR_BOT_TOKEN')
