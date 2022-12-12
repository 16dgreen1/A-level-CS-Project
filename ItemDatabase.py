import sqlite3

connector = sqlite3.connect("item.db")
cursor = connector.cursor()

# creating the database
cursor.execute("""CREATE TABLE items (
name text,
damage real,
shot_delay real,
spread real,
bullet_speed real,
bullets_at_once integer,
is_auto text,
clip_size integer,
max_ammo integer,
reload_time integer
)""")

# adding the weapons into the database
cursor.execute("INSERT INTO items VALUES ('handgun', 30, 5, 5, 15, 1, 'False', 15, 200, 180)")
cursor.execute("INSERT INTO items VALUES ('assault rifle', 30, 10, 10, 15, 1, 'True', 30, 270, 240)")
cursor.execute("INSERT INTO items VALUES ('smg', 20, 5, 15, 15, 1, 'True', 30, 300, 240)")
cursor.execute("INSERT INTO items VALUES ('lmg', 40, 15, 10, 15, 1, 'True', 60, 300, 360)")
cursor.execute("INSERT INTO items VALUES ('revolver', 50, 5, 2, 20, 1, 'False', 6, 96, 240)")
cursor.execute("INSERT INTO items VALUES ('sniper rifle', 300, 60, 0, 30, 2, 'False', 10, 100, 300)")  # this weapon has 0 spread and shoots 2 bullets at the same time, this means that if the first shot kills an enemy, the second will kill one behind it
cursor.execute("INSERT INTO items VALUES ('shotgun', 50, 20, 30, 10, 6, 'False', 8, 88, 300)")

connector.commit()
connector.close()
