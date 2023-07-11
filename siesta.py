import discord
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import os
import asyncio
import json

def config():
    with open('config.json', encoding='utf-8') as f:
        return json.load(f)

config = config()

bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.streaming, name=config["activity"], url='https://www.twitch.tv/riotgames'))
    bot.add_view(ServerAboutButton())

async def load():
    for filename in os.listdir('./komutlar'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'komutlar.{filename[:-3]}')
                print(f'[KOMUT] {filename} yüklendi')
            except Exception as e:
                print(f'Hata yüklenirken: {e}')

# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Böyle bir komut bulunamadı.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Bu komutu kullanmak için yetkiniz yok.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Bu komutu kullanmak için gerekli argümanları girmediniz.')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Bu komutu tekrar kullanabilmek için {} saniye beklemelisiniz.'.format(math.ceil(error.retry_after)))
    if isinstance(error, commands.NotOwner):
        await ctx.send('Bu komutu sadece bot sahibi kullanabilir.')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('Bu komutu kullanmak için gerekli rolünüz yok.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Bu komutu kullanmak için botun gerekli yetkileri yok.')
    if isinstance(error, commands.MissingRole):
        await ctx.send('Bu komutu kullanmak için gerekli rolünüz yok.')
    if isinstance(error, commands.RoleNotFound):
        await ctx.send('Bu komutu kullanmak için gerekli rol bulunamadı.')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Bu komutu kullanmak için gerekli üye bulunamadı.')
    if isinstance(error, commands.ChannelNotFound):
        await ctx.send('Bu komutu kullanmak için gerekli kanal bulunamadı.')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(config["resimlihgbbid"])) # picture entry and exit
    image = Editor('background.png')
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((140, 140)).circle_image()
    poppins = Font.poppins(size=50, variant='bold')
    poppins_small = Font.poppins(size=25, variant='light')
    image.paste(profile, (280, 60))
    image.ellipse((275,55), 150,150, outline='#00ff2a', stroke_width=5)
    image.text((260, 215), f'{member.name}', font=poppins, color='white')
    image.text((200, 260), f'Welcome to our server!', font=poppins_small, color='white')
    image.save(f'./users/welcome/welcome_{member.name}.png')
    file = discord.File(f'./users/welcome/welcome_{member.name}.png')
    await channel.send(file=file)
    channel = bot.get_channel(int(config["gelengidenlogid"])) # incoming outgoing log
    embed = discord.Embed(title=f'Welcome!', description=f'{member.mention}', color=0x00ff00)
    embed.add_field(name=f'Name', value=f'{member.name}', inline=False)
    embed.add_field(name=f'ID', value=f'{member.id}', inline=False)
    embed.add_field(name=f'Created At', value=f'{member.created_at}', inline=False)
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text=f'{member.guild}')
    await channel.send(embed=embed)
    channel = bot.get_channel(int(config["sayaclogid"])) # user count
    if channel:
        count = len(list(channel.guild.members))
        embed = discord.Embed(title=f'{member.guild}', color=0x7f9cfc)
        embed.add_field(name='Total Members', value=f'{count}', inline=True)
        embed.add_field(name='Member Target', value=f'500/({500-count} people left)', inline=True)
        await channel.send(embed=embed)
    role = member.guild.get_role(int(config["otorolid"])) # unregistered role
    await member.add_roles(role)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(config["resimlihgbbid"])) # picture entry and exit
    image = Editor('background.png')
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((140, 140)).circle_image()
    poppins = Font.poppins(size=50, variant='bold')
    poppins_small = Font.poppins(size=25, variant='light')
    image.paste(profile, (280, 60))
    image.ellipse((275,55), 150,150, outline='#ff0000', stroke_width=5)
    image.text((260, 215), f'{member.name}', font=poppins, color='white')
    image.text((200, 260), f'Goodbye, See You Again!', font=poppins_small, color='white')
    image.save(f'./users/godbye/goodbye_{member.name}.png')
    file = discord.File(f'./users/godbye/goodbye_{member.name}.png')
    await channel.send(file=file)
    channel = bot.get_channel(int(config["gelengidenlogid"])) # incoming outgoing log
    embed = discord.Embed(title=f'Goodbye!', description=f'{member.mention}', color=0xff0000)
    embed.add_field(name=f'Name', value=f'{member.name}', inline=False)
    embed.add_field(name=f'ID', value=f'{member.id}', inline=False)
    embed.add_field(name=f'Created At', value=f'{member.created_at}', inline=False)
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text=f'{member.guild}')
    await channel.send(embed=embed)
    channel = bot.get_channel(int(config["sayaclogid"])) # user count
    if channel:
        count = len(list(channel.guild.members))
        embed = discord.Embed(title=f'{member.guild}', color=0x7f9cfc)
        embed.add_field(name='Total Members', value=f'{count}', inline=True)
        embed.add_field(name='Member Target', value=f'{config["sayachedef"]}/({int(config["sayachedef"])-count} people left)', inline=True)
        await channel.send(embed=embed)

class ServerAboutButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Kurallar', custom_id='rules', style=discord.ButtonStyle.blurple, emoji='📜')
    async def rules(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='Kurallar', description='Selamlar, Sunucumuzda derli toplu güzel ve sorunsuz bir topluluk oluşturmak için belli başlı belirlediğimiz kurallar vardır. Sunucumuzdaki kurallar şunlardır', color=0x7f9cfc)
        embed.add_field(name='# Genel Kurallar:', value='* Farklı sunucular hakkında bilgi vermek yasaktır.\n* Başka sunucularda olan sunucu dışı olayları sunucuya yansıtmak yasaktır.\n* Grup veya ekip kurmak yasaktır, buna benzer davranışlar yasaktır.\n* Sunucu üyelerimizi DM veya sesli kanallarda reklam yapmak yasaktır.\n* Sunucu içerisinde din, dil, ırk ayrımı ve siyaset yapmak yasaktır.\n* Sunucu içerisinde veya özel mesaj yoluyla reklam yapmak yasaktır.', inline=False)
        embed.add_field(name='# Metin Kanalları:', value='* Din, dil, ırk, siyaset ile ilgili hakaret edici ve aşağılayıcı konular konuşmak yasaktır.\n* Büyük harf (CAPS LOCK) kullanımı yasaktır. \n*  Flood yapmak yasaktır. (üst üste 3 - 4 kez veya daha fazla mesajı alt alta yazmak.)\n*  Spam yapmak yasaktır. (üst üste 4 - 5 kez veya daha fazla aynı mesajı alt alta yazmak.)\n Birinin kişisel bilgisini paylaşmak yasaktır. (isim - soy isim, numara vb.)\n* Küfür, hakaret, kışkırtıcı ve aşağılayıcı konular konuşmak yasaktır.\n* Ücretli tasarım yapan arkadaşlardan ücretsiz dilenmek yasaktır lütfen yapmayınız.', inline=False)
        embed.add_field(name='# Ses Kanalları:', value='* Küfür, hakaret, kışkırtıcı ve aşağılayıcı konuşmalar yasaktır.\n* Soundpad vb. programlar kullanarak milleti rahatsız etmek kesinlikle yasaktır.\n* Bağırmak, odada ki ses bütünlüğünü bozmak diğer kişilere üstünlük kurmaya çalışmak yasaktır.', inline=False)
        embed.add_field(name='# Discord Varsayılan topluluk kuralları:', value='* https://discord.com/terms\n* https://discord.com/guidelines\n buralardaki kurallar geçerlidir.', inline=False)
        embed.add_field(name='# Bilgilendirme:', value='Sunucumuzda kendinizce kurallar koyarak diğer üyelere üstünlük sağlamak yasaktır. bir sorununuz olursa <@&1127717154041647315> rolündeki yetkililere ulaşabilirsiniz.', inline=False)
        embed.set_footer(text='Kurallarımızı okuduğunuz için teşekkür ederiz.')
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='SSS', custom_id='sss',style=discord.ButtonStyle.blurple, emoji='❓')
    async def faq(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='Sıkça Sorulan Sorular', description='Sunucumuzda sıkça sorulan sorulara buradan ulaşabilirsiniz.', color=0x7f9cfc)
        embed.add_field(name='1. Ücretsiz Tasarım yapıyormusunuz?' , value='Hayır, ücretsiz tasarım yapmıyoruz.', inline=False)
        embed.add_field(name='2. Tasarım yaptırmak istiyorum nasıl iletişime geçebilirim?' , value='Tasarım yaptırmak istiyorsanız <#1128103377360912547> kanalına giderek ticket açabilirsiniz.', inline=False)
        embed.add_field(name='3. Tasarım yaptırmak istiyorum ama ücretleri çok pahalı' , value='Eğer ücretli tasarımcılarımızın fiyatları size pahalı geliyorsa ücretsiz tasarım yapan başka sunuculara bakabilirsiniz.', inline=False)
        embed.add_field(name='Daha fazlası Eklenecek' , value='Sıkça sorulan sorulara buradan ulaşabilirsiniz.', inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='Ticket', custom_id='ticket', style=discord.ButtonStyle.blurple, emoji='🎫')
    async def ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='Tasarım Talep', description='Tasarım talebinde bulunmak için aşağıdaki butona tıklayınız.', color=0x7f9cfc)
        embed.set_footer(text='Tasarım talebinde bulunmak için aşağıdaki butona tıklayınız.')
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.command()
@commands.has_permissions(administrator=True)
async def serverabout(ctx):
    embed = discord.Embed(title=" ",color=discord.Colour.blurple())
    embed.set_image(url="https://media.discordapp.net/attachments/800009379868180494/1128089163581894686/si_es_ta.png?width=1250&height=500")
    embedserver = discord.Embed(title="İsim Graphic Sunucusuna Hoş Geldiniz!",description="Discord'daki grafik tasarımcılar için özel olarak hazırladığımız topluluğa hoş geldiniz \nbu sunucuda isterseniz hazır paylaşılan tasarım şablonlarını istersenizde özel olarak tasarım yaptırabileceğiniz kişileri bulabilirsiniz.\nİyi eğlenceler!", color=discord.Colour.blurple())
    embedserver.set_image(url="https://media.discordapp.net/attachments/800009379868180494/1128086681845772470/asdsad.png?width=1250&height=50")
    await ctx.send(embed=embed)
    await ctx.send(embed=embedserver , view=ServerAboutButton())

async def main():
    await load()
    await bot.login(config['token'])
    await bot.connect()

asyncio.run(main())