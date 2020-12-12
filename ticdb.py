import sqlite3
from player import Player

class DBConnection:

	def __init__(self):
		self.conn = sqlite3.connect("scores.sqlite") #creates the database if it doesn't already exist
		self.cursor = self.conn.cursor() #provides are cursor to the above connection (the means of executing the SQL queries)
		#execute the create table query
		try:
			self.cursor.execute("CREATE TABLE playerScores \
					(ID integer PRIMARY KEY AUTOINCREMENT,		\
					Name text,						\
					Wins integer, 					\
					Losses integer)")
		except:
			print("Database already exists")
		self.SCORES = []


	def getUserByName(self,name):
		entry = self.cursor.execute("SELECT *        \
                FROM playerScores               \
                WHERE Name = ?;", [name])

		data = entry.fetchall()
		#print(data)
		if len(data) != 0:
			print("Alreaady Exists")
			print(data)
		else:
			self.cursor.execute("INSERT INTO    \
			playerScores(Name, Wins, Losses)    \
			VALUES(?,?,?)", [name, 0, 0])

			self.conn.commit()

			new = self.cursor.execute("SELECT *        \
                FROM playerScores               \
                WHERE Name = ?;", [name])
			data = new.fetchall()
			print(data)

		return Player(data[0][0], data[0][1], data[0][2], data[0][3]) #FIXED

	def updateUserScores(self, player):
			if not player:
				return
		
			self.cursor.execute("UPDATE playerscores \
			SET Wins = ?, Losses=? \
			WHERE ID = ?", [player.wins, player.losses, player.id])
			self.conn.commit()

	def displayScores(self):
		data = self.cursor.execute("SELECT Name, Wins	\
			FROM playerscores	\
			WHERE Wins in (SELECT Wins	\
						FROM playerscores	\
						ORDER BY Wins DESC LIMIT 3)	\
			ORDER BY Wins DESC")

		self.SCORES = data.fetchall()
		return self.SCORES
		self.conn.commit()


		
			

