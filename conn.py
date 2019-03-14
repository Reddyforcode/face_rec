import psycopg2

try:
    connection = psycopg2.connect("dbname=reconocimiento user=reddytintayaconde password=123456")
    cursor = connection.cursor()
    postgres_insert_query = """ INSERT INTO reg (nombre, img_src) VALUES (%s,%s)"""
    record_to_insert = ('reddy', 'path')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into mobile table")
except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")