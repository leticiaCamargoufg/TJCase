
from sistema.models.base_model import BaseModel, db

projeto_usuario = db.Table(
    'projeto_usuario',
    db.Column('projeto_id', db.Integer, db.ForeignKey('projeto.id'), primary_key=True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
)

class ProjetoModel(BaseModel):
    '''Model de registro de projetos'''

    __tablename__ = 'projeto'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    objetivo = db.Column(db.String(255), nullable=True)

   # Relacionamento 1:N com 'casoDeTeste'
    casos_de_teste = db.relationship("CasoDeTesteModel", back_populates="projeto")
    
    # Relacionamento N:N com usuários
    usuarios = db.relationship("UsuarioModel", secondary=projeto_usuario, back_populates="projetos")

    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, nome, status, objetivo):
        self.nome = nome
        self.status = status
        self.objetivo = objetivo

    def is_active(self):
        return self.ativo
