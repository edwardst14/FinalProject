from ticdb import DBConnection
from player import Player

db = DBConnection()

def testConnection():
	db.getUserByName("Gula")
	player = Player("Gula", 100, 100)
	db.updateUserScores(player)

