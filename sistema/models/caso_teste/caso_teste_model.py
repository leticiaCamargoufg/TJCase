from sistema.models.base_model import BaseModel, db
from sistema.models.autenticacao.usuario_model import UsuarioModel
from sistema.models.projeto.projeto_model import ProjetoModel

class CasoDeTesteModel(BaseModel):
    '''Model de registro de caso de teste'''

    __tablename__ = 'casos_de_teste'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    titulo = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    objetivo = db.Column(db.String(255), nullable=False)
    passos = db.Column(db.String(255), nullable=False)
    resultado_esperado = db.Column(db.String(255), nullable=False)
    observacoes = db.Column(db.String(255))

    # Relacionamento 1:N com tabela 'usuarios'
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship("UsuarioModel", back_populates="casos_de_teste")

    # Relacionamento 1:N com tabela 'projetos'
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    projeto = db.relationship("ProjetoModel", back_populates="casos_de_teste")

    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, titulo, status, objetivo, passos, resultado_esperado, observacoes, usuario_id, projeto_id):
        self.titulo = titulo
        self.status = status
        self.objetivo = objetivo
        self.passos = passos
        self.resultado_esperado = resultado_esperado
        self.observacoes = observacoes
        self.usuario_id = usuario_id
        self.projeto_id = projeto_id

    def is_active(self):
        return self.ativo
