from database.db import db
from datetime import datetime

class CasoTeste(db.Model):
    __tablename__ = 'casos_teste'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    passos = db.Column(db.Text, nullable=False)
    resultado_esperado = db.Column(db.Text, nullable=False)
    observacoes = db.Column(db.Text)
    ultima_edicao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, titulo, objetivo, passos, resultado_esperado, observacoes, usuario_id):
        self.titulo = titulo
        self.objetivo = objetivo
        self.passos = passos
        self.resultado_esperado = resultado_esperado
        self.observacoes = observacoes
        self.usuario_id = usuario_id
