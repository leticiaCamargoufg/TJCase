"""Inicializando controle de versão no banco existente

Revision ID: 385c4c658508
Revises: 
Create Date: 2025-03-23 17:09:11.660807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '385c4c658508'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projeto',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('objetivo', sa.String(length=255), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('data_cadastro', sa.DateTime(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=False),
    sa.Column('deletado', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('casos_de_teste',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('titulo', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('objetivo', sa.String(length=255), nullable=False),
    sa.Column('passos', sa.String(length=255), nullable=False),
    sa.Column('resultado_esperado', sa.String(length=255), nullable=False),
    sa.Column('observacoes', sa.String(length=255), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('data_cadastro', sa.DateTime(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=False),
    sa.Column('deletado', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('titulo')
    )
    op.create_table('projeto_usuario',
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('projeto_id', 'usuario_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projeto_usuario')
    op.drop_table('casos_de_teste')
    op.drop_table('projeto')
    # ### end Alembic commands ###
