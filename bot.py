import os # standard library
import time

import discord # 3rd party packages 
from discord.ext import commands, tasks
import praw
import asyncpraw 
from dotenv import load_dotenv

from loop import MyLoop #local modules

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')
async_reddit = asyncpraw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# TODO: Write help documentations
@bot.command()
async def fetch(ctx, sr, st):
    ret_str = __gen_ret_str(sr, st)
    await ctx.send(ret_str)

# TODO: Write help documentations
@bot.command(name='auto')
async def fetch_auto(ctx, sr, st, interval):
    loop = MyLoop(ctx.channel, sr, st, interval, __gen_ret_str)

# TODO: Write help documentations
@bot.command()
async def feed(ctx, sr):

    ret_str = __gen_ret_str(sr, 'new')
    await ctx.send(ret_str)
    
    count = 0
    sub = await async_reddit.subreddit(sr)
    async for submission in sub.stream.submissions():
        if count < 100:
            count += 1
            continue
        sub_str = f'Here is the latest post on {sr}: {submission.score} points | {submission.title} | {submission.url}'
        await ctx.send(sub_str)

# TODO: Write help documentations
@bot.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(bot.latency * 1000)}ms')

# TODO: Find a way to better format the strings, maybe add some hyperlinks rather then posting the whole link
def __gen_ret_str(sr, st):
    submission_list = []

    if st.lower() == 'new':
        for submission in reddit.subreddit(sr).new(limit=5):
            submission_list.append(submission)
    elif st.lower() == 'top':
        for submission in reddit.subreddit(sr).top(limit=5):
            submission_list.append(submission)
    elif st.lower() == 'hot':
        for submission in reddit.subreddit(sr).hot(limit=5):
            submission_list.append(submission)
    elif st.lower() == 'rising':
        for submission in reddit.subreddit(sr).rising(limit=5):
            submission_list.append(submission)
    
    sub_str = ""
    for submission in submission_list:
        sub_str += f'{submission.score} points | {submission.title} | {submission.url} \n\n '

    ret_str = f"Here are the 5 {st.lower()} posts on {sr}: \n {sub_str}" 

    return ret_str

# TODO: Maybe a copmmand to get comments from a post? 

bot.run(TOKEN)
