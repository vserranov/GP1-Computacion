#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re, time, sys, schedule
import sqlite3 as lite
from beebotte import *

API_KEY = '99302716969be17770b3ec06830b5ec5'
SECRET_KEY = '3064706736c55bd8841e392983aaeeb6248fbd93a6283f5fda94050d72c06a5a'

def job():
    # Obtenemos el codigo fuente de la pagina 
    url = 'http://www.numeroalazar.com.ar/'
    pagina = urllib2.urlopen(url)
    codigo = pagina.read()
    pagina.close()

    # Nos quedamos solo con el primer numero
    regex = r'\s([\d]{1,3}\.[\d]{2})'
    array = re.findall(regex,codigo)

    # Almacenamos el numero, la fecha y la hora en la base de datos local (sqlite)
    datos = (
        (time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"), float(array[2]))
    )

    try:
        con = lite.connect('datos.db')

        cur = con.cursor()

#        cur.execute("DROP TABLE IF EXISTS Datos")
#        cur.execute("CREATE TABLE Datos(Fecha TEXT, Hora TEXT, Numero FLOAT)")
        cur.execute("INSERT INTO Datos VALUES(?, ?, ?)", datos)

        con.commit()

        cur.execute("SELECT * FROM Datos")
        cols = [cn[0] for cn in cur.description]
        rows = cur.fetchall()

        print "%-10s %-8s %s" % (cols[0], cols[1], cols[2])

        for row in rows:
	    print row[0], row[1], row[2]

    except lite.Error, e:
        if con:
	    con.rollback()

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
	    con.close()

    # Almacenamos el numero, la fecha y la hora en la base de datos en la nube (beebotte)
    bclient = BBT(API_KEY, SECRET_KEY)

    bclient.write('Datos', 'Fecha', datos[0])
    bclient.write('Datos', 'Hora', datos[1]) 
    bclient.write('Datos', 'Numero', datos[2])

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
