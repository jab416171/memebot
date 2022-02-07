# help.py

import traceback
import sys
import discord
import re
from discord.ext import commands
import Levenshtein as lev

class HelpCog(commands.Cog):
    """ Handles everything related to the help menu. """

    def __init__(self, bot, color):
        """ Set attributes and remove default help command. """
        self.bot = bot
        self.color = color
        self.bot.remove_command('help')
        self.message_url = re.compile("https://discord.com/channels/(\d+)/(\d+)/(\d+)")

    def help_embed(self, title):
        embed = discord.Embed(title=title, color=self.color)
        prefix = self.bot.command_prefix
        prefix = prefix[0] if prefix is not str else prefix

        for cog in self.bot.cogs:  # Uset bot.cogs instead of bot.commands to control ordering in the help embed
            for cmd in self.bot.get_cog(cog).get_commands():
                if cmd.brief:
                    if cmd.usage:  # Command has usage attribute set
                        embed.add_field(name=f'**{prefix}{cmd.usage}**', value=f'_{cmd.brief}_', inline=True)
                    else:
                        embed.add_field(name=f'**{prefix}{cmd.name}**', value=f'_{cmd.brief}_', inline=True)

        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        """ Set presence to let users know the help command. """
        activity = discord.Activity(type=discord.ActivityType.listening, name="I am a simple discord bot")
        await self.bot.change_presence(activity=activity)

    async def cog_before_invoke(self, ctx):
        """ Trigger typing at the start of every command. """
        await ctx.trigger_typing()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Send help message when a mis-entered command is received. """

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        if type(error) is commands.CommandNotFound:
            # Get Levenshtein distance from commands
            in_cmd = ctx.invoked_with
            bot_cmds = list(self.bot.commands)
            lev_dists = [lev.distance(in_cmd, str(cmd)) / max(len(in_cmd), len(str(cmd))) for cmd in bot_cmds]
            lev_min = min(lev_dists)

            # Prep help message title
            embed_title = f'**```{ctx.message.content}```** is not valid!'
            prefix = self.bot.command_prefix
            prefix = prefix[0] if prefix is not str else prefix

            # Make suggestion if lowest Levenshtein distance is under threshold
            if lev_min <= 0.5:
                embed_title += f' Did you mean `{prefix}{bot_cmds[lev_dists.index(lev_min)]}`?'
            else:
                embed_title += f' Use `{prefix}help` for a list of commands'

            embed = discord.Embed(title=embed_title, color=self.color)
            await ctx.send(embed=embed)

    @commands.command(brief='Display the help menu')  # TODO: Add 'or details of the specified command'
    async def help(self, ctx):
        """ Generate and send help embed based on the bot's commands. """
        embed = self.help_embed('__Simple Bot Commands__')
        await ctx.send(embed=embed, delete_after=30)
        try:
            await ctx.message.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        matches = re.findall(self.message_url, message.content)
        for match in matches:
            print(match)
            guild_id = int(match[0])
            channel_id = int(match[1])
            message_id = int(match[2])
            if message.guild.id != guild_id:
                continue
            guild = self.bot.get_guild(guild_id)
            print(guild)
            text_channel = await guild.fetch_channel(channel_id)
            print(text_channel)
            linked_message = await text_channel.fetch_message(message_id)
            print(linked_message)
            embed = discord.Embed(title=f"fetched message from {linked_message.author.display_name} in channel #{text_channel.name}", description=linked_message.content)
            await message.channel.send(embed=embed)

        print(f"{message.channel.name} {message.author.display_name}: {message.content}")
        original_message = message
        if original_message.author.discriminator == "0000":
            return
        if original_message.author == self.bot.user:
            return
        if original_message.content.startswith(self.bot.command_prefix):
            return

        nicks_channel = "💬"
        webhook = None
        if message.guild.id == 437821760046366721 and message.channel.name == "nick":
            nicks_guild = self.bot.get_guild(912905291459338260)
            hook_name = f"💬_hook"
            for channel in nicks_guild.text_channels:
                for w in await channel.webhooks():
                    if w.name == hook_name:
                        webhook = w
                        break

        else:
            webhooks = await original_message.channel.webhooks()
            channel_name = original_message.channel.name
            hook_name = f"{channel_name}_hook"
            for w in webhooks:
                if w.name == hook_name:
                    webhook = w
                    break
            if not webhook:
                webhook = await original_message.channel.create_webhook(name=hook_name)
        # await message.delete()
        top_role = original_message.author.top_role
        # members = message.guild.members
        # members_with_role = []
        # for member in members:
        #     if top_role in member.roles:
        #         members_with_role.append(member)
        # chosen_member = random.choice(members_with_role)
        chosen_member = original_message.author
        avatar = chosen_member.avatar
        if chosen_member.guild_avatar:
            avatar = chosen_member.guild_avatar
        # for a in original_message.attachments:
        #     f = await a.to_file(use_cached=True)
        #     await webhook.send(username = chosen_member.display_name, avatar_url = avatar, file=f)

        # try:
        #     # if original_message.reference:
        #     await webhook.send(username = chosen_member.display_name, avatar_url = avatar, content = original_message.content)
        # except:
        #     print('webhook send failed')