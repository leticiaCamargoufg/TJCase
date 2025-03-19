CHAVE_SECRETA_FLASK = 'minha-chave'


# ------------------ Banco de Dados --------------------

DB_USERNAME = "teste"
DB_PASSWORD = "1234"
DB_SERVER = "localhost"
DB_DATABASE = "projeto_case"

SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
