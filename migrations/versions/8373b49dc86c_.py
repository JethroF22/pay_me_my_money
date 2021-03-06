"""empty message

Revision ID: 8373b49dc86c
Revises: 74f1bbb89bfd
Create Date: 2019-01-28 04:03:13.822071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8373b49dc86c'
down_revision = '74f1bbb89bfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('revoked_token')
    # ### end Alembic commands ###
