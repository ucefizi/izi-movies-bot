import discord

from math import ceil

from conf.credentials import TOKEN
from bot.commands import *
from conf.pages import pages
from conf.constants import *


client = discord.Client()

commands = {
    'help': get_commands,
    'add': add_movie,
    'remove': remove_movie,
    'watch': watch_movie,
}


def get_list(movies, page, channel_id):
    msg = ''
    for v in movies[page * 5: (page + 1) * 5]:
        msg += """
                            `{}.` **[{}](https://imdb.com/find?q={})** | *`Added by {}`*
                            > {}{}<:upvote:695448204040470568> {}<:downvote:695448203885019207> [**VOTE**](https://discordapp.com/channels/{}/{}/{})\n
                        """.format(
            v.index,
            v.name,
            "+".join(v.name.split()),
            v.username,
            ':ballot_box_with_check: ' if v.watched else '',
            v.upvotes,
            v.downvotes,
            v.server_id,
            channel_id,
            v.message_id
        )

    embed = discord.embeds.Embed(title="**List of movies**\n",
                                 description=msg,
                                 colour=0x291711)
    embed.set_footer(text="Page {}/{}".format(page + 1, ceil(len(movies) / 5)))
    return embed


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        return

    if message.content.startswith("!movies "):
        server_id = message.guild.id
        username = message.author.name
        icon_url = message.author.avatar_url
        message_id = message.id
        channel_id = message.channel.id

        cmd = message.content.split()
        command = cmd[1]
        if command != "list":
            movie_name = " ".join(cmd[2:])
            await message.channel.send(embed=commands[command](movie_name, server_id, username, message_id, icon_url))

        else:

            movies = get_all(server_id)

            if not movies:
                embed = discord.embeds.Embed(title="404",
                                             description="**Wow, such empty.**",
                                             colour=0xef8354)
                msg = await message.channel.send(embed=embed)

            msg = ''
            for v in movies[:5]:
                msg += """
                    `{}.` **[{}](https://imdb.com/find?q={})** | *`Added by {}`*
                     > {}{}<:upvote:{}}> {}<:downvote:{}}> [**VOTE**](https://discordapp.com/channels/{}/{}/{})\n
                     """.format(v.index, v.name, "+".join(v.name.split()), v.username,
                                ':ballot_box_with_check: ' if v.watched else '', v.upvotes, UPVOTE_ID, v.downvotes, DOWNVOTE_ID, v.server_id, channel_id, v.message_id)

            embed = discord.embeds.Embed(title="**List of movies**\n",
                                         description=msg,
                                         colour=0x291711)
            embed.set_footer(text="Page 1/{}".format(ceil(len(movies)/5)), icon_url=icon_url)

            msg = await message.channel.send(embed=embed)

            await msg.add_reaction("⬅")
            await msg.add_reaction("➡")

            pages[msg.id] = {
                "current": 0,
                "msg": msg
            }


@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name.endswith("vote"):
        vote_movie("", payload.guild_id, "", payload.message_id, payload.emoji.name)
    else:
        if payload.user_id != client.user.id:
            try:
                movies = get_all(payload.guild_id)
                page = pages[payload.message_id]["current"]

                if payload.emoji.name == "➡":
                    page += 1
                    if page > len(movies) // 5:
                        page = len(movies) // 5
                elif payload.emoji.name == "⬅":
                    page -= 1
                    if page < 0:
                        page = 0

                await pages[payload.message_id]["msg"].edit(embed=get_list(movies, page, payload.channel_id))
                pages[payload.message_id] = {
                    "current": page,
                    "msg": pages[payload.message_id]["msg"]
                }

            except:
                return


@client.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.name.endswith("vote"):
        un_vote_movie("", payload.guild_id, "", payload.message_id, payload.emoji.name)
    else:
        if payload.user_id != client.user.id:
            try:
                movies = get_all(payload.guild_id)
                page = pages[payload.message_id]["current"]

                if payload.emoji.name == "➡":
                    page += 1
                    if page > len(movies) // 5:
                        page = len(movies) // 5
                elif payload.emoji.name == "⬅":
                    page -= 1
                    if page < 0:
                        page = 0

                await pages[payload.message_id]["msg"].edit(embed=get_list(movies, page, payload.channel_id))
                pages[payload.message_id] = {
                    "current": page,
                    "msg": pages[payload.message_id]["msg"]
                }
            except:
                return


@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('Client id:', client.user.id)
    print('------\n')

client.run(TOKEN)
