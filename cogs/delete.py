import discord
import json
import os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # 開啟頻道紀錄檔案
        path = "database/channels.json"
        with open(path, "r") as file:
            data = json.load(file)

        # 檢測原本的頻道是否是動態語音
        if not before.channel.id in data:
            return  # 如果不是就結束指令

        # 檢查該頻道是不是沒有其他人了
        if len(before.channel.voice_states) != 0:
            return  # 如果這個頻道還有其他人 結束運行

        # 刪除原頻道
        try:
            await before.channel.delete()
        except:
            pass

        # 刪除這個頻道的紀錄
        with open(path, "w") as file:
            data.remove(before.channel.id)
            json.dump(data, file)


def setup(bot):
    bot.add_cog(delete(bot))
