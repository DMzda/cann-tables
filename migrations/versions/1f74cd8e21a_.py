"""empty message

Revision ID: 1f74cd8e21a
Revises: 133628a3aff
Create Date: 2014-04-22 17:28:28.719192

"""

# revision identifiers, used by Alembic.
revision = '1f74cd8e21a'
down_revision = '133628a3aff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###