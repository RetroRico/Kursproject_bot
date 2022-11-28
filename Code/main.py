import discord
import requests
import Config
import Music
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=Config.Prefix,
                   intents=intents)  # Створюємо префікс для команд і щоб бот бачив користувачів серверу


@bot.event  # Повідомляє в консоль про працездатність бота
async def on_ready():
    print('{0.user} зараз працює'.format(bot))


@bot.command()  # Команда ping - показує час оклику бота
async def ping(ctx):
    await ctx.send(f"Pong *{round(bot.latency * 1000)} Ms*")


bot.remove_command('help')


@bot.command()  # Команда help - виводить список команд бота
async def help(ctx):
    await ctx.send(Config.help)


@bot.command()  # Команда join - приєднується до голосового каналу де знаходиться користувач
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()  # Команда leave - виходить з голосового каналу
async def leave(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@bot.command()  # Команда play <url> - (виконується коли бот знаходиться в голосовому каналі) відтворює звуковий youtube url запит в голосовому каналі
async def play(ctx, *, url):
    ctx.voice_client.stop()
    async with ctx.typing():
        player = await Music.YTDLSource.from_url(url, loop=bot.loop)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send(f'Now playing: {player.title}')


@bot.command()  # Команда pause - призупиняє відтворенню url запита
async def pause(ctx):
    ctx.voice_client.pause()


@bot.command()  # Команда pause - відновляє відтворення url запита
async def resume(ctx):
    ctx.voice_client.resume()


@bot.command()  # Команда weather <city> - виводить інформацію про погоду в <city> (місто повинно бути написано на англ мові)
async def weather(ctx, *, City: str):
    def kelvin_to_celsius(kelvin):
        celsius = kelvin - 273.15
        return celsius

    url = Config.weather_url + "appid=" + Config.API_key + "&q=" + City  # Причина, чому потрібно писати місто на англ мові - він створює url запить для отримання інформації
    response = requests.get(url).json()
    weather = response['weather'][0]['main']
    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    cloud = response['clouds']['all']
    await ctx.send(f"""
        ```
Погода: {weather}
Температура: {temp_celsius:.2f}°C
За відчуттям: {feels_like_celsius:.2f}°C
Вологість: {humidity}%
Хмарність: {cloud}%
Швидкість повітря: {wind_speed} м/c ``` """)


@bot.command()  # Команда sd - вимкнення бота через дискорд (якщо не хочеться вимикати через консоль )
async def sd(ctx):
    await ctx.send("Виконується викнення бота")
    await bot.logout()


# Події отримання ролі (список знаходиться в файлі Config, клас Roles())
@bot.event  # Виконання події при якій якщо користувач додає "реакцію" (або іншим словом емодзі) під конкрентним повідомленням, він отримає роль, яка привязана до цієї реакції
async def on_raw_reaction_add(payload):
    if payload.message_id == Config.Post_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = Config.Roles(payload, guild).Role()
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await payload.member.add_roles(role)
                print("Додано роль {0} для {1}.".format(role, member))
            else:
                print("Користувача не знайдено.")
        else:
            print("Роль не знайдено.")


@bot.event  # Виконання події при якій якщо користувач видаляє "реакцію" (або іншим словом емодзі) під конкрентним повідомленням, з нього видаляється роль, яка привязана до цієї реакції
async def on_raw_reaction_remove(payload):
    if payload.message_id == Config.Post_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = Config.Roles(payload, guild).Role()
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("Віднято роль {0} у {1}.".format(role, member))
            else:
                print("Користувача не найдено.")
        else:
            print("Роль не знайдено.")


bot.run(Config.TOKEN)  # Запуск бота
