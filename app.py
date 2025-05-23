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

#rutas de la pagina hueb
@app.route('/')
def index():
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    print(data)
    
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
            cur.execute('INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)' , (nombre, correo, telefono, direccion))
            conn.commit()
            flash('Cliente Agregado Exitosamente')
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    
@app.route('/delete/<string:id_cliente>')
def deleteClient(id_cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM clientes WHERE id_cliente = (%s)', (id_cliente,))
    conn.commit()
    flash('Cliente Eliminado Exitosamente')
    
    return redirect(url_for('index'))
    
@app.route('/edit/<string:id_cliente>')
def getClient(id_cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clientes WHERE id_cliente = %s', (id_cliente,))
    data = cur.fetchall()
    
    return render_template('editClient.html', cliente = data[0])

@app.route('/update/<string:id_cliente>', methods = ['POST'])
def updateClient(id_cliente):
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        conn=get_connection()
        cur=conn.cursor()
        cur.execute("""
        UPDATE clientes
        SET nombre = %s,
        correo = %s,
        telefono = %s,
        direccion = %s
        WHERE id_cliente = %s        
        """, (nombre, correo, telefono, direccion, id_cliente,))
        conn.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
