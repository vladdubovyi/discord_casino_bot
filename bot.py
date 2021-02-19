import config
import discord
import db
from random import randint

# Инициализируем подключение к БД
db = db.SQLite(config.db_fileName)

def roll_drums():
	symbs = ['🍎', '🍌', '🍑', '🍍', '🥝']
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
	balance = db.get_bal(str(message.author.id))
	balance = float(str(balance[0]))
	if balance >= bet:
		# Если баланса хватает на кручение
		balance -= bet
		drum = roll_drums()
		bet = check_prize(drum, bet)
		await message.reply(drum[0] + '\t' + drum[1] + '\t' + drum[2] + '\n'
						+ drum[3] + '\t' + drum[4] + '\t' + drum[5] +'\n'
						+ drum[6] + '\t' + drum[7] + '\t' + drum[8] +'\n', mention_author=True)
		await message.reply('Ваш выигрыш составляет ' + str(bet) + '!')
		db.update_bal(str(message.author.id), str(balance + bet))
	else:
		await message.reply('У вас недостаточно копеек для этого кручения!')

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self, message):

		# Основная функция для игры и кручения казиныча
		if message.content.startswith('$play'):
			if db.check_user(str(message.author.id)):
				cont = message.content.split()
				if len(cont) > 1:
					# Кручение на заданую ставку
					bet = float(cont[1])
					await roll_casino(bet, message)
				else:
					# Кручение на 1 копейку
					await roll_casino(1, message)

			else:
				await message.reply('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')

		# Регистрация нового пользователя
		if message.content.startswith('$reg'):
			if(db.check_user(str(message.author.id))):
				await message.reply('Вы уже зарегистрированы! Для просмотра баланса напишите $bal')
			else:
				db.add_user(str(message.author), str(message.author.id))
				await message.reply('Вы были успешно зарегистрированы!')

		# Проверка баланса
		if message.content.startswith('$bal'):
			if(db.check_user(str(message.author.id))):
				a = db.get_bal(str(message.author.id))
				await message.reply('Ваш баланс составляет: ' + str(a[0]) + ' копеек!')
			else:
				await message.reply('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')

		# Вывод помощи
		if message.content.startswith('$help'):
			await message.reply(file=discord.File('img/papich.gif'))
			await message.reply('Здравствуйте ' + message.author.name 
				+ '!\nМеня зовут Казиныч бот 🤖, я был создан специально по заказу величайших участников конференции Distance learning и призван крутить казиныч для все желающих работяг 👨‍🏭\n'
				+ 'Основная валюта в нашем казиныче - копейки 💰, но так же у нас есть специальные сезонные ивенты 🔥, так что следите за новостями\n'
				+ 'Что я могу: \n$play [ставка] - крутить казиныч\n$reg - зарегистрировать работягу в рабочий класс и выдать первые микрогрошы\n$bal - посмотреть баланс\n'
				+ '$update - обновить свой ник в базе данных\n$trans <money> @<user>- передать средства другому игроку'
				+ 'Желаю всем быть на удачичах и грошоподнималычах 🍀!')

		# Перевод денег с одного счета на другой
		if message.content.startswith('$trans'):
			if db.check_user(str(message.author.id)):
				cont = message.content.split()
				if len(cont) == 3:
					money = float(cont[1])
					recipient = str(cont[2])
					recipient = recipient[3 : len(recipient) - 1]
					if db.check_user(recipient):
						source = str(message.author.id)
						balance = db.get_bal(source)
						balance = float(str(balance[0]))
						if(balance >= money):
							balance_r = db.get_bal(recipient)
							balance_r = float(str(balance_r[0]))
							db.update_bal(source, str(balance - money))
							db.update_bal(recipient, str(balance_r + money))
							r_n = db.get_name(str(recipient))
							await message.reply('Операция прошла успешно!\nВы передали ' + str(money) + ' копеек работяге ' + str(r_n[0]))
						else:
							# Если недостаточно средств
							await message.reply('У вас недостаточно средств для перевода!')
					else:
						# Если получатель не найден
						await message.reply('Данный пользователь не найден!')
				else:
					# Вывод ошибки
					await message.reply('Вы неправильно написали комамнду! Правильный формат - $trans [сумма] [имя + id пользователя]')

			else:
				await message.reply('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')

		#Обновление ника в базе данных
		if message.content.startswith('$update'):
			if db.check_user(str(message.author.id)):
				db.update_name(str(message.author.id), str(message.author))
				await message.reply('Вы успешно сменили ник на ' + str(message.author) + '!')
			else:
				await message.reply('Вы еще не зарегистрированы!\nДля регистрации напишите $reg')



client = MyClient()
client.run(config.Bot_token)