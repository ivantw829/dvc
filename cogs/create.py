import discord
import json
import os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 創建語音頻道
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):  # 偵測成員語音狀態更新
        # 讀取群組設置資料
        with open("database/guild.json", "r") as file:
            data = json.load(file)

        # 檢查所在群組是否有設置
        if not str(member.guild.id) in data:
            return  # 如果改選組沒有設置就結束運行

        # 檢查成員是不是退出
        if after.channel == None:
            return  # 如果成員是退出頻道，結束運行

        # 檢查連接的是否是創建頻道
        data = data[str(member.guild.id)]  # 將data縮為只有該群的dict
        if after.channel.id != data["channel"]:
            return  # 如果連接的不是創建頻道就結束運行

        # 嘗試抓取要創建至的類別
        try:
            category = await member.guild.fetch_channel(data["category"])
        except:
            # 嘗試私聊連接的用戶回報錯誤
            try:
                await member.send("找不到設置的類別，請管理員重新設置")
                return
            except:
                return

        # 嘗試創建語音頻道
        try:
            channel = await member.guild.create_voice_channel(member.name, category=category)
        except:
            # 嘗試私聊連接的用戶回報錯誤
            try:
                await member.send("無法創建頻道，請管理員檢查權限")
                return
            except:
                return

        # 嘗試移動成員至新頻道
        try:
            await member.move_to(channel)
        except:
           # 嘗試私聊連接的用戶回報錯誤
            try:
                await member.send("無法移動成員，請管理員檢查權限")
                await channel.delete()
                return
            except:
                return

        # 記錄這個頻道
        with open("database/channels.json", "r") as file:
            data = json.load(file)
            data.append(channel.id)
        with open("database/channels.json", "w") as file:
            json.dump(data, file)


def setup(bot):
    bot.add_cog(create(bot))
