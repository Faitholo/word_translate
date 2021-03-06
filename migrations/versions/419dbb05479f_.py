"""empty message

Revision ID: 419dbb05479f
Revises: 
Create Date: 2022-06-19 23:15:41.605654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '419dbb05479f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('A', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('B', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('C', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('D', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('answer', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz')
    # ### end Alembic commands ###
