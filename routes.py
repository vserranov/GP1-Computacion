from flask import Flask, render_template, request
from beebotte import *
import sqlite3 as lite
import array, json

API_KEY = '99302716969be17770b3ec06830b5ec5'
SECRET_KEY = '3064706736c55bd8841e392983aaeeb6248fbd93a6283f5fda94050d72c06a5a'

med_local = 0
med_remota = 0

app = Flask(__name__)

@app.route('/')
def inicio():
  con = lite.connect('datos.db')
  cur = con.cursor()
  cur.execute("SELECT * FROM Datos ORDER BY Fecha,Hora DESC limit 10")
  return render_template('inicio.html', rows=cur.fetchall())

@app.route('/umbral', methods=['GET','POST'])
def umbral():
  umb = 100
  cuenta = 0

  if request.method == 'POST':
    superan = []
    umb = request.form['Umbral']

    con = lite.connect('datos.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Datos ORDER BY Fecha,Hora DESC limit 5")
    rows = cur.fetchall()
    for row in rows:
      if float(umb) < row[2]:
	superan[0+cuenta*3:3+cuenta*3] = [row[0], row[1], row[2]] 
        cuenta = cuenta+1

    long = range(len(superan)/3)
    return render_template('umbral.html', umbral=umb, pasan=superan, longitud=long, veces=cuenta)

  else:
    return render_template('umbral.html', umbral=umb, veces=cuenta)

@app.route('/media', methods=['GET','POST'])
def media():
  global med_local
  global med_remota

  if request.method == 'POST':
    if request.form['Media'] == 'Local': 
      med_local = 0
      con = lite.connect('datos.db')
      cur = con.cursor()
      cur.execute("SELECT * FROM Datos ORDER BY Fecha,Hora DESC limit 3")
      rows = cur.fetchall()
      num = len(rows)
      for row in rows:
        med_local = med_local+row[2]

      med_local = med_local/num
      return render_template('media.html', media=med_local, datos=med_remota) 

    elif request.form['Media'] == 'Beebotte':
      med_remota = 0
      bclient = BBT(API_KEY, SECRET_KEY)
      leer = bclient.read('Datos', 'Numero', limit = 3)
      tot = len(leer)
      for lectura in range(len(leer)):
	med_remota = med_remota+float(leer[lectura]['data'])

      med_remota = med_remota/tot
      return render_template('media.html', datos=med_remota, media=med_local)

  else:
    return render_template('media.html', media=0, datos=0)

@app.route('/graficas')
def graficas():
  con = lite.connect('datos.db')
  cur = con.cursor()
  cur.execute("SELECT * FROM Datos ORDER BY Fecha,Hora DESC limit 10")
  return render_template('graficas.html', rows=cur.fetchall())

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
