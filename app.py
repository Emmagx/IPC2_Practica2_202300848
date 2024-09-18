import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from auto import Auto
import csv

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Carpeta donde se almacenarán las imágenes subidas
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

autos_registrados = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cargar_autos():
    global autos_registrados
    autos_registrados.clear()
    try:
        with open('data/autos.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 8:  
                    placa, marca, modelo, descripcion, precio_unitario, disponible, cantidad, imagen = row
                    auto = Auto(placa, marca, modelo, descripcion, float(precio_unitario), int(cantidad), imagen)
                    auto.disponible = disponible == 'True'
                    autos_registrados.append(auto)
                else:
                    print(f"Fila ignorada (número incorrecto de columnas): {row}")
    except FileNotFoundError:
        print("Archivo autos.csv no encontrado.")

def guardar_autos():
    with open('data/autos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for auto in autos_registrados:
            writer.writerow([auto.placa, auto.marca, auto.modelo, auto.descripcion, auto.precio_unitario, auto.disponible, auto.cantidad, auto.imagen])

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'empleado' and password == '$uper4utos#':
            session['logged_in'] = True
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cargar_autos()
    return render_template('index.html', autos=autos_registrados)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_auto():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        descripcion = request.form['descripcion']
        precio_unitario = float(request.form['precio_unitario'])
        cantidad = int(request.form['cantidad'])

        # Manejar la imagen subida
        if 'imagen' not in request.files:
            flash('No se subió ninguna imagen.', 'error')
            return redirect(request.url)

        file = request.files['imagen']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Guardar la imagen en la carpeta 'static/images'
            imagen = os.path.join("images/"+filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Extensión de archivo no permitida.', 'error')
            return redirect(request.url)

        # Validar si ya existe el auto con esa placa
        for auto in autos_registrados:
            if auto.placa == placa:
                flash('Ya existe un auto con esa placa.', 'error')
                return redirect(url_for('registrar_auto'))

        # Registrar el auto
        auto = Auto(placa, marca, modelo, descripcion, precio_unitario, cantidad, imagen)
        autos_registrados.append(auto)
        guardar_autos()
        flash('Auto registrado con éxito.', 'success')
        return redirect(url_for('index'))

    return render_template('registrar.html')

@app.route('/eliminar/<placa>', methods=['POST'])
def eliminar_auto(placa):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global autos_registrados
    autos_registrados = [auto for auto in autos_registrados if auto.placa != placa]
    guardar_autos()
    flash('Auto eliminado con éxito.', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
