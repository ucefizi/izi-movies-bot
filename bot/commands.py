import discord

from conf.mdb import *
from conf.model import Movie


def get_commands(movie_name, server_id, username, msg_id, icon_url):
    value = """
                 `!movies help`  To get this list of commands.  
                 `!movies add <name>`  To add a movie to the queue.  
                 `!movies remove <name>`  To remove a movie from the queue.  
                 `!movies remove <index>`  To remove a movie from the queue by index.  
                 `!movies list`  To list the movies in the queue.  
                 `!movies watch <name>`  To set a movie as watched.  
                 `!movies watch <index>`  To set a movie as watched by index.  
            """

    embed = discord.embeds.Embed(title="Movies Bot Commands\n", description=value,  colour=0x5E239D)

    return embed


def add_movie(movie_name, server_id, username, msg_id, icon_url):
    movie_name = movie_name.strip()

    movie = Movie(**{
        "id": None,
        "name": movie_name,
        "index": max_index(server_id)+1,
        "server_id": server_id,
        "username": username,
        "message_id": msg_id,
        "watched": False,
        "upvotes": 0,
        "downvotes": 0
    })

    mov = find_by_name(server_id, movie_name)

    if not mov:
        insert(movie)
        embed = discord.embeds.Embed(title="Success", description="Movie '**{}**' added to the queue.".format(movie_name), colour=0x15B097)
    else:
        embed = discord.embeds.Embed(title="Error", description="Movie '**{}**' already exists in the queue at index **{}**.".format(movie_name, mov.index), colour=0xff6700)
    return embed


def remove_movie(movie_name, server_id, username, msg_id, icon_url):
    try:
        index = int(movie_name)
        delete_by_index(index, server_id)
        embed = discord.embeds.Embed(title="Success",
                                     description="Movie at index **{}** removed from the queue.".format(index),
                                     colour=0xD33F49)
        return embed
    except:
        pass

    delete_by_name(movie_name, server_id)
    embed = discord.embeds.Embed(title="Success",
                                 description="Movie '**{}**' removed from the queue.".format(movie_name),
                                 colour=0xD33F49)
    return embed


def watch_movie(movie_name, server_id, username, msg_id, icon_url):
    try:
        index = int(movie_name)
        watch_by_index(index, server_id)
        embed = discord.embeds.Embed(title="Success",
                                     description="Movie at index **{}** set as watched.".format(movie_name),
                                     colour=0x15B097)
        return embed
    except:
        pass

    watch_by_name(movie_name, server_id)
    embed = discord.embeds.Embed(title="Success",
                                 description="Movie '**{}**' set as watched.".format(movie_name),
                                 colour=0x15B097)
    return embed


def vote_movie(movie_name, server_id, username, msg_id, emoji_name):
    if emoji_name == "upvote":
        upvote(msg_id)
    elif emoji_name == "downvote":
        downvote(msg_id)


def un_vote_movie(movie_name, server_id, username, msg_id, emoji_name):
    if emoji_name == "upvote":
        un_upvote(msg_id)
    elif emoji_name == "downvote":
        un_downvote(msg_id)
