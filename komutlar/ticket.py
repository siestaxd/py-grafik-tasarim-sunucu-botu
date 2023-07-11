import discord
from discord.ext import commands
import discord.ui
from discord.ui import View, Button, Select
import asyncio
import os
import json

def config():
    with open('config.json', encoding='utf-8') as f:
        return json.load(f)

config = config()

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Ticket.TicketClose())

    class TicketClose(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(label='Ticket kapat', custom_id='ticketclose', style=discord.ButtonStyle.red, emoji='🔒')
        async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.defer()
            ticketlog = discord.utils.get(interaction.guild.channels, id=int(config['ticketlog']))
            embed = discord.Embed(title='Ticket Log' ,description=f'({interaction.user.mention}) adlı kullanıcı ticketı kapattı.', colour=discord.Colour.blurple())
            embed.add_field(name='Kullanıcı:', value=interaction.user.mention, inline=True)
            embed.add_field(name='Kullanıcı adı:', value=interaction.user.display_name, inline=True)
            embed.add_field(name='Kullanıcı ID:', value=interaction.user.id, inline=True)
            embed.add_field(name='Ticket name:', value=interaction.channel.name, inline=True)
            embed.add_field(name='Ticket ID:', value=interaction.channel.id, inline=True)
            await ticketlog.send(embed=embed)
            messages = []
            async for message in interaction.channel.history(limit=1000):
                messages.append(f'{message.author.name} - {message.content}\n')
            filename = f'{interaction.channel.name}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(messages)
            with open(filename, 'rb') as f:
                await ticketlog.send(file=discord.File(f, filename=filename))
            os.remove(filename)
            await interaction.channel.send('Ticket kapatılıyor.')
            await asyncio.sleep(3)
            await interaction.channel.delete()

        @discord.ui.button(label='ticket log', custom_id='ticketlog', style=discord.ButtonStyle.green, emoji='📜')
        async def log(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.defer()
            messages = []
            async for message in interaction.channel.history(limit=1000):
                messages.append(f'{message.author.name} - {message.content}\n')
        
            filename = f'{interaction.channel.name}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(messages)
            with open(filename, 'rb') as f:
                await interaction.channel.send(file=discord.File(f, filename=filename))
            os.remove(filename)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name='Graphic Support')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            role: discord.PermissionOverwrite(view_channel=True)
        }

        select = Select(options=[
            discord.SelectOption(label='Tasarım Satın alacam', value='01' ,description='Herhangi bir tasarım yaptırmak istiyorsanız buraya basın', emoji='💰'),
            discord.SelectOption(label='Tasarım ile ilgili bir şey soracam', value='02', description='Aklınızda soru veya başka bir şey varsa buraya basarak iletebilirsiniz.', emoji='📝'),
            discord.SelectOption(label='Diğer', value='03', description='Tasarım dışında başka bir sorununuz varsa burdan sorabilirsiniz', emoji='📌')
        ])

        async def ticketcallback(interaction: discord.Interaction):
            if select.values[0] == '01':
                category = discord.utils.get(guild.categories, id=int(config['ticketcategory']))
                channel = await guild.create_text_channel(name=f'ticket-{interaction.user.display_name}-01', category=category, overwrites=overwrites)
                await interaction.response.send_message(f'Ticket oluşturuldu. - <#{channel.id}>', ephemeral=True)
                await channel.send(f'(<@&1127717158940577844>) - ({interaction.user.mention})')
                embed = discord.Embed(title='Tasarım Satın Alım', description='Merhaba açtığınız tickettan dolayı tasarım yaptırmak istediğinizi varsayıyorum ne tasarımı yaptırmak istiyorsunuz logo,banner vb, bizlere ne yaptırmak istediğinizi ve nasıl olacağı konusunda detaylı bilgi verirmisiniz.', colour=discord.Colour.blurple())
                embed.add_field(name='Örnek:', value='Logo yaptırmak istiyorum, logo da bir kurt olsun ve kurtun rengi kırmızı olsun.', inline=False)
                embed.add_field(name='kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Departman:', value=f'<@&1127717158940577844>', inline=True)
                await channel.send(embed=embed, view=self.TicketClose())

                #-------------------------------------------------------------------------- log

                channellog = discord.utils.get(guild.channels, id=int(config['ticketlog']))
                embed = discord.Embed(title='Ticket Log' ,description=f'({interaction.user.mention}) adlı kullanıcı (Tasarım Satın alacam) ticketı açtı.', colour=discord.Colour.blurple())
                embed.add_field(name='Kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Kullanıcı adı:', value=interaction.user.display_name, inline=True)
                embed.add_field(name='Ticket:', value=channel.mention, inline=True)
                embed.add_field(name='Ticket adı:', value=channel.name, inline=True)
                embed.add_field(name='Ticket ID:', value=channel.id, inline=True)
                embed.add_field(name='Ticket oluşturulma tarihi:', value=channel.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
                embed.add_field(name='Ticket oluşturulma zamanı:', value=channel.created_at.strftime('%H:%M:%S'), inline=True)
                embed.set_thumbnail(url=interaction.user.avatar)
                await channellog.send(embed=embed)

                #----------------------------------------------------------------------------------

            if select.values[0] == '02':
                category = discord.utils.get(guild.categories, id=int(config['ticketcategory']))
                channel = await guild.create_text_channel(name=f'ticket-{interaction.user.display_name}-02', category=category, overwrites=overwrites)
                await interaction.response.send_message(f'Ticket oluşturuldu. - <#{channel.id}>', ephemeral=True)
                await channel.send(f'(<@&1127717158940577844>) - ({interaction.user.mention})')
                embed = discord.Embed(title='Tasarım ile ilgili bir şey soracam', description='Merhaba açtığınız tickettan dolayı tasarım ile ilgili bir sorunuz olduğunu varsayıyorum, sorunuz nedir?', colour=discord.Colour.blurple())
                embed.add_field(name='Örnek:', value='Logo yaptırdım ama beğenmedim, logo da bir kurt olsun ve kurtun rengi kırmızı olsun.', inline=False)
                embed.add_field(name='kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Departman:', value=f'<@&1127717158940577844>', inline=True)
                await channel.send(embed=embed, view=self.TicketClose())

                #-------------------------------------------------------------------------- log

                channellog = discord.utils.get(guild.channels, id=int(config['ticketlog']))
                embed = discord.Embed(title='Ticket Log' ,description=f'({interaction.user.mention}) adlı kullanıcı (Tasarım ile ilgili bir şey soracam) ticketı açtı.', colour=discord.Colour.blurple())
                embed.add_field(name='Kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Kullanıcı adı:', value=interaction.user.display_name, inline=True)
                embed.add_field(name='Ticket:', value=channel.mention, inline=True)
                embed.add_field(name='Ticket adı:', value=channel.name, inline=True)
                embed.add_field(name='Ticket ID:', value=channel.id, inline=True)
                embed.add_field(name='Ticket oluşturulma tarihi:', value=channel.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
                embed.add_field(name='Ticket oluşturulma zamanı:', value=channel.created_at.strftime('%H:%M:%S'), inline=True)
                embed.set_thumbnail(url=interaction.user.avatar)
                await channellog.send(embed=embed)

                #----------------------------------------------------------------------------------

            if select.values[0] == '03':
                category = discord.utils.get(guild.categories, id=config['ticketcategory'])
                channel = await guild.create_text_channel(name=f'ticket-{interaction.user.display_name}-03', category=category, overwrites=overwrites)
                await interaction.response.send_message(f'Ticket oluşturuldu. - <#{channel.id}>', ephemeral=True)
                await channel.send(f'(<@&1127717158940577844>) - ({interaction.user.mention})')
                embed = discord.Embed(title='Diğer', description='Merhaba açtığınız tickettan dolayı tasarım dışında bir sorununuz olduğunu varsayıyorum, sorunuz nedir?', colour=discord.Colour.blurple())
                embed.add_field(name='Örnek:', value='Sunucuda şu yetkileden şikayetçiyim yada şu kullanıcıdan şikayetçiyim.', inline=False)
                embed.add_field(name='kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Departman:', value=f'<@&1127717158940577844>', inline=True)
                await channel.send(embed=embed, view=self.TicketClose())

                #-------------------------------------------------------------------------- log

                channellog = discord.utils.get(guild.channels, id=int(config['ticketlog']))
                embed = discord.Embed(title='Ticket Log' ,description=f'({interaction.user.mention}) adlı kullanıcı (Diğer) ticketı açtı.', colour=discord.Colour.blurple())
                embed.add_field(name='Kullanıcı:', value=interaction.user.mention, inline=True)
                embed.add_field(name='Kullanıcı adı:', value=interaction.user.display_name, inline=True)
                embed.add_field(name='Ticket:', value=channel.mention, inline=True)
                embed.add_field(name='Ticket adı:', value=channel.name, inline=True)
                embed.add_field(name='Ticket ID:', value=channel.id, inline=True)
                embed.add_field(name='Ticket oluşturulma tarihi:', value=channel.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=True)
                embed.add_field(name='Ticket oluşturulma zamanı:', value=channel.created_at.strftime('%H:%M:%S'), inline=True)
                embed.set_thumbnail(url=interaction.user.avatar)
                await channellog.send(embed=embed)

        select.callback = ticketcallback
        select.disabled = False
        view = View(timeout=None)
        view.add_item(select)
        await interaction.response.send_message('Lütfen bir seçim yapınız.', view=view, ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx):
        TicketButton = discord.ui.Button(style=discord.ButtonStyle.green, label='Ticket Aç', custom_id='ticketolustur')
        TicketButton.callback = self.callback
        TicketButton.disabled = False
        TicketView = discord.ui.View(timeout=None)
        TicketView.add_item(TicketButton)
        embed = discord.Embed(title='Ticket', description='Ticket kanalı açmak için lütfen aşağıdaki butona basınız.', colour=discord.Colour.blurple())
        embed.add_field(name='Kurallar:', value='* Lütfen boş yere veya denemek için ticket açmayınız.\n* Bedava tasarım yaptırmak için ticket açmayınız.\n* ticket oluşturduğunuz anda yaptırmak istediğiniz tasarımı yada sorununuzu detaylı bir şekilde belirtiniz.\n* Yaptırmak istediğiniz tasarım veya sorununuzu açık ve anlaşılır bir şekilde belirtiniz.', inline=False)
        embed.add_field(name='Bilgilendirme:', value='* Ticket açtıktan sonra hemen cevap alamayabilirsiniz lütfen sabırlı olunuz teşekkürler <3', inline=False)
        embed.set_footer(text='Developed by siestaxd')
        await ctx.send(embed=embed, view=TicketView)

def setup(bot):
    bot.add_cog(Ticket(bot))