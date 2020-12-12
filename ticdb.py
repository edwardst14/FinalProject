import sqlite3
from player import Player

class DBConnection:

	def __init__(self):
		self.conn = sqlite3.connect("scores.sqlite") #creates the database if it doesn't already exist
		self.cursor = self.conn.cursor() #provides are cursor to the above connection (the means of executing the SQL queries)
		#execute the create table query
		try:
			self.cursor.execute("create table playerScores (name text, wins integer, losses integer)")
		except:
			print("Database already exists")


	def getUserByName(self,name):
		entry = self.cursor.execute("SELECT *        \
                FROM playerScores               \
                WHERE name = ?;", [name])

		data = entry.fetchall()
		#print(data)
		if len(data) != 0:
			print("Alreaady Exists")
			print(data)
		else:
			self.cursor.execute("INSERT INTO    \
			playerScores(name, wins, losses)    \
			VALUES(?,?,?)", [name, 0, 0])

			self.conn.commit()

			new = self.cursor.execute("SELECT *        \
                FROM playerScores               \
                WHERE name = ?;", [name])
			data = new.fetchall()
			print(data)

		return Player(data[0][0], data[0][1], data[0][2]) #FIXED

	def updateUserScores(self, player):
			if not player:
				return
		
			self.cursor.execute("update playerscores \
			set  wins = ?, losses=? \
			where name=?", [player.wins, player.losses, player.name])
			self.conn.commit()
			

