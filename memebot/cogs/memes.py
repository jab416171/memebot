import discord
from discord.ext import commands
from discord.commands import Option, permissions, SlashCommandGroup, CommandPermission

import youtube_dl
from discord import FFmpegOpusAudio

class MemesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Display invite link')
    async def invite(self, ctx):
        await ctx.send(f"Invite link is https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands")


    @commands.command(brief='play')
    async def play(self, ctx, url: str=None):
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass
        await self.connect(ctx)
        if not self.voice_client:
            await ctx.send("Join a voice channel first!")
            return
        if not url or 'list=' in url:
            await ctx.send('invalid url, make sure its not a playlist')
        self.voice_client.stop()
        FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                          "options": "-vn"}
        YDL_OPTIONS = {"format": "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except youtube_dl.utils.DownloadError as e:
                await ctx.send(e, delete_after=30)
                return
            #info = ydl.extract_info(url)
            url2 = info["formats"][0]["url"]
            print(info['formats'][0])
            await ctx.send(f"playing {info['title']}\nabr: {info['formats'][0]['abr']}")
            source = await FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            self.voice_client.play(source)

    async def connect(self, ctx):
        member = ctx.author
        voice_state = member.voice
        if not voice_state:
            self.voice_client = None
            return
        voice_channel = voice_state.channel

        if not self.bot.user in voice_channel.members:
            try:
                self.voice_client = await voice_channel.connect(reconnect=True)
            except discord.ClientException:
                await self.voice_client.disconnect()
                self.voice_client = await voice_channel.connect(reconnect=True)
        await ctx.guild.change_voice_state(channel=voice_channel, self_deaf=True)

    @commands.command()
    async def sudo(self, ctx):
        original_message = ctx.message
        if original_message.author.discriminator == "0000":
            return
        if original_message.author == self.bot.user:
            return

        mention = original_message.mentions[0]
        webhooks = await original_message.channel.webhooks()
        channel_name = original_message.channel.name
        hook_name = f"{channel_name}_hook"
        webhook = None
        for w in webhooks:
            if w.name == hook_name:
                webhook = w
        if not webhook:
            webhook = await original_message.channel.create_webhook(name=hook_name)
        await ctx.message.delete()
        new_message = " ".join(original_message.clean_content.split(" ")[1:])
        new_message = new_message.replace(mention.display_name, "").replace("@", "")
        await webhook.send(username = mention.display_name, avatar_url = mention.avatar, content = new_message)

    @commands.slash_command(guild_ids=[912905291459338260], name="nick")
    async def slash_nick(self, ctx, extra: Option(str, required=False)):
        user = "<@!911313391484825610>"
        await self._ping(ctx, user, extra)
        await ctx.respond(f"{user} pinged", ephemeral=True)

    @commands.command()
    async def nick(self, ctx):
        message = " ".join(ctx.message.content.split(" ")[1:])
        user = "<@!911313391484825610>"
        await ctx.message.delete()
        await self._ping(ctx, user, message)

    @commands.slash_command(guild_ids=[912905291459338260], name="jon")
    async def slash_jon(self, ctx, extra: Option(str, required=False)):
        user = "<@!140534416983326720>"
        await self._ping(ctx, user, extra)
        await ctx.respond(f"{user} pinged", ephemeral=True)

    @commands.command()
    async def jon(self, ctx):
        message = " ".join(ctx.message.content.split(" ")[1:])
        user = "<@!140534416983326720>"
        await ctx.message.delete()
        await self._ping(ctx, user, message)

    @commands.slash_command(guild_ids=[912905291459338260], name="mike")
    async def slash_mike(self, ctx, extra: Option(str, required=False)):
        user = "<@!638213298218729472>"
        await self._ping(ctx, user, extra)
        await ctx.respond(f"{user} pinged", ephemeral=True)

    @commands.command()
    async def mike(self, ctx):
        message = " ".join(ctx.message.content.split(" ")[1:])
        user = "<@!638213298218729472>"
        await ctx.message.delete()
        await self._ping(ctx, user, message)

    @commands.slash_command(guild_ids=[912905291459338260], name="vytas")
    async def slash_vytas(self, ctx, extra: Option(str, required=False)):
        user = "<@!136184754910396416>"
        await self._ping(ctx, user, extra)
        await ctx.respond(f"{user} pinged", ephemeral=True)

    @commands.command()
    async def vytas(self, ctx):
        message = " ".join(ctx.message.content.split(" ")[1:])
        user = "<@!136184754910396416>"
        await ctx.message.delete()
        await self._ping(ctx, user, message)

    async def _ping(self, ctx, user, message):
        for i in range(0, 5):
            if not message:
                message = ""
            await ctx.send(f"{user} {message}", delete_after=30)