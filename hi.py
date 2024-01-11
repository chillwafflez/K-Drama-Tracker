from api.db import get_connection

synopsis = "i love aot. it's justin's favorite anime EVER! but yorimoi is a close second. penis's"
synopsis = synopsis.replace("'", "''")
title = "justin's cafe"
title = title.replace("'", "''")
sql = f"INSERT INTO drama(mdl_id, title, native_title, synopsis, duration, air_year, airing, cover_path) VALUES (6969, '{title}', 'dqdw', '{synopsis}', 43, 2023, False, 'blah/blah/wsup.png');"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()

sql2 = f"SELECT * FROM drama WHERE drama.title = {title};"
cursor.execute(sql2)
results = cursor.fetchone()
print(results)

cursor.close()
conn.close()