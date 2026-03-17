import sqlite3
c=sqlite3.connect("database.db");cur=c.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS agencies(id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS agents(id INTEGER PRIMARY KEY, name TEXT, agency_id INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, name TEXT, season TEXT, price INTEGER)")
c.commit(); c.close()
print("DB ready")
