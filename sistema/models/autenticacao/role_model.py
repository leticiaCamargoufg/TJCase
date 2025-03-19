from sistema.models.base_model import BaseModel, db

class RoleModel(BaseModel):
    '''Model de registro de users '''
    
    __tablename__ = 'role'
    id = db.Column(db.Integer, autoincrement= True, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    cargo = db.Column(db.String(100), nullable = False)
    
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo