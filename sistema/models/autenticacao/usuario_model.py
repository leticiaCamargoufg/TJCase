from flask import url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from sistema import login_manager
from sistema.models.base_model import BaseModel, db
from sistema.models.upload_arquivo.upload_arquivo_model import \
    UploadArquivoModel
from sistema.models.projeto.projeto_model import *

@login_manager.user_loader
def get_user(user_id):
    return UsuarioModel.query.filter_by(id=user_id).first()

class UsuarioModel(BaseModel, UserMixin):
    '''Model de registro de usuário'''
    
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    
    #Relacionamento 1:1 com tabela 'role'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('RoleModel', backref=db.backref('usuario', lazy = True))
    
    #Relacionamento 1:1 com tabela 'upload_aquivos'
    foto_perfil_id = db.Column(db.Integer, db.ForeignKey('upload_arquivo.id'))
    foto_perfil = db.relationship('UploadArquivoModel', backref=db.backref('usuario', lazy = True))
    
    #Relacionamento 1:N com tabela 'CasoTeste'
    casos_de_teste = db.relationship('CasoDeTesteModel', back_populates='usuario')
    
    # Relacionamento N:N com projetos
    projetos = db.relationship("ProjetoModel", secondary=projeto_usuario, back_populates="usuarios")


    ativo = db.Column(db.Boolean, nullable=False, default= True)

    def __init__(self, nome, email, senha_hash, role_id, ativo, foto_perfil_id):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha_hash)
        self.role_id = role_id
        self.ativo = ativo
        self.foto_perfil_id = foto_perfil_id
        
    def set_password(self, senha):
        """Gera um hash seguro da senha e armazena"""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha digitada corresponde ao hash armazenado"""
        return check_password_hash(self.senha_hash, senha)
    
    def is_active(self):
        return self.ativo

    def get_foto_perfil(self):
        if self.foto_perfil_id:
            arquivo = UploadArquivoModel.query.get(self.foto_perfil_id)
            if arquivo:
                return url_for('static', filename=arquivo.caminho)
        return url_for('static', filename='uploads/undraw_profile.png')  