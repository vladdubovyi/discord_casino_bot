import sqlite3

class SQLite:

	def __init__(self, database_fileName):
		self.connection = sqlite3.connect(database_fileName)
		self.cursor = self.connection.cursor()

	def check_user(self, UserId):
		with self.connection:
			return self.cursor.execute("SELECT * FROM `Users` WHERE `UserId` = ?", (UserId, )).fetchall()

	def add_user(self, UserName, UserId):
		with self.connection:
			return self.cursor.execute("INSERT INTO `Users`(`UserId`, `Name`, `Money`) VALUES(?, ?, ?)", (UserId, UserName, 200))

	def get_bal(self, UserId):
		with self.connection:
			return self.cursor.execute("SELECT `Money` FROM `Users` WHERE `UserId` = ?", (UserId,)).fetchone()

	def update_bal(self, UserId, Money):
		with self.connection:
			return self.cursor.execute("UPDATE `Users` SET `Money` = ? WHERE `UserId` = ?", (Money, UserId))

	def update_name(self, UserId, UserName):
		with self.connection:
			return self.cursor.execute("UPDATE `Users` SET `Name` = ? WHERE `UserId` = ?", (UserName, UserId))

	def get_name(self, UserId):
		with self.connection:
			return self.cursor.execute("SELECT `Name` FROM `Users` WHERE `UserId` = ?", (UserId,)).fetchone()