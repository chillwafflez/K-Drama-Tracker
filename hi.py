from api.db import get_connection

synopsis = "i love aot. it's justin's favorite anime EVER! but yorimoi is a close second. penis's"
synopsis = synopsis.replace("'", "''")
sql = f"INSERT INTO drama(mdl_id, title, native_title, synopsis, duration, airing, cover_path) VALUES (6969, 'test drama', 'dqdw', '{synopsis}', 43, False, 'blah/blah/wsup.png');"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()

sql2 = "SELECT * FROM drama WHERE drama.title = 'test drama';"
cursor.execute(sql2)
results = cursor.fetchone()
print(results)

cursor.close()
conn.close()