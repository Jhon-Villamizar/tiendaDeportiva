from flask import Flask, render_template, redirect, url_for, request
import pymysql

conn = pymysql.connect('localhost','root','','tiendaDeportiva')
app = Flask(__name__)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    print(productos)
    return render_template('index.html',data = productos)

@app.route('/add')
def add():
    return render_template('add_product.html')

@app.route('/add_product', methods=['POST'])
def add_product():
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

@app.route('/update/<id>')
def update(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id={0}".format(id))
    productos= cur.fetchall()
    return render_template('update_product.html',productos = productos[0])

@app.route('/update_product/<id>', methods=['POST'])
def update_product(id):
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

@app.route('/delete/<id>')
def delete(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id={0}".format(id))
    conn.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000,debug=True)