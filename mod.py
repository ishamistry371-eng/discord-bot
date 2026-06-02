import discord # bot  calling bot dont not give permission
from discord import app_commands
import random
import asyncio#
import os#(operating system) it will let python interact with my computer
import yt_dlp # search it seacre from yt
import re # this command used for lead the built-in regalar expression(built-in means types into serveal categorise based on the nature of the data)
from discord.ui import View,Button#nbutton working on it
from dotenv import load_dotenv #env file se information inkalta tha like token
from discord.ext import commands # this a use for calling command (ext = extension /tools coomand = command system main dicord libary)
def create_welcome_embed(member):#member when ever they come they got hello from the bot
          embed = discord.Embed(
        title="🌸 Welcome to the Server 🌸",
        description=(
            f"Hey {member.mention} 💖\n\n"
            "We're super happy you're here ✨\n"
            "Enjoy cozy vibes, music, fun and amazing people 🌙\n\n"
            "🎶 Use `!play <song>` to enjoy music with Kuku\n"
            "💌 Make yourself at home!"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )
          embed.set_thumbnail(url=member.display_avatar.url)
          embed.set_image(url="https://media.tenor.com/bl-A7jwBiWoAAAAm/gif-pet.webp")
          embed.set_footer(
        text=f"You are member #{member.guild.member_count} ✨"
    )
          return embed
     





intents = discord.Intents.default()# it is use for what information i want to give to my bot
intents.message_content = True# bot can read message
intents.members= True #bot can detect join or leave
bot = commands.Bot(command_prefix= "!", intents=intents)
#gui grafics user interface

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
love_count={}
class MusicControls(View):

    def __init__(self, vc):
        super().__init__(timeout=None)
        self.vc = vc

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: Button):

        await self.vc.disconnect()
        await interaction.response.send_message("⏹ stopped", ephemeral=True)

          # ⏸ Pause / Resume
    @discord.ui.button(emoji="⏸️", style=discord.ButtonStyle.secondary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if vc.is_playing():
            vc.pause()
            await interaction.response.send_message(
                "⏸️ Music Paused",
                ephemeral=True
            )

        elif vc.is_paused():
            vc.resume()
            await interaction.response.send_message(
                "▶️ Music Resumed",
                ephemeral=True
            )


    # ⏭ Skip
    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()

            await interaction.response.send_message(
                "⏭️ Song Skipped",
                ephemeral=True
            )


    # 🔁 Repeat
    @discord.ui.button(label="Repeat", emoji="🔁", style=discord.ButtonStyle.success)
    async def repeat_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_id = interaction.guild.id

        repeat_modes[guild_id] = not repeat_modes.get(guild_id, False)

        if repeat_modes[guild_id]:

            await interaction.response.send_message(
                "🔁 Repeat Enabled",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ Repeat Disabled",
                ephemeral=True
            )


    # ♾️ Autoplay
    @discord.ui.button(label="Autoplay", emoji="♾️", style=discord.ButtonStyle.primary)
    async def autoplay_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_id = interaction.guild.id

        autoplay_servers[guild_id] = not autoplay_servers.get(guild_id, False)

        if autoplay_servers[guild_id]:

            await interaction.response.send_message(
                "♾️ Autoplay Enabled",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ Autoplay Disabled",
                ephemeral=True
            )


    # ❤️ Love Counter
    @discord.ui.button(label="Love", emoji="❤️", style=discord.ButtonStyle.danger)
    async def love_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_id = interaction.guild.id

        if guild_id not in love_count:
            love_count[guild_id] = 0

        love_count[guild_id] += 1

        await interaction.response.send_message(
            f"❤️ Kuku received love!\n"
            f"Total Loves: **{love_count[guild_id]}** 💖",
            ephemeral=True
        )


    # ❓ Help
    @discord.ui.button(label="Help", emoji="❓", style=discord.ButtonStyle.secondary)
    async def help_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(
            title="🎵 Kuku Music Controls",
            description="Cozy controls for your music 💖",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="⏸️ Pause",
            value="Pause or resume music",
            inline=False
        )

        embed.add_field(
            name="⏭️ Skip",
            value="Skip current song",
            inline=False
        )

        embed.add_field(
            name="🔁 Repeat",
            value="Loop current song",
            inline=False
        )

        embed.add_field(
            name="♾️ Autoplay",
            value="Automatically play songs",
            inline=False
        )

        embed.add_field(
            name="❤️ Love",
            value="Give Kuku some love 😭",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
      
      

#############################################################################################
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
    "before_options": (
        "-reconnect 1 "
        "-reconnect_streamed 1 "
        "-reconnect_delay_max 5 "
        "-nostdin"
    ),
    "options": "-vn"
}
#____________________________________________________________________________________________
# this is for music bot to play song but it will save other song as well
music_queue={}#empty dictionsry which will help store song 
#------------------------------------------------------------------------------------------




async def play_next(ctx):

    guild_id = ctx.guild.id
    vc = ctx.voice_client

    if vc and vc.channel:
        human = [m for m in vc.channel.members if not m.bot]
        if len(human) == 0:
            await vc.disconnect()
            return
        if not music_queue[guild_id]:
             async def leave_if_idle():
                  await asyncio.sleep(300)

    # if queue empty
    if guild_id not in music_queue or not music_queue[guild_id]:

        if autoplay_servers.get(guild_id) == True:

            search_query = random.choice([
                "top english songs",
                "lofi music",
                "top hindi songs",
                "anime songs",
                "phonk",
                "pop hits",
                "soft Arijit singh songs"
                "kpop treading song"
            ])

            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(
                    f"ytsearch1:{search_query}",
                    download=False
                )

                video = info['entries'][0]

                music_queue[guild_id] = [{
                    "url": video['url'],
                    "title": video['title'],
                    "thumbnail":video.get['thumbnail']
                }]
        else:
            return

    # repeat system
    if repeat_modes.get(guild_id) == True:
        song = music_queue[guild_id][0]
    else:
        song = music_queue[guild_id].pop(0)

    source = await discord.FFmpegOpusAudio.from_probe(
        song["url"],
        **FFMPEG_OPTIONS
    )

    def after_play(error):
        if error:
            print(f"sorry but i am facing this error {error} ")

        bot.loop.create_task(play_next(ctx))

    if vc.is_playing():
        return

    vc.play(source, after=after_play)

    embed = discord.Embed(
        title="🎶 Now Playing",
        description=song["title"],
        color=discord.Color.red()
    )
    embed.set_image(url=song["thumbnail"])

    view = MusicControls(vc)

    await ctx.send(embed=embed, view=view)










@bot.command()
async def kuku(ctx):

    if ctx.author.voice is None:
        return await ctx.send("Join a VC first 💖")

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:

        vc = await channel.connect()

        vc.autoplay_enabled = False

        embed = discord.Embed(
            title="🎵 Kuku Joined VC!",
            description=(
                "✨ Kuku is here now!\n\n"
                "🎶 Use `!play <song>` to play music\n"
                "💖 Ready for cozy vibes!"
            ),
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)

    else:
        await ctx.send("I'm already in VC 😎")
#________________________________________________________________________________________



#____________________________________________________________________________________________
#auto play button
autoplay_servers={}
@bot.command()
async def autoplay(ctx,mode=None):
      
      guild_id=ctx.guild.id
      if mode == "on":
            autoplay_servers[guild_id]= True
            embed = discord.Embed(
            title="🔁 Autoplay Enabled",
            description="Kuku will now keep playing songs automatically 💖",
            color=discord.Color.green()
        )
            await ctx.send(embed=embed)
      elif mode == "off":
            autoplay_servers[guild_id]= False
            embed = discord.Embed(
            title="⏹️ Autoplay Disabled",
            description="Kuku stopped automatic music 🌙",
            color=discord.Color.red()
        )
            await ctx.send(embed=embed)
      else:
        await ctx.send("Use: `!autoplay on` or `!autoplay off`")

#__________________________________________________________________________________________
#this is for bot to goo on any chat 

welcome_channel={}
@bot.command()
@commands.has_permissions(administrator=True)#only admin can use 
async def setwelcome(ctx,channel:discord.TextChannel):#channel become tragged a specific channel
      welcome_channel[ctx.guild.id]= channel.id# cureent channel id when needed u can change from here
      await ctx.send(f"welcome channel set to {channel.mention}")#tell us in discord that which channel is saved

#__________________________________________________________________________________________
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
            embed= create_welcome_embed(member)
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
                  thumbnail= video_entry.get("thumbnail")
                  source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                  #stop current song
                  vc= ctx.voice_client
                  guild_id=ctx.guild.id
                  if guild_id not in music_queue:
                        music_queue[guild_id]=[]
                  music_queue[guild_id].append({"url":url,
                                          "title":title,
                                          "thumbnail":thumbnail
                                          })
                  embed= discord.Embed(title="Added to Queue",
                                       description=title,
                                       color= discord.Color.red())
                  await ctx.send(embed=embed)
                  if  vc.is_playing():
                       return
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
#______________________________________________________________________________________


#_________________________________________________________________________________________--

#fake self so u can see where bot was working or not use !testwelcome
@bot.command()
async def testwelcome(ctx):
      member=ctx.author#fake=me as new member
      embed=create_welcome_embed(member)
      await ctx.send(embed=embed)
#_________________________________________________________________________________________

repeat_modes= {}


@bot.command()
async def stop(ctx):
     vc= ctx.voice_client
     if vc is None:
          await ctx.send("kuku is not in vc")
          return
     if vc.is_playing() or vc.is_paused():
          vc.stop()
          guild_id = ctx.guild.id
          if guild_id in music_queue:
               music_queue[guild_id].clear()
               await ctx.send("kuku stopped the music")
     else:
          await ctx.send("nothing playing")
@bot.command()
async def repeat(ctx,mode=None):
     guild_id= ctx.guild.id
     if mode == "on":
          repeat_modes[guild_id]= True
          await ctx.send("🔁 repeat enabled")
     elif mode == "off":
          repeat_modes[guild_id]=False
          await ctx.send("❌repeat disable")
     else:
          await ctx.send("use: !repeat on/off")

          
#________________________________________________________________________________________
#this is for member when they leave the server
@bot.event 
async def on_member_remove(member):
       channel= member.guild.system_channel
       if channel:
             await channel.send(f"{member.mention}left this server :<")
#pil/pillow libary used fir working with images
# pil is on work we will se it later

@bot.tree.command(name="help", description="Shows all Kuku bot commands")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎵 Kuku Music Bot Help",
        description="✨ Cozy music bot with cute controls and vibes 💖",
        color=discord.Color.from_rgb(255, 105, 180)
    )

    # MUSIC
    embed.add_field(
        name="🎶 Music Commands",
        value=(
            "`!play <song>` → Play music\n"
            "`!pause` → Pause / Resume music\n"
            "`!skip` → Skip current song\n"
            "`!stop` → Stop music\n"
            "`!repeat on/off` → Toggle repeat\n"
            "`!autoplay on/off` → Toggle autoplay"
        ),
        inline=False
    )

    # BUTTONS
    embed.add_field(
        name="🎛️ Music Buttons",
        value=(
            "⏸️ Pause music\n"
            "⏭️ Skip song\n"
            "🔁 Repeat current song\n"
            "♾️ Autoplay songs\n"
            "❤️ Give love to Kuku\n"
            "❓ Open help menu"
        ),
        inline=False
    )

    # WELCOME
    embed.add_field(
        name="🌸 Welcome System",
        value=(
            "`!setwelcome #channel` → Set welcome channel\n"
            "`!testwelcome` → Test welcome message"
        ),
        inline=False
    )

    # EXTRA
    embed.add_field(
        name="💖 Extra Features",
        value=(
            "• Love Counter ❤️\n"
            "• Repeat System 🔁\n"
            "• Autoplay ♾️\n"
            "• Cozy Welcome Messages 🌸\n"
            "• Interactive Buttons ✨"
        ),
        inline=False
    )
     # SECRET VC
    embed.add_field(
        name="🕵️ Secret VC",
        value=(
            "`/setsecretvc` → Set secret VC\n"
            "`/secretentry` → Join secret VC"
        ),
        inline=False
    )


    embed.set_footer(
        text="Made with ❤️ by Kuku"
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

secret_vcs = {}
@bot.tree.command(name="setsecretvc", description="Set a secret voice channel")
@app_commands.checks.has_permissions(administrator=True)
async def setsecretvc(
    interaction: discord.Interaction,
    channel: discord.VoiceChannel
):

    secret_vcs[interaction.guild.id] = channel.id

    embed = discord.Embed(
        title="🕵️ Secret VC Set",
        description=f"Secret VC is now {channel.mention} ✨",
        color=discord.Color.purple()
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )
@bot.tree.command(name="secretentry", description="Join the secret VC")
async def secretentry(interaction: discord.Interaction):

    guild_id = interaction.guild.id

    if guild_id not in secret_vcs:

        await interaction.response.send_message(
            "❌ No secret VC configured",
            ephemeral=True
        )

        return

    vc = interaction.guild.get_channel(secret_vcs[guild_id])

    if vc is None:

        await interaction.response.send_message(
            "❌ Secret VC not found",
            ephemeral=True
        )

        return

    await interaction.user.move_to(vc)

    await interaction.response.send_message(
        f"✨ Welcome to {vc.name}",
        ephemeral=True
    )
@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"Logged in as {bot.user}")
    print("Slash commands synced!")

load_dotenv()
TOKEN= os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)