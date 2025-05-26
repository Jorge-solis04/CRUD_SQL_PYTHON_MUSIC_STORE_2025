from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import config
from db import get_connection

# Models
from src.models.ModelUser import ModelUser

#Entities
from src.models.entities.user import User

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

#rutas de la pagina hueb
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    conn = get_connection()
    if request.method == 'POST':
        
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(conn, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash ("Invalid password")
        else:
            flash("User Not Found")
            return render_template('sesion.html')
    else:
        return render_template('sesion.html')

@app.route('/home')
def home():
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
       
    return render_template('index.html', clientes = data)

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
            cur.execute('INSERT INTO cliente (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)' , (nombre, correo, telefono, direccion))
            conn.commit()
            flash('Cliente Agregado Exitosamente')
        finally:
            conn.close()
        
        return redirect(url_for('home'))
    
@app.route('/delete/<string:idCliente>')
def deleteClient(idCliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cliente WHERE idCliente = (%s)', (idCliente,))
    conn.commit()
    flash('Cliente Eliminado Exitosamente')
    
    return redirect(url_for('home'))
    
@app.route('/edit/<string:idCliente>')
def getClient(idCliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cliente WHERE idCliente = %s', (idCliente,))
    data = cur.fetchall()
    
    return render_template('editClient.html', cliente = data[0])

@app.route('/update/<string:idCliente>', methods = ['POST'])
def updateClient(idCliente):
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        conn=get_connection()
        cur=conn.cursor()
        cur.execute("""
        UPDATE cliente
        SET nombre = %s,
        correo = %s,
        telefono = %s,
        direccion = %s
        WHERE idCliente = %s        
        """, (nombre, correo, telefono, direccion, idCliente,))
        conn.commit()
        return redirect(url_for('home'))


@app.route('/products')
def products():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM vinyl")
    data=cur.fetchall()
    
    print(data)
    
    return render_template('product.html')



if __name__ == '__main__':
    app.run(port = 5000, debug=True)
