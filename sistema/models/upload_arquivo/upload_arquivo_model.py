from sistema.models.base_model import BaseModel, db


class UploadArquivoModel(BaseModel):
    
    '''Model reponsável por armazenar todos os arquivos que for feito upload'''
    
    __tablename__= 'upload_arquivo'
    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    nome = db.Column(db.String(100))
    caminho = db.Column(db.String(100))
    extensao = db.Column(db.String(100))
    tamanho = db.Column(db.String(100))
    
    def __init__(self, nome, caminho, extensao,tamanho):
        self.nome = nome
        self.caminho = caminho
        self.extensao = extensao
        self.tamanho = tamanho