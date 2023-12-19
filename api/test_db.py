import psycopg2

try:
    print("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(host = "localhost",
                            database = "k_drama_data_TEST",
                            user = "postgres",
                            password = "justin101")
    
    cur = conn.cursor()

    # test statement
    print("PostgreSQL database version: ")
    cur.execute('SELECT * FROM drama')

    print(cur.fetchone())


except (Exception, psycopg2.DatabaseError) as error:
    print(error)
                        
