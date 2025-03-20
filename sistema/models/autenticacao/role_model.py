from sistema.models.base_model import BaseModel, db
from sqlalchemy import asc

class RoleModel(BaseModel):
    '''Model de registro de users '''
    
    __tablename__ = 'role'
    id = db.Column(db.Integer, autoincrement= True, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    cargo = db.Column(db.String(100), nullable = False)
    
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo
        
    
    def busca_roles_asc_cargo():
        roles = RoleModel.query.filter(
            RoleModel.deletado == 0
        ).order_by(
            asc(RoleModel.cargo)
        ).all()
        
        return roles
    
    def busca_role_id(id):
        role = RoleModel.query.filter(
            RoleModel.id == id
        ).first()
        
        return role