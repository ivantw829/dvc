import json

import discord
from discord.commands import Option, slash_command
from discord.ext import commands


class set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 設置指令
    @slash_command(description="設置群組動態語音頻道")
    async def setup(self, ctx,
                    channel: Option(discord.VoiceChannel, "創建頻道", default=None),
                    category: Option(discord.CategoryChannel, "會創建至的類別", default=None)):
        await ctx.defer()  # 延遲回應斜線指令

        if not ctx.author.guild_permissions.administrator:  # 限定管理員使用 https://youtu.be/nyF_qKBYvog
            await ctx.respond("你不是管理員，所以不能使用本指令。")
            return  # 如果不是管理員就結束這個指令

        # 如果使用者沒輸入指定頻道，就直接創建
        if category == None:
            try:
                category = await ctx.guild.create_category("動態語音頻道")
            except:
                await ctx.respond("無法創建類別，請檢查機器人權限。")
                return  # 如果沒辦法創建類別就結束指令

        if channel == None:
            try:
                channel = await ctx.guild.create_voice_channel("語音頻道", category=category)
            except:
                await ctx.respond("無法正確創建語音頻道，請檢查權限。")
                return  # 如果沒辦法創建語音頻道就結束指令運行

        # 測試機器人是否有創建頻道的權限？
        try:
            # 試一下機器人有沒有辦法創建頻道
            test = await ctx.guild.create_voice_channel("權限測試頻道", category=category)
            await test.delete()  # 刪除那個創建的測試頻道
        except:
            await ctx.respond("機器人無法正確創建/刪除頻道，請檢查機器人權限。")

        # 紀錄設置資料
        with open("database/guild.json", "r") as file:  # 用read模式開啟檔案
            data = json.load(file)  # 讀取檔案內的資料
            # 更改資料內的字典元素 https://youtu.be/y7Wa7NaSKgs
            data[str(ctx.guild.id)] = {
                "channel": channel.id, "category": category.id}
        with open("database/guild.json", "w") as file:  # 用write模式開啟資料檔案
            json.dump(data, file, indent=4)  # 更改後的資料寫入檔案內

        embed = discord.Embed(title="動態語音頻道", description=F"已成功設置動態語音頻道\n\
                            Channel:{channel.mention}\n\
                            Category:{category.mention}")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(set(bot))
