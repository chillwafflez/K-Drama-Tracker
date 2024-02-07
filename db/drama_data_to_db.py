import csv
from db_connection import get_connection

def move_drama_genres_to_db(title, mdl_id, year, genre_str, conn):
    cursor = conn.cursor()

    # first get drama id
    sql = f"SELECT drama.id FROM drama WHERE drama.title='{title}' AND drama.mdl_id={mdl_id};"
    cursor.execute(sql)
    drama_id = cursor.fetchone()[0]

    genres = genre_str.split(",")
    for genre in genres:
        # check if genre already exists in db
        genre_check_query = f"SELECT EXISTS (SELECT genre_name FROM genre WHERE genre_name = '{genre}');"
        cursor.execute(genre_check_query)
        record_exists = cursor.fetchone()[0]

        if record_exists:       # check if genre is a record in genre table
            print("Genre already exists, not making new record")

            # get id of genre record
            genre_id_query = f"SELECT genre.id FROM genre WHERE genre.genre_name='{genre}';"
            cursor.execute(genre_id_query)
            genre_id = cursor.fetchone()[0]

            # check if association record between drama and genre exists
            drama_genre_check_query = f"SELECT EXISTS (SELECT * FROM drama_genre WHERE drama_id = {drama_id} AND genre_id = {genre_id});"
            cursor.execute(drama_genre_check_query)
            drama_genre_exist = cursor.fetchone()[0]

            if drama_genre_exist:
                print("DramaGenre association alreaedy exists, not making new record")
            else:
                # create association record between drama and genre
                drama_genre_query = f"INSERT INTO drama_genre(drama_id, genre_id) VALUES ({drama_id}, {genre_id});"
                cursor.execute(drama_genre_query)
                conn.commit()
        else:                   
            # create new record for genre in genre table
            new_genre_query = f"INSERT INTO genre(genre_name) VALUES ('{genre}');"
            cursor.execute(new_genre_query)
            conn.commit()
        
            # get id of genre record
            genre_id_query = f"SELECT genre.id FROM genre WHERE genre.genre_name='{genre}';"
            cursor.execute(genre_id_query)
            genre_id = cursor.fetchone()[0]

            # create association record between drama and genre
            drama_genre_query = f"INSERT INTO drama_genre(drama_id, genre_id) VALUES ({drama_id}, {genre_id});"
            cursor.execute(drama_genre_query)
            conn.commit()
    cursor.close()
    

def move_drama_tags_to_db(title, mdl_id, year, tag_str, conn):
    cursor = conn.cursor()

    # first get drama id
    sql = f"SELECT drama.id FROM drama WHERE drama.title='{title}' AND drama.mdl_id={mdl_id};"
    cursor.execute(sql)
    drama_id = cursor.fetchone()[0]

    tags = tag_str.split(",")
    for tag in tags:
        # check if tag already exists in db
        tag_check_query = f"SELECT EXISTS (SELECT tag_name FROM tag WHERE tag_name = '{tag}');"
        cursor.execute(tag_check_query)
        record_exists = cursor.fetchone()[0]

        if record_exists:       # check if tag is a record in genre table
            print("Tag already exists, not making new record")

            # get id of tag record
            tag_id_query = f"SELECT tag.id FROM tag WHERE tag.tag_name='{tag}';"
            cursor.execute(tag_id_query)
            tag_id = cursor.fetchone()[0]

            # check if association record between drama and tag exists
            drama_tag_check_query = f"SELECT EXISTS (SELECT * FROM drama_tag WHERE drama_id = {drama_id} AND tag_id = {tag_id});"
            cursor.execute(drama_tag_check_query)
            drama_tag_exist = cursor.fetchone()[0]

            if drama_tag_exist:
                print("DramaTag association alreaedy exists, not making new record")
            else:
                # create association record between drama and tag
                drama_tag_query = f"INSERT INTO drama_tag(drama_id, tag_id) VALUES ({drama_id}, {tag_id});"
                cursor.execute(drama_tag_query)
                conn.commit()
        else:                   
            # create new record for tag in tag table
            new_tag_query = f"INSERT INTO tag(tag_name) VALUES ('{tag}');"
            cursor.execute(new_tag_query)
            conn.commit()
        
            # get id of tag record
            tag_id_query = f"SELECT tag.id FROM tag WHERE tag.tag_name='{tag}';"
            cursor.execute(tag_id_query)
            tag_id = cursor.fetchone()[0]

            # create association record between drama and tag
            drama_tag_query = f"INSERT INTO drama_tag(drama_id, tag_id) VALUES ({drama_id}, {tag_id});"
            cursor.execute(drama_tag_query)
            conn.commit()
    cursor.close()


def move_drama_networks_to_db(title, mdl_id, year, network_str, conn):
    cursor = conn.cursor()

    # first get drama id
    sql = f"SELECT drama.id FROM drama WHERE drama.title='{title}' AND drama.mdl_id={mdl_id};"
    cursor.execute(sql)
    drama_id = cursor.fetchone()[0]

    networks = network_str.split(",")
    for network in networks:
        # check if network already exists in db
        network_check_query = f"SELECT EXISTS (SELECT network_name FROM network WHERE network_name = '{network}');"
        cursor.execute(network_check_query)
        record_exists = cursor.fetchone()[0]

        if record_exists:       # check if tag is a record in genre table
            print("Network already exists, not making new record")

            # get id of tag record
            network_id_query = f"SELECT network.id FROM network WHERE network.network_name='{network}';"
            cursor.execute(network_id_query)
            network_id = cursor.fetchone()[0]

            # check if association record between drama and tag exists
            drama_network_check_query = f"SELECT EXISTS (SELECT * FROM drama_network WHERE drama_id = {drama_id} AND network_id = {network_id});"
            cursor.execute(drama_network_check_query)
            drama_network_exist = cursor.fetchone()[0]

            if drama_network_exist:
                print("DramaNetwork association already exists, not making new record")
            else:
                # create association record between drama and tag
                drama_network_query = f"INSERT INTO drama_network(drama_id, network_id) VALUES ({drama_id}, {network_id});"
                cursor.execute(drama_network_query)
                conn.commit()
        else:                   
            # create new record for network in network table
            new_network_query = f"INSERT INTO network(network_name) VALUES ('{network}');"
            cursor.execute(new_network_query)
            conn.commit()
        
            # get id of network record
            network_id_query = f"SELECT network.id FROM network WHERE network.network_name='{network}';"
            cursor.execute(network_id_query)
            network_id = cursor.fetchone()[0]

            # create association record between drama and network
            drama_network_query = f"INSERT INTO drama_network(drama_id, network_id) VALUES ({drama_id}, {network_id});"
            cursor.execute(drama_network_query)
            conn.commit()
    cursor.close()


def main():
    conn = get_connection()

    with open ('data\completed_SK_extra_info.csv', 'r') as csvfile:
       reader = csv.reader (csvfile, delimiter=',')
       next(reader)     # skip first row which are just column headers
       for row in reader: # loop over the rows
        drama_title = row[0]
        year = row[1]
        mdl_id = row[2]
        network_string = row[3].replace("'", "''")
        genre_string = row[4].replace("'", "''")
        tag_string = row[5].replace("'", "''")

        try:
            if genre_string != "":
                move_drama_genres_to_db(drama_title, mdl_id, year, genre_string, conn)
            if tag_string != "":
                move_drama_tags_to_db(drama_title, mdl_id, year, tag_string, conn)
            if network_string != "":
                move_drama_networks_to_db(drama_title, mdl_id, year, network_string, conn)
        except:
           print("bruh")
    
    conn.close()

main()

def testing():
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT * FROM drama_genre WHERE drama_id = 2 AND genre_id = 2);"
    cursor.execute(sql)
    drama_record_exists = cursor.fetchone()[0]
    print(drama_record_exists)
    
    cursor.close()
    conn.close()

