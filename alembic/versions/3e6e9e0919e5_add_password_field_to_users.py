"""Add password field to users

Revision ID: 3e6e9e0919e5
Revises: a57ac754f90c
Create Date: 2019-12-17 16:51:14.427932

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3e6e9e0919e5'
down_revision = 'a57ac754f90c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
