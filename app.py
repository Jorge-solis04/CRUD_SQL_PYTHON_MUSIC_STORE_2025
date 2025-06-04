from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required


import pymysql
import config
from db import get_connection

# Models
from src.models.ModelUser import ModelUser

#Entities
from src.models.entities.user import User

app = Flask(__name__)
login_manager_app = LoginManager(app)

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

@login_manager_app.user_loader
def load_user(id):
    conn = get_connection()
    return ModelUser.get_by_id(conn, id)

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
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash ("Invalid password")
        else:
            flash("User Not Found")
            return render_template('sesion.html')
    else:
        return render_template('sesion.html')
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/home')
@login_required
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
       
    return render_template('index.html', clientes = data)

@app.route('/addClient' , methods = ['POST'])
@login_required
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
@login_required
def deleteClient(idCliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cliente WHERE idCliente = (%s)', (idCliente,))
    conn.commit()
    flash('Cliente Eliminado Exitosamente')
    
    return redirect(url_for('home'))
    
@app.route('/edit/<string:idCliente>')
@login_required
def getClient(idCliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cliente WHERE idCliente = %s', (idCliente,))
    data = cur.fetchall()
    
    return render_template('editClient.html', cliente = data[0])

@app.route('/update/<string:idCliente>', methods = ['POST'])
@login_required
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
@login_required
def productos():
    filtro = request.args.get('filtro', 'todos')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM album  ")
    album = cursor.fetchall()
            
    cursor.execute("SELECT nombre FROM artista")
    artistas = cursor.fetchall()
    
    if filtro == 'vinilo':
        cursor.execute("""
            SELECT 'vinilo' AS tipo, v.idVinyl AS id, a.nombre AS album, v.precio, v.stock
            FROM vinyl v
            JOIN album a ON v.idAlbum = a.idAlbum
        """)
    elif filtro == 'cd':
        cursor.execute("""
            SELECT 'cd' AS tipo, c.idCD AS id, a.nombre AS album, c.precio, c.stock
            FROM cd c
            JOIN album a ON c.idAlbum = a.idAlbum
        """)
    elif filtro == 'casete':
        cursor.execute("""
            SELECT 'casete' AS tipo, cs.idCasete AS id, a.nombre AS album, cs.precio, cs.stock
            FROM casete cs
            JOIN album a ON cs.idAlbum = a.idAlbum
        """)
    else:
        cursor.execute("""
            SELECT 'vinyl' AS tipo, v.idVinyl AS id, a.nombre AS album, v.precio, v.stock
            FROM vinyl v
            JOIN album a ON v.idAlbum = a.idAlbum

            UNION ALL

            SELECT 'cd' AS tipo, c.idCD AS id, a.nombre AS album, c.precio, c.stock
            FROM cd c
            JOIN album a ON c.idAlbum = a.idAlbum

            UNION ALL

            SELECT 'casete' AS tipo, cs.idCasete AS id, a.nombre AS album, cs.precio, cs.stock
            FROM casete cs
            JOIN album a ON cs.idAlbum = a.idAlbum
        """)

    productos = cursor.fetchall()
    conn.close()
    return render_template('product.html', productos=productos, filtro=filtro, artistas=artistas, album=album)

@app.route('/addProduct', methods=['POST'])
@login_required
def addProduct():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']  # 'cd', 'vinyl' o 'casete'
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        conn = get_connection()
        cur = conn.cursor()

        # Obtener idAlbum
        cur.execute("SELECT idAlbum FROM album WHERE nombre = %s", (nombre,))
        album_row = cur.fetchone()
        if not album_row:
            flash('Álbum no encontrado')
            return redirect(url_for('productos'))
        idAlbum = album_row['idAlbum']

        # Determinar tabla y campos según tipo
        if tipo == 'vinyl':
            tabla = 'vinyl'
            id_campo = 'idAlbum'
        elif tipo == 'cd':
            tabla = 'cd'
            id_campo = 'idAlbum'
        elif tipo == 'casete':
            tabla = 'casete'
            id_campo = 'idAlbum'
        else:
            flash('Tipo de producto no válido')
            return redirect(url_for('productos'))

        # Verificar si ya existe ese album en ese formato
        cur.execute(f"SELECT * FROM {tabla} WHERE {id_campo} = %s", (idAlbum,))
        existe = cur.fetchone()

        if existe:
            # Si existe, actualiza el stock
            cur.execute(f"UPDATE {tabla} SET stock = stock + %s WHERE {id_campo} = %s", (stock, idAlbum))
            flash('Stock actualizado correctamente')
        else:
            # Si no existe, inserta el nuevo producto
            cur.execute(f"INSERT INTO {tabla} (idAlbum, precio, stock) VALUES (%s, %s, %s)", (idAlbum, precio, stock))
            flash('Producto agregado correctamente')

        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

@app.route('/deleteProduct', methods=['POST'])
@login_required
def deleteProduct():
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    
    
    conn = get_connection()
    cur = conn.cursor()

    # Obtener idAlbum
    cur.execute("SELECT idAlbum FROM album WHERE nombre = %s", (nombre,))
    
    album_row = cur.fetchone()

    
    idAlbum = album_row['idAlbum']

    # Determinar tabla según tipo
    if tipo == 'vinyl':
        tabla = 'vinyl'
    elif tipo == 'cd':
        tabla = 'cd'
    elif tipo == 'casete':
        tabla = 'casete'
    else:
        flash('Tipo de producto no válido')
        return redirect(url_for('productos'))

    # Eliminar el producto
    cur.execute(f"DELETE FROM {tabla} WHERE idAlbum = %s", (idAlbum,))
    conn.commit()
    conn.close()
    
    print(tabla,idAlbum )
    return redirect(url_for('productos'))

@app.route('/updateProduct', methods=['POST'])
@login_required
def updateProduct():
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])

    conn = get_connection()
    cur = conn.cursor()

    # Obtener idAlbum
    cur.execute("SELECT idAlbum FROM album WHERE nombre = %s", (nombre,))
    album_row = cur.fetchone()
    idAlbum = album_row['idAlbum']

    # Determinar tabla según tipo
    if tipo == 'vinyl':
        tabla = 'vinyl'
    elif tipo == 'cd':
        tabla = 'cd'
    elif tipo == 'casete':
        tabla = 'casete'
    else:
        flash('Tipo de producto no válido')
        return redirect(url_for('productos'))

    # Actualizar el producto
    cur.execute(f"UPDATE {tabla} SET precio = %s, stock = %s WHERE idAlbum = %s", (precio, stock, idAlbum))
    conn.commit()
    conn.close()
    flash('Producto actualizado correctamente')
    return redirect(url_for('productos'))

@app.route('/editProduct')
@login_required
def editProduct():
    tipo = request.args.get('tipo')
    nombre = request.args.get('nombre')
    precio = request.args.get('precio')
    stock = request.args.get('stock')
    item = {
        'tipo': tipo,
        'nombre': nombre,
        'precio': precio,
        'stock': stock
    }
    return render_template('editProduct.html', item=item)


@app.route('/Artistas')
@login_required
def Artistas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista")
    data_artista = cursor.fetchall()
    print(data_artista)

    return render_template("artistas.html", data_artista = data_artista)

@app.route('/addartista', methods = ['POST'])
@login_required
def addartista():

    if request.method == 'POST':
        nombre = request.form['nombre']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO artista (nombre) VALUES (%s)", nombre)
        conn.commit()

        return redirect(url_for("Artistas"))
    
    #Validacion si ya existe el artista que no te deje y redirija a la pagina Artista
    
@app.route('/getArtista/<string:idArtista>')
@login_required
def getArtista(idArtista):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista WHERE idArtista = %s", (idArtista,))
    data = cursor.fetchall() 

    return render_template("editArtista.html", data_artista = data[0])

@app.route('/updateArtista/<string:idArtista>', methods = ['POST'])
@login_required
def updateArtista(idArtista):
     
     if request.method == 'POST':
        nombre = request.form['nombre']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE artista SET nombre = %s WHERE idArtista = %s", (nombre, idArtista,))
        conn.commit()

        return redirect(url_for('Artistas'))

#De album que se muestren, agreguen, editen, y que no se pueda agregar un mismo album que ya existe.

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada, buscala en tupu</h1>"

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
