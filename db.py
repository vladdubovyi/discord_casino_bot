import sqlite3

class SQLite:

	def __init__(self, database_fileName):
		self.connection = sqlite3.connect(database_fileName)
		self.cursor = self.connection.cursor()

	def check_user(self, UserName):
		with self.connection:
			return self.cursor.execute("SELECT * FROM `Users` WHERE `Name` = ?", (UserName, )).fetchall()

	def add_user(self, UserName):
		with self.connection:
			return self.cursor.execute("INSERT INTO `Users`(`Name`, `Money`) VALUES(?, ?)", (UserName, 200))

	def get_bal(self, UserName):
		with self.connection:
			return self.cursor.execute("SELECT `Money` FROM `Users` WHERE `Name` = ?", (UserName,)).fetchone()

	def update_bal(self, UserName, Money):
		with self.connection:
			return self.cursor.execute("UPDATE `Users` SET `Money` = ? WHERE `Name` = ?", (Money, UserName))