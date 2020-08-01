# movies-bot
A Discord bot to manage a movies library from a channel.


## List of commands:

> `!movies help`
To get this list of commands.  
> `!movies add movie_name`
To add a movie to the queue.  
> `!movies remove movie_name`
To remove a movie from the queue.  
> `!movies remove movie_index`
To remove a movie from the queue by providing its index.  
> `!movies list`
To list the movies in the queue by the order they were added.  
> `!movies watch movie_name`
To set a movie as watched.  
> `!movies watch movie_index`
To set a movie as watched by providing its index.  

## How to use:
* Install dependencies `$ pip install -r requirements.txt`  
* [Create a Discord Bot account](https://discordpy.readthedocs.io/en/latest/discord.html) 
* Add bot to your server  
* Add your bot token in [`conf/credentials.py`](conf/credentials.py)  
* Connect the bot to a MongoDB instance putting your connection string in [`conf/credentials.py`](conf/credentials.py)  
* Run the bot (either from your local machine, a cloud based VM instance like AWS EC or Google cloud Compute or from a VPS) using `python3 main.py`  
* Call one of the command s to test it out  
