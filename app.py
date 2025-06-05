from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

import pymysql
import config
from db import get_connection

# Models
from src.models.ModelUser import ModelUser

#Entities
from src.models.entities.user import User
from datetime import datetime

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

@app.route("/register")
def register():
    
    return render_template("registro.html")

@app.route("/registerUser", methods = ['POST'])
def registerUser():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
    
    
    
    hashed_password = generate_password_hash(password)

    print(fullname, username, password)
    print(hashed_password)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (username, password, fullname) VALUES (%s, %s, %s)", (username, hashed_password, fullname))
    conn.commit()
    
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

        # Validación si ya existe
        cursor.execute("SELECT * FROM artista WHERE nombre = %s", (nombre,))
        existente = cursor.fetchone()
        if existente:
            return redirect(url_for("Artistas"))

        cursor.execute("INSERT INTO artista (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        return redirect(url_for("Artistas"))
    
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
@app.route('/albumes')
@login_required
def albumes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT album.idAlbum, album.nombre, album.anio, album.genero, album.disquera, artista.nombre AS artista
        FROM album
        LEFT JOIN artista ON album.idArtista = artista.idArtista
    """)
    data_album = cursor.fetchall()

    cursor.execute("SELECT * FROM artista")
    data_artista = cursor.fetchall()

    return render_template("albumes.html", data_album=data_album, data_artista=data_artista)

@app.route('/addalbum', methods=['POST'])
@login_required
def addalbum():
    nombre = request.form['nombre']
    anio = request.form['anio']
    genero = request.form['genero']
    disquera = request.form['disquera']
    idArtista = request.form['idArtista']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM album WHERE nombre = %s", (nombre,))
    existente = cursor.fetchone()
    if existente:
        flash("El álbum ya existe", "error")
        return redirect(url_for("albumes"))

    cursor.execute(
        "INSERT INTO album (nombre, anio, genero, disquera, idArtista) VALUES (%s, %s, %s, %s, %s)",
        (nombre, anio, genero, disquera, idArtista)
    )
    conn.commit()
    return redirect(url_for("albumes"))

@app.route('/getAlbum/<string:idAlbum>')
@login_required
def getAlbum(idAlbum):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM album WHERE idAlbum = %s", (idAlbum,))
    data_album = cursor.fetchone()

    cursor.execute("SELECT * FROM artista")
    data_artista = cursor.fetchall()

    return render_template("editAlbum.html", album=data_album, data_artista=data_artista)

@app.route('/updateAlbum/<string:idAlbum>', methods=['POST'])
@login_required
def updateAlbum(idAlbum):
    nombre = request.form['nombre']
    anio = request.form['anio']
    genero = request.form['genero']
    disquera = request.form['disquera']
    idArtista = request.form['idArtista']

    conn = get_connection()
    cursor = conn.cursor()

    # Validar que no exista otro álbum con el mismo nombre
    cursor.execute("SELECT * FROM album WHERE nombre = %s AND idAlbum != %s", (nombre, idAlbum))
    existente = cursor.fetchone()
    if existente:
        flash("Ya existe otro álbum con ese nombre", "error")
        return redirect(url_for("albumes"))

    cursor.execute("""
        UPDATE album SET nombre = %s, anio = %s, genero = %s, disquera = %s, idArtista = %s WHERE idAlbum = %s """, (nombre, anio, genero, disquera, idArtista, idAlbum))
    conn.commit()
    return redirect(url_for("albumes"))

@app.route('/ventas')
@login_required
def ventas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        v.idVenta,
        c.nombre AS cliente,
        v.fecha,
        dv.formato,
        dv.idFormato,
        a.nombre AS nombre_album,
        dv.precio_unitario
    FROM venta v
    JOIN cliente c ON v.idCliente = c.idCliente
    JOIN detalle_venta dv ON v.idVenta = dv.idVenta
    LEFT JOIN cd ON dv.formato = 'cd' AND dv.idFormato = cd.idCD
    LEFT JOIN vinyl ON dv.formato = 'vinyl' AND dv.idFormato = vinyl.idVinyl
    LEFT JOIN casete ON dv.formato = 'casete' AND dv.idFormato = casete.idCasete
    LEFT JOIN album a ON 
        (cd.idAlbum = a.idAlbum OR vinyl.idAlbum = a.idAlbum OR casete.idAlbum = a.idAlbum)
    ORDER BY v.idVenta DESC
    """)
    ventas = cursor.fetchall()
    cursor.execute("SELECT idCliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    # Productos por formato
    cursor.execute("""
        SELECT cd.idCD AS idFormato, a.nombre AS album
        FROM cd
        JOIN album a ON cd.idAlbum = a.idAlbum
    """)
    cds = cursor.fetchall()

    cursor.execute("""
        SELECT v.idVinyl AS idFormato, a.nombre AS album
        FROM vinyl v
        JOIN album a ON v.idAlbum = a.idAlbum
    """)
    vinilos = cursor.fetchall()

    cursor.execute("""
        SELECT cs.idCasete AS idFormato, a.nombre AS album
        FROM casete cs
        JOIN album a ON cs.idAlbum = a.idAlbum
    """)
    casetes = cursor.fetchall()

    cursor.close()
    conn.close()
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template(
        "ventas.html",
        ventas=ventas,
        clientes=clientes,
        fecha_actual=fecha_actual,
        cds=cds,
        vinilos=vinilos,
        casetes=casetes
    )

@app.route('/add_venta', methods=['POST'])
@login_required
def add_venta():
    idCliente = request.form['idCliente']
    fecha = request.form['fecha']
    formato = request.form['formato']
    idFormato = request.form['idFormato']
    cantidad = int(request.form['cantidad'])

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Obtener el precio y stock actual del producto
    if formato == 'cd':
        cursor.execute("SELECT precio, stock FROM cd WHERE idCD = %s", (idFormato,))
    elif formato == 'vinyl':
        cursor.execute("SELECT precio, stock FROM vinyl WHERE idVinyl = %s", (idFormato,))
    elif formato == 'casete':
        cursor.execute("SELECT precio, stock FROM casete WHERE idCasete = %s", (idFormato,))
    else:
        flash('Formato no válido')
        return redirect(url_for('ventas'))

    producto = cursor.fetchone()
    if not producto:
        flash('Producto no encontrado')
        return redirect(url_for('ventas'))

    precio_unitario = float(producto['precio'])
    stock_actual = int(producto['stock'])

    # 2. Validar stock suficiente
    if cantidad > stock_actual:
        flash('No hay suficiente stock para esta venta')
        cursor.close()
        conn.close()
        return redirect(url_for('ventas'))

    total = cantidad * precio_unitario

    # 3. Insertar en venta
    cursor.execute(
        "INSERT INTO venta (idCliente, fecha, total) VALUES (%s, %s, %s)",
        (idCliente, fecha, total)
    )
    conn.commit()
    idVenta = cursor.lastrowid

    # 4. Insertar en detalle_venta
    cursor.execute(
        "INSERT INTO detalle_venta (idVenta, formato, idFormato, cantidad, precio_unitario) VALUES (%s, %s, %s, %s, %s)",
        (idVenta, formato, idFormato, cantidad, precio_unitario)
    )

    # 5. Restar stock
    if formato == 'cd':
        cursor.execute("UPDATE cd SET stock = stock - %s WHERE idCD = %s", (cantidad, idFormato))
    elif formato == 'vinyl':
        cursor.execute("UPDATE vinyl SET stock = stock - %s WHERE idVinyl = %s", (cantidad, idFormato))
    elif formato == 'casete':
        cursor.execute("UPDATE casete SET stock = stock - %s WHERE idCasete = %s", (cantidad, idFormato))

    conn.commit()
    cursor.close()
    conn.close()
    flash('Venta registrada correctamente')
    return redirect(url_for('ventas'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada, buscala en tupu</h1>"

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
