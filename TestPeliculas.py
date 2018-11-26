import unittest
import Peliculapro

class TestInsert(unittest.TestCase):
#Creamos la tabla peliculas antes de comenzar el test para evitar problemas en los querys
	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")

		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def tearDown(self):
		#Borramos la info de la base de datos para evitar problemas con otros test
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def test_insertarPelicula(self):
		#Caso de prueba correcto, se espera recibir una lista con datos
		pelicula = Peliculapro.Pelicula('cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		resultado = Peliculapro.Sqlitedb.insertarPelicula(self, pelicula)
		self.assertEqual(resultado, [('cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')])

		#Caso de prueba donde se trata de insertar un string de una película que no existe en lugar de un objeto pelicula,
		#se espera recibir un string notificando error.
		res2 = Peliculapro.Sqlitedb.insertarPelicula(self, "98754333))))")
		self.assertEqual(res2, "No se pudo agregar la pelicula a la tabla, probablemente no está en la api")

class TestDelete(unittest.TestCase):

#Creamos la tabla peliculas e insertamos peliculas para eliminar
	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')""")

		conn.commit()
		conn.close()

#Borramos la info de la base de datos para evitar problemas con otros test
	def tearDown(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()


	def test_eliminarPelicula(self):

		#Caso de prueba donde se elimna una película que si existe y que se recibio un objeto pelicula como parametro
		#Se espera recibir una lista vacía
		pelicula = Peliculapro.Pelicula('rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')
		resultado = Peliculapro.Sqlitedb.eliminarPelicula(self, pelicula)
		self.assertEqual(resultado, [])

		#Caso de prueba donde se elimna una película que no existe y que se recibio un objeto pelicula como parametro
		#Se espera recibir un string de error con la eliminacion
		pelicula = Peliculapro.Pelicula('aaaaaaabbbbbb', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		resultado = Peliculapro.Sqlitedb.eliminarPelicula(self, pelicula)
		self.assertEqual(resultado, "No se puede eliminar la película porque no está en la base de datos")

		#Caso de prueba donde se elimna una película que no existe y que se recibio un Nulo como parametro
		#Se espera recibir un string de error con la eliminacion
		resultado2 = Peliculapro.Sqlitedb.eliminarPelicula(self, None)
		self.assertEqual(resultado, "No se puede eliminar la película porque no está en la base de datos")


class TestUpdate(unittest.TestCase):

	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')""")

		c.execute("""INSERT INTO peliculas VALUES (
		'bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde', Null, Null, Null)""")

		conn.commit()
		conn.close()

#Se elimina toda la información de la bd para no generar problemas con otros test
	def tearDown(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def test_agregarLink(self):
        #Caso de prueba donde se intenta actualizar una pelicula que no existe en la BD
		#Se espera un string notificando error
		pelicula = Peliculapro.Pelicula('aaaaaaabbbbbb', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
        'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
        'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		resultado = Peliculapro.Sqlitedb.agregarLink(self, pelicula, "Youtube.com/watch=gdhbsjkvdh3")
		self.assertEqual(resultado, "No se puede actualizar el link de la película porque no está en la base de datos")

		#Caso de prueba donde se intenta actualizar una pelicula pasando un parametro None
		#Se espera un string notificando error
		resultado2 = Peliculapro.Sqlitedb.agregarLink(self, None, "Youtube.com/watch=abcdefghijk")
		self.assertEqual(resultado2, "No se puede actualizar el link de la película porque no está en la base de datos")

		#Caso de prueba donde se actualiza el link de una pelicula existente en la BD
		#Se espera recibir una lista de la pelicula actualizada con el nuevo link
		pelicula2 = Peliculapro.Pelicula('rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')
		resultado3 = Peliculapro.Sqlitedb.agregarLink(self, pelicula2, "Pelisplus.com/ver_ralph_espanol")
		self.assertEqual(resultado3, [('rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'Pelisplus.com/ver_ralph_espanol')])

		#Caso de prueba donde se actualiza el link de una pelicula existente pero que no tiene los datos completos en la BD
		#Se espera recibir una lista de la pelicula actualizada con el nuevo link en ligar de un None
		pelicula3 = Peliculapro.Pelicula('bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde', None, None, None)
		resultado4 = Peliculapro.Sqlitedb.agregarLink(self, pelicula3, "PelisChidas.com/ver_bolt_full_hd_4k_100_real_no_fake")
		self.assertEqual(resultado4, [('bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde',
		None, None, 'PelisChidas.com/ver_bolt_full_hd_4k_100_real_no_fake')])

class TestSelect(unittest.TestCase):

	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')""")

		c.execute("""INSERT INTO peliculas VALUES (
		'bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde',
		Null, Null, Null)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')""")

		conn.commit()
		conn.close()

#Se elimina toda la información de la bd para no generar problemas con otros test
	def tearDown(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def test_consultarPelicula(self):
		#Caso de prueba donde se busca una pelicula existente en la BD
		#Se espera una lista
		pelicula = Peliculapro.Pelicula('cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		resultado = Peliculapro.Sqlitedb.consultarPelicula(self, pelicula)
		self.assertEqual(resultado, [('cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')])

		#Caso de prueba donde se busca una pelicula que no existe en la BD
		#Se espera un string notificando error
		resultado2 = Peliculapro.Sqlitedb.consultarPelicula(self, None)
		self.assertEqual(resultado2, "La película que buscas no está en la base de datos")

		#Caso de prueba donde se busca una pelicula no existente en la BD
		#Se espera un string notificando error
		pelicula2 = Peliculapro.Pelicula('!@#$DFgdfg456', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')
		resultado3 = Peliculapro.Sqlitedb.consultarPelicula(self, pelicula2)
		self.assertEqual(resultado3, "La película que buscas no está en la base de datos")

		#Caso de prueba donde se busca una pelicula existente en la BD pero tiene datos incompletos
		#Se espera una lista con los datos de la pelicula
		pelicula3 = Peliculapro.Pelicula('bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde', None, None, None)
		resultado4 = Peliculapro.Sqlitedb.consultarPelicula(self, pelicula3)
		self.assertEqual(resultado4, [('bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde', None, None, None)])

class TestGetSqlite(unittest.TestCase):

	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'rh3859309', 'Ralph', 'Ficcion, Aventura, Infantil', '22 abril 2015',
		'https://m.media-amazon.com/images/ralhdjshka384384jasj.jpg', '8.5',
		'Un personaje de un videojuego se cansa de ser malo', 'http://youtube.com/whatch=vi64va84pe93na',
		'Ralph Wifi', 'www.pelispedia.com')""")

		c.execute("""INSERT INTO peliculas VALUES (
		'bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde',
		Null, Null, Null)""")

		c.execute("""INSERT INTO peliculas VALUES (
		'cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')""")

		conn.commit()
		conn.close()

#Se elimina toda la información de la bd para no generar problemas con otros test
	def tearDown(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def test_get_pelicula(self):

		#Caso de prueba donde se obtiene una pelicula con un titulo de la base de datos con un titulo de una pelcula existente
		#Se comparan los id's
		res = Peliculapro.Sqlitedb.get_pelicula(self, "Cars")
		pelicula = Peliculapro.Pelicula('cs4820384', 'Cars', 'Infanitl, Fantasia', '10 oct 2005',
		'https://m.media-amazon.com/images/kusdhf9e829scarsjejejd.jpg', '9.0', 'Los carritos se adentran en una aventura divertida',
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		self.assertEqual(res.id, pelicula.id)

		#Caso de prueba donde se intenta obtener una película con un titulo no existente en la BD
		#Se espera recibir un None
		res2 = Peliculapro.Sqlitedb.get_pelicula(self, "ABABABABA")
		self.assertEqual(res2, None)

		#Caso de prueba donde se obtiene una pelicula de la base de datos con un titulo de una pelcula existente pero está con datos incompletos
		#Se comparan los id's
		res3 = Peliculapro.Sqlitedb.get_pelicula(self, 'Bolt')
		pelicula2 = Peliculapro.Pelicula('bt9345875', 'Bolt', 'Infantil, Aventura', '24 ene 2009',
		'https://m.media-amazon.com/images/boltelshido349578.jpg', '9.7',
		'Un perrito guapo que cree que tiene poderes se pierde', None, None, None)
		self.assertEqual(res3.id, pelicula2.id)

class TestGetOMDBApi(unittest.TestCase):

	def setUp(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()

		c.execute("""CREATE TABLE IF NOT EXISTS peliculas (
					ID text PRIMARY KEY,
					TITULO text,
					GENERO text,
					FECHA_DE_LANZAMIENTO text,
					POSTER text,
					RATING text,
					SINOPSIS text,
					TRAILER text,
					RELACIONADAS text,
					LINK text)""")


		conn.commit()
		conn.close()

#Se elimina toda la información de la bd para no generar problemas con otros test
	def tearDown(self):
		conn = Peliculapro.sqlite3.connect('peliculas.db')
		c = conn.cursor()
		c.execute('''DELETE FROM peliculas''')
		conn.commit()
		conn.close()

	def test_get_pelicula(self):
		api = Peliculapro.OmdbApi()
		res = Peliculapro.OmdbApi.get_pelicula(api, "Cars")

		#Caso de prueba donde se obtiene una pelicula de la api con un titulo de una pelcula existente
		#Se comparan los id's
		pelicula = Peliculapro.Pelicula('tt0317219', 'Cars', 'Animation, Comedy, Family, Sport', '09 Jun 2006',
		'https://m.media-amazon.com/images/M/MV5BMTg5NzY0MzA2MV5BMl5BanBnXkFtZTYwNDc3NTc2._V1_SX300.jpg', '7.1', "A hot-shot race-car named Lightning McQueen gets waylaid in Radiator Springs, where he finds the true meaning of friendship and family.",
		'http://youtube.com/whatch=cars2urjfj659', 'Cars 2, Cars 3, Aviones', 'www.youtube.com/watch=ver_cars_full_espanol')
		self.assertEqual(res.id, pelicula.id)

		#Caso de prueba donde se obtiene una pelicula de laapi con un titulo de una pelcula no existente
		#Se espera un string notificando error
		res2 = Peliculapro.OmdbApi.get_pelicula(api, "LOLOLOLOLOL")
		self.assertEqual(res2, "No se encontró la pelicula en la Api")

		#Caso de prueba donde se obtiene una pelicula de la api con un titulo mas complejo en caracteres de una pelcula existente
		#Se comparan los id's
		res3 = Peliculapro.OmdbApi.get_pelicula(api, 'Bolt')
		pelicula2 = Peliculapro.Pelicula("tt0397892", 'Bolt' 'Animation, Adventure, Comedy, Drama, Family', '21 Nov 2008',
		"https://m.media-amazon.com/images/M/MV5BNDQyNDE5NjQ1N15BMl5BanBnXkFtZTcwMDExMTAwMg@@._V1_SX300.jpg", '6.9',
		"The canine star of a fictional sci-fi/action show that believes his powers are real embarks on a cross country trek to save his co-star from a threat he believes is just as real.",
		None, None, None)
		self.assertEqual(res3.id, pelicula2.id)

if __name__ == '__main__':
	unittest.main()
