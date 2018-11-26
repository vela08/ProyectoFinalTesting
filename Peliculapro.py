from abc import ABC, abstractmethod
import requests
import json
import sqlite3
import os
import time

class Pelicula():

    def __init__(self,id,titulo,genero,fecha_lanz,poster,rating,sinopsis,trailer=None,relacionados=None,link=None):

        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.fecha_lanz = fecha_lanz
        self.poster = poster
        self.rating = rating
        self.sinopsis = sinopsis
        self.trailer = trailer
        self.relacionados = relacionados
        self.link = link

class AbstractApi(ABC):
    @abstractmethod
    def get_pelicula(self, nombre):
        pass
        """Toma como parametro el nombre de la película y regresa un objeto de tipo película, la clase se que conecte al api implementa esta clase abstracta"""

class AbstractDb(ABC):
    @abstractmethod
    def crearTablaPeliculas(self):
        pass

    @abstractmethod
    def insertarPelicula(self, pelicula):
        pass
        """Toma como parametro un objeto de tipo pelicula y regresa un objeto de tipo pelicula con los nuevos datos,
        la clase que se conecta a la base de datos implementa este metodo"""

    @abstractmethod
    def agregarTrailer(self, pelicula):
        pass
        """Toma como parametro un objeto de tipo pelicula y regresa un objeto de tipo pelicula con los nuevos datos,
        la clase que se conecta a la base de datos implementa este metodo"""


    @abstractmethod
    def agregarRelacionados(self, pelicula):
        pass

    @abstractmethod
    def agregarLink(self, pelicula):
        pass


    @abstractmethod
    def consultarPelicula(self, pelicula):
        pass

    @abstractmethod
    def eliminarPelicula(self, pelicula):
        pass

    @abstractmethod
    def get_pelicula(self, titulo):
        pass

class Sqlitedb(AbstractDb):
    def crearTablaPeliculas(self):
        conn = sqlite3.connect('peliculas.db')
        c = conn.cursor()
        if c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
                    ID text PRIMARY KEY,
                    TITULO text,
                    GENERO text,
                    FECHA_DE_LANZAMIENTO text,
                    POSTER text,
                    RATING text,
                    SINOPSIS text,
                    TRAILER text,
                    RELACIONADAS text,
                    LINK text
                    )"""):
                    return "Tabla peliculas creada con exito"
        else:
            return "Error al crear la tabla peliculas"
        conn.commit()
        conn.close()

    def get_pelicula(self, titulo):
        #conectar a la base de datos
        conexion = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        consulta = conexion.cursor()

        consulta.execute("""SELECT * FROM peliculas WHERE titulo= :titulo """, {'titulo':titulo})
        #terminamos la consulta
        resultado = consulta.fetchall()
        if not resultado:
            print("No se encontró la pelicula en la base de datos.")
            return None
        else:
            pelicula = Pelicula(resultado[0][0],resultado[0][1],resultado[0][2],resultado[0][3],resultado[0][4],resultado[0][5],resultado[0][6],resultado[0][7],
            resultado[0][8],resultado[0][9])
            conexion.commit()
            #guardamos los cambios en la base de datos
            #cerramos la conexion a la base de datos
            return pelicula
        conexion.close()

    def insertarPelicula(self, pelicula):
        if type(pelicula) is str:
            return "No se pudo agregar la pelicula a la tabla, probablemente no está en la api"
        conn = sqlite3.connect('peliculas.db')
        c = conn.cursor()
        c.execute('''SELECT id FROM peliculas WHERE id = :ID''',{'ID': pelicula.id})
        id = c.fetchone()
        if not id:
            if c.execute("""INSERT INTO peliculas VALUES (
            :ID, :TITULO, :GENERO, :FECHA_DE_LANZAMIENTO, :POSTER, :RATING, :SINOPSIS, :TRAILER, :RELACIONADAS, :LINK)""",
            {'ID': pelicula.id, 'TITULO': pelicula.titulo, 'GENERO': pelicula.genero, 'FECHA_DE_LANZAMIENTO': pelicula.fecha_lanz, 'POSTER': pelicula.poster,
            'RATING': pelicula.rating, 'SINOPSIS': pelicula.sinopsis, 'TRAILER': pelicula.trailer, 'RELACIONADAS': pelicula.relacionados, 'LINK': pelicula.link}):
                print("La pelicula {} fue insertada con exito a la tabla de la base de datos".format(pelicula.titulo))
            else:
                print("Error al insertar la pelicula en la tabla")
            conn.commit()
            c.execute("""SELECT * FROM PELICULAS WHERE TITULO = :TIT""",
            {'TIT': pelicula.titulo})
            return c.fetchall()
            conn.close()
        else:
            resultado = 'La película {} ya está en la base de datos, no es necesario agregarla'.format(pelicula.titulo)
            conn.close()
            return resultado

    def agregarTrailer(self, pelicula, trailer):
        conn = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        c = conn.cursor()
        #sql = ("""UPDATE peliculas
        #SET trailer= "https://youtu.be/JcpWXaA2qeg"
        #WHERE id= :ID)""", {'ID': pelicula.id})
        if pelicula == None:
            return "No se puede actualizar el trailler de la película porque no está en la base de datos"
        else:
            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            verif = c.fetchall()
            if verif == []:
                return "No se puede actualizar el trailler de la película porque no está en la base de datos"
            c.execute("""UPDATE peliculas SET trailer= :trailer WHERE id= :ID""", {'ID': pelicula.id, 'trailer': trailer})

            #terminamos la consulta
            #guardamos los cambios en la base de datos
            conn.commit()

            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id': pelicula.id})
            return c.fetchall()
            conn.commit()
            #cerramos la conexion a la base de datos
            conn.close()

    def agregarRelacionados(self, pelicula, rel):
        conn = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        c = conn.cursor()
        #sql = ("""UPDATE peliculas
        #SET trailer= "https://youtu.be/JcpWXaA2qeg"
        #WHERE id= :ID)""", {'ID': pelicula.id})
        if pelicula == None:
            return "No se puede actualizar las películas relacionadas porque la película no está en la base de datos"
        else:
            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            verif = c.fetchall()
            if verif == []:
                return "No se puede actualizar las películas relacionadas porque la película no está en la base de datos"
            c.execute("""UPDATE peliculas SET relacionadas= :rel WHERE id= :ID""", {'ID': pelicula.id, 'rel': rel})

            #terminamos la consulta
            #guardamos los cambios en la base de datos
            conn.commit()

            c.execute("SELECT * FROM PELICULAS WHERE id= :ID", {'ID': pelicula.id})
            return c.fetchall()
            conn.commit()

            #cerramos la conexion a la base de datos
            conn.close()

    def agregarLink(self, pelicula, link):
        conn = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        c = conn.cursor()
        #sql = ("""UPDATE peliculas
        #SET trailer= "https://youtu.be/JcpWXaA2qeg"
        #WHERE id= :ID)""", {'ID': pelicula.id})
        if pelicula == None:
            return "No se puede actualizar el link de la película porque no está en la base de datos"
        else:
            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            verif = c.fetchall()
            if verif == []:
                return "No se puede actualizar el link de la película porque no está en la base de datos"
            c.execute("""UPDATE peliculas SET link= :LINK WHERE id= :ID""", {'ID': pelicula.id, 'LINK': link})

            #terminamos la consulta
            #guardamos los cambios en la base de datos
            conn.commit()

            c.execute("SELECT * FROM PELICULAS WHERE id= :ID", {'ID': pelicula.id})
            return c.fetchall()
            conn.commit()

            #cerramos la conexion a la base de datos
            conn.close()

    def consultarPelicula(self, pelicula):
        conexion = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        c = conexion.cursor()
        if pelicula == None:
            return "La película que buscas no está en la base de datos"
        else:
            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            verif = c.fetchall()
            if verif == []:
                return "La película que buscas no está en la base de datos"
        query = c.execute(""" SELECT * FROM peliculas WHERE id= :id """, {'id': pelicula.id})
        return query.fetchall()
        #for row in query:
            #print(' ID: {}'.format(row[1])
        #guardamos los cambios en la base de datos
        conexion.commit()
        #cerramos la conexion a la base de datos
        conexion.close()

    def eliminarPelicula(self, pelicula):
        #conectar a la base de datos
        conexion = sqlite3.connect("peliculas.db")
        #seleccionar el cursor para realizar la consulta
        c = conexion.cursor()
        # c.execute('''SELECT id FROM peliculas WHERE id = :ID''',{'ID': pelicula.id})
        # id = c.fetchone()
        if pelicula == None:
            return "No se puede eliminar la película porque no está en la base de datos"
        else:
            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            verif = c.fetchall()
            if verif == []:
                return "No se puede eliminar la película porque no está en la base de datos"
            c.execute("""DELETE FROM peliculas WHERE id= :id """, {'id':pelicula.id})

            #terminamos la consulta
            #guardamos los cambios en la base de datos
            conexion.commit()

            c.execute("SELECT * FROM PELICULAS WHERE id = :id", {'id':pelicula.id})
            res = c.fetchall()
            print('Se ha eliminado con éxito la pelicula: "{}"'.format(pelicula.titulo))
            return res

            conexion.commit()

            #cerramos la conexion a la base de datos
            conexion.close()

#De aqui para abajo es lo que editaremos, es solo una idea
class OmdbApi(AbstractApi):
    def __init__(self,urlbase = "http://www.omdbapi.com/?", apikey = "2541db07", headers = {'Content-Type': 'application/json'}):
        self.urlbase = urlbase
        self.apikey = apikey
        self.headers = headers

    def get_pelicula(self, nombrepeli):
        api_url = '{0}&apikey={1}&t='.format(self.urlbase,self.apikey)+nombrepeli
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            contenidopelicula = json.loads(response.content.decode('utf-8'))
            if contenidopelicula is not None:
                if contenidopelicula['Response'] == "False":
                    return "No se encontró la pelicula en la Api"
                else:
                    #print("Información obtenida de la api (OMDBapi): ")
                    for k, v in contenidopelicula.items():
                        if k == 'imdbID':
                            #print('ID:{}'.format(v))
                            id = v
                        if k == 'Title':
                            #print('Título:{}'.format(v))
                            titulo = v
                        if k == 'Genre':
                            #print('Género:{}'.format(v))
                            genero = v
                        if k == 'Released':
                            #print('Fecha de lanzamiento:{}'.format(v))
                            fecha = v
                        if k == 'Poster':
                            #print('Póster:{}'.format(v))
                            poster = v
                        if k == 'imdbRating':
                            #print('Rating:{}'.format(v))
                            rating = v
                        if k == 'Plot':
                            #print('Sinopsis:{}'.format(v))
                            sinopsis = v
                    pelicula = Pelicula(id,titulo,genero,fecha,poster,rating,sinopsis)
                    print("Se encontró la película {} y se creó su objeto".format(nombrepeli))
                    return pelicula
            else:
                print('[!] Request Failed')
        else:
            return None

def menu():
    # Mostramos el menu
    os.system('clear')
    print ("PROGRAMA PARA LA MATERIA DE TESTING")
    print ("\t1 - Consultar una Película")
    print ("\t2 - Eliminar una Película")
    print ("\t3 - Actualizar información de una Película")
    print ("\t4 - Agregar una Película a la Base de Datos")
    print ("\t9 - Salir")


def main():
    while True:
        api = OmdbApi()
        sqlite = Sqlitedb()
        crear = sqlite.crearTablaPeliculas()
        print(crear)
        menu()
        opcionMenu = input("Selecciona la opción que desees : ")
        if opcionMenu=="1":
            print ("")
            peli = input("Has pulsado la opción 1...\nIntroduce el nombre de la película a Consultar: ")
            obj = sqlite.get_pelicula(peli)
            if not obj:
                input('Pulsa una tecla para volver al menú')
            else:
                res = sqlite.consultarPelicula(obj)
                print('\nId: {}'.format(res[0][0]))
                print('Title: {}'.format(res[0][1]))
                print('Genre: {}'.format(res[0][2]))
                print('Released: {}'.format(res[0][3]))
                print('Poster: {}'.format(res[0][4]))
                print('Rating: {}'.format(res[0][5]))
                print('Plot: {}'.format(res[0][6]))
                print('Trailer: {}'.format(res[0][7]))
                print('Related Movies: {}'.format(res[0][8]))
                print('Link for watch online: {}'.format(res[0][9]))
                print("")
                input('Pulsa una tecla para volver al menú')
        elif opcionMenu=="2":
            print ("")
            peli = input("Has pulsado la opción 2...\nIntroduce el nombre de la película a Eliminar: ")
            obj = sqlite.get_pelicula(peli)
            # if not obj:
            #     input('Pulsa una tecla para volver al menú')
            # else:
            res = sqlite.eliminarPelicula(obj)
            print(res)
            input('Pulsa una tecla para volver al menú')

        elif opcionMenu=="3":
            print ("")
            peli = input("Has pulsado la opción 3...\nIntroduce el nombre de la película a Actualizar: ")
            obj = sqlite.get_pelicula(peli)
            if not obj:
                input('Pulsa una tecla para volver al menú')
            else:
                opcion = input('Qué deseas agregar/actualizar? \n1.- Link \n2.- Relacionadas \n3.- Trailer \nEscribe tu opción: ')
                if opcion == "1":
                    link = input('Introduce el link para ver la pelicula en linea: ')
                    res = sqlite.agregarLink(obj,link)
                    print('\nId: {}'.format(res[0][0]))
                    print('Title: {}'.format(res[0][1]))
                    print('Genre: {}'.format(res[0][2]))
                    print('Released: {}'.format(res[0][3]))
                    print('Poster: {}'.format(res[0][4]))
                    print('Rating: {}'.format(res[0][5]))
                    print('Plot: {}'.format(res[0][6]))
                    print('Trailer: {}'.format(res[0][7]))
                    print('Related Movies: {}'.format(res[0][8]))
                    print('Link for watch online: {}'.format(res[0][9]))
                    print("")
                    input('Pulsa una tecla para volver al menú')
                elif opcion == "2":
                    relacionadas = input('Introduce las peliculas relacionadas a agregar: ')
                    res = sqlite.agregarRelacionados(obj, relacionadas)
                    print('\nId: {}'.format(res[0][0]))
                    print('Title: {}'.format(res[0][1]))
                    print('Genre: {}'.format(res[0][2]))
                    print('Released: {}'.format(res[0][3]))
                    print('Poster: {}'.format(res[0][4]))
                    print('Rating: {}'.format(res[0][5]))
                    print('Plot: {}'.format(res[0][6]))
                    print('Trailer: {}'.format(res[0][7]))
                    print('Related Movies: {}'.format(res[0][8]))
                    print('Link for watch online: {}'.format(res[0][9]))
                    print("")
                    input('Pulsa una tecla para volver al menú')
                elif opcion == "3":
                    trailer = input('Introduce el link del trailer de la pelicula: ')
                    res = sqlite.agregarTrailer(obj,trailer)
                    print('\nId: {}'.format(res[0][0]))
                    print('Title: {}'.format(res[0][1]))
                    print('Genre: {}'.format(res[0][2]))
                    print('Released: {}'.format(res[0][3]))
                    print('Poster: {}'.format(res[0][4]))
                    print('Rating: {}'.format(res[0][5]))
                    print('Plot: {}'.format(res[0][6]))
                    print('Trailer: {}'.format(res[0][7]))
                    print('Related Movies: {}'.format(res[0][8]))
                    print('Link for watch online: {}'.format(res[0][9]))
                    print("")
                    input('Pulsa una tecla para volver al menú')
        elif opcionMenu=="4":
            print ("")
            peli = input("Has pulsado la opción 4...\nIntroduce el nombre de la película a Agregar: ")
            obj = api.get_pelicula(peli)
            if not obj:
                input('Pulsa una tecla para volver al menú')
            else:
                res = sqlite.insertarPelicula(obj)
                print('\nId: {}'.format(res[0][0]))
                print('Title: {}'.format(res[0][1]))
                print('Genre: {}'.format(res[0][2]))
                print('Released: {}'.format(res[0][3]))
                print('Poster: {}'.format(res[0][4]))
                print('Rating: {}'.format(res[0][5]))
                print('Plot: {}'.format(res[0][6]))
                print('Trailer: {}'.format(res[0][7]))
                print('Related Movies: {}'.format(res[0][8]))
                print('Link for watch online: {}'.format(res[0][9]))
                print("")
                input('Pulsa una tecla para volver al menú')
        elif opcionMenu=="9":
            break
        else:
            print ("")
            input("No has pulsado ninguna opción correcta...\nPulsa una tecla para volver al menú")
    #Comentar o descomentar los metodos que se quieran probar, comentar crearTablaPeliculas una vez que ya se creo la tabla para

    #pelicula = sqlite.get_pelicula("It")

    #pelicula = api.get_pelicula("It")
    #sqlite.insertarPelicula(pelicula)
    #sqlite.agregarTrailer(pelicula)
    #sqlite.agregarRelacionados(pelicula)
    #sqlite.agregarLink(pelicula)
    #sqlite.consultarPelicula(pelicula)
    #sqlite.eliminarPelicula(pelicula)

if __name__ == '__main__':
    main()
