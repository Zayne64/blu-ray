import discord
import aiohttp
import config
import random
import json
import time
import os
import asyncio
import brfilter
import main
from discord.ext import tasks, commands

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def view(self, ctx, arg):
        """View a tag."""
        tags = await main.bot_load_tags()
        if tags.get(arg) == None:
            await ctx.send('No tag exists with that name.')
        else:
            await ctx.send(tags[arg])

    @commands.command(pass_context=True)
    async def create(self, ctx, arg1, arg2):
        """Creates a tag."""
        tags = await main.bot_load_tags()
        tagso = await main.bot_load_tagso()
        settings_superfilterbans = await main.bot_load_sfbans()
        if tags.get(arg1) != None:
            await ctx.send('A tag already exists with that name.')
        elif any(s in arg1.lower() for s in brfilter.badwords):
            await ctx.send('Your tag contains filtered words.')
        elif any(s in arg2.lower() for s in brfilter.badwords):
            await ctx.send('Your message contains filtered words.')
        elif any(s in arg1.lower() for s in brfilter.superbadwords):
            if settings_superfilterbans.get(str(ctx.message.author.id)) == None:
                settings_superfilterbans[str(ctx.message.author.id)] = 0
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nThe next time you use those, I\'ll have to ban you from this command!```')
                await main.bot_save_sfbans(settings_superfilterbans)
            elif settings_superfilterbans[str(ctx.message.author.id)] == 0:
                settings_superfilterbans[str(ctx.message.author.id)] = 1
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nYou\'ve been banned from the say command.\nJoin our support server to appeal the ban.```')
                await ctx.send('https://discord.gg/g2SWnrg')
                await main.bot_save_sfbans(settings_superfilterbans)
        elif any(s in arg2.lower() for s in brfilter.superbadwords):
            if settings_superfilterbans.get(str(ctx.message.author.id)) == None:
                settings_superfilterbans[str(ctx.message.author.id)] = 0
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nThe next time you use those, I\'ll have to ban you from this command!```')
                await main.bot_save_sfbans(settings_superfilterbans)
            elif settings_superfilterbans[str(ctx.message.author.id)] == 0:
                settings_superfilterbans[str(ctx.message.author.id)] = 1
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nYou\'ve been banned from the say command.\nJoin our support server to appeal the ban.```')
                await ctx.send('https://discord.gg/g2SWnrg')
                await main.bot_save_sfbans(settings_superfilterbans)
        elif settings_superfilterbans.get(str(ctx.message.author.id)) != None:
            if settings_superfilterbans[str(ctx.message.author.id)] == 1:
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYou\'ve been banned from the say command.\nJoin our support server to appeal the ban.```')
                await ctx.send('https://discord.gg/g2SWnrg')
        else:
            tags[arg1] = arg2
            tagso[arg1] = ctx.message.author.id
            await main.bot_save_tags(tags)
            await main.bot_save_tagso(tagso)
            await ctx.send('Tag made!')

    @commands.command(pass_context=True)
    async def delete(self, ctx, arg):
        """Deletes a tag."""
        tags = await main.bot_load_tags()
        tagso = await main.bot_load_tagso()
        if tags.get(arg) == None:
            await ctx.send('No tag exists with that name.')
        elif tagso[arg] != ctx.message.author.id:
            await ctx.send('You don\'t own that tag.')
        else:
            tags.pop(arg, None)
            tagso.pop(arg, None)
            await main.bot_save_tags(tags)
            await main.bot_save_tagso(tagso)
            await ctx.send('Tag deleted!')

    @commands.command(pass_context=True)
    async def edit(self, ctx, arg1, arg2):
        """Edits a tag."""
        tags = await main.bot_load_tags()
        tagso = await main.bot_load_tagso()
        settings_superfilterbans = await main.bot_load_sfbans()
        if tags.get(arg1) == None:
            await ctx.send('No tag exists with that name.')
        elif tagso[arg1] != ctx.message.author.id:
            await ctx.send('You don\'t own that tag.')
        elif any(s in arg2.lower() for s in brfilter.badwords):
            await ctx.send('Your message contains filtered words.')
        elif any(s in arg2.lower() for s in brfilter.superbadwords):
            if settings_superfilterbans.get(str(ctx.message.author.id)) == None:
                settings_superfilterbans[str(ctx.message.author.id)] = 0
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nThe next time you use those, I\'ll have to ban you from this command!```')
                await main.bot_save_sfbans(settings_superfilterbans)
            elif settings_superfilterbans[str(ctx.message.author.id)] == 0:
                settings_superfilterbans[str(ctx.message.author.id)] = 1
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYour message contained super filtered words!\nYou\'ve been banned from the say command.\nJoin our support server to appeal the ban.```')
                await ctx.send('https://discord.gg/g2SWnrg')
                await main.bot_save_sfbans(settings_superfilterbans)
        elif settings_superfilterbans.get(str(ctx.message.author.id)) != None:
            if settings_superfilterbans[str(ctx.message.author.id)] == 1:
                msg = ctx.message
                await msg.delete()
                await ctx.send('```Superfilter Alert\nYou\'ve been banned from the say command.\nJoin our support server to appeal the ban.```')
                await ctx.send('https://discord.gg/g2SWnrg')
        else:
            tags[arg1] = arg2
            await main.bot_save_tags(tags)
            await ctx.send('Tag edited!')

def setup(bot):
    bot.add_cog(Tags(bot))
