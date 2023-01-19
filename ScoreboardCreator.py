import sqlite3

connector = sqlite3.connect("scoreboard.db")
cursor = connector.cursor()

cursor.execute("""CREATE TABLE scores (
name text,
score integer
)""")

connector.commit()
connector.close()
