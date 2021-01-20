import config
import discord
import db
from random import randint

# Инициализируем подключение к БД
db = db.SQLite(config.db_fileName)

def roll_drums():
	symbs = ['#', '@', '*', '%', '^']
	res = []
	i = 0
	while i < 10: 
		res.append(symbs[randint(0, 4)])
		i = i + 1
	return res


def check_prize(drum, bet):
	tmp = bet
	if drum[0] == drum[1] and drum[1] == drum[2]:
		bet *= 2
	if drum[3] == drum[4] and drum[4] == drum[5]:
		bet *= 2
	if drum[6] == drum[7] and drum[7] == drum[8]:
		bet *= 2
	if drum[0] == drum[4] and drum[4] == drum[2]:
		bet *= 1.7
	if drum[3] == drum[7] and drum[7] == drum[5]:
		bet *= 1.7
	if drum[3] == drum[1] and drum[1] == drum[5]:
		bet *= 1.7
	if drum[0] == drum[4] and drum[4] == drum[8]:
		bet *= 1.8
	if drum[2] == drum[4] and drum[4] == drum[6]:
		bet *= 1.8
	if drum[6] == drum[4] and drum[4] == drum[8]:
		bet *= 1.7

	if tmp == bet:
		return 0
	else:
		return bet

async def roll_casino(bet, message):
	balance = db.get_bal(str(message.author))
	balance = float(str(balance[0]))
	if balance >= bet:
		# Если баланса хватает на кручение
		balance -= bet
		drum = roll_drums()
		bet = check_prize(drum, bet)
		await message.channel.send(drum[0] + '\t' + drum[1] + '\t' + drum[2] + '\n'
						+ drum[3] + '\t' + drum[4] + '\t' + drum[5] +'\n'
						+ drum[6] + '\t' + drum[7] + '\t' + drum[8] +'\n')
		await message.channel.send('Ваш выигрыш составляет ' + str(bet) + '!')
		db.update_bal(str(message.author), str(balance + bet))
	else:
		await message.channel.send('У вас недостаточно копеек для этого кручения!')

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self, message):

		# Основная функция для игры и кручения казиныча
		if message.content.startswith('$play'):
			if db.check_user(str(message.author)):
				cont = message.content.split()
				if len(cont) > 1:
					# Кручение на заданую ставку
					bet = float(cont[1])
					await roll_casino(bet, message)
				else:
					# Кручение на 1 копейку
					await roll_casino(1, message)

			else:
				await message.channel.send('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')

		# Регистрация нового пользователя
		if message.content.startswith('$reg'):
			if(db.check_user(str(message.author))):
				await message.channel.send('Вы уже зарегистрированы! Для просмотра баланса напишите $bal')
			else:
				db.add_user(str(message.author))
				await message.channel.send('Вы были успешно зарегистрированы!')

		# Проверка баланса
		if message.content.startswith('$bal'):
			if(db.check_user(str(message.author))):
				a = db.get_bal(str(message.author))
				await message.channel.send('Ваш баланс составляет: ' + str(a[0]) + ' копеек!')
			else:
				await message.channel.send('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')

		# Вывод помощи
		if message.content.startswith('$help'):
			await message.channel.send(file=discord.File('img/papich.gif'))
			await message.channel.send('Здравствуйте ' + message.author.name 
				+ '!\nМеня зовут Казиныч бот 🤖, я был создан специально по заказу величайших участников конференции Distance learning и призван крутить казиныч для все желающих работяг 👨‍🏭\n'
				+ 'Основная валюта в нашем казиныче - копейки 💰, но так же у нас есть специальные сезонные ивенты 🔥, так что следите за новостями\n'
				+ 'Что я могу: \n$play [ставка] - крутить казиныч\n$reg - зарегистрировать работягу в рабочий класс и выдать первые микрогрошы\n$bal - посмотреть баланс\n'
				+ 'Желаю всем быть на удачичах и грошоподнималычах 🍀!')




client = MyClient()
client.run(config.Bot_token)