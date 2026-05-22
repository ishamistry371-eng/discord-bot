import discord# bot  calling bot dont not give permission
import asyncio#
import os#(operating system) it will let python interact with my computer
import yt_dlp# search it seacre from yt
import re# this command used for lead the built-in regalar expression(built-in means types into serveal categorise based on the nature of the data)
from discord.ui import view,Button#button working on it
from dotenv import load_dotenv #env file se information inkalta tha like token
from discord.ext import commands # this a use for calling command (ext = extension /tools coomand = command system main dicord libary)
def create_welcome_embed(member):#member when ever they come they got hello from the bot
      embed=discord.Embed(title="welcome! to our server\n",
                          description=f"welcome enjoy your time with us\n {member.name}! \n make sure to join and follow us on social media",
                          color=0x8B0000)
      embed.set_thumbnail(url=member.display_avatar.url)# discort me join ker wake members ka photo lagta hai
      return embed # this is for fancy text message use for titles decription etc
intents = discord.Intents.default()# it is use for what information i want to give to my bot
intents.message_content = True# bot can read message
intents.members= True #bot can detect join or leave
bot = commands.Bot(command_prefix= "!", intents=intents)
#____________________________________________________________________________________________
# this is for music bot to play song but it will save other song as well
music_queue={}#empty dictionsry which will help store song 
async def play_next(ctx):#function i make is for playing next song
      
      guild_id=ctx.guild.id 
      vc=ctx.voice_client
      if guild_id not in music_queue or not  music_queue[guild_id] :
            return
      song= music_queue[guild_id].pop(0)
      source= discord.FFmpegPCMAudio(song["url"],**FFMPEG_OPTIONS)
      def after_play(error):
            bot.loop.create_task(play_next(ctx))
      vc.play(source,after=after_play)
      embed= discord.Embed(title="now playing!",description=song["title"],
                           color=discord.Color.red())
      await ctx.send(embed=embed)
bot.command()
#__________________________________________________________________________________________
#this is for bot to goo on any chat 

welcome_channel={}
@bot.command()
@commands.has_permissions(administrator=True)#only admin can use 
async def setwelcome(ctx,channel:discord.TextChannel):#channel become tragged a specific channel
      welcome_channel[ctx.guild.id]= channel.id# cureent channel id when needed u can change from here
      await ctx.send(f"welcome channel set to {channel.mention}")#tell us in discord that which channel is saved

#__________________________________________________________________________________________
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}
#_________________________________________________________________________________________
#this id for checking if bot is log or not

@bot.event
async def on_ready():
     print(f"logged in as{bot.user}")
#_________________________________________________________________________________________
##########################################################################################
#this is for members to join the server so to welcome them
@bot.event
async def on_member_join(member):
      channel_id = welcome_channel.get(member.guild.id) #member  they have name embed welcome
      if channel_id is None:
          return
      channel = bot.get_channel(channel_id)
      if channel:
            embed=create_welcome_embed(member)
            await channel.send(embed=embed)
#########################################################################################
#________________________________________________________________________________________



@bot.command()# its a decorator which tell discord to runn a command
async def play(ctx,*,query):#its 
      #user not in vc
      if ctx.author.voice is None:
            await ctx.send("join vc first!")
            return
      channel = ctx.author.voice.channel
      #connect bot
      if ctx.voice_client is None:
            embed=discord.Embed(title="Musickuku joined!",
                                description="kuku is here for cozy vibes" \
                                " \t to play music write !play <song name>" \
                                "\tand have fun with me ",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            await channel.connect()
      else:
            await ctx.voice_client.move_to(channel)
      vc= ctx.voice_client
      try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                  if re.match(r'https?://',query):
                        search_query = query
                  else:
                        search_query= f"ytsearch1:{query}"

                  info = ydl.extract_info(search_query,download= False)
                  if 'entries' in info:
                        video_entry = info['entries'][0]
                  else:
                        video_entry=info
                  url = video_entry['url']
                  title = video_entry['title']
                  source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                  #stop current song
                  vc= ctx.voice_client
                  guild_id=ctx.guild.id
                  if guild_id not in music_queue:
                        music_queue[guild_id]=[]
                  music_queue[guild_id].append({"url":url,
                                          "title":title
                                          })
                  embed= discord.Embed(title="Added to Queue",
                                       description=title,
                                       color= discord.Color.red())
                  await ctx.send(embed=embed)
                  if not vc.is_playing():
                        await play_next(ctx)
      except Exception as e:
            await ctx.send(f"error:{e}")


#____________________________________________________________________________________________
#____________________________________________________________________________________________
# this for skip replay repeat pause stop button
@bot.command()
async def pause(ctx):
      vc=ctx.voice_client
      if vc is None:
            await ctx.send("kuku is not in vc")
            return
      if vc.is_playing():
            vc.pause()
            await ctx.send("music paused")
      elif vc.is_paused():
            vc.resume()
            await ctx.send("music resumed")
      else:
            await ctx.send("nothing is playing")
#*******************************************************************************************
@bot.command()
async def skip(ctx):
      vc= ctx.voice_client
      if vc is None:
            await ctx.send("kuku is not in vc")
            return
      if vc.is_playing() or vc.is_paused():
            vc.stop()
            await ctx.send("skipped")
      else:
            await ctx.send("nothing is playing")

#_________________________________________________________________________________________--

#fake self so u can see where bot was working or not use !testwelcome
@bot.command()
async def testwelcome(ctx):
      member=ctx.author#fake=me as new member
      embed=create_welcome_embed(member)
      await ctx.send(embed=embed)
#________________________________________________________________________________________
#this is for member when they leave the server
@bot.event 
async def on_member_remove(member):
       channel= member.guild.system_channel
       if channel:
             await channel.send(f"{member.mention}left this server :<")
#pil/pillow libary used fir working with images
# pil is on work we will se it later

load_dotenv()
TOKEN= os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)