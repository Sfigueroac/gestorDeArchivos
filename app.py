from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Necesario para mensajes flash

# Crear la carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    search_results = request.args.get('search_results', None)
    return render_template('index.html', files=files, search_results=search_results)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Archivo subido correctamente')
        return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Archivo eliminado correctamente')
    else:
        flash('El archivo no existe')
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '').lower()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    results = [f for f in files if query in f.lower()]
    
    return render_template('index.html', files=files, search_results=results or None)

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename', '')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        flash('El archivo no existe')
        return redirect(url_for('index'))

@app.route('/rename', methods=['POST'])
def rename_file():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_name)
    new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        flash('Archivo renombrado correctamente')
    else:
        flash('El archivo original no existe')
    
    return redirect(url_for('index'))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        flash('Carpeta creada correctamente')
    else:
        flash('La carpeta ya existe')
    
    return redirect(url_for('index'))

@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    
    if os.path.exists(folder_path):
        try:
            os.rmdir(folder_path)
            flash('Carpeta eliminada correctamente')
        except OSError:
            flash('No se puede eliminar la carpeta (no está vacía)')
    else:
        flash('La carpeta no existe')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)