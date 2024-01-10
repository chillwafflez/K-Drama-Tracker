import csv
# from ..api.db import get_connection

with open ('scraped_data\completed_SK_extra_info.csv', 'r') as csvfile:
  reader = csv.reader (csvfile, delimiter=',')
  next(reader)
  for row in reader: # loop over the rows
    drama_title = row[0]
    mdl_id = row[2]
    network_string = row[3]
    genre_string = row[4]
    tag_string = row[5]

    print(f"{drama_title} | {mdl_id} | {network_string} | {genre_string} | {tag_string}")

# conn = get_connection()
# cursor = conn.cursor()
# # Get drama's id
# drama_name = "Move to Heaven"
# mdl_id = 49231

# sql = f"SELECT drama.id FROM drama WHERE drama.title='{drama_name}' AND drama.mdl_id={mdl_id};"
# cursor.execute(sql)
# drama_id = cursor.fetchone()[0]


# genre_str = "Action,Youth,Drama"
# genres = genre_str.split(",")
# for genre in genres:
#     genre_check_query = f"SELECT EXISTS (SELECT genre_name FROM genre WHERE genre_name = '{genre}');"
#     cursor.execute(genre_check_query)
#     record_exists = cursor.fetchone()[0]

#     if record_exists:       # check if genre is a record in genre table
#         print("Genre already exists, not making new one record")
#     else:                   
#         # create new record for genre in genre table
#         new_genre_query = f"INSERT INTO genre(genre_name) VALUES ('{genre}');"
#         cursor.execute(new_genre_query)
#         conn.commit()
    
#     # get id of genre record
#     genre_id_query = f"SELECT genre.id FROM genre WHERE genre.genre_name='{genre}';"
#     cursor.execute(genre_id_query)
#     genre_id = cursor.fetchone()[0]

#     # create association record between drama and genre
#     drama_genre_query = f"INSERT INTO drama_genre(drama_id, genre_id) VALUES ({drama_id}, {genre_id});"
#     cursor.execute(drama_genre_query)
#     conn.commit()


# conn.close()
# cursor.close()