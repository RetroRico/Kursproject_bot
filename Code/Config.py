# Тут знаходяться значення, які можна змінювати для іншого бота
import discord

TOKEN = 'MTAzOTU1OTc0MzI1OTI5OTg3MA.GW58h1.Vu2p8PYxzROz3DS00kzLTBrfr7tIa_1CROHMqc'  # Спеціальний ключ для запуску бота в сервері
Prefix = '!'  # Префікс команд
Post_ID = 1041072950184530070  # IP повідомлення, де потрібно вставити "реакцію" (подія отримання ролей)
FFMPEG_OPTIONS = {'options': '-vn'}  # Налагодження для відтворення музики (звуків) (команда play)
YDL_OPTIONS = {'format': 'bestaudio'}  # Налагодження для встановлення музики (звуків) (команда play)
API_key = "5b87e18761461ba64128d0fd42c9aee0"  # Спеціальний ключ користувача OpenWeather (команда weather)
weather_url = "http://api.openweathermap.org/data/2.5/weather?"  # Посилання OpenWeather для створення посилання міста (команда weather)
help = """ 
    ```
!help - Відображення доступних команд (її зараз ви використали)
!ping - Відображає швидкість оклику бота
!join - Бот виконує вхід в голосовий канал
!leave - Бот покидає голосовий канал   
!play <url> - Бот відтворює <url> 
!pause - Бот призупиняє відтворення 
!resume - Бот продовжує відтворення 
!weather <city> - Показує погоду в <city>
!sd - Вимкнення бота ``` """  # Список, який виводить команда help


class Roles():  # Список емодзі та прив'язаних до них ролі (подія отримання ролей)
    def __init__(self, payload, guild):
        self.payload = payload
        self.guild = guild

    def Role(self):
        if self.payload.emoji.name == '👦':
            role = discord.utils.get(self.guild.roles, name='Учень')
        elif self.payload.emoji.name == '🎓':
            role = discord.utils.get(self.guild.roles, name='Студент')
        elif self.payload.emoji.name == '💼':
            role = discord.utils.get(self.guild.roles, name='Працівник')
        else:
            role = None
        return role
