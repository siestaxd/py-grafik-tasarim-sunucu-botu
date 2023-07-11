import discord
from discord.ext import commands
from discord.commands import slash_command as slash

bot = discord.Bot()

class CustomerComments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash(name="customer-comments", description="Customer comments")
    async def customer_comments(self, interaction: discord.Interaction, comments):
        channel =  discord.utils.get(interaction.guild.channels, name='customer-comments')
        embed = discord.Embed(title=f'__Customer Comment__',description=f"{comments}",colour=discord.Colour.blurple())
        embed.set_author(name=f'{interaction.user.name}', icon_url=interaction.user.avatar)
        message = await channel.send(embed=embed)
        await message.add_reaction('<a:sieshearth:1128391996722131054>')
        await interaction.response.send_message(f'yorumunuz gönderildi. geri bildiriminiz için teşekkürler!', ephemeral=True)

def setup(bot):
    bot.add_cog(CustomerComments(bot))