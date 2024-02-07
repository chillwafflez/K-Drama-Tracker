# import psycopg2
# import psycopg2.pool
# from dotenv import load_dotenv
# import os

# def get_connection():
#     try:
#         load_dotenv() 
#         print("Connecting to PostgreSQL database...")

#         conn = psycopg2.connect(host = os.environ.get("DB_HOST"),
#                                 database = os.environ.get("DB_NAME"),
#                                 user = os.environ.get("DB_USER"),
#                                 password = os.environ.get("DB_PASSWORD"))
#         print(f"Successfully connected")
#         return conn
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)

# def select_query(stmt):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(stmt)
#     results = cursor.fetchone()

#     cursor.close()
#     conn.close()
#     return results

# def select_all_query(stmt):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(stmt)
#     results = cursor.fetchall()

#     cursor.close()
#     conn.close()
#     return results

# genre_sql = "SELECT genre.id, genre_name FROM genre JOIN drama_genre ON drama_genre.genre_id = genre.id JOIN drama ON drama_genre.drama_id = drama.id WHERE drama.id = 1;"
# results = select_all_query(genre_sql)
# print(results)


bruh = "Jo Jeong Seok,  Cho Jung Seok,  Justin Nguyen"
yuh = bruh.replace(" ", "").split(',')
yippee = ""
for i in range(len(yuh)):
    if i == len(yuh) - 1:
        yippee += yuh[i]
        break
    yippee += yuh[i] + "__"

print(yippee)