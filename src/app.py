from flask import Flask, render_template, redirect, url_for, request, session, escape
import pymysql

conn = pymysql.connect('localhost','root','root','tiendaDeportiva')
app = Flask(__name__)
app.secret_key=12345

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email='{0}' AND password='{1}'".format(email,password))
        usuario = cur.fetchall()
        if len(usuario)>0:
            return redirect(url_for('index'))
    return redirect(url_for('start'))

@app.route('/index')
def index():
    if "useremail" in session:
        return render_template('index.html')
    return redirect(url_for('start'))
@app.route('/proteinas')
def proteinas():
    if "useremail" in session:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM productos WHERE tipo='proteina'
            """)
        proteinas = cur.fetchall()
        print(proteinas)
        return render_template('proteinas.html', data = proteinas)
    return redirect(url_for('start'))
@app.route('/quemadores')
def quemadores():
    if "useremail" in session:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM productos WHERE tipo='quemador'
            """)
        quemadores = cur.fetchall()
        print(quemadores)
        return render_template('quemadores.html',data = quemadores)
    return redirect(url_for('start'))
@app.route('/preentrenos')
def preentrenos():
    if "useremail" in session:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM productos WHERE tipo='preentreno'
            """)
        preentrenos = cur.fetchall()
        print(preentrenos)
        return render_template('preentrenos.html',data = preentrenos)
    return redirect(url_for('start'))
@app.route('/add')
def add():
    if "useremail" in session:
        return render_template('add_product.html')
    return redirect(url_for('start'))
@app.route('/add_product', methods=['POST'])
def add_product():
    if "useremail" in session:
        if request.method == "POST":
            nombre = request.form['nombre']
            tipo = request.form['tipo']
            valor = request.form['valor']
            descripcion = request.form['descripcion']
            img = request.form['img']
            cur = conn.cursor()
            cur.execute("INSERT INTO productos(nombre,tipo,valor,descripcion,img)VALUE(%s,%s,%s,%s)",(nombre, tipo, valor, descripcion,img))
            conn.commit()
            cur.close
        return redirect(url_for('index'))
    return redirect(url_for('start'))
@app.route('/update/<id>')
def update(id):
    if "useremail" in session:
        cur = conn.cursor()
        cur.execute("SELECT * FROM productos WHERE id={0}".format(id))
        productos= cur.fetchall()
        return render_template('update_product.html',productos = productos[0])
    return redirect(url_for('start'))
@app.route('/update_product/<id>', methods=['POST'])
def update_product(id):
    if "useremail" in session:
        # el name en los inputs debe coincidir con el nombre de los campos en la tabla de la base de datos
        if request.method == 'POST':
            nombre = request.form['nombre']
            tipo = request.form['tipo']
            valor = request.form['valor']
            descripcion = request.form['descripcion']
            img = request.form['img']
            cur = conn.cursor()
            cur.execute("""
                UPDATE productos
                SET nombre = '{0}',
                    tipo = '{1}',
                    valor = {2},
                    descripcion = '{3}'
                    img = '{4}'
                WHERE id = {5}
            """.format(nombre, tipo, valor, descripcion, img, id))
        return redirect(url_for('index'))
    return redirect(url_for('start'))
@app.route('/delete/<id>')
def delete(id):
    if "useremail" in session:
        cur = conn.cursor()
        cur.execute("DELETE FROM productos WHERE id={0}".format(id))
        conn.commit()
        cur.close()
        return redirect(url_for('index'))
    return redirect(url_for('start'))
if __name__ == '__main__':
    app.run(port=3000,debug=True)