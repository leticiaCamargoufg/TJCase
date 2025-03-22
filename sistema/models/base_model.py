from datetime import datetime

from pytz import timezone

from sistema import db

fuso = timezone('America/Sao_Paulo')

class BaseModel(db.Model):
    __abstract__ = True
    data_cadastro = db.Column(
        db.DateTime, default=lambda: datetime.now(fuso), nullable = False
    )
    data_alteracao = db.Column(
        db.DateTime, default=lambda: datetime.now(fuso), nullable = False,
        onupdate = lambda: datetime.now()
    )
    deletado = db.Column(db.Boolean, default=False, nullable=False)
    
