from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
db_path = 'C:/Users/marcos.oliveira/Desktop/Faculdade/Desen. Sistemas de Informação/ac3/ac3_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Arquivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300))
    conteudo = db.Column(db.LargeBinary)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_arquivo', methods=['POST'])
def upload_arquivo():
    arquivo = request.files['inputFile']
    novoArquivo = Arquivo(nome=arquivo.filename, conteudo=arquivo.read())
    db.session.add(novoArquivo)
    db.session.commit()
    return render_template('upload_realizado.html')

@app.route('/arquivos')
def arquivos():
    arquivos = Arquivo.query.all()
    return render_template("arquivos.html", title="Arquivos", arquivos=arquivos)

@app.route('/download/<int:id>')
def download_arquivo(id):
    arquivo = Arquivo.query.filter_by(id=id).first()
    return send_file(BytesIO(arquivo.conteudo), attachment_filename=arquivo.nome, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)