import sqlite3

connector = sqlite3.connect("item.db")
cursor = connector.cursor()
# cursor.execute("""CREATE TABLE items (
# name text,
# damage real,
# firerate real,
# spread real,
# bullet_speed real,
# bullets_at_once integer,
# fire_type text
# )""")
connector.commit()
connector.close()
