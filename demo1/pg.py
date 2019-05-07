import psycopg2

PSQL_HOST = "localhost"
PSQL_PORT = 5432
PSQL_USER = "reddytintayaconde"
PSQL_PASS = "123456"
PSQL_DB   = "reconocimiento"
#connstr ="host=%s port=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
class Persona:
    def __init__(self, img_source, nombre):
        self.img_source =img_source
        self.nombre = nombre
    def getNombre(self):
        return self.nombre
    def getImgSrc(self):
        return self.img_source

know_face_persons = []


try:
    conn = psycopg2.connect("dbname=reconocimiento user=reddytintayaconde password=123456")
    cur =conn.cursor()
    sqlquery = "select nombre, img_src from know_users ORDER BY id;"
    cur.execute(sqlquery)
    row =cur.fetchone()

    while row is not None:
        print (row)
        know_face_persons.append(Persona(row[1], row[0]))
        print(know_face_persons[len(know_face_persons)-1].getNombre())
        row =cur.fetchone()

    cur.close()
    conn.close()
except:
    print("DB error")

"""
from PIL import Image

im = Image.open("obama.jpg")
im.save("obama.png")

convertir formato de imagen
"""
