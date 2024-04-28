import discord
from typing import Final
from random import choice, randint
from discord import *
import asyncio
import datetime
import discord.ext
from discord.ext import commands
import os
import requests
import functions as F
from dotenv import load_dotenv

block_links = ["http://", "https://", "discord.gg"]

admin_chat = 1222504650398240788
welcome_channel = 1222504650763403309

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
DESC: Final[str] = os.getenv("BOT_DESCRIPTION")
LINKS: Final[str] = os.getenv("USEFUL_LINKS")

intents = discord.Intents().all()
intents.message_content = True
Client = commands.Bot(command_prefix="$", intents=intents)


@Client.event
async def on_member_join(member):
    channel = Client.get_channel(welcome_channel)
    embed = discord.Embed(
        description=f":wave:Welcome {member.mention} to Cassiopeia Developments!",
        color=0x5A0C8A,
        timestamp=datetime.datetime.now(),
    )
    role = discord.utils.get(member.guild.roles, name="Users")
    await member.add_roles(role)
    await channel.send(embed=embed)


@Client.event
async def on_ready() -> None:
    print(f"{Client.user} is Ready")
    try:
        synced = await Client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("An Error Occured:\n", e)


@Client.tree.command(name="hello", description="Say Hello to Sgàthach!")
async def Hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hey {interaction.user.mention}, How are you?!", ephemeral=True
    )


@Client.tree.command(name="info", description="Information about Sgàthach")
async def info(interaction: discord.Interaction):
    embedVar = discord.Embed(
        title="Sgàthach Information", description=DESC, color=0x5A0C8A
    )
    embedVar.add_field(
        name="Useful Links",
        value=LINKS,
        inline=False,
    )
    await interaction.response.send_message(embed=embedVar)


@Client.tree.command(name="say", description="What do you want to say?")
@app_commands.describe(thing_to_say="What should I say?")
async def Say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(
        f"{interaction.user.name} said: '{thing_to_say}'"
    )


@Client.tree.command(name="roll", description="Ask me to roll a dice!")
@app_commands.describe(
    number_of_dice="How may dice?", size_of_dice="What is the dice value?"
)
async def RollDice(
    interaction: discord.Interaction, number_of_dice: int, size_of_dice: int
):
    start_str = f"You Rolled {number_of_dice}D{size_of_dice}:"
    for el in range(number_of_dice):
        start_str += f"\n:game_die: You Rolled: {str(randint(1, size_of_dice))}"

    await interaction.response.send_message(f"{start_str}")


@Client.tree.command(name="statroll", description="Roll some stats for DnD!")
async def StatRoll(interaction: discord.Interaction) -> None:
    start_str = "Your Stat Block:"
    for i in range(6):
        lst = []
        for el in range(4):
            lst.append(randint(1, 6))
        lst = sorted(lst)
        total = 0
        for el in lst[1:]:
            total += el
        start_str += f"\nRoll:game_die:{i} : **{lst[1:]}** = **{total}**"
    await interaction.response.send_message(f"{start_str}")


@Client.tree.command(name="alert", description="Report an Issue")
@app_commands.describe(issue="What is the issue?")
async def Alert(interaction: discord.Interaction, issue: str) -> None:
    channel = Client.get_channel(admin_chat)
    channel2 = interaction.channel.mention
    embed = discord.Embed(
        title="**ALERT!**",
        description=f"In: {channel2}\nReason: {issue}\n<@&1222504650398240780>",
        color=0x5A0C8A,
        timestamp=datetime.datetime.now(),
    )
    await asyncio.gather(
        channel.send(embed=embed),
        interaction.response.send_message(f"Your report has been sent", ephemeral=True),
    )


@Client.tree.command(name="tellmeajoke", description="Wanna here a joke?")
async def DadJoke(interaction: discord.Interaction):
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"},
    )
    try:
        joke = response.json()["joke"]
    except Exception as e:
        print(e)
    await interaction.response.send_message(f"### Your Joke:\n{joke}")


@Client.tree.command(name="rules", description="Want to know the rules?")
async def Rules(interaction: discord.Interaction) -> None:
    if interaction.user != Client.user:
        await interaction.response.send_message(
            f"You Cannot Use This Command", ephemeral=True
        )
    else:
        with open(r"rules.txt") as rulesBlock:
            rulesBlock = rulesBlock.read().split(",")
            rules = ""
            count = 0
            for i in rulesBlock:
                count += 1
                rules += f"\n{count}) {i}"
                embed = discord.Embed(
                    title="**Cassiopeia Development - Rules**",
                    description=f"Welcome to Cassiopeia Developments!\n While in this server you will have to follow a series of rules:{rules}",
                    color=0x5A0C8A,
                )
                embed.add_field(
                    name="Other Notices",
                    value=f"The staff team reserve the right to act without something being a direct violation of the rules. If something happens that they deem is wrong, they can step in.",
                    inline=False,
                )
                embed.add_field(
                    name="Other Notices",
                    value=f"**please note that this server is a primarily English speaking server, and while we have no issue with other languages, to regulate the moderation and to keep other in the loop with ask that you speak in English within the server**",
                    inline=False,
                )
            await interaction.response.send_message(embed=embed)


#     embed = discord.Embed(
#     title="**ALERT!**",
#     description=f"In: {msg.channel.mention}\nReason: {issue}\n<@&1222504650398240780>",
#     color=0x5A0C8A,
#     timestamp=datetime.datetime.now(),
# )


@Client.event
async def on_message(msg) -> None:
    channel = Client.get_channel(admin_chat)

    with open(r"blocked_words.txt") as block_list:
        block_list = block_list.read().strip().split()
        if msg.author != Client.user:
            for text in block_list:
                if text in str(msg.content.lower()):
                    embed = discord.Embed(
                        title="**ALERT!**",
                        description=f"In: {msg.channel.mention}\nReason: {msg.author} said -> ||{text}||\n<@&1222504650398240780>",
                        color=0x5A0C8A,
                        timestamp=datetime.datetime.now(),
                    )
                    await msg.delete()
                    await channel.send(embed=embed)
            for text in block_links:
                if "staff" not in str(msg.author.roles) and text in str(
                    msg.content.lower()
                ):
                    embed = discord.Embed(
                        title="**ALERT!**",
                        description=f"In: {msg.channel.mention}\nReason: {msg.author} sent a link!\n<@&1222504650398240780>",
                        color=0x5A0C8A,
                        timestamp=datetime.datetime.now(),
                    )
                    await msg.delete()
                    await channel.send(embed=embed)
        if msg.content.lower() == "e":
            reaction = "💀"
            await msg.add_reaction(reaction)


Client.run(TOKEN)
