from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import config


app = Flask(__name__)

#Coneccion a la base de datos de MySQL
def get_connection():
    return pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB,
        port=config.MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# settings
app.secret_key = 'mySecretKey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addClient' , methods = ['POST'])
def addClient():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        conn = get_connection() 
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)' , (nombre, correo, telefono, direccion))
            conn.commit()
            flash('Cliente Agregado Exitosamente')
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(port = 3000 ,debug=True)
