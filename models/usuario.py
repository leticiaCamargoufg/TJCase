from database.db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    casos_teste = db.relationship('CasoTeste', backref='usuario', lazy=True)

    def __init__(self, nome, email, senha_hash):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
